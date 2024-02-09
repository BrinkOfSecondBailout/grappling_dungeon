from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomTechniqueCreationForm
from moviepy.video.io.VideoFileClip import VideoFileClip

# Create your views here.
@login_required
def add(request):
    if request.method == 'POST':
        tech_form = CustomTechniqueCreationForm(request.POST)
        if tech_form.is_valid:
            technique = tech_form.save(commit=False)
            technique.uploaded_by = request.user

            if technique.video_option == 'cropped':
                start_time = technique.start_time
                end_time = technique.end_time

                video_url = technique.youtube_url
                cropped_video_path = crop_video(video_url, start_time, end_time)

                technique.cropped_video_path = cropped_video_path
            
            technique.save()
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
    return render(request, 'private_archive.html')

@login_required
def public(request):
    return render(request, 'public_archive.html')