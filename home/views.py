from django.shortcuts import render
from .models import destination

# Create your views here.
def index(request):
    destinations = destination.objects.all()
    return render(request,'index.html',{"destinations" : destinations})