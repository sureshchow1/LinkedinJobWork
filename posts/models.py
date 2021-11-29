import datetime

from django.db import models
# from django.contrib.auth.models import User
from LinkedinJobPost import settings
from userauth.models import User
# Create your models here.
from django.conf import settings

class Post(models.Model):
    text = models.TextField()
    image_linked = models.ImageField(upload_to='article/images/', blank=True, null=True)
    video_linked = models.FileField(upload_to='article/videos/', blank=True, null=True)
    doc_linked = models.FileField(upload_to='article/docs', blank=True, null=True)
    # Remove later
    media_type = models.CharField(max_length=6, null=True)
    written_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles")
    bookmarked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="bookmarked_posts", blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return f'{self.written_by.first_name} {self.written_by.last_name} : {self.text[:30]}'

    class Meta:
        ordering = ('-posted_at',)