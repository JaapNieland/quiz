from django.test import TestCase

from.models import Player, Question, Response, Choice

# Create your tests here.


class QuestionModelTests(TestCase):
    def test_determine_the_most_voted_single_answer(self):
        """
        correct_answers() returns 1 when the first option is the most voted option
        """
        player1 = Player(username='p1')                                          # Setup player 1
        player2 = Player(username='p2')                                          # Setup player 2
        player1.save()                                                           # Save p1 to database
        player2.save()                                                           # Save p2 to database

        question = Question(question_text='test_question', question_type='VO')   # Create a test question
        question.save()                                                          # Save test question to database

        choice = Choice(choice_text='option1', question=question)                # Create choice option
        choice.save()                                                            # Save choice to DB

        answer1 = Response(player=player1, question=question, choice=choice)     # P1 answers choice
        answer2 = Response(player=player2, question=question, choice=choice)     # P2 answers choice
        answer1.save()                                                           # Save to DB
        answer2.save()                                                           # Save to DB

        correct_answer_id = question.correct_answers()                           # Calculate the most correct answer
        choice.refresh_from_db()                                                 # Get the newest info from DB
        assert(correct_answer_id == [choice.id])
        assert choice.correct

    def test_determine_the_most_voted_two_answers(self):
        """
        correct_answers() returns [1,2] or [2,1] when the first two options are the most voted answers
        """
        player1 = Player(username='p1')                                             # Setup player 1
        player2 = Player(username='p2')                                             # Setup player 2
        player1.save()                                                              # Save p1 to database
        player2.save()                                                              # Save p2 to database

        question = Question(question_text='test_question', question_type='VO')   # Create a test question
        question.save()                                                             # Save test question to database

        choice1 = Choice(choice_text='option1', question=question)               # Create choice option
        choice2 = Choice(choice_text='option2', question=question)               # Create choice option
        choice1.save()                                                              # Save choice to DB
        choice2.save()                                                              # Save choice to DB

        answer1 = Response(player=player1, question=question, choice=choice1)      # P1 answers choice
        answer2 = Response(player=player2, question=question, choice=choice2)      # P2 answers choice
        answer1.save()                                                              # Save to DB
        answer2.save()                                                              # Save to DB

        correct_answer_id = question.correct_answers()                              # Calculate the most correct answer
        choice1.refresh_from_db()
        choice2.refresh_from_db()
        assert(correct_answer_id == [choice1.id, choice2.id] or correct_answer_id == [choice2.id, choice1.id])
        assert choice1.correct
        assert choice2.correct

    def test_determine_the_single_correct_answer(self):
        """
        correct_answer
        :return:
        """
        question = Question(question_text='test_question', question_type='AN')      # Create a test question
        question.save()                                                             # Save test question to database

        choice1 = Choice(choice_text='option1', question=question, correct=True)    # Create correct choice option
        choice2 = Choice(choice_text='option2', question=question, correct=False)   # Create incorrect choice option
        choice1.save()                                                               # Save choice to DB
        choice2.save()                                                               # Save choice to DB

        correct_answer_id = question.correct_answers()
        assert(correct_answer_id == [choice1.id])

    def test_determine_the_multiple_correct_answers(self):
        """
        correct_answer
        :return:
        """
        question = Question(question_text='test_question', question_type='AN')   # Create a test question
        question.save()                                                             # Save test question to database

        choice1 = Choice(choice_text='option1', question=question, correct=True)  # Create correct choice option
        choice2 = Choice(choice_text='option2', question=question, correct=True) # Create incorrect choice option
        choice1.save()                                                               # Save choice to DB
        choice2.save()                                                               # Save choice to DB

        correct_answer_id = question.correct_answers()
        assert(correct_answer_id == [choice1.id, choice2.id])

    def test_player_score_calculation(self):
        """

        :return:
        """
        player1 = Player(username='p1')                                             # Setup player 1
        player1.save()                                                              # Save p1 to database

        question = Question(question_text='test_question', question_type='AN')   # Create a test question
        question.save()                                                             # Save test question to database

        choice1 = Choice(choice_text='option1', question=question, correct=True)               # Create choice option
        choice1.save()                                                              # Save choice to DB

        answer1 = Response(player=player1, question=question, choice=choice1)      # P1 answers choice
        answer1.save()                                                              # Save to DB
        player1.update_total_score()
        assert(player1.total_score==1)
