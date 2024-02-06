from django.shortcuts import render, redirect


# Create your views here.
def add(request):
    if request.user.is_authenticated:
        return render(request, 'add_new.html')
    else:
        return redirect('index')

def private(request):
    if request.user.is_authenticated:
        return render(request, 'private_archive.html')
    else:
        return redirect('index')
    
def public(request):
    if request.user.is_authenticated:
        return render(request, 'public_archive.html')
    else:
        return redirect('index')