from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm , ComplaintForm ,UpdateForm
from django.contrib.auth.decorators import login_required
from .models import *
from .mail import *
import random
# Create your views here.
def home(request):
    total_complaints=Complaint.objects.count()
    pending=Complaint.objects.all().filter(status='Pending').count()
    solved=Complaint.objects.all().filter(status='Resolved').count()
    new=Complaint.objects.all().filter(status='Submitted').count()
    context={'total_complaints':total_complaints,'pending':pending,'solved':solved,'new':new}
    if request.method=='POST':
        name=request.POST['username']
        email=request.POST['email']
        message=request.POST['message']
        Queries.objects.create(name=name,email=email,message=message)
        
        return redirect('home')
    return render(request,'city/home.html',context=context)

def about(request):

    return render(request,'city/about.html')

def services(request):
    return render(request,'city/services.html')

def login_page(request):
    if request.method=='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None and user.is_user==True:
            login(request,user)
            print(user.is_user)
            # return render(request,"city/login.html")
            return redirect('home')
        else:
            messages.info(request,'uername or password is incorrect')
        
    return render(request,"city/login.html")
 
def register(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            email=form.cleaned_data['email']
            sub='Account Created Successfully'
            messages.success(request,'Account Created '+ user)
            body=f'Hello {user},\n\tYou have successfully created the user account in Green City. Kindly login to raise the complaints. Hope you will help us to make the city clean and green\n\t\t Thank You\n\nRegards,\nGreen City\nChennai'
            #mail(email,sub,body)
            return redirect('login')
    context={
        'form':form
    }
    return render(request,"city/register.html",context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST,request.FILES)
        if form.is_valid():
            types=form.cleaned_data['complaint_type']
            area=form.cleaned_data['area']
            tracking_id=(request.user.email[0:4]+str(random.randint(100,999))+types[0:2]+str(random.randint(0,9))+types[-1:-3]+area[1:3]).upper()
            complaint = form.save(commit=False)
            complaint.user_name = request.user
            complaint.tracking_id=tracking_id
            complaint.save()
            
            email_reciever=request.user.email
            sub='Complaint Registered'
            body=f'Hello {request.user}, \n\tYour complaint on {types} at {area}, It will be solved within two working days. You can track the complaint with this tracking {tracking_id}. \n\nGreen City\nChennai'
            #mail(email_reciever,sub,body)
            return redirect('user_complaints')
    else:
        form = ComplaintForm()
    return render(request, 'city/complaint.html', {'form': form})

@login_required(login_url='login')
def user_complaints(request):
    complaint=Complaint.objects.all().filter(user_name=request.user).order_by('-complaint_date')
    return render(request,'city/user_complaints.html',{'complaint':complaint})


def employee_login(request):
    if request.method=='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        
        if user is not None and user.is_employee==True:
            login(request,user)
            print(user.is_employee)
            # return render(request,"city/login.html")
            return redirect('emp_main')
        else:
            messages.info(request,'uername or password is incorrect')
    
    return render (request,'city/employee_login.html')

@login_required(login_url='employee_login')
def emp_main(request):
    if request.user.is_employee==True:
        new=Complaint.objects.all().filter(status='Submitted').count()
        pending=Complaint.objects.all().filter(status='Pending').count()
        solved=Complaint.objects.all().filter(status='Resolved').count()
        query=Queries.objects.all().count()
        context={
            'new':new,
            'pending':pending,
            'solved':solved,
            'query':query
        }
        return render(request,'city/emp_main.html',context=context)
    else:
        return redirect('employee_login')


@login_required(login_url='employee_login')
def new_complaints(request):
    
    if request.user.is_employee==True:
        new=Complaint.objects.all().filter(status='Submitted')
        return render(request,'city/new_complaints.html',{'new':new})
    else:
        return redirect('employee_login')
    
@login_required(login_url='employee_login')
def pending_complaints(request):
    
    if request.user.is_employee==True:
        pending=Complaint.objects.all().filter(status='Pending')
        return render(request,'city/pending_complaints.html',{'pending':pending})
    else:
        return redirect('employee_login')

@login_required(login_url='employee_login')
def solved_complaints(request):
    
    if request.user.is_employee==True:
        solved=Complaint.objects.all().filter(status='Resolved')
        return render(request,'city/solved_complaints.html',{'solved':solved})
    else:
        return redirect('employee_login')



@login_required(login_url='employee_login')
def update_new_complaints(request,pk):
    
    if request.user.is_employee==True:
        complaints=Complaint.objects.get(id=pk)
        form =UpdateForm(instance=complaints)
        context={
            'form':form
        }
        if request.method=='POST':
            form=UpdateForm(request.POST,instance=complaints)
            if form.is_valid():
                form.save()
                return redirect('new_complaints')
        return render(request,'city/update_complaints.html',context=context)
    else:
        return redirect('employee_login')

@login_required(login_url='employee_login')
def update_pending_complaints(request,pk):
    
    if request.user.is_employee==True:
        complaints=Complaint.objects.get(id=pk)
        form =UpdateForm(instance=complaints)
        context={
            'form':form
        }
        if request.method=='POST':
            form=UpdateForm(request.POST,instance=complaints)
            if form.is_valid():
                email_reciever=complaints.user_name.email
                sub='Complaint Resolved'
                body=f'Hello {complaints.user_name}, \nYour complaint on {complaints.complaint_type} at {complaints.area} has been resolved. \n\t\tThank You\nGreen City'
                form.save()
                #mail(email_reciever,sub,body)
                return redirect('pending_complaints')
        return render(request,'city/update_complaints.html',context=context)
    else:
        return redirect('employee_login')


@login_required(login_url='employee_login')
def update_solved_complaints(request,pk):
    
    if request.user.is_employee==True:
        complaints=Complaint.objects.get(id=pk)
        form =UpdateForm(instance=complaints)
        context={
            'form':form
        }
        if request.method=='POST':
            form=UpdateForm(request.POST,instance=complaints)
            if form.is_valid():
                form.save()
                return redirect('solved_complaints')
        return render(request,'city/update_complaints.html',context=context)
    else:
        return redirect('employee_login')


@login_required(login_url='employee_login')
def queries(request):
    if request.user.is_employee==True:
        queries=Queries.objects.all()
        if request.method=='POST':
            queries.all().delete()
            return redirect('queries')
        return render (request,'city/queries.html',{'queries':queries})
    else:
        return redirect('employee_login')

def check_status(request):
    if request.method=='POST':
        tracking_id=request.POST['id']
        try:
            complaints=Complaint.objects.get(tracking_id=tracking_id)
            return render(request,'city/check_status.html',{'complaints':complaints})
        except:
            messages.warning(request,'Invalid Tracking ID')
    return render(request,'city/check_status.html')