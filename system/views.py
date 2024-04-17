from django.shortcuts import render,redirect
from .models import *

# Create your views here.
def home(request):
    destinations = destination.objects.all()
    return render(request,'index.html',{"destinations" : destinations})

def login_page(request):
    return render(request,'login.html')


def signup_page(request):
    if request.method == 'POST':
        name = request.POST.get('Name')  
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User(name=name,username=username, password=password)
        user.save()
        return redirect('home') 
    else:
        return render(request, 'signup.html')