from jinja2 import Environment, FileSystemLoader
import json
import os

def create_podcast_category(category, pod_list):

    category_file = open(os.path.join('src/categorylist.json'), 'r')
    category_list = json.loads(category_file.read())
    category_file.close()

    template_env = Environment(loader=FileSystemLoader(searchpath='./layouts/'))
    podcast_list_template = template_env.get_template('category.html')

    cat_list = list(category_list[category.replace('_', ' ')])
    cat_podcast_list = []
    
    if cat_list:
        for categ in cat_list:
            podcast_data = {}
            index = [ j for j, v in enumerate(pod_list) if categ in v.values()][0]
            podcast_data['title'] = pod_list[index]['title']
            podcast_data['link'] = pod_list[index]['links']
            podcast_data['cover'] = pod_list[index]['cover']

            cat_podcast_list.append(podcast_data)

            with open(os.path.join(f"site/category/{category}/index.html"), 'w', encoding='utf-8') as cat_file:
                cat_file.write(
                    podcast_list_template.render(
                        podcast_list = cat_podcast_list
                        )
                    )

        



