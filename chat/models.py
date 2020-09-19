from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(User,related_name='messages',on_delete=models.CASCADE,null=True)
    room= models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message