from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from src.categories import create_category_page
import feedparser
import json
import os
import re

template_env = Environment(loader=FileSystemLoader(searchpath='./layouts/'))

podcast_file= open(os.path.join('podlist.json'), 'r')
podcast_list = json.loads(podcast_file.read())
podcast_file.close()
feed_list = []
podcast_list_json = podcast_list.items()

for k, v in podcast_list_json:
    feed_list.append(v)
     
ep=[]
audiofiles = []
ep_title = []
pod_title = []
pod_list = []

BASE_DIR = Path(__file__).resolve().parent.parent
output_dir = os.path.join(BASE_DIR, 'site')
os.system('mkdir site')
os.system('touch site/index.html')

for feed_link in feed_list:

    pod_obj = {}
    ep_list=[]
    episode_obj= {}
    c=0
    
    feed = feedparser.parse(feed_link)
    #https://feeds.pacific-content.com/commandlineheroes

    index_template = template_env.get_template('index.html')
    list_template = template_env.get_template('list.html')
    podcast_template = template_env.get_template('podcast.html')
    episode_template = template_env.get_template('episode.html')

    pod_obj['title'] = feed['feed']['title']

    pod_name=pod_obj['title']
    pod_name = re.sub('[^\w_.)( -]', '', pod_name)
    pod_name = pod_name.replace('(', '_')
    pod_name = pod_name.replace(')', '_')
    pod_name = pod_name.replace(' ', '_')

    os.system(f"cd site/ && mkdir list")
    os.system("touch site/list/index.html")

    os.system(f"cd site/ && mkdir {pod_name}")
    os.system(f"cd site/{pod_name} && mkdir ep")
    os.system(f"touch site/{pod_name}/index.html")

    for i in range(0,len(feed['entries'])):

        c+=1

        ep_title = feed['entries'][i]['title']

        if(feed['entries'][i].has_key('image')):
            if feed_link in ['https://feeds.buzzsprout.com/300035.rss', "https://www.omnycontent.com/d/playlist/aaea4e69-af51-495e-afc9-a9760146922b/b92baa3c-b9c8-488c-aa9e-aafd001cbf66/12abbc3c-ae53-487a-b83b-aafd001cbf79/podcast.rss"]:
                audiofiles = feed['entries'][i]['links'][0]['href']
            else:
                audiofiles = feed['entries'][i]['links'][1]['href']
            cover_image = feed['entries'][i]['image']['href']
            cover_image = cover_image.replace('http:', 'https:')
        else:
            if feed_link == 'https://www.pythonpodcast.com/feed/mp3/':
                audiofiles = feed['entries'][i]['links'][2]['href']
                cover_image = None
            elif (feed['feed']['image']['href']):
                cover_image = feed['feed']['image']['href']
                cover_image = cover_image.replace('http:', 'https:')

        obj = {}

        obj['name'] = feed['feed']['title']
        obj['title'] = ep_title
        obj['audiolink'] = audiofiles

        episode_obj['name'] = feed['feed']['title']
        episode_obj['podlink'] = f"/{pod_name}/"
        episode_obj['title'] = ep_title
        episode_obj['audiolink'] = audiofiles 
        episode_obj['cover'] = cover_image
        episode_obj['summary'] = str(feed['entries'][i]['summary'])
        episode_obj['link'] = feed['entries'][i]['links'][0]['href']
        episode_obj['date'] = feed['entries'][i]['published']

        os.system(f"cd site/{pod_name}/ep && mkdir {c}")
        os.system(f"touch site/{pod_name}/ep/{c}/index.html")
        
        obj['link'] = f"/{pod_name}/ep/{c}"
        if cover_image:
            obj['cover'] = cover_image
        else:
            obj['cover'] = None
        ep_list.append(obj)
        if(i==0):    
            ep.append(obj)

        with open(os.path.join(f"site/{pod_name}/ep/{c}/index.html"), 'w', encoding='utf-8') as ep_file:
            ep_file.write(
                    episode_template.render(
                        episode = episode_obj
                        )
                    )
    
    if cover_image:
        pod_obj['cover'] = feed['feed']['image']['href']
        pod_obj['cover'] = pod_obj['cover'].replace('http:', 'https:')
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
#os.system('python -m http.server -d site')
