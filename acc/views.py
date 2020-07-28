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
                user=User.objects.create_user(username=username,password=pass1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                print('user created')
                return redirect('login')
        else:
            messages.info(requests,'Passwords do not match')
            return redirect('register')
        return redirect('/')
    else:
        return render(requests,'register.html')  