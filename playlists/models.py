from django.db import models
from django.conf import settings
from techniques.models import Technique

# Create your models here.

class Playlist(models.Model):


    user_model = settings.AUTH_USER_MODEL

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True)
    techniques = models.ManyToManyField(Technique, through='PlaylistItem')
    owner = models.ForeignKey(user_model, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    technique = models.ForeignKey(Technique, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.playlist.owner.username}'s Playlist Item {self.order}"
