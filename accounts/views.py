from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import auth
from accounts.models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages

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
            user = register_form.save()
            auth_login(request, user)
            print(user.email)
            return redirect('dashboard')
        else:
            for field, errors in register_form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('register')

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
                print(user.email)
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('login')

    login_form = CustomAuthenticationForm()
    context = {'login_form': login_form}
    return render(request, 'login.html', context)


def dashboard(request):
    if request.user.is_authenticated:
        all_users = User.objects.exclude(username='admin')
        return render(request, 'dashboard.html', {'all_users': all_users})
    else:
        return redirect('index')
    
def user(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=user_id)
        return render(request, 'user.html', {'user': user})
    else:
        return redirect('index')

def logout(request):
    auth.logout(request)
    return redirect('index')