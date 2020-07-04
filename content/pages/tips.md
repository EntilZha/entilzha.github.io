Title: Tips
Slug: tips
Authors: Pedro Rodriguez
Description: Random tips for myself and others

Here are a bunch of software/tips/resources I've found. I like to have them in a publicly accessible webpage, but hope that its helpful to others as well. I've framed some of these as FAQs to improve discoverability.

## What are useful python cheatsheets?

* [PDB Cheatsheet](static/pdf/pdb-cheatsheet.pdf) from [https://github.com/nblock/pdb-cheatsheet](https://github.com/nblock/pdb-cheatsheet)
* [Pandas Cheatsheet](static/pdf/pandas-cheat-sheet.pdf) from [https://pandas.pydata.org/](https://pandas.pydata.org/
)

## How do you do X in Plotnine?

* [Plotnine: Bar Plot with Arrows](https://colab.research.google.com/drive/1JrTGUftkNVK2RoZyHtAqoIbPPQGxaSj9?usp=sharing)
* [Plotnine: Category Ordering](https://colab.research.google.com/drive/1DBSclyy0USbi4SyANCFAL9ZzWKIyvqwO?usp=sharing)

## Software

### What software is useful for writing research papers?
* [Paperpile for organizing research papers](https://paperpile.com/)
* [Plotnine for figures](https://plotnine.readthedocs.io)
* [draw.io for diagrams](https://draw.io)

### Operating Systems
* I use [Arch Linux](https://www.archlinux.org/) on machines I own.
* For cloud instances, I use Ubuntu

### What are some awesome (rust-based) command line tools?
* [bat: cat replacement](https://github.com/sharkdp/bat)
* [exa: ls replacement](https://the.exa.website/)
* [Glances, a better top/htop](https://nicolargo.github.io/glances/) (be sure to `pip install nvidia-ml-py3` for GPU support)
* [fd: find replacement](https://github.com/sharkdp/fd)
* [starship: make a better prompt](https://starship.rs/)
* [dust: check disk usage](https://github.com/bootandy/dust)
* [ripgrep: grep replacement](https://github.com/BurntSushi/ripgrep)
* [watchexec: run commands on file changes](https://github.com/watchexec/watchexec)

### How can I install software on linux without root?
* [linuxbrew works on linux, in addition to mac](https://docs.brew.sh/Homebrew-on-Linux)

### What is some software for managing ML experiments?
* [Comet.ml for external hosted experiment tracking](https://comet.ml)
* [MLFlow for self-hosted experiment tracking](https://mlflow.org/)

### What are good python debugging tools/tricks?

* `ipdb` and `pdb` are fantastic for command line debugging
* To start debugger on if allennlp errors: `ipython -m ipdb (which allennlp) -- train config.jsonnet` and press `c` to continue when terminal starts
* Anaconda pip installations from source packages causing g++ errors like "file format not recognized", rename anaconda's `ld` to `ld_` so that pip uses the system version [https://github.com/pytorch/pytorch/issues/16683#issuecomment-459982988](https://github.com/pytorch/pytorch/issues/16683#issuecomment-459982988)

### How can I search for types of Wikipedia pages?
* [PetScan: Tool Searching for Wiki Pages with Complex Queries](https://petscan.wmflabs.org/), [Manual](https://meta.wikimedia.org/wiki/PetScan/en)

### What is some software for data analytics/distributed computing?
* [Apache Spark: SQL-based analytics and distributed computing](https://spark.apache.org/)
* [Dask: pure python distributed computing](https://dask.org/)

### What are good python libraries for creating websites?

* For small APIs, [FastAPI](fastapi.tiangolo.com/) or websites that you don't need/want pre-made user system
* For more "out of the box", but more opinionated use [Django](https://www.djangoproject.com/)
* For static sites Static site (like this page) [Pelican](https://docs.getpelican.com/en/stable/)

### What are some good NLP libraries?
* [Allennlp](https://github.com/allenai/allennlp) is an amazing library for research in natural language processing, use it!
*[Spacy](https://spacy.io/): Fantastic, easy to use tools for tokenization, dependency parsing, named entity recognition and more, often used in other NLP software.

## What data formats should I use?

* Unless you have a *very good* reason and have purely numerical data, *never* use csv; saying a file is csv format is insufficient information to be able to parse the file
* Default to [json](https://www.json.org/)
* For large json files that are table-like (the root object is an array, and looks like rows), consider [JSON lines/jsonl](http://jsonlines.org/). Large JSON objects can be expensive to parse, and make it difficult to run parallel jobs (eg Apache Spark uses line delimited rows from text files)
* For data you expect to analyze, you might consider creating a read-only SQlite database and running analysis in SQL.

## Hardware

### How can I improve my ergonomics and avoid repetetive strain injuries?

* I bought a [vari electric sit/stand desk](https://www.vari.com/electric-standing-desk-60x30/FD-ESD6030.html) and love it. It encourages me to stretch, improves my posture, and gets me moving throughout the day

### How can I improve my home internet?

* Option 1: Use a very long ethernet cable with [No Damage Wall Hangers](https://www.amazon.com/slp/no-damage-wall-hangers/6n75kefycjaf38m)
* Option 2: [Ethernet over Powerline Network Adaptors](https://www.amazon.com/Powerline-Computer-Network-Adapters/b?ie=UTF8&node=1194444) are magical and work extremeley well. Personally, I bought the "TP-Link AV2000 Powerline Adapter"

## AllenNLP Tips

* `allennlp` sets [random seeds](https://github.com/allenai/allennlp/blob/v0.9.0/allennlp/common/util.py#L177) deterministically which helps improve reproducibility of experiments. Occasionally, when doing things like running multiple trials of identical hyper parameters, this behavior causes results for each trial to be identical. In these cases, its helpful to manually specify a random seed; for example using the trial number as the random seed.

## Tips from Others
* [Style guide from my advisor](http://users.umiacs.umd.edu/~jbg/static/style.html)

## Docs

* [Slurm sbatch](https://slurm.schedmd.com/sbatch.html)

## Where do you keep your configuration files for applications?

* [Dotfiles](https://github.com/EntilZha/dotfiles)
* [vimrc](https://github.com/EntilZha/dotfiles/blob/master/vimrc)


## Where can I find resources related to the UMD CLIP lab?

### Links
* [CLIP Homepage](https://wiki.umiacs.umd.edu/clip/index.php/Main_Page)
* [CLIP Wiki](https://wiki.umiacs.umd.edu/clip/clipwiki/index.php)

### Where can I store files at UMD?

UMIACS offers long term file storage and hosting through [object stores](https://obj.umiacs.umd.edu/obj/) using a set of [s3-like utilities](https://gitlab.umiacs.umd.edu/staff/umobj/tree/master).
Specific to the `clip-quiz` group, you should mirror the layout of `/fs/clip-quiz` and the contents of the `clip-quiz` bucket to make storing/restoring files easy.
For example, moving a file `/fs/clip-quiz/code/old-big-project/` could be done using: `cpobj -V -r -f /fs/clip-quiz/code/old-big-project clip-quiz:code/`

## LaTeX

### What format should figures be in?
* Create PDF version of figures

### What is `~`? Non-breaking space in latex?
* LaTeX will not break lines between alpha and beta in `alpha~beta`

