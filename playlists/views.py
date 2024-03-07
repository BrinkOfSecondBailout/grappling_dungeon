from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import PlaylistForm, PlaylistChangeForm
from .models import Playlist, PlaylistItem, Technique
from django.contrib import messages
from django.http import JsonResponse
import json

# Create your views here.
@login_required
def show_playlist(request, playlist_id):
    user = request.user
    current_playlist = get_object_or_404(Playlist, id=playlist_id)
    all_playlists = Playlist.objects.filter(owner=user)

    if current_playlist and current_playlist.owner == user:
        playlist_items = PlaylistItem.objects.filter(playlist=current_playlist).order_by('order')
        playlist_techniques = [item.technique for item in playlist_items]
        form = PlaylistChangeForm(instance=current_playlist)
        return render(request, 'show_playlist.html', {'playlist_techniques': playlist_techniques, 'playlist': current_playlist, 'form': form, 'playlists': all_playlists})
    else:
        print(f'Unauthorized actions')
        return redirect('private')


@login_required
def add_to_playlist(request):
    if request.method == 'POST':
        user = request.user
        playlist_name = request.POST.get('name')
        technique_id = request.POST.get('technique')

        if playlist_name:
            playlist = Playlist.objects.filter(owner=user, name=playlist_name).first()
            technique = get_object_or_404(Technique, id=technique_id)

            if playlist:
                if PlaylistItem.objects.filter(playlist=playlist, technique=technique).exists():
                    print(f'This technique already exists in playlist: {playlist_name}')
                    messages.error(request, f'This technique already exists in playlist: {playlist_name}')
                    return redirect('private')

                order = PlaylistItem.objects.filter(playlist=playlist).count() + 1

                playlist_item = PlaylistItem(playlist=playlist, technique=technique, order=order)
                playlist_item.save()
                messages.info(request, f'Technique added to existing playlist: {playlist_name}')
                print(f'Technique added to existing playlist: {playlist_name}')

            else:
                new_playlist = Playlist(owner=user, name=playlist_name)
                new_playlist.save()

                order = 1

                playlist_item = PlaylistItem(playlist=new_playlist, technique=technique, order=order)
                playlist_item.save()
                messages.info(request, f'Technique added to new playlist: {playlist_name}')
                print(f'Technique added to new playlist: {playlist_name}')

            return redirect('private')
        else:
            messages.error(request, f'Name for playlist is required')
            print(f'Name for playlist is required')
            return redirect('private')

    else:
        pass


@login_required
def extract_from_playlist(request, technique_id, playlist):
    user = request.user
    technique = get_object_or_404(Technique, id=technique_id)
    current_playlist = get_object_or_404(Playlist, name=playlist)
    if (current_playlist.owner == user):
        playlist_item = get_object_or_404(PlaylistItem, playlist=current_playlist, technique=technique)
        playlist_item.delete()

        print(f'Technique {technique.name} removed from playlist {playlist}')

        if PlaylistItem.objects.filter(playlist=current_playlist).count() == 0:
            current_playlist.delete()
            print(f'Playlist {playlist} deleted since it has no items')
            messages.info(request, f'Successfully removed the last item and the empty playlist "{playlist}"')
            return redirect('all_playlists')
    else:
        print(f'Unauthorized actions')
    return redirect(reverse('edit_playlist', args=[current_playlist.id]))


@login_required
def edit_playlist(request, playlist_id):
    user = request.user
    current_playlist = get_object_or_404(Playlist, id=playlist_id)
    all_playlists = Playlist.objects.filter(owner=user)

    if request.method == 'POST':
        form = PlaylistChangeForm(request.POST, instance=current_playlist)
        if form.is_valid():
            form.save()
            messages.info(request, 'All changes successfully saved')
        else:
            messages.error(request, 'Changes not saved. Check your modifications')
        return redirect(reverse('edit_playlist', args=[playlist_id]))
    else:
        if current_playlist and current_playlist.owner == user:
            playlist_items = PlaylistItem.objects.filter(playlist=current_playlist).order_by('order')
            playlist_techniques = [item.technique for item in playlist_items]
            form = PlaylistChangeForm(instance=current_playlist)
            return render(request, 'edit_playlist.html', {'playlist_techniques': playlist_techniques, 'playlist': current_playlist, 'form': form, 'playlists': all_playlists})
        else:
            print(f'Unauthorized actions')
            return redirect('private')
        
@login_required
def all_playlists(request):
    user = request.user
    playlists = Playlist.objects.filter(owner=user)
    playlist_and_technique = {}

    for playlist in playlists:
        item = PlaylistItem.objects.filter(playlist_id=playlist.id).first()
        technique = get_object_or_404(Technique, id=item.technique_id)
        playlist_and_technique[playlist] = technique

    context = {
        'playlist_and_technique': playlist_and_technique,
    }

    return render(request, 'all_playlists.html', context)

@login_required
def new_playlist(request):
    user = request.user

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        playlist_name = data['name']
        techniques = data['techniques']
        description = data['description']
        new_playlist = Playlist(owner=user, name=playlist_name, description=description)
        new_playlist.save()

        order = 1
        for technique_id in techniques:
            technique = get_object_or_404(Technique,id=technique_id)
            playlistItem = PlaylistItem(playlist=new_playlist, technique=technique, order=order)
            playlistItem.save()
            order += 1

        return JsonResponse({'success': True})


    else:
        all_techniques = Technique.objects.filter(uploaded_by=user)
        all_playlists = Playlist.objects.filter(owner=user)

        context = {
            'all_techniques': all_techniques,
            'playlists': all_playlists
        }
        return render(request, 'new_playlist.html', context)

@login_required
def delete_whole_playlist(request, playlist_id):
    user = request.user
    current_playlist = get_object_or_404(Playlist, id=playlist_id)
    if current_playlist.owner == user:
        current_playlist.delete()
        messages.info(request, f'Playlist {current_playlist.name} successfully deleted')
        print(f'Playlist "{current_playlist.name}" successfully deleted')
    else:
        print(f'Unauthorized actions')
        messages.error(request, 'Unauthorized actions')
    return redirect('all_playlists')
