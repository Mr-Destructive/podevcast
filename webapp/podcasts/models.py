from django.db import models


class Podcast(models.Model):
    name = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    link = models.URLField()
    cover_image = models.URLField()
    summary = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.title


class Pod(models.Model):
    rss_link = models.URLField()
    is_scraped = models.BooleanField(default=False)
    podcast = models.OneToOneField(
        Podcast, on_delete=models.CASCADE, null=True, blank=True
    )


class Episode(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    podcast_name = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    puid = models.CharField(max_length=128)

    def __str__(self):
        return self.puid
