from django.db import models
from django.conf import settings

# Create your models here.

class Playlist(models.Model):


    user_model = settings.AUTH_USER_MODEL

    owner = models.ForeignKey(user_model, on_delete=models.CASCADE)