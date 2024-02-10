from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomTechniqueCreationForm, CustomTechniqueChangeForm
from moviepy.video.io.VideoFileClip import VideoFileClip
from .models import Technique
from django.contrib import messages
from django.urls import reverse

# Create your views here.
@login_required
def add(request):
    if request.method == 'POST':
        tech_form = CustomTechniqueCreationForm(request.POST)
        if tech_form.is_valid:
            technique = tech_form.save(commit=False)
            technique.uploaded_by = request.user

            if technique.video_option == 'full':
                if 'youtube.com' in technique.youtube_url:
                    video_id = technique.youtube_url.split('v=')[1]
                    if '&' in video_id:
                        video_id = video_id.split('&')[0]
                    embed_url = f'https://www.youtube.com/embed/{video_id}'
                    technique.embed_url = embed_url
                else:
                    messages.error(request, 'Error uploading technique. Check the URL and ensure a valid Youtube link')
                    return redirect('add')

            if technique.video_option == 'cropped':
                start_time = technique.start_time
                end_time = technique.end_time

                video_url = technique.youtube_url
                cropped_video_path = crop_video(video_url, start_time, end_time)

                technique.cropped_video_path = cropped_video_path
            
            technique.save()
            messages.info(request, 'Successfully added new technique')
            return redirect('add')
    else:
        tech_form = CustomTechniqueCreationForm()

    context = {'tech_form': tech_form}
    return render(request, 'add_new.html', context)


def crop_video(video_url, start_time, end_time):
    video_clip = VideoFileClip(video_url)
    cropped_video_clip = video_clip.subclip(start_time, end_time)
    cropped_video_path = f"media/cropped_videos/{uuid.uuid4()}.mp4"
    cropped_video_clip.write_videofile(cropped_video_path, codec="libx264", audio_codec="aac")
    return cropped_video_path


@login_required
def private(request):
    user = request.user
    private_techniques = Technique.objects.filter(uploaded_by=user, privacy_status='private')
    return render(request, 'private_archive.html', {'private_techniques': private_techniques})



@login_required
def remove(request, technique_id):
    technique = get_object_or_404(Technique, id=technique_id)
    user = request.user
    if technique.uploaded_by != user:
        messages.error(request, 'You do not have the credentials to delete that')
        return redirect('private')
    else:
        messages.info(request, f'Successfully removed {technique.name} from database')
        technique.delete()
    return redirect('private')

@login_required
def edit(request, technique_id):
    technique = get_object_or_404(Technique, id=technique_id)
    user = request.user
    if technique.uploaded_by != user:
        messages.error(request, 'You do not have the credentials to modify that')
        return redirect('private')
    
    if request.method == 'POST':
        form = CustomTechniqueChangeForm(request.POST, instance=technique)
        if form.is_valid():
            form.save()
            messages.info(request, 'All changes successfully saved')
        else:
            messages.error(request, 'Changes not saved. Check your modifications')
        return redirect(reverse('edit', args=[technique.id]))

    form = CustomTechniqueChangeForm(instance=technique)

    return render(request, 'edit-technique.html', {'form': form, 'technique': technique})



@login_required
def public(request):
    return render(request, 'public_archive.html')