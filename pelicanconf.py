#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import date
from filters import blog_date_format, default_description
import assets
import sitemap
import gzip_cache

AUTHOR = u'Pedro Rodriguez'
SITENAME = u'Pedro Rodriguez'
SITEURL = 'http://localhost:8000'
HOST = 'pedrorordiguez.io'

PATH = 'content'

TIMEZONE = 'America/Denver'

CURRENT_YEAR = date.today().year

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

PAGE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}/index.html'

STATIC_PATHS = [
    'robots.txt',
    'favicon.ico',
    'resume.pdf',
    'CNAME',
    'static',
    'posts'
]

DEFAULT_PAGINATION = 10

THEME = 'theme'

DEFAULT_METADATA = {
    'link_target': 'blank-target'
}

PLUGINS = [assets, sitemap, gzip_cache, 'ipynb.liquid']

SITEMAP = {
    'format': 'xml'
}

DEBUG_MODE = True

JINJA_FILTERS = {
    'blog_date_format': blog_date_format,
    'default_description': default_description
}

MARKUP = ('md', )

PLUGIN_PATHS = ['./plugins']
