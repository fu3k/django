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