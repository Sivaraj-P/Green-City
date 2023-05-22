from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class MyUser(AbstractUser):
    email=models.EmailField(unique=True)
    is_user=models.BooleanField(default=True)
    is_employee=models.BooleanField(default=False)


class Complaint(models.Model):
    STATUS=(
        ('Submitted','Submitted'),
        ('Pending','Pending'),
        ('Resolved','Resolved')
    )
    COMPLAINTS=(
        ('Garbage dump','Garbage dump'),
        ('Overflow of Septic Tanks','Overflow of Septic Tanks'),
        ('Burning of Garbage','Burning of Garbage'),
        ('Stagnant Water','Stagnant Water'),
        ('Dustbins not cleaned','Dustbins not cleaned'),
        ('Improper Sanitization','Improper Sanitization'),
        ('Open Manholes or Drains','Open Manholes or Drains'),
    )
    user_name=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    complaint_type=models.CharField(max_length=200,null=True,choices=COMPLAINTS)
    address=models.CharField(max_length=500,null=True)
    area=models.CharField(max_length=50,null=True)
    city=models.CharField(max_length=100,null=True)
    pincode=models.CharField(max_length=6,null=True)
    landmark=models.CharField(max_length=200,null=True)
    info=models.CharField(max_length=200,null=True)
    complaint_date=models.DateTimeField(auto_now_add=True,null=True)
    picture=models.ImageField(null=True)
    tracking_id=models.CharField(null=True,max_length=16)
    if MyUser.is_authenticated and MyUser.is_user==True:
        status=models.CharField(max_length=200,null=True,default='Submitted')
    else:
        status=models.CharField(max_length=200,null=True,default='Submitted',choices=STATUS)
    
    def __str__(self):
        return f"{self.user_name}"

class Queries(models.Model):
    name=models.CharField(max_length=100,null=True)
    email=models.CharField(max_length=100,null=True)
    message=models.CharField(max_length=500,null=True)

    def __str__(self):
        return f"{self.name}"
        
class Employee(models.Model):
    name=models.CharField(max_length=200,null=True)
    phone=models.IntegerField(null=True)
    email=models.CharField(max_length=100,null=True)
    password=models.CharField(max_length=100,null=True)
    def __str__(self):
        return f"{self.name}"
