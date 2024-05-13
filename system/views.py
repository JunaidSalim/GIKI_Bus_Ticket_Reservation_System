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
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import HttpResponseForbidden

# Create your views here.
# data.ticket_no, data.from_destination, data.to_destination, data.regNo, data.name, data.bus_No, data.bus_location, data.date, data.time, data.driver_name, data.driver_number
def send_email(ticket):
    ticket_no = ticket.pk
    from_destination = ticket.dest_pk.from_destination
    to_destination  = ticket.dest_pk.to_destination
    regNo = ticket.user_pk.username
    name = ticket.user_pk.first_name + " " + ticket.user_pk.last_name
    bus_No = ticket.dest_pk.bus_No
    bus_location = ticket.dest_pk.bus_location
    date = ticket.dest_pk.date
    time = ticket.dest_pk.time
    driver_name = ticket.dest_pk.bus_driver.driver_name
    driver_number = ticket.dest_pk.bus_driver.driver_number
    email = ticket.user_pk.email
    subject = "Ticket Confirmed"
    message = """Thanks for Booking Ticket
Your Ticket has been confirmed

Ticket Details:
Ticket no: {}
From: {}
To: {}
Your Reg No: {}
Your Name: {}
Bus No: {}
Bus Location: {}
Date: {}
Time: {}
Driver Name: {}
Driver Number: {}""".format(ticket_no, from_destination, to_destination, regNo, name, bus_No, bus_location, date, time, driver_name, driver_number)

    from_email = settings.EMAIL_HOST
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

def index(request):
    return render(request,'landingPage.html')

def search(request):
    now = datetime.now()
    destinations = destination.objects.filter(
        Q(date__gt=now.date()) | (Q(date=now.date(), time__gt=now.time())),tickets__gt=0
    )
    return render(request,'search.html',{"destinations" : destinations})

@login_required(login_url='/login/') 
def render_pdf_view(request,id):
    referrer = request.META.get('HTTP_REFERER')
    if referrer and (('booking/confirm/' in referrer) or ('tickets/' in referrer)):
        template_path = 'print.html'
        ticket_set = get_object_or_404(ticket, id=id)
        user_set = User.objects.get(pk=ticket_set.user_pk.pk)
        dest_set = destination.objects.get(id=ticket_set.dest_pk.pk)
        
        context = {'ticket': ticket_set,'User_set': user_set,'dest':dest_set}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename="{ticket_set.pk}-Ticket.pdf"'    # find the template and render it.
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
    else:
        return HttpResponseForbidden("Access Denied: Invalid Request")

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')

        user = auth.authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid Credentials')
            return redirect('/login/')
        else:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(2592000)
            messages.info(request,"Signed In")
            return redirect('/')
    else:
        return render(request, 'login.html')


@login_required(login_url='/login/')
def logout_page(request):
    logout(request)
    messages.info(request,"Logged Out")
    return redirect('/')

def signup_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')  
        username = request.POST.get('username')
        email = request.POST.get('email')
        remember_me = request.POST.get('remember')
        cont = "@giki.edu.pk"
        
        if cont in email:
            password = str(random.randint(100000,999999))
            user  = User.objects.filter(username=username)
            if user.exists():
                messages.error(request,"RegNo Already exists")
                return redirect('/signup/')
            else:
                user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
                user.save()
                if not remember_me:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(2592000)
                messages.info(request,"Account Created Successfully!\nYou will receive credentials shortly on provided Email")
                subject = "Account Credentials"
                message = """Thanks for Creating Account
Your Account has been Created

Account Details:
Username/RegNo: {}
Email: {}
Password: {}

You can change Password through Account after Sign In or through reset Password""".format(username,email,password)
                from_email = settings.EMAIL_HOST
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list)
                
                return redirect('/login/')
        else:
            messages.error(request,"Kindly Enter GIKI Email(@giki.edu.pk)")
            return redirect('/signup/') 
    else:
        return render(request, 'signup.html')


@login_required(login_url='/login/')
def booking(request,id):
    dest = destination.objects.get(id=id)
    user_tickets = ticket.objects.filter(user_pk=request.user.pk, dest_pk__date=dest.date)
    if user_tickets.exists() and request.user.is_superuser==False:
        messages.error(request,"You Cannot Book Ticket for Same Date")
        return redirect('/')
    context = {"dest":dest}
    return render(request,'booking.html',context)

@login_required(login_url='/login/')
def account(request):
    id = request.user.pk
    query_set = User.objects.get(id=id)
    if request.method == "POST":
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')  
        old_password = request.POST.get('oldpassword')
        check = authenticate(request,username = request.user.username,password = old_password)
        if check:
            password = request.POST.get('password')
            query_set.first_name = first_name
            query_set.last_name = last_name
            query_set.set_password(password)
            query_set.save()
            return redirect('/login')
        else:
            messages.error(request,"Invalid Old Password")
            return redirect(f'/account/{request.user.pk}')
    context = {"account" : query_set}
    return render(request,'account.html',context)


@login_required(login_url='/login/')
def delete_account(request):
    id = request.user.pk
    query_set = User.objects.get(id=id)
    query_set.delete()
    return redirect('/')


@login_required(login_url='/login/')
def confirm(request):
    if request.method=="POST":
        id = request.POST.get('id')
        ticket_check = ticket.objects.filter(dest_pk = id,user_pk = request.user.pk)
        if ticket_check.exists() and request.user.is_superuser==False:
            return redirect('/')   
        user_instance = request.user
        dest_instance = get_object_or_404(destination, id=id)
        dest_instance.tickets = dest_instance.tickets -1 
        dest_instance.save()
        ticket_instance = ticket(user_pk=user_instance, dest_pk=dest_instance)
        ticket_instance.save()
        tick = get_object_or_404(ticket, dest_pk=id, user_pk=request.user.pk)
        send_email(tick)
        return render(request,'confirm.html',{"ticket" : ticket_instance})    
    else:
        return HttpResponse("Server Error")
        

@login_required(login_url='/login/')
def tickets(request):
    user_tickets = ticket.objects.filter(user_pk = request.user.pk)
    print(user_tickets)
    return render(request,'tickets.html',{"tickets" : user_tickets})
        
