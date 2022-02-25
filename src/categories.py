from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from .podcategory import create_podcast_category
import feedparser
import json
import os


def create_category_page(pod_list):
    category_file = open(os.path.join('src/categorylist.json'), 'r')
    category_list = json.loads(category_file.read())
    category_file.close()

    categories = list(category_list.keys())

    loader = FileSystemLoader(searchpath='./layouts/')
    template_env = Environment(loader=loader, autoescape=select_autoescape())
    category_template = template_env.get_template('categories.html')

    catlist = []

    if not os.path.isdir(f'site/category'):
        os.system(f"cd site/ && mkdir category")

    for category in categories:
        cat_obj = {}
        cat_obj['title'] = category
        category = category.replace(' ', '_')
        cat_obj['link'] = f"/category/{category}/"
        catlist.append(cat_obj)

        if not os.path.isdir(f'site/category/{category}'):
            os.system(f"cd site/category && mkdir {category}")
        os.system(f"touch site/category/index.html")
        os.system(f"touch site/category/{category}/index.html")

        create_podcast_category(category, pod_list)

    with open(os.path.join(f"site/category/index.html"), 'w', encoding='utf-8') as cat_file:
        cat_file.write(
                category_template.render(
                    categories = catlist
                    )
                )
