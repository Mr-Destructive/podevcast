from datetime import datetime
import feedparser
from django.db.models.signals import post_save
from django.dispatch import receiver
from podcasts.models import Episode, Pod, Podcast


def scrape_podcast(feed_link):
    podcast = dict()
    episodes = list()
    feed = feedparser.parse(feed_link)
    podcast['name'] = feed['feed']['title']
    podcast['title'] = feed['feed']['title']
    podcast['link'] = feed['feed']['link']
    podcast['summary'] = feed['feed']['subtitle']

    podcast_episodes = feed['entries']
    for episode in podcast_episodes:
        episode_obj = dict()
        episode_obj['title'] = episode['title']
        episode_obj['description'] = episode['summary']
        episode_obj['link'] = episode['links'][0]['href']
        episode_obj['puid'] = episode['id']
        episode_obj['date'] = datetime.strptime(episode['published'], '%a, %d %b %Y %H:%M:%S %z')
        if episode.get('image'):
            cover_image = episode.get('image')
        elif feed.feed.get('image'):
            cover_image = feed.feed['image'].get('href')
        episode_obj['image'] = cover_image
        episodes.append(episode_obj)
    return podcast, episodes

@receiver(post_save, sender=Pod)
def scrap_pod_feed(sender, instance, created, **kwargs):
    if created:
        podcast, episodes = scrape_podcast(instance.rss_link)
        podcast = Podcast.objects.create(**podcast)
        for episode in episodes:
            episode_instance = Episode.objects.create(**episode)
        instance.is_scraped = True
        instance.save()
    elif not instance.is_scraped:
        podcasts = Podcast.objects.filter(id=instance.id)
        if not podcasts:
            podcast, episodes = scrape_podcast(instance.rss_link)
            podcast = Podcast.objects.create(**podcast)
        else:
            podcast = podcasts.first()
            episodes = Episode.objects.filter(podcast_name_id=podcast.id)
            if not episodes:
                _, episodes = scrape_podcast(instance.rss_link)

        print(podcast)
        for episode in episodes:
            episode['podcast_name_id'] = podcast.id
        Episode.objects.bulk_create([Episode(**episode) for episode in episodes])

        instance.is_scraped = True
        instance.save()

