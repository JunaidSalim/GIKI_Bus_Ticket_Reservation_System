from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User,auth
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime

# Create your views here.
@login_required(login_url='/login/') 
def render_pdf_view(request,id):
    template_path = 'print.html'
    ticket_set = ticket.objects.get(id=id)
    user_set = User.objects.get(pk=ticket_set.user_pk.pk)
    dest_set = destination.objects.get(id=ticket_set.dest_pk.pk)
    
    context = {'ticket': ticket_set,'User_set': user_set,'dest':dest_set}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    # return render(request,'print.html')


def home(request):
    now = datetime.now()
    destinations = destination.objects.filter(
        Q(date__gt=now.date()) | (Q(date=now.date(), time__gt=now.time())),tickets__gt=0
    )
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


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def booking(request,id):
    dest = destination.objects.get(id=id)
    user_tickets = ticket.objects.filter(user_pk=request.user.pk, dest_pk__date=dest.date, dest_pk__from_destination= dest.from_destination, dest_pk__to_destination = dest.to_destination)
    if user_tickets.exists() and request.user.is_superuser==False:
        messages.error(request,"You Cannot Book A Ticket Twice")
        return redirect('/')
    context = {"dest":dest}
    return render(request,'booking.html',context)

@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def delete_account(request,id):
    query_set = User.objects.get(id=id)
    query_set.delete()
    return redirect('/')


@login_required(login_url='/login/')
def confirm(request,id):
    user_instance = request.user
    dest_instance = get_object_or_404(destination, id=id)
    dest_instance.tickets = dest_instance.tickets -1 
    dest_instance.save()
    ticket_instance = ticket(user_pk=user_instance, dest_pk=dest_instance)
    ticket_instance.save()
    return render(request,'confirm.html',{"ticket" : ticket_instance})    

@login_required(login_url='/login/')
def tickets(request):
    user_tickets = ticket.objects.filter(user_pk = request.user.pk)
    print(user_tickets)
    return render(request,'tickets.html',{"tickets" : user_tickets})
        
