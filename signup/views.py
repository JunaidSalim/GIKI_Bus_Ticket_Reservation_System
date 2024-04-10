from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from .models import User
import os

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('Name')  
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User(name=name,username=username, password=password)
        user.save()
        return redirect('index') 
    else:
        return render(request, 'signup.html')
