from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import auth
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# Create your views here.
def index(request):
    login_form = CustomAuthenticationForm()
    register_form = CustomUserCreationForm()
    context = {'register_form': register_form, 'login_form': login_form}
    return render(request, 'index.html', context)

def register(request):
    if request.method == 'POST':
        register_form = CustomUserCreationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return redirect('dashboard')
        else:
            return redirect('login')

    register_form = CustomUserCreationForm()
    context = {'register_form': register_form}
    return render(request, 'register.html', context)

def login(request):
    if request.method == 'POST':
        login_form = CustomAuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
            if user is not None:
                auth_login(request, user)
            return redirect('dashboard')

    login_form = CustomAuthenticationForm()
    context = {'login_form': login_form}
    return render(request, 'login.html', context)


def dashboard(request):
    return render(request, 'dashboard.html')

def logout(request):
    auth.logout(request)
    return redirect('index')