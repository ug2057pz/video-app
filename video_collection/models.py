from django.db import models
from django.db import models
from urllib import parse
from django.core.exceptions import ValidationError

# Create your models here.

class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    video_id = models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        try:
            url_components = parse.urlparse(self.url)

            if url_components.scheme != 'https':
                raise ValidationError(f'Not a YouTube URL {self.url}')

            if url_components.netloc != 'www.youtube.com':
                raise ValidationError(f'Not a YouTube URL {self.url}')
                
            if url_components.path != '/watch':
                raise ValidationError(f'Not a YouTube URL {self.url}')
            
            query_string = url_components.query
            if not query_string:
                raise ValidationError(f'Invalid YouTube URL {self.url}')
            parameters = parse.parse_qs(query_string, strict_parsing=True)
            parameter_list = parameters.get('v')
            if not parameter_list:   # empty string, empty list... 
                raise ValidationError(f'Invalid YouTube URL parameters {self.url}')
            self.video_id = parameter_list[0]   # set the video ID for this Video object 
        except ValueError as e:   # URL parsing errors, malformed URLs
            raise ValidationError(f'Unable to parse URL {self.url}') from e

        super().save(*args, **kwargs)  # don't forget!
                    
    def __str__(self):
        if not self.notes:
            notes = 'No notes'
        else:
            notes = self.notes[:200]
            return f'ID: {self.pk}, Name: {self.name}, URL: {self.url},  \
            Video ID: {self.video_id},  Notes: {notes}'