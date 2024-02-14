from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomTechniqueCreationForm, CustomTechniqueChangeForm, CustomNoteChangeForm
from moviepy.video.io.VideoFileClip import VideoFileClip
from .models import Technique
from django.contrib import messages
from django.urls import reverse
from pytube import YouTube
import os
import time
import uuid

# Create your views here.
@login_required
def add(request):
    if request.method == 'POST':
        if request.POST['start_time'] and ':' in request.POST['start_time']:
            start_minutes, start_seconds = map(int, request.POST['start_time'].split(':'))
            new_start_time = start_minutes * 60 + start_seconds

        if request.POST['end_time'] and ':' in request.POST['end_time']:
            end_minutes, end_seconds = map(int, request.POST['end_time'].split(':'))
            new_end_time = end_minutes * 60 + end_seconds

        if request.POST['start_time'] and request.POST['end_time']:
            modified_form = {
                'csrfmiddlewaretoken': request.POST['csrfmiddlewaretoken'],
                'name': request.POST['name'],
                'athlete': request.POST['athlete'],
                'category': request.POST['category'],
                'privacy_status': request.POST['privacy_status'],
                'youtube_url': request.POST['youtube_url'],
                'video_option': request.POST['video_option'],
                'note': request.POST['note'],
                'keywords': request.POST['keywords'],
                'start_time': new_start_time,
                'end_time': new_end_time,
            }
            tech_form = CustomTechniqueCreationForm(modified_form)
        else:
            tech_form = CustomTechniqueCreationForm(request.POST)

        if tech_form.is_valid():
            technique = tech_form.save(commit=False)
            user = request.user
            technique.uploaded_by = user

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

                if not cropped_video_path:
                    messages.error(request, 'Timeout: File not downloaded within allotted time')
                    return redirect('add')
                
                technique.cropped_video = cropped_video_path
            
            technique.save()
            messages.info(request, 'Successfully added new technique')
            return redirect('add')
        else: 
            print(tech_form.errors)
            messages.error(request, 'Error uploading technique. Check the form for errors.')
            return redirect('add')
    else:
        tech_form = CustomTechniqueCreationForm()

    context = {'tech_form': tech_form}
    return render(request, 'add_new.html', context)


def crop_video(video_url, start_time, end_time):
    try:
        youtube_video = YouTube(video_url)
        video_stream = youtube_video.streams.filter(file_extension='mp4').first()
        custom_name = 'temp_video'

        video_stream.download(output_path='media/temp/', filename=f'{custom_name}.mp4')

        temp_download_path = f'media/temp/{custom_name}.mp4'

        max_wait_time = 20
        waited_time = 0

        while not os.path.exists(temp_download_path) and waited_time < max_wait_time:
            time.sleep(1)
            waited_time += 1

        if os.path.exists(temp_download_path):
            video_clip = VideoFileClip(temp_download_path)
            cropped_video_clip = video_clip.subclip(start_time, end_time)

            cropped_video_name = f'{uuid.uuid4()}.mp4'
            cropped_video_path = f'media/cropped_videos/{cropped_video_name}'
            cropped_video_clip.write_videofile(codec='libx264', audio_codec='aac', filename=cropped_video_path)

            video_clip.reader.close()
            video_clip.audio.reader.close_proc()
            os.remove(temp_download_path)
            print(cropped_video_path)
            return cropped_video_path
        else:
            print('Timeout: File not downloaded within allotted time')
            return None


    except Exception as e:
        print(f'Error: {e}')
        return None


@login_required
def private(request):
    user = request.user
    private_techniques = Technique.objects.filter(uploaded_by=user, privacy_status='private')
    total = len(private_techniques)
    categories = private_techniques.values_list('category', flat=True).distinct()

    context = {
        'private_techniques': private_techniques,
        'categories': categories,
        'total': total,
    }

    return render(request, 'private_archive.html', context)



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
def save_note(request, technique_id):
    technique = get_object_or_404(Technique, id=technique_id)
    user = request.user
    if technique.uploaded_by != user:
        messages.error(request, 'You do not have the credentials to modify that')
        return redirect('private')
    
    print(request.POST)
    form = CustomNoteChangeForm(request.POST, instance=technique)
    print(form)
    if form.is_valid():
        form.save()
        messages.info(request, 'Note successfully saved')
    else:
        messages.error(request, 'Error saving note. Try again.')
        redirect(reverse('edit', args=[technique.id]))
    return redirect('private')

@login_required
def filter_result(request):
    if request.method == 'GET':
        user = request.user
        category = request.GET.get('category')
        if category:
            filtered_data = Technique.objects.filter(uploaded_by=user, privacy_status='private', category=category)
        else:
            filtered_data = [];
    results_total = len(filtered_data)

    return render(request, 'filtered_results.html', {'filtered_data': filtered_data, 'category': category, 'results_total': results_total})

@login_required
def search_result(request):
    if request.method == 'GET':
        user = request.user
        keywords = request.GET.get('keywords')
        if keywords:
            search_keywords = keywords.split()

            search_result = Technique.objects.filter(
                uploaded_by=user,
                privacy_status='private',
                keywords__icontains=search_keywords[0]
            )

            for keyword in search_keywords[1:]:
                search_result = search_result.filter(keywords__icontains=keyword)
        else:
            search_result = [];
    results_total = len(search_result)

    return render(request, 'search_results.html', {'search_result': search_result, 'keywords': keywords, 'results_total': results_total})

@login_required
def public(request):
    return render(request, 'public_archive.html')

