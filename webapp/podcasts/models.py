from django.db import models
from django.urls import reverse


class Pod(models.Model):
    rss_link = models.URLField(unique=True)
    is_scraped = models.BooleanField(default=False)

    def get_absolute_url(self):  
        return reverse("pod-list")

    def __str__(self):
        return self.rss_link


class Podcast(models.Model):
    name = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=128)
    link = models.URLField()
    cover_image = models.URLField(null=True, blank=True)
    summary = models.TextField()
    rss = models.OneToOneField(
        Pod, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.title


class Episode(models.Model):
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    podcast_name = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    puid = models.CharField(max_length=128)

    def __str__(self):
        return self.title
