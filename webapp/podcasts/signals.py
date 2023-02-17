import feedparser
from django.db.models.signals import post_save
from django.dispatch import receiver
from podcasts.models import Pod, Podcast

@receiver(post_save, sender=Pod)
def scrap_pod_feed(sender, instance, created, **kwargs):
    if created:
        feed = feedparser.parse(instance.rss_link)
        obj = {}
        print(feed.feed.keys())
        obj['name'] = feed['feed']['title']
        obj['title'] = feed['feed']['title']
        obj['link'] = feed['feed']['link']
        obj['summary'] = feed['feed']['subtitle']
        podcast = Podcast.objects.create(**obj)
        print(podcast.id)
