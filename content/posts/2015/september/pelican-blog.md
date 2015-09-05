Title: Creating a Github Pages Website with Pelican
Date: 2015-9-5
Tags: python, github pages, pelican
Slug: github-website-with-pelican
Author: Pedro Rodriguez
Description: Guide for creating website with Github Pages and Pelican
Status: draft

This week I finally got around to refreshing my resume, and with it decided to also refresh my website. Previously,
I had two websites: a Ghost blog at pedrorodriguez.io and a resume site at cv.pedrorodriguez.io. I didn't like the
Ghost blog because: 1. It costs money to host and 2. For writing purposes it wasn't ideal (I love Vim bindings).
The problem with the resume site was that it was hard to keep up to date and didn't most visitors didn't scroll below
the fold.

So, I am tried something new which will hopefully encourage me to write more often, make it easier, and serve as a
better web front for myself. The main components I used were:

1. Github Pages to host the site
2. Pelican to generate static HTML for Github Pages using Markdown and Jinja2 templates
3. `ghp-import` to stitch the two together.

Github Pages is a service that can take care of hosting a static HTML or Jekyll website using a Github respository. For
example, this blog's code is at [github.com/EntilZha/entilzha.github.io](https://github.com/EntilZha/entilzha.github.io).
The nice thing about using it is that I can update my website in the same way that I work on code: via Git. Likewise,
I can write in whatever editor suits my fancy (currently Vim, Atom, or Jetbrains IDEs).
