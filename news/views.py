# news/views.py

from django.shortcuts import render
from django.views.generic import ListView
from .models import News
import feedparser
import random
import datetime
# import requests
# from bs4 import BeautifulSoup


class NewsListView(ListView):
    """Listing of news"""
    template_name = 'news/news-list.html'
    paginate_by = 10

    def get_queryset(self):

        news = []

        for src in News.objects.all():
            publisher = src.publisher
            url = src.rss_url
            fdate = src.date_format
            posts = feedparser.parse(url)
            author_title = src.publisher
            tags = src.tags

            query_srch = tags.split()

            for post in posts['entries']:
                if query_srch:
                    for tag in query_srch:
                        if tag:
                            if tag in post.get('title') or tag in post.get('description'):
                                title = post.get('title')
                                link = post.get('link')
                                content = post.get('description')
                                if post.get('enclosures'):
                                    image = post.get('enclosures')[0]['href']
                                else:
                                    image = None
                                published = datetime.datetime.strptime(
                                    post.get('published'), fdate).strftime('%d.%m.%Y %H:%M')
                                news.append(
                                    [published, title, content, link, author_title, image, ])
                                break
                            else:
                                continue
                        else:
                            continue
                else:
                    title = post.get('title')
                    link = post.get('link')
                    content = post.get('description')
                    if post.get('enclosures'):
                        image = post.get('enclosures')[0]['href']
                    else:
                        image = None
                    published = datetime.datetime.strptime(
                        post.get('published'), fdate).strftime('%d.%m.%Y %H:%M')
                    news.append([published, title, content,
                                 link, author_title, image, ])

        return sorted(news, key=lambda new: datetime.datetime.strptime(new[0], '%d.%m.%Y %H:%M'), reverse=True)
