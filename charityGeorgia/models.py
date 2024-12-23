from django.db import models

class Charity(models.Model):
    name = models.CharField(max_length=255)
    scraped_text = models.TextField()
    website = models.URLField()


    def __str__(self):
        return self.name


