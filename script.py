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
for feed_link in feed_list:
    pod_obj = {}
    feed = feedparser.parse(feed_link)
    #https://feeds.pacific-content.com/commandlineheroes


    index_template = template_env.get_template('index.html')
    list_template = template_env.get_template('list.html')

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
        if(i==0):    
            ep.append(obj)
    pod_obj['title'] = feed['feed']['title']
    pod_obj['cover'] = feed['feed']['image']['href']
    pod_list.append(pod_obj)


BASE_DIR = Path(__file__).resolve().parent.parent
output_dir = os.path.join(BASE_DIR, 'site')
os.system('mkdir site')
os.system('touch site/index.html')

with open(os.path.join('site/index.html'), 'w') as index_file:
    index_file.write(
        index_template.render(
            ep=ep,
        )
    )

with open(os.path.join('site/list.html'), 'w') as list_file:
    list_file.write(
        list_template.render(
            ep=pod_list,
        )
    )
os.system('cp -r static site')
#os.system('python -m http.server -d site')
