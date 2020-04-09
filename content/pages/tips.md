Title: Tips
Slug: tips
Authors: Pedro Rodriguez
Description: Random tips for myself and others

Over my career I've made many mistakes, occasionally learn from them,
sometimes find useful software/tips/resources, and such. I don't expect to
remember all or even most of these so I compile everything here so that I
have a quick and easy way to reference them on the web; hopefully in doing so it also turns
out to be helpful for others as well.


## Cheatsheets

* [PDB Cheatsheet](static/pdf/pdb-cheatsheet.pdf) from [https://github.com/nblock/pdb-cheatsheet](https://github.com/nblock/pdb-cheatsheet)
* [Pandas Cheatsheet](static/pdf/pandas-cheat-sheet.pdf) from [https://pandas.pydata.org/](https://pandas.pydata.org/
)

## Data Formats

* Unless you have a *very good* reason and have purely numerical data, *never* use csv; saying a file is csv format is insufficient information to be able to parse the file
* Default to [json](https://www.json.org/)
* For large json files that are table-like (the root object is an array, and looks like rows), consider [JSON lines/jsonl](http://jsonlines.org/). Large JSON objects can be expensive to parse, and make it difficult to run parallel jobs (eg Apache Spark uses line delimited rows from text files)

## Software
* [Zotero for organizing research papers](https://www.zotero.org/)
* [MLFlow for experiment tracking](https://mlflow.org/)
* [Glances, a better top/htop](https://nicolargo.github.io/glances/) (be sure to `pip install nvidia-ml-py3` for GPU support)
* [Plotnine for figures](https://plotnine.readthedocs.io)
* [draw.io for diagrams](https://draw.io)
* [Apache Spark for "Big Data"](https://spark.apache.org/)
* I use [Arch Linux](https://www.archlinux.org/) on machines I own.
* [bat: cat replacement](https://github.com/sharkdp/bat)
* [exa: ls replacement](https://the.exa.website/)
* [linuxbrew: package manager when I don't have sudo](https://docs.brew.sh/Homebrew-on-Linux)

## Web Tools
* [PetScan: Tool Searching for Wiki Pages with Complex Queires](https://petscan.wmflabs.org/), [Manual](https://meta.wikimedia.org/wiki/PetScan/en)


## Libraries

### Python

* For small APIs, [Flask](http://flask.pocoo.org/), for anything more [Django](https://www.djangoproject.com/)
* Static site (like this page) [Pelican](https://docs.getpelican.com/en/stable/)

### Natural Language Processing
* [Allennlp](https://github.com/allenai/allennlp) is an amazing library for natural language processing, use it!

#### AllenNLP Tips

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
