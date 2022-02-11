from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import feedparser
import os

template_env = Environment(loader=FileSystemLoader(searchpath='./layouts/'))
feed_list = ['https://feeds.pacific-content.com/commandlineheroes',
        'https://www.pythonpodcast.com/feed/mp3/',
        'https://talkpython.fm/episodes/rss',
        'https://realpython.com/podcasts/rpp/feed',
        'https://feeds.simplecast.com/l_5sU3vk']
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

    feed = feedparser.parse(feed_link)
    #https://feeds.pacific-content.com/commandlineheroes


    index_template = template_env.get_template('index.html')
    list_template = template_env.get_template('list.html')
    podcast_template = template_env.get_template('podcast.html')

    for i in range(0,len(feed['entries'])):
        ep_title = feed['entries'][i]['title']
        audiofiles = feed['entries'][i]['links'][1]['href']
        if(feed['entries'][i].has_key('image')):
            cover_image = feed['entries'][i]['image']['href']
        else:
            cover_image = feed['feed']['image']

        obj = {}

        obj['title'] = ep_title
        obj['audiolink'] = audiofiles
        obj['cover'] = cover_image
        ep_list.append(obj)
        if(i==0):    
            ep.append(obj)


    pod_obj['title'] = feed['feed']['title']

    pod_name=pod_obj['title']
    pod_name = pod_name.replace(' ', '_')
    
    pod_obj['cover'] = feed['feed']['image']['href']
    pod_obj['list'] = ep_list
    pod_obj['links'] = f"/{pod_name}/"
    pod_list.append(pod_obj)
    
    os.system(f"cd site/ && mkdir list")
    os.system("touch site/list/index.html")

    pod_path = f"mkdir site/{pod_name}"
    os.system(f"cd site/ && mkdir {pod_name}")
    os.system("touch "+ pod_path +"/index.html")

    with open(os.path.join(f"site/{pod_name}/index.html"), 'w') as pod_file:
            pod_file.write(
                podcast_template.render(
                    podcast = pod_obj
                    )
                )



with open(os.path.join('site/index.html'), 'w') as index_file:
    index_file.write(
        index_template.render(
            ep=ep,
        )
    )

with open(os.path.join('site/list/index.html'), 'w') as list_file:
    list_file.write(
        list_template.render(
            ep=pod_list,
        )
    )
os.system('cp -r static site')
#os.system('python -m http.server -d site')
