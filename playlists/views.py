from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PlaylistForm
from .models import Playlist, PlaylistItem, Technique

# Create your views here.

@login_required
def find_playlist(request):
    if request.method == 'GET':
        user = request.user
        playlist = request.GET.get('playlist')
        if playlist:
            playlist_techniques = []
        else:
            playlist_techniques = []
    playlist_total = len(playlist_techniques)

    return render(request, 'playlist_results.html', {'playlist_techniques': playlist_techniques, 'playlist': playlist, 'playlist_total': playlist_total})

@login_required
def add_to_playlist(request):
    if request.method == 'POST':
        user = request.user
        playlist_name = request.POST.get('name')
        technique_id = request.POST.get('technique')
        print(playlist_name)
        print(technique_id)

        playlist = Playlist.objects.filter(owner=user, name=playlist_name).first()
        technique = get_object_or_404(Technique, id=technique_id)

        if playlist:
            order = PlaylistItem.objects.filter(playlist=playlist).count() + 1

            playlist_item = PlaylistItem(playlist=playlist, technique=technique, order=order)
            playlist_item.save()

            print(f'Technique added to existing playlist: {playlist_name}')

        else:
            new_playlist = Playlist(owner=user, name=playlist_name)
            new_playlist.save()

            order = 1

            playlist_item = PlaylistItem(playlist=new_playlist, technique=technique, order=order)
            playlist_item.save()

            print(f'Technique added to new playlist: {playlist_name}')

        return redirect('private')

    else:
        pass