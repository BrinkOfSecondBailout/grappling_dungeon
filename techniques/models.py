from django.db import models

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

    name = models.CharField(max_length = 255)
    category = models.CharField(max_length = 20, choices=CATEGORY_CHOICES)
    privacy_status = models.CharField(max_length=20, choices=PRIVACY_CHOICES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
