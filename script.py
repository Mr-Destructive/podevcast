from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import feedparser
import os

template_env = Environment(loader=FileSystemLoader(searchpath='./layouts/'))
feed = feedparser.parse('https://feeds.pacific-content.com/commandlineheroes')

index_template = template_env.get_template('index.html')

ep=[]
audiofiles = []
ep_title = []
for i in range(0,len(feed['entries'])):
    ep_title=(feed['entries'][i]['title'])
    audiofiles=(feed['entries'][i]['links'][1]['href'])
    
    obj = {}
    obj['title'] = ep_title
    obj['audiolink'] = audiofiles
    ep.append(obj)

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
#os.system('python -m http.server -d site')
