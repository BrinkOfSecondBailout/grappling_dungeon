from django.db import models
from django.conf import settings
# Create your models here.

class Technique(models.Model):
    CATEGORY_CHOICES = [
        ('passing', 'Passing'),
        ('guard', 'Guard'),
        ('submission', 'Submission'),
        ('takedown', 'Takedown'),
    ]

    PRIVACY_CHOICES = [
        ('private', 'Private'),
        ('group', 'Group'),
        ('public', 'Public'),
    ]

    VIDEO_CHOICES = [
        ('full', 'Full Youtube Video'),
        ('cropped', 'Crop Short Clip from Youtube Video'),
    ]

    user_model = settings.AUTH_USER_MODEL

    name = models.CharField(max_length = 255)
    category = models.CharField(max_length = 20, choices=CATEGORY_CHOICES)
    privacy_status = models.CharField(max_length=20, choices=PRIVACY_CHOICES)
    uploaded_by = models.ForeignKey(user_model, on_delete=models.CASCADE)
    video_option = models.CharField(max_length = 10, choices=VIDEO_CHOICES)
    youtube_url = models.URLField()

    start_time = models.PositiveIntegerField(blank=True, null=True)
    end_time = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
    
