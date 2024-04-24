from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User,auth


# Create your views here.
def home(request):
    destinations = destination.objects.all()
    return render(request,'index.html',{"destinations" : destinations})

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Username: {username}, Password: {password}")  # Debugging print

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')

        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is None:
            messages.error(request, 'Invalid Credentials')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/')
    else:
        return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('/')

def signup_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')  
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user  = User.objects.filter(username=username)
        if user.exists():
            messages.error(request,"RegNo Already exists")
            return redirect('/signup/')
        else:
            user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.save()
            messages.info(request,"Account Created Successfully")
            return redirect('/login/') 
    else:
        return render(request, 'signup.html')

def booking(request,id):
    dest = destination.objects.get(id=id)
    context = {"dest":dest}
    return render(request,'booking.html',context)

def account(request,id):
    query_set = User.objects.get(id=id)
    if request.method == "POST":
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')  
        password = request.POST.get('password')
        query_set.first_name = first_name
        query_set.last_name = last_name
        query_set.set_password(password)
        query_set.save()
        return redirect('/')
    context = {"account" : query_set}
    return render(request,'account.html',context)

def delete_account(request,id):
    query_set = User.objects.get(id=id)
    query_set.delete()
    return redirect('/')

def confirm(request,id,id2):
    user_instance = get_object_or_404(User, id=id2)
    dest_instance = get_object_or_404(destination, id=id)
    ticket_instance = ticket(user_pk=user_instance, dest_pk=dest_instance)
    ticket_instance.save()
    return redirect('/')
    