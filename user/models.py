from django.db import models
from django.contrib.auth.models import AbstractUser
from post.models import Post

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    chosen_posts = models.ManyToManyField(Post, related_name='chosen_by', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'



