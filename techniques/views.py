from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def add(request):
    return render(request, 'add_new.html')

@login_required
def private(request):
    return render(request, 'private_archive.html')

@login_required
def public(request):
    return render(request, 'public_archive.html')