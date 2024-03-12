from django.db import models
from django.conf import settings
from accounts.models import User
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
    correspondence = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Threads in {self.inbox.owner.name}'s Inbox"

class Message(models.Model):
    content = models.TextField(max_length=1000)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Messages in {self.thread.inbox.owner.name}'s Inbox"
