from django.shortcuts import render, redirect


# Create your views here.
def add(request):
    return render(request, 'add_new.html')