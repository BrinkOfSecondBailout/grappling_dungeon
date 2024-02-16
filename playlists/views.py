from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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