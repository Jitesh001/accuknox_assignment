from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} to {self.to_user}'

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friend1_set', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friend2_set', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user1} and {self.user2}'
