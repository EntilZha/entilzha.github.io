Title: Creating a Github Pages Website with Pelican
Date: 2015-9-15
Tags: python, github pages, pelican
Slug: github-website-with-pelican
Author: Pedro Rodriguez
Description: Guide for creating website with Github Pages and Pelican

The (PhD) intern application season fast approaching which means its about time to refresh all those websites, resumes,
and cvs out there, including mine. In the process of working on my website, I decided to switch my hosting and workflow.

Before my recent changes, I had two websites: a [Ghost](https://ghost.org/) blog at
[pedrorodriguez.io](http://pedrorodriguez.io) and a resume site at [cv.pedrorodriguez.io](http://cv.pedrorodriguez.io).
I didn't like the first because it costs money to host (I am now a "poor" grad student, so finding
savings here and there is *very nice*). Second, I didn't want to invest the time to learn Ghost's templating system, and
keep the server updated to prevent all those
[nasty security bugs](http://www.wired.com/2014/12/most-dangerous-software-bugs-2014/). Lastly, my career site and
actual resume fell far out of sync. It is much better to maintain only a [resume](http://pedrorodriguez.io/resume.pdf)
and point to it from here.

Roughly speaking, the website portion involved:

1. [Github Pages](https://pages.github.com/) to host the site.
2. [Pelican](http://docs.getpelican.com/en/3.6.3/) to generate static HTML for [Github Pages](https://pages.github.com/)
using Markdown and [Jinja2](http://jinja.pocoo.org/) templates.
3. [`ghp-import`](https://github.com/davisp/ghp-import) to stitch the two together.

[Github Pages](https://pages.github.com/) is a service that can take care of hosting a static HTML or
[Jekyll](http://jekyllrb.com/) website using a Github repository. For
example, this blog's code is at [github.com/EntilZha/entilzha.github.io](https://github.com/EntilZha/entilzha.github.io).
This has the advantage of being a git/vim centric workflow, no security maintenance requirements, and easy to understand.

At the center of this is using software to compile template files and posts to valid HTML/CSS/Javascript. This is
what engines such as Jekyll do. Since the only thing to host are static files, it is dead simple and cheap/free to host
on Github Pages and many other places.

While I could have used Jekyll and been happy, there turned out to be a
[Python equivalent, Pelican](http://docs.getpelican.com/en/3.6.3). Given the choice between Ruby and Python, I
prefer Python since I am more comfortable and productive with it.

Lets get started.

### Github Pages
In my case, I initially setup the domain [entilzha.github.io](https://entilzha.github.io). Since it is a account page
(as opposed to a project page), Github requires that the repository name be exactly named `username.github.io`.
After creating this, the master branch is automagically deployed to [username.github.io](https://entilzha.github.io).

To host your content at a custom domain, there are a
[few additional steps](https://help.github.com/articles/setting-up-a-custom-domain-with-github-pages/).

### Default Theme and Pelican
To get that started, lets
install Pelican then run its init command.

```
:::bash
$ pip install pelican markdown
$ mkdir -p ~/projects/yoursite
$ cd ~/projects/yoursite
$ pelican-quickstart
```

Pelican will ask a few questions, and eventually generate a site. Be sure to generate a fab file since it is quite
useful. The next thing to do is create a dummy article so
Pelican can generate the site. In `content/sample.md` try something like:

```
Title: My First Post
Date: 2050-12-03
Category: blog

My first pelican post
```

Then run `pelican content`. By default this should render a full site at `output/`. To view the site (assuming you said
yes to the fab file option), you can run `fab regenerate` and `fab serve` in separate terminal sessions. The first will regenerate
the site when changes are detected and the second will start a webserver running at
[http://localhost:8000](http://localhost:8000). The theme will be from the Pelican defaults, but there are a
[wealth of options](https://github.com/getpelican/pelican-themes) to choose from. It is also not very difficult to roll
your own theme like I did. To do that, look at the
[Pelican docs](http://docs.getpelican.com/en/3.6.3/pelican-themes.html) and [Jinja2 docs](http://jinja.pocoo.org/).

Editing templates and configs is subject of another post, but to get started you need to at least modify
`pelicanconf.py` and `publishconf.py`. The largest difference will be insuring that the `SITEURL` variable is set to
localhost for development but `username.github.io` for publishing.

Lets talk publishing. At the end, your generated site must be on the `master` branch to be hosted on Github Pages.
This means that most of the code will need to live in a different branch. I named mine `source`, but the name should not
matter. The most important point is that the `master` branch will get nuked at every deploy so **don't store any
files in the master branch**. I also found it helpful to empty out the `output` directory, add a `output/.gitkeep` file
using `touch output/.gitkeep`, and add `output/` in your `.gitignore`. Since `output` can be considered a build
artifact, it should **not** be under source control.

The next thing to do is generate the site using your production settings: `pelican content -o output -s publishconf.py`.
Finally, this has to get published by replacing the contents of the `master` branch with the contents of the `output`
directory. Run `pip install ghp-import` to install the utility that will make this easy.

Then from the `source` branch run: `ghp-import -b master output`.

This will have the effect of nuking the contents of `master` then copying the contents of `output/` to `master`. The
last step will be to push this changes to Github: `git push origin master`.

Hopefully you now have a basic site running. There are many Pelican blogs out there including mine to use as a reference.
The documentation is also fantastic so be sure to check that first.
