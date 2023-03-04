from django.db import models
from django.db.models import Count
from django.utils.translation import gettext_lazy as _


class Question(models.Model):
    """
    Class to store "ranking the stars" questions. The answer to these questions is determined based on the answer with
    that was given by the majority of voters.
    Attributes:
         question_text  The question the players have to answer
         question_type  The type of question: "VO" is a voted question, "AN" has a predetermined correct answer
         active         Flag whether the question can currently be answered
    """

    class QuestionType(models.TextChoices):
        """
        This subclass defines the types of questions that exist. There are two types of questions:
            VOTE:   These are questions where the correct answer(s) is/are the ones that the largest share of
                    participants responded with.
            ANSWER: These are questions where the correct answer(s) are predetermined by the quiz maker.
        """
        VOTE = 'VO', _('Vote')
        ANSWER = 'AN', _('Answer')

    question_text = models.CharField(max_length=200)
    question_type = models.CharField(
        max_length=2,
        choices=QuestionType.choices,
        default=QuestionType.ANSWER,
    )
    active = models.BooleanField(default=False)

    def get_overview(self):
        """
        This function returns an object with all choices that are connected to the question and ranks them by the number
        of votes that they received.
        :return: queryset with the choices that were possible including their counts
        """
        overview = Choice.objects.filter(question_id=self.id) \
                         .annotate(nr_resp=Count('response'))  \
                         .order_by('-nr_resp')
        return overview

    def correct_answers(self):
        """
        This function determines which answer(s) received the highest number of votes and returns an array that contains
        the most voted answer(s)
        :return: list with the id('s) of the correct answer(s)
        """

        # If the question has (a) predetermined answer(s), filter it and return
        if self.question_type == self.QuestionType.ANSWER:
            correct_answers = self.choice_set.filter(correct=True).values('id')
            correct_answers_id = list(correct_answers.values_list('id', flat=True))  # Determine the id's
            return correct_answers_id

        # If the correct answer is simply the one with the most votes
        elif self.question_type == self.QuestionType.VOTE:
            answers = self.response_set.values('choice_id')                                 # get the votes
            score = answers.annotate(count=Count('choice_id')).order_by('-choice_id')       # count them
            highest_score = score[0]['count']                                               # identify the max
            correct_answers = score.filter(count=highest_score)                             # Identify correct choices
            correct_answers_id = list(correct_answers.values_list('choice_id', flat=True))  # Determine the id's

            # update the choices that are correct in the DB
            Choice.objects.filter(id__in=correct_answers_id).update(correct=True)

            return correct_answers_id

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """
    Choice contains the options the player can choose from per question
    Attributes:
        question    The question this particular choice relates to
        choice_text The description of this choice option (should answer the question)
        correct     Whether choice is the correct answer, can be outdated in case of VOTE type of questions
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Player(models.Model):
    """
    The player will contain the contestants of the game. These are not linked to Django's default "User"-class.

    Attributes:
        username    The screen name of the player
        active      If the user has signed out, they will be lost but not forgotten
        total_score Holder for the total score of the player
    """
    username = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    total_score = models.IntegerField(default=0)

    def update_total_score(self):
        """
        This function calculates the total score of a player by counting the number of correct answers they have given.
        :return: int
        """
        total_score = 0                                                     # Holder for the player's score
        responses = self.response_set.all()                                 # Get all responses
        for response in responses:
            if response.choice.id in response.question.correct_answers():   # Check if response in correct answer set
                total_score += 1                                            # Increase total score with 1 point

        self.total_score = total_score                                      # Put the score to the object attribute
        self.save()                                                         # Save to database

    def __str__(self):
        return self.username


class Response(models.Model):
    """
    The response object contains which answer the player has voted on.

    Attributes:
        player      Who gave the response
        choice      What the player voted on
        question    Which question belongs to (for easier querying)
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.player.__str__() + ": " + self.question.__str__() + " " + self.choice.__str__()
