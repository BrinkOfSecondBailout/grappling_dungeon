from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
def index(request):
    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    context = {'register_form': register_form, 'login_form': login_form}
    return render(request, 'index.html', context)
