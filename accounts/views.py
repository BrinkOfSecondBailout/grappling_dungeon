from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from accounts.models import User
from techniques.models import Technique
from playlists.models import Playlist
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
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
        user = request.user
        all_users = User.objects.exclude(username='admin')
        total_users = len(all_users)
        private_techniques = Technique.objects.filter(uploaded_by=user, privacy_status='private')
        total_private = len(private_techniques)
        playlists = Playlist.objects.filter(owner=user)
        return render(request, 'dashboard.html', {'all_users': all_users, 'total_users': total_users, 'total_private': total_private, 'playlists': playlists })
    else:
        return redirect('index')

@login_required
def user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user.html', {'user': user})


def edit(request):
    if request.user.is_authenticated:
        user = request.user

        if (request.method == 'POST'):
            form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.info(request, 'All changes successfully saved.')
                return redirect('edit')
        else:
            form = CustomUserChangeForm(instance=user)

        return render(request, 'edit.html', {'form': form})
    else:
        return redirect('index')

@login_required
def password(request):
    return redirect('password_change')


def logout(request):
    auth.logout(request)
    return redirect('index')