#!/usr/bin/env python
from datetime import date
import subprocess
from filters import blog_date_format, default_description, news
import assets
import sitemap
import gzip_cache


MARKUP = ("md",)
PLUGIN_PATHS = ["/home/entilzha/code/pelican-plugins", "./plugins"]
PLUGINS = [assets, sitemap, gzip_cache, "pubs", "react", "render_math"]
# PLUGINS = [assets, sitemap, gzip_cache, 'ipynb.liquid', 'pubs', 'react']
IGNORE_FILES = [".ipynb_checkpoints"]

LIQUID_CONFIGS = (
    ("IPYNB_FIX_CSS", "False", ""),
    ("IPYNB_SKIP_CSS", "False", ""),
    ("IPYNB_EXPORT_TEMPLATE", "base", ""),
)

AUTHOR = "Pedro Rodriguez"
SITENAME = "Pedro Rodriguez"
SITEURL = "http://localhost:8000"
HOST = "www.pedro.ai"

PATH = "content"

TIMEZONE = "US/Eastern"

CURRENT_YEAR = date.today().year

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

INDEX_URL = "blog"
INDEX_SAVE_AS = "blog/index.html"

ARTICLE_URL = "blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html"

TAGS_SAVE_AS = ""
TAG_SAVE_AS = ""
CATEGORIES_SAVE_AS = ""
CATEGORY_SAVE_AS = ""
AUTHORS_SAVE_AS = ""
AUTHOR_SAVE_AS = ""
ARCHIVES_SAVE_AS = ""
ARCHIVE_SAVE_AS = ""

PAGE_URL = "{slug}"
PAGE_SAVE_AS = "{slug}/index.html"

STATIC_PATHS = [
    "robots.txt",
    "favicon.ico",
    "cv.pdf",
    "resume.pdf",
    "CNAME",
    "static",
    "posts",
]

DEFAULT_PAGINATION = 10

THEME = "theme"

DEFAULT_METADATA = {"link_target": "blank-target"}


SITEMAP = {"format": "xml"}

DEBUG_MODE = True

JINJA_FILTERS = {
    "blog_date_format": blog_date_format,
    "default_description": default_description,
    "news": news,
}

MARKUP = ("md",)
