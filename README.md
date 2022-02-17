## Podevcast

### Podevcast is a web application or a static site that renders the top programming/development podcasts. You can listen to the top podcasts around developer community from a single source. 

Podevcast, is a static site generated using a script. There is a static site generation which is heavily done in Python and deployed to Netlify. You can simply listen to the podcasts in the web page or go to the canonical page of the podcast episode. From the canonical page you can choose to hop to your choice music player, but the default music player should be fine for casual listening. The core idea is to keep things a single place for developer podcast.

## Preview

Podevcast has multiple pages like:

1. [Home page](https://podevcast.netlify.app/)
2. [Podcast page](https://podevcast.netlify.app/list)
3. [Episode page](https://podevcast.netlify.app/the_real_python_podcast/ep/1/)
4. [Podcast List page](https://podevcast.netlify.app/command_line_heroes/)
5. [Categories page](https://podevcast.netlify.app/category/)

The Home page has the latest episode of all the podcasts. It also has the audio player to play on the go.

![Podevcast home page](https://res.cloudinary.com/techstructive-blog/image/upload/v1645113477/blog-media/iafi8nthhj0vvvrcbhka.png)

The Podcast List page has the list of all the Podcast available in the project. It has the name of the podcast with the link to the podcast page that has the list of all the episodes of that podcast.

![Podevcast Podcast list](https://res.cloudinary.com/techstructive-blog/image/upload/v1645113598/blog-media/cnprgufs3lrouvgdl8jn.png)

The categories page has the list of categories of the podcasts like Web-development, backend, frontend, data science, DevOps and so on. More categories will be added soon.

![Podevcast Categories](https://res.cloudinary.com/techstructive-blog/image/upload/v1645113626/blog-media/uloq4xi1d4zfo8sfl7bm.png)

The Episode page has the audio player, the summary of the episode, canonical episode and podcast page. 

![Podevcast Episode page](https://res.cloudinary.com/techstructive-blog/image/upload/v1645113654/blog-media/omqks44p8b3u7jclkhgz.png)

## Why Podevcast?

Listening to music is one thing and listening to Podcast is different. I wanted a place from where developers can listen to developer specific podcast from a dingle source not just give out the article **"Top 10 podcast you should be listening as a developer"**. Having played around with python and some libraries like feedparser and jinga previously I saw this Hackathon as an opportunity to convert the idea into a project. It fits the JAMStack area well from the Hackathon and project perspective.  

## Tech Stack

- Python
  - [feedparser](https://pypi.org/project/feedparser/)
  - [jinga2](https://pypi.org/project/Jinja2/)
- GitHub Actions
- HTML / CSS

The data is extracted from various RSS Feeds using the feedparser library in Python. 

Using GitHub Actions, the feed is refreshed every 24 hours to fetch the latest episodes from the respective podcast feeds. Basically the GitHub action triggers a Netlify deployment that in turn generates the static site by running the script.

The command for running the script on Netlify and generating the `Podevcast` webpage is :

```
pip install -r rquirements.txt && python script.py
```

And the directory for deployed web pages (published directory) is `site` which contains all the `HTML` files that can be rendered as the website itself. 