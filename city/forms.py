from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Complaint,MyUser

class CreateUserForm(UserCreationForm):
    class Meta:
        model=MyUser
        fields=['username','email','password1','password2']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        
        fields =['complaint_type','address','area','city','pincode','landmark','info','picture']
        
        

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields =['complaint_type','info','picture','status']
