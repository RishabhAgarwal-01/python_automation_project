from django.shortcuts import render
from django.http import HttpResponse
from dataentry.tasks import celery_test_task
from .forms import RegistrationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth


def home(request):
    return render(request,'home.html')


def celery_test(request):

    # testing the celery tasks 
    celery_test_task.delay()

    return HttpResponse('<h3>Function Got Executed </h3>')



def register(request):
    if request.method == 'POST':
        # 1. Capture the data submitted in the form
        form = RegistrationForm(request.POST)
        
        # 2. Check if passwords match, username is unique, etc.
        if form.is_valid():
            form.save() # Saves the new user to the database
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('home') # Redirect to home (or login page once you build it)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # If it's a GET request, just show the empty form
        form = RegistrationForm()
        
    context = {'form': form}
    return render(request, 'register.html', context)



def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')  # Redirect to home page after successful login

            else:
                messages.error(request, 'Invalid username or password.')
                
    else:
        form = AuthenticationForm()

    context = {'form': form}
    return render(request, 'login.html', context)



def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')  # Redirect to home page after logout