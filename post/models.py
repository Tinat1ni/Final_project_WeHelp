from django.db import models
from django.conf import settings
from datetime import datetime


class Category(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=20, blank=True)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    picture = models.ImageField('picture',upload_to='post_pictures/', null=True, blank=True,  default='default_images/default_picture.png')
    deadline_date = models.DateField(null=True, blank=True)
    deadline_time = models.TimeField(null=True, blank=True)
    custom_input_1 = models.CharField(max_length=255, blank=True, null=True)  # Add this line
    custom_input_2 = models.CharField(max_length=255, blank=True, null=True)  # Add this line
    prefer = models.CharField(max_length=255, blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='posts', blank=True)
    completed = models.BooleanField(default=False)

    deadline = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.deadline_date and self.deadline_time:
            self.deadline = datetime.combine(self.deadline_date, self.deadline_time)
        super(Post, self).save(*args, **kwargs)


    def __str__(self):
        return self.title or 'no title'





