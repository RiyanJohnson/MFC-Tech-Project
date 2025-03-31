from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username}: {self.message}'

class Interests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(null=True)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username}: {self.message}'