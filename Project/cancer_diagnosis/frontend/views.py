# frontend/views.py
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully. Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Error creating user.')
    else:
        form = UserCreationForm()
    return render(request, 'create_user.html', {'form': form})
