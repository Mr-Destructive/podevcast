from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.categories import create_category_page
from pathlib import Path
from random import sample
import feedparser
import json
import os
import re

loader = FileSystemLoader(searchpath='./layouts/')
template_env = Environment(loader=loader, autoescape=select_autoescape())

podcast_file = open(os.path.join('podlist.json'), 'r')
podcast_list = json.loads(podcast_file.read())
podcast_file.close()
feed_list = []
podcast_list_json = podcast_list.items()

for k, v in podcast_list_json:
    feed_list.append(v)

ep = []
audiofiles = []
ep_title = []
pod_title = []
pod_list = []

BASE_DIR = Path(__file__).resolve().parent.parent
output_dir = os.path.join(BASE_DIR, 'site')
if not os.path.isdir(output_dir):
    os.system('mkdir site')
os.system('touch site/index.html')

for feed_link in feed_list:

    pod_obj = {}
    ep_list = []
    episode_obj = {}
    c = 0

    feed = feedparser.parse(feed_link)
    # https://feeds.pacific-content.com/commandlineheroes

    index_template = template_env.get_template('index.html')
    list_template = template_env.get_template('list.html')
    podcast_template = template_env.get_template('podcast.html')
    episode_template = template_env.get_template('episode.html')

    pod_obj['title'] = feed.get('feed').get('title')

    pod_name = pod_obj['title']
    pod_name = re.sub("[^a-zA-Z0-9\s]+", "", pod_name)
    pod_name = pod_name.replace('(', '_')
    pod_name = pod_name.replace(')', '_')
    pod_name = pod_name.replace(' ', '_')

    if not os.path.isdir('site/list'):
        os.system(f"cd site/ && mkdir list")
    os.system("touch site/list/index.html")

    if not os.path.isdir(f'site/{pod_name}'):
        os.system(f"cd site/ && mkdir {pod_name}")
        if not os.path.isdir(f'site/{pod_name}/ep'):
            os.system(f"cd site/{pod_name} && mkdir ep")

    os.system(f"touch site/{pod_name}/index.html")

    for i in range(0, len(feed['entries'])):

        c += 1

        ep_title = feed['entries'][i]['title']

        if('image' in feed['entries'][i]):
            if feed_link in ['https://feeds.buzzsprout.com/300035.rss', 
                            "https://www.omnycontent.com/d/playlist/aaea4e69-af51-495e-afc9-a9760146922b/b92baa3c-b9c8-488c-aa9e-aafd001cbf66/12abbc3c-ae53-487a-b83b-aafd001cbf79/podcast.rss", 
                            "https://pinecast.com/feed/ladybug-podcast",
                            "https://feeds.buzzsprout.com/1097978.rss"]:
                audiofiles = feed['entries'][i]['links'][0]['href']
            else:
                if len(feed["entries"][i]['links']) > 1:
                    audiofiles = feed['entries'][i]['links'][1]['href']
            cover_image = feed['entries'][i]['image']['href'].replace('http:', 'https:')
        else:
            if feed_link == 'https://www.pythonpodcast.com/feed/mp3/':
                audiofiles = feed['entries'][i]['links'][1]['href']
                cover_image = None
            elif feed.feed.get('image').get('href'):
                cover_image = (feed['feed']['image']['href']).replace('http:', 'https:')

        obj = {}

        obj['name'] = feed['feed']['title']
        obj['title'] = ep_title
        obj['audiolink'] = audiofiles
        obj['date'] = feed['entries'][i]['published']

        episode_obj['name'] = feed['feed']['title']
        episode_obj['podlink'] = f"/{pod_name}/"
        episode_obj['title'] = ep_title
        episode_obj['audiolink'] = audiofiles
        episode_obj['cover'] = cover_image
        episode_obj['summary'] = str(feed['entries'][i]['summary'])
        episode_obj['link'] = feed['entries'][i]['links'][0]['href']
        episode_obj['date'] = obj["date"]

        if not os.path.isdir(f'site/{pod_name}/ep/{c}'):
            os.system(f"cd site/{pod_name}/ep && mkdir {c}")
        os.system(f"touch site/{pod_name}/ep/{c}/index.html")

        obj['link'] = f"/{pod_name}/ep/{c}"
        if cover_image:
            obj['cover'] = cover_image
        else:
            obj['cover'] = None
        ep_list.append(obj)
        if(i == 0):
            ep.append(obj)

        with open(os.path.join(f"site/{pod_name}/ep/{c}/index.html"), 'w', encoding='utf-8') as ep_file:
            ep_file.write(
                    episode_template.render(
                        episode = episode_obj
                        )
                    )

    if cover_image:
        pod_obj['cover'] = cover_image.replace('http:', 'https:')
    else:
        pod_obj['cover'] = None
    pod_obj['list'] = ep_list
    pod_obj['links'] = f"/{pod_name}/"
    pod_obj['oglink'] = feed['feed']['link']
    pod_list.append(pod_obj)

    with open(os.path.join(f"site/{pod_name}/index.html"), 'w', encoding='utf-8') as pod_file:
        pod_file.write(
            podcast_template.render(
                podcast = pod_obj
                )
            )

ep = sorted(ep, key=lambda x: x["date"], reverse=True)[:13][3:]

with open(os.path.join('site/index.html'), 'w', encoding='utf-8') as index_file:
    index_file.write(
        index_template.render(
            ep=ep,
        )
    )

with open(os.path.join('site/list/index.html'), 'w', encoding='utf-8') as list_file:
    list_file.write(
        list_template.render(
            ep=pod_list,
        )
    )

create_category_page(pod_list)

os.system('cp -r static site')
# os.system('python -m http.server -d site')
