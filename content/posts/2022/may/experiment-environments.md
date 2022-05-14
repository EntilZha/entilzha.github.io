Title: Reproducible Python Environments for Science
Date: 2022-05-13
Tags: engineering
Slug: reproducible-python-environments
Author: Pedro Rodriguez

The topic of how to create and maintain reproducible experiments has come up a few times recently.
I've previously discussed ways to do [reproducible hyper parameter sweeps](https://www.pedro.ai/blog/2020/03/24/reproducible-ml-and-parameter-sweeps/) and as part of that briefly discussed using anaconda environments.
This (short) post elaborates on that with what I've learned since then.
I'll break this into two parts: (1) how to manage python installations and (2) how to manage python packages.
The first part will discuss how to actually install python and specify which version of python to use.
The second part will discuss how to define python package versions, assuming the specified python version is active.

## Managing Python Installations

When using python, it is extremely desirable to separate the python system-wide installation from the installation used by your experimental code.
Mixing these to leads to a bad time for various reasons and should be avoided.
The easiest way to accomplish this is to use [Anaconda python](https://www.anaconda.com/products/distribution) or its minimal cousin [miniconda](https://docs.conda.io/en/latest/miniconda.html).
Installing in both cases is as easy as downloading the binary, running `bash downloaded_binary.sh`, and following the instructions.

After this, for every project you should run a command like:

```bash
# Create a new environment
conda create -n mynewenv python=3.9

# When working on project code, activate it
conda activate mynewenv
```

This will let you install packages in that environment without affecting the system python installation or any other installation.
It also makes it incredibly easy to use different python versions for each experiment (e.g., some older code might require older python versions, while newer code requires newer versions).
Let's move to defining python package dependencies now.

## Managing Python Packages

Generally speaking, I've found three ways to manage python package versions:

1. Using [Python Poetry](https://python-poetry.org)
2. Using a hand-crafted conda `environment.yaml` or pip `requirements.txt` file
3. Using `pip freeze` or `conda list --export` to generate `requirements.txt` (or the conda equivalent).

Before discussing why I think poetry is the best option, let's take a step back and outline what we need a package management system to do:

1. It should be easy to fully reproduce an experiment, down to exact package versions, whether that is tomorrow or in three years.
2. It should be easy to add a package as a dependency
3. It should be easy to upgrade package versions

The main problem with solution (2) is that it does not define transitive dependencies, and it is very easy to under-specify required packages.
This is the main reason I avoid this solution in most cases.

The problem with solution (3) is that nothing distinguishes direct project dependencies from transitive dependencies.
Because of this, it is difficult to upgrade package versions.
This also becomes a problem when adding a package that requires the transitive dependency of a direct project dependency to be upgraded.
Since there is no version solver in this case, you have to resolve this manually.
Here is one concrete example: suppose you have package `A` which transitively depends on `B=1.0.*`; then you add `C` which transitively depends on `B>1.0.0,B=1.0.*`.

For this reason I prefer poetry. A poetry configuration will add direct dependencies to `pyproject.toml` and define a complete, exhaustive dependency list in `poetry.lock`.
This site uses this `pyproject.toml` for example:

```toml
[tool.poetry.dependencies]
python = "^3.8"
pelican = "^4.7.2"
pygments = "2.7.4"
typogrify = "2.0.7"
markdown = "3.1.1"
webassets = "0.12.1"
cssmin = "0.2.0"
bibtexparser = "^1.1"
nbconvert = "^5.6.1"
rich = "^10.7.0"
ipython = "^7.13.0"
ipython_genutils = "^0.2.0"
pelican-jupyter = "^0.10.1"
contextfilter = "^0.3.0"
jinja2 = "3.0.3"
pelican-render-math = "^1.0.3"

[tool.poetry.dev-dependencies]
black = "^19.10b0"
pylint = "^2.4.4"

[build-system]
requires = ["poetry>=0.12"]
build-backend = "poetry.masonry.api"
```

You get best of both worlds, plus an easy way to manage dependencies.
As an added bonus, you get some other nice things like easy ability to `poetry publish` to pypi.

I'll wrap up with a summary of the development flow.

### The Development Flow

1. Create a conda environment like `conda create -n project python=3.9`
2. Activate the environment like `conda activate project`
3. Initiate poetry (one-time) `poetry init`
4. (To Add Packages): `poetry add packagename`
5. (To Upgrade Packages): `poetry update`
6. (To Install everything, e.g., a fresh environment): `poetry install`
7. Commit both `pyproject.toml` and `poetry.lock` to git.

The one last thing I'll mention, is that sometimes there are dependencies that are not `pip` installable for various reasons.
In this case, I resort to a manually and carefully updated conda environment file or documentation.
The main package I do this for is `altair` which for rendering to PDF requires vega-lite which requires vega which requires the node stack.
In this specific case, I start out with `conda install -c conda-forge vega-cli vega-lite-cli` then figure out what the current version of packages is to pin to.

Thanks and happy packaging!


### Alternatives

A few alternatives I've seen:

1. [pip-compile](https://modelpredict.com/wht-requirements-txt-is-not-enough): Have not tried, but know someone who likes it.
2. Pipenv: Tried this one time, didn't mesh with my mental model.
