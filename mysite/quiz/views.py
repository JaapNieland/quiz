from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required

from .models import Question, Choice, Response, Player


def index(request):
    """
    The home page of th whole bit. Just serving the index html file.
    :param request: Django request object
    :return: render of the index file
    """
    return render(request, 'quiz/index.html')


def signup(request):
    """
    This function build the page where you can signup with a username. A new Player object is created with the given
    username. This username and the player id are stored in the session.
    :param request:
    :return:
    """

    # Check the reqeust type. With a POST request the player can actually sign up
    if request.method == 'POST':
        username = request.POST['username']     # Retrieve the POSTed data from request
        if username is not None:
            player = Player.objects.create(     # Create the player in the database
                username=username,
                active=True
            )
            request.session['username'] = player.username   # Dump username in the player's session cookie
            request.session['player_id'] = player.id           # Dump user id in the player's session cookie
        return redirect('index')                            # Redirect the player to the home page

    # If the request is not a POST request, serve up the signup page
    else:
        return render(request, 'quiz/signup.html')


def signoff(request):
    """
    This function is used to sign off. The player is set to inactive and the session is cleared from the player's
    browser.Currently, it is not possible for the player to reactivate. Records are kept though for audit purposes etc.
    :param request:
    :return:
    """

    # Check if the request is actually from a player
    if 'player_id' in request.session:
        player_id = request.session['player_id']
        p = Player.objects.get(id=player_id)
        p.active = False
        p.save()
        del request.session['username']
        del request.session['player_id']
    return redirect('index')


def detail_next_question(request):
    """
    This function first checks if there is a registered player on the other end. If that is satisfied, the player is
    served the next question that is active. If no player is registered, a redirect to the signup page is served
    """
    # Check if player is registered
    if 'player_id' in request.session:
        # Identity the current player.
        user_id = request.session['player_id']
        player = Player.objects.get(id=user_id)

        # Identify the next active question
        question = Question.objects.filter(active=True).first()
        if question is None:
            # When no question is active, the a 404 is served
            return Http404('No active question found.')
        choices = get_list_or_404(Choice, question=question)

        prev_choice = Response.objects.filter(question=question, player=player).first()
        return render(request, 'quiz/detail.html',
                      {'question': question,
                       'choices': choices,
                       'prev_choice': prev_choice})
    else:
        return HttpResponseRedirect('/quiz/signup')


def vote(request, question_id):
    """
    This function is used to proces the votes from the Player. It is permitted to send the form as often as you'd like.
    However, the Response is only updated. Only 1 Response, per Player, per Question is saved.
    :param request:
    :param question_id:
    :return:
    """
    question = get_object_or_404(Question, pk=question_id)
    choice = get_object_or_404(Choice, pk=request.POST['choice'])
    player_id = request.session['player_id']
    player = get_object_or_404(Player, id=player_id)

    Response.objects.update_or_create(
        player=player,
        question=question,
        defaults={'choice': choice}
    )
    print(request.session)

    print(choice)
    return HttpResponseRedirect('/quiz/detail')


def question_results(request, question_id):
    """
    This function returns the votes cast, inlcuding the correct one
    :param request:
    :param question_id:
    :return:
    """
    question = get_object_or_404(Question, pk=question_id)      # Get the question we're worried about
    question.correct_answers()                                  # Update the correct answers in the DB based on votes

    result = Choice.objects.filter(question=question_id) \
        .annotate(votes=Count('response'))

    return render(request, 'quiz/results.html', {'results': result, 'question': question})


@staff_member_required
def score_board(request):
    """
    This function returns an overview of the score board, showing for every player how many points they have, ranked
    by number of points
    :param request:
    :return:
    """
    [p.update_total_score() for p in Player.objects.filter(active=True)]  # Update the score for the active players
    players = Player.objects.all().order_by('-total_score')  # Get the players, ordered by total score
    print(players)
    return render(request, 'quiz/score_board.html', {'players': players})


@staff_member_required
def control_panel(request):
    """
    This function returns the quiz control panel. Only controllable by the admins
    :param request:
    :return:
    """
    questions = Question.objects.all().order_by('id')
    return render(request, 'quiz/control_panel.html', {'questions': questions})


@staff_member_required
def switch_question_status(request):
    """
    This view function is used to update a question status, based on a post request that sends in the question to alter
    :param request:
    :return: success if the change was done successfully
    """
    if request.method == 'POST':
        question_description = request.POST['question_description']
        question_id = int(question_description.split('_')[3])
        question = Question.objects.get(id=question_id)
        question.active = not question.active
        question.save()

        return HttpResponse('success')

    else:
        return HttpResponseBadRequest


def currently_active_question(request):
    question = Question.objects.filter(active=True).first()
    return(HttpResponse(question.id))


