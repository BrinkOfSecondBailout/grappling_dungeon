from django.db import models
from django.conf import settings

# Create your models here.

class Inbox(models.Model):
    user_model = settings.AUTH_USER_MODEL
    owner = models.ForeignKey(user_model, on_delete=models.SET_NULL, null=True)

    new_items = models.PositiveIntegerField(default=0)
    total_items = models.PositiveIntegerField(default=0)