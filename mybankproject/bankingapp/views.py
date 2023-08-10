from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import LoginForm, BankInfoForm


def home(request):
    return render(request, 'home.html')


def login_user(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def dashboard(request):
    return render(request, 'dashboard.html')


# forms

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid username or password.')  # Add error message to form
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        # Create a user instance from the submitted data
        username = request.POST['username']
        password = request.POST['password']
        user = User(username=username)
        user.set_password(password)
        user.save()
        # Create a bank info instance associated with the user
        form = BankInfoForm(request.POST)
        if form.is_valid():
            bank_info = form.save(commit=False)
            bank_info.user = user
            bank_info.save()
            return redirect('')  # Redirect to a success page
    else:
        form = BankInfoForm()

    return render(request, 'register.html', {'form': form})


def dashboard(request):
    if request.method == 'POST':
        form = BankInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BankInfoForm()
    return render(request, 'dashboard.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')
