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

        existing_file_path = os.path.join('media', str(existing_profile_picture))
        
        if existing_profile_picture != self.profile_picture:
            if existing_profile_picture:
                if os.path.exists(existing_file_path):
                    os.remove(existing_file_path)
                    print(f'Removing existing profile picture at {existing_file_path}')
                    print('New profile picture saved')
                else:
                    print(f'Cannot find existing profile picture at {existing_file_path}')
                    print('New profile picture saved')

        super().save(*args, **kwargs)
