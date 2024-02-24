from django.contrib.auth.models import AbstractUser
from django.db import models
import os

# Create your models here.

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        existing_profile_picture = User.objects.get(pk=self.pk).profile_picture if self.pk else None
        
        if existing_profile_picture:
            existing_file_path = os.path.join(str(existing_profile_picture))
            
            os.remove(existing_file_path)

        super().save(*args, **kwargs)
