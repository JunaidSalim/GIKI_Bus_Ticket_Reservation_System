from django.db import models

# Create your models here.

Destination_Choices = (
    ("GIKI","GIKI"),
    ("Peshawar","Peshawar"),
    ("Abbotabad","Abbotabad"),
    ("Pindi","Pindi"),
    ("Islamabad","Islamabad")
)

class destination(models.Model):
    from_destination = models.CharField(max_length=20,choices=Destination_Choices)
    to_destination = models.CharField(max_length=20,choices=Destination_Choices)
    bus_No = models.IntegerField()
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    bus_location = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.from_destination+ "-" + self.to_destination

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.username




