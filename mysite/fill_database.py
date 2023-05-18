from quiz.models import Question, Choice

# clear database
Question.objects.all().delete()
Choice.objects.all().delete()

# Create list to store questions in for adding choices to
question_list = []

# Insert questions
with open('questions.csv', 'r') as q:
    questions = q.read().splitlines()
    for question_text in questions:
        question = Question(question_text=question_text,
                            question_type='VO')
        question.save()

        question_list.append(question)
        question_text = q.readline()

# Insert choices
with open('choice.csv', 'r') as c:
    choices = c.read().splitlines()
    for choice_text in choices:
        # Insert choice to every question
        for q in question_list:
            choice = Choice(choice_text=choice_text,
                            question=q)
            choice.save()
        choice_text = c.readline()

