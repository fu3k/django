#PART 1:BASICS
#PART-2 DATABASE
# PART3 : templates, views ,A shortcut: render and get_object_or_404(), Namespacing Urls
#PART 4 : Write a minimal form,generic views

#PART1 BASICS
#start proj
$ django-admin startproject mysite
#run server
$ python manage.py runserver
#start app   // aproj can have many apps 
$ python manage.py startapp polls

# each app should have its own urlpatterns : create urls.py
--- polls/urls.py -----------------------------------
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

# create view for index
----polls/views.py------------------------------------
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


#add apps url to site urls
--- mysite/urls.py -----------------------------------
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),]
    
    
##############################################################################################################
#PART-2 DATABASE
####################
#Database in settings file :add this code to settings.py
------ mysite/settins.py --------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'webapp',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST':'localhost',
    }
}

#addd database to project workspace
$ python manage.py migrate

# to create table - create model : this model will serve as schema for tables
----polls/models.py---------------------------------------------
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
# configure refrence of this apps model with project(mysite)
# polls app will have app.py in which it will have config
# add it to installed apps : 'polls.apps.PollsConfig'
-----mysite/settings.py------------------------------------------------------
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

#make migration to create tables
$ python manage.py makemigrations polls
#to check changes and sql query check polls/migrations folder
$ python manage.py sqlmigrate polls 0001
#migrate
$ python manage.py migrate

#----API for managing database with terminal 
$ python manage.py shell
'''
>>Question.objects.all()
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())
>>> q.save()
>>> q.id
>>> q.question_text
>>> Question.objects.all()

# Display any choices from the related object set -- none so far.
>>> q.choice_set.all()
>>> q.choice_set.create(choice_text='Not much', votes=0
>>> q.choice_set.create(choice_text='The sky', votes=0)
>>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)
>>> c = q.choice_set.filter(choice_text__startswith='Just hacking')
>>> c.delete()
>>> Choice.objects.filter(question__pub_date__year=current_year)
'''

#create some models to access questions and to add choices.
----polls/models.py----------------------------------------------
import datetime
from django.db import models
from django.utils import timezone

class Question(models.Model):
    # ...
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    # ...
    def __str__(self):
        return self.choice_text


# Introducing the Django Admin
#.......
$ python manage.py createsuperuser
$ python manage.py runserver
# in browser 
http://127.0.0.1:8000/admin/


# Make the poll app modifiable in the admin
-----polls/admin.py------------------------------------------
from django.contrib import admin
from .models import Question

admin.site.register(Question)

########################################################################################################
# PART3 : templates, views ,A shortcut: render and get_object_or_404(), Namespacing Urls
##############
# Writing more views 
# A shortcut: render and get_object_or_404()
-------polls/views.py------------------------------------------
from django.shortcuts import render,get_object_or_404
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Leave the rest of the views (detail, results, vote) unchanged
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
    
#add url to urlpatterns
----polls/urls.py----------------------------------------------
from django.urls import path
from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

#Time to add templates(html pages)
#The default(mysite) settings file configures 
# a DjangoTemplates backend whose APP_DIRS option is set to True.
'''
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]'''
# By convention DjangoTemplates looks for a “templates” subdirectory in each of the INSTALLED_APPS.
#create required folders and file
-----polls/templates/polls/index.html------------------------------------
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}

----polls/templates/polls/detail.html--------------------------------
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>

# Removing hardcoded URLs in templates like this
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
#with
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>


#Namespacing URL names
-----polls/urls.py---------------------------------------------------
from django.urls import path
from . import views
#add name
app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    
#change URL in index.html 
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
#with
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>


##################################################################################################################
#PART 4 : Write a minimal form,generic views
#######################
#Write a minimal form
----polls/templates/polls/detail.html-------------------------------------
<h1>{{ question.question_text }}</h1>

{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
{% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
{% endfor %}
<input type="submit" value="Vote">
</form>

#add path for vote adn result in 
-----polls/urls.py----------------------------------------------
path('<int:question_id>/vote/', views.vote, name='vote'),
path('<int:pk>/results/', views.vote, name='vote'),

# add view for vote and result in
--------polls/views.py-----------------------------------------
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question
# ...
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})        

# template for result
------polls/templates/polls/results.html-------------------------------
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
{% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">Vote again?</a>   

#Use generic views: Less code is better
'''
--------polls/urls.py---------------------------------------
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

-----polls/views.py----------------------------------------
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    ... # same as above, no changes needed
'''
