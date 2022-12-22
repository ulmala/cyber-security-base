import logging
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Choice, Question
from .forms import CreateQuestionForm, CreateChoiceForm

#logger = logging.getLogger('polls')

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def index(request):
    context = {
        'latest_question_list' : Question.objects.order_by('-pub_date'),
    }
    return render(request, 'polls/index.html', context)

@login_required(login_url="/polls/login/")
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('polls:index')
    else:
        form = UserCreationForm()
    return render(request, 'polls/register.html', {'form': form})

def login_(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            #logger.info(f'{user.username} logged in')
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('polls:index')
    else:
        form = AuthenticationForm()
    return render(request, 'polls/login.html', {'form': form})

def logout_(request):
    if request.method == 'POST':
        logout(request)
        #logger.info(f'{request.user.get_username()} logged out')
        return redirect('polls:index')


#@login_required(login_url="/polls/login/")
def create(request):
    if request.method == 'POST':
        question_form = CreateQuestionForm(data=request.POST)
        choice_form = []
        if question_form.is_valid() and all(c.is_valid for c in choice_form):
            question = question_form.save()
            for choice_text in dict(request.POST)['choice_text']:
                question.choice_set.create(choice_text=choice_text)
            return redirect('polls:index')
    else:
        question_form = CreateQuestionForm()
        choice_form = [CreateChoiceForm()] * 3
    return render(request, 'polls/create.html', {'question_form': question_form, 'choice_form': choice_form})