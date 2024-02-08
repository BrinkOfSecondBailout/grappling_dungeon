from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomTechniqueCreationForm

# Create your views here.
@login_required
def add(request):
    if request.method == 'POST':
        tech_form = CustomTechniqueCreationForm(request.POST)
        if tech_form.is_valid:
            technique = tech_form.save(commit=False)
            technique.uploaded_by = request.user
            technique.save()
            return redirect('add')
    else:
        tech_form = CustomTechniqueCreationForm()

    context = {'tech_form': tech_form}
    return render(request, 'add_new.html', context)

@login_required
def private(request):
    return render(request, 'private_archive.html')

@login_required
def public(request):
    return render(request, 'public_archive.html')