Title: Tips
Slug: tips
Authors: Pedro Rodriguez
Description: Random tips for myself and others

Here are a bunch of software/tips/resources I've found. I like to have them in a publicly accessible webpage, but hope that its helpful to others as well.

## Cheatsheets

* [PDB Cheatsheet](static/pdf/pdb-cheatsheet.pdf) from [https://github.com/nblock/pdb-cheatsheet](https://github.com/nblock/pdb-cheatsheet)
* [Pandas Cheatsheet](static/pdf/pandas-cheat-sheet.pdf) from [https://pandas.pydata.org/](https://pandas.pydata.org/
)

## Software

### Paper Writing
* [Paperpile for organizing research papers](https://paperpile.com/)
* [Plotnine for figures](https://plotnine.readthedocs.io)
* [draw.io for diagrams](https://draw.io)

### Operating Systems
* I use [Arch Linux](https://www.archlinux.org/) on machines I own.
* For cloud instances, I use Ubuntu

### Rust-based Alternatives to Common CLI Tools
* [bat: cat replacement](https://github.com/sharkdp/bat)
* [exa: ls replacement](https://the.exa.website/)
* [Glances, a better top/htop](https://nicolargo.github.io/glances/) (be sure to `pip install nvidia-ml-py3` for GPU support)
* [fd: find replacement](https://github.com/sharkdp/fd)
* [starship: make a better prompt](https://starship.rs/)
* [dust: check disk usage](https://github.com/bootandy/dust)
* [ripgrep: grep replacement](https://github.com/BurntSushi/ripgrep)
* [watchexec: run commands on file changes](https://github.com/watchexec/watchexec)

### Package Managers
* [linuxbrew: package manager when I don't have sudo](https://docs.brew.sh/Homebrew-on-Linux)

### Data Tools
* [PetScan: Tool Searching for Wiki Pages with Complex Queires](https://petscan.wmflabs.org/), [Manual](https://meta.wikimedia.org/wiki/PetScan/en)
* [Comet.ml for external hosted experiment tracking](https://comet.ml)
* [MLFlow for self-hosted experiment tracking](https://mlflow.org/)
* [Apache Spark for "Big Data"](https://spark.apache.org/)

### Python Libraries

* For small APIs, [FastAPI](fastapi.tiangolo.com/), for larger projects [Django](https://www.djangoproject.com/)
* Static site (like this page) [Pelican](https://docs.getpelican.com/en/stable/)
* [Allennlp](https://github.com/allenai/allennlp) is an amazing library for natural language processing, use it!

## Data Formats

* Unless you have a *very good* reason and have purely numerical data, *never* use csv; saying a file is csv format is insufficient information to be able to parse the file
* Default to [json](https://www.json.org/)
* For large json files that are table-like (the root object is an array, and looks like rows), consider [JSON lines/jsonl](http://jsonlines.org/). Large JSON objects can be expensive to parse, and make it difficult to run parallel jobs (eg Apache Spark uses line delimited rows from text files)

## Hardware

### Desks

* I bought a [vari electric sit/stand desk](https://www.vari.com/electric-standing-desk-60x30/FD-ESD6030.html) and love it.

### Better Internet

* Option 1: Use a very long ethernet cable with [No Damage Wall Hangers](https://www.amazon.com/slp/no-damage-wall-hangers/6n75kefycjaf38m)
* Option 2: [Ethernet over Powerline Network Adaptors](https://www.amazon.com/Powerline-Computer-Network-Adapters/b?ie=UTF8&node=1194444) are magical and work extremeley well. Personally, I bought the "TP-Link AV2000 Powerline Adapter"

## AllenNLP Tips

* `allennlp` sets [random seeds](https://github.com/allenai/allennlp/blob/v0.9.0/allennlp/common/util.py#L177) deterministically which helps improve reproducibility of experiments. Occasionally, when doing things like running multiple trials of identical hyper parameters, this behavior causes results for each trial to be identical. In these cases, its helpful to manually specify a random seed; for example using the trial number as the random seed.

## Tips from Others
* [Style guide from my advisor](http://users.umiacs.umd.edu/~jbg/static/style.html)

## Docs

* [Slurm sbatch](https://slurm.schedmd.com/sbatch.html)

## Configs

* [Dotfiles](https://github.com/EntilZha/dotfiles)
* [vimrc](https://github.com/EntilZha/dotfiles/blob/master/vimrc)


## UMD CLIP Resources

### Links
* [CLIP Homepage](https://wiki.umiacs.umd.edu/clip/index.php/Main_Page)
* [CLIP Wiki](https://wiki.umiacs.umd.edu/clip/clipwiki/index.php)

### Storage

UMIACS offers long term file storage and hosting through [object stores](https://obj.umiacs.umd.edu/obj/) using a set of [s3-like utilities](https://gitlab.umiacs.umd.edu/staff/umobj/tree/master).
Specific to the `clip-quiz` group, you should mirror the layout of `/fs/clip-quiz` and the contents of the `clip-quiz` bucket to make storing/restoring files easy.
For example, moving a file `/fs/clip-quiz/code/old-big-project/` could be done using: `cpobj -V -r -f /fs/clip-quiz/code/old-big-project clip-quiz:code/`

## LaTeX

* What is `~`? Non-breaking space, LaTeX will not break lines between alpha and beta in `alpha~beta`
* Create PDF version of figures

## Debugging

* `ipdb` and `pdb` are fantastic for command line debugging
* To start debugger on if allennlp errors: `ipython -m ipdb (which allennlp) -- train config.jsonnet` and press `c` to continue when terminal starts
* Anaconda pip installations from source packages causing g++ errors like "file format not recognized", rename anaconda's `ld` to `ld_` so that pip uses the system version [https://github.com/pytorch/pytorch/issues/16683#issuecomment-459982988](https://github.com/pytorch/pytorch/issues/16683#issuecomment-459982988)
