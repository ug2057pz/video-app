from django.db import models

# Create your models here.
class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URl: {self.url}, Notes: {self.notes[:200]}'
    