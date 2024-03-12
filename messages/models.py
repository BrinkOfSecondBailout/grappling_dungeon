from django.db import models
from django.conf import settings

# Create your models here.

class Inbox(models.Model):
    user_model = settings.AUTH_USER_MODEL
    owner = models.ForeignKey(user_model, on_delete=models.SET_NULL, null=True)

    new_items = models.PositiveIntegerField(default=0)
    total_items = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.owner.username}'s Inbox"
    
class Thread(models.Model):
    inbox = models.ForeignKey(Inbox, on_delete=models.CASCADE, related_name='threads')

    def __str__(self):
        return f"Thread in {self.inbox.owner.name}'s Inbox"

class Message(models.Model):
    content = models.TextField(max_length=1000)
    
