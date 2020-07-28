#####################################################################################################
# mysite
-------polls/views.py------------------------------------------
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

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Leave the rest of the views (detail, results, vote) unchanged
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


#####################################################################################################
# webapp
-------techie/views.py------------------------------------------
from django.shortcuts import render
from .models import Destination
#from django.http import HttpResponse
# Create your views here.

def home(request):
    print('home')
    return render(request,'home.html')

def techie(request):
    dest=Destination.objects.all()
    return render(request,'techie.html',{'dest':dest})

def add(request):
    
    if request.method=='POST':
        num1=request.POST['num1']
        num2=request.POST['num2']
        addresult=int(num1)+int(num2)
        res=({"num1":num1,"num2":num2,"result":addresult})
        
        
        return render(request,'add.html',res)
    else:
        return render(request,'add.html')
    
-------acc/views.py------------------------------------------
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.
def logout(requests):
    auth.logout(requests)
    return redirect('/')

def login(requests):
    if requests.method=='POST':
        username=requests.POST['username']
        password=requests.POST['password']
        user=auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(requests,user)
            return redirect('/')
        else:
            messages.info(requests,'invalid credentials')
    
    else:
        return render(requests,'login.html')

def register(requests):
    if requests.method=='POST':
        first_name=requests.POST['first_name']
        last_name=requests.POST['last_name']
        username=requests.POST['username']
        pass1=requests.POST['pass2']
        pass2=requests.POST['pass1']
        email=requests.POST['email']
        
        if pass1==pass2:
            if User.objects.filter(username=username).exists():
                messages.info(requests,'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(requests,'Email registered')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,password=pass1,
                                              email=email,first_name=first_name,last_name=last_name)
                user.save()
                print('user created')
                return redirect('login')
        else:
            messages.info(requests,'Passwords do not match')
            return redirect('register')
        return redirect('/')
    else:
        return render(requests,'register.html')  
    

###############################################################################################################3##############################
#