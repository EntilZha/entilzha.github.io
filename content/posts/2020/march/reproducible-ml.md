Title: Reproducible Hyper Parameter Sweeps in Machine Learning
Date: 2020-3-24
Tags: machine learning,engineering
Slug: reproducible-ml-and-parameter-sweeps
Author: Pedro Rodriguez

In the past couple weeks I've been working on writing machine learning code in python with the following goals:

1. Make experiments easy to reproduce (or retroactively debug). Primarily, this means saving the configuration *and* the code as it was at the time it was run.
2. Make it easy to run hyper parameter sweeps and multiple trials of the same parameters.

I've done both in the past, but I've never been satisfied with my prior approaches.
Thankfully, I think I've learned from the mistakes I made before and found a nice solution.
The approach is generalizable to any experiment setup, but I've made some specializations to my specific use case using [allennlp](https://github.com/allenai/allennlp).
Overall, my solution amounts to a python script of about 150 lines plus some configuration files. I'll refer to that as `hyper.py` and include its contents later on.
I plan on open sourcing the whole project I'm working on with this, but for now I've put the `hyper.py` [script in a gist](https://gist.github.com/EntilZha/b6034de3d2d0e6e2bd3e595e91aade69).

Here is the approach:

1. Define a configuration file for a class of model (e.g., bert) that defines a hyper parameter sweep.
2. In the case of `allennlp`, hyper parameters for a specific experiment are defined in a `json` or `jsonnet` file. I have a base configuration which the parameter values from (1) fill.
3. Use `hyper.py` to create a directory for each set of hyper parameters and copy the configuration files into it
4. Use python's `setup.py` to copy the source to this same directory.
5. Write out a script that can run all the experiments. In my case, I have a flag that I can use to control whether its a ordinary bash script or a [slurm](https://slurm.schedmd.com/documentation.html) job.

## The `setup.py` Script and Environment

First, write a `setup.py` script for your code. Optionally, you can encode your packages dependencies here or assume that they are installed on the system or virtual environment. In this example, I used the following `setup.py`

```python
from setuptools import setup, find_packages
setup(
    name='qb',
    version='0.0.0',
    author='pedro rodriguez',
    author_email='me@pedro.ai',
    url='https://github.com/EntilZha/qb-bert',
    packages=find_packages(),
)
```

I also prefer [anaconda virtual environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#create-env-file-manually), this is what mine looks like.

```yaml
name: qb
dependencies:
  - python=3.7
  - pytorch=1.4.*
  - cudatoolkit=10.1
  - numpy
  - scipy
  - pandas=1.0.*
  - requests
  - flask
  - ipython
  - pylint
  - pyflakes
  - pycodestyle
  - jedi
  - click=7.0.*
  - toml
  - pip
  - pip:
    - allennlp==0.9.*
    - overrides
    - spacy
    - plotnine
    - unidecode
channels:
  - anaconda
  - pytorch
  - conda-forge
```

## The Hyper Parameter and Model Configurations

There are a variety of configuration file formats, but I generally prefer [toml](https://github.com/toml-lang/toml) for configuration files. This is what my configuration looks like for a recurrent neural network parameter sweep.

```toml
model = "rnn"
n_trials = 1

[slurm]
qos = "gpu-medium"
time = "1-00:00:00"

[hyper]
"params.lr" = [0.001, 0.0001, 0.00001]
"params.dropout" = [0.2, 0.35, 0.5]
"params.hidden_dim" = [100, 300, 500, 1000]
"params.n_hidden_layers" = [1, 2]

[params]
dropout = 0.5
lr = 0.001
hidden_dim = 300
n_hidden_layers = 1
```

There are a few things to note:

1. I define default parameter values in `params`
2. I define parameters to sweep over in `hyper`. For now, my code performs an exhaustive grid, but that could be changed.
3. I added extra information for `slurm` that will be helpful since the UMD compute cluster has varying queue times that have different restrictions of number of jobs and runtime limit.

The last thing we'll need as a valid `allennlp` config which for my model is:

```jsonnet
function(lr=0.001, dropout=0.25, hidden_dim=1500, n_hidden_layers=1, debug=false) {
  dataset_reader: {
    qanta_path: '/fs/clip-quiz/entilzha/code/qb-bert/src/data/qanta.mapped.2018.04.18.json',
    lazy: false,
    debug: debug,
    type: 'qanta',
    full_question_only: false,
    first_sentence_only: false,
    char_skip: null,
    tokenizer: {
      type: 'word',
    },
    token_indexers: {
      text: {
        type: 'single_id',
        lowercase_tokens: true
      }
    },
  },
  train_data_path: 'guesstrain',
  validation_data_path: 'guessdev',
  model: {
    type: 'rnn_guesser',
    dropout: dropout,
    hidden_dim: hidden_dim,
    n_hidden_layers: n_hidden_layers,
  },
  iterator: {
    type: 'bucket',
    sorting_keys: [['text', 'num_tokens']],
    batch_size: 128,
  },
  trainer: {
    type: 'callback',
    callbacks: [
      {
        type: 'checkpoint',
        checkpointer: { num_serialized_models_to_keep: 1 },
      },
      { type: 'track_metrics', patience: 3, validation_metric: '+accuracy' },
      'validate',
      { type: 'log_to_tensorboard' },
      {
        type: 'update_learning_rate',
        learning_rate_scheduler: {
          type: 'reduce_on_plateau',
          patience: 2,
          mode: 'max',
          verbose: true,
        },
      },
    ]
    optimizer: {
      type: 'adam',
      lr: lr,
    },
    num_epochs: 50,
    cuda_device: 0,
  },
}
```

As is, this will run my code via `allennlp train rnn_model.jsonnet`.
Lets look at the `hyper.py` script and then return too running the model.

## The `hyper.py` Script

To start, I've defined some helper functions.
Before that, these imports are used.

```python
import os
import random
import glob
import copy
import subprocess
import toml
import click
import toml
from sklearn.model_selection import ParameterGrid
```

Allennlp configurations (or any `jsonnet` file) can be filled with parameters and converted to json via `jsonnet rnn_model.jsonnet --tla-scode lr=.0003`.
This makes this functionality callable via a python function.

```python
def run_jsonnet(base_model: str, args: str, out_path: str):
    subprocess.run(f"jsonnet {base_model} {args} > {out_path}", shell=True, check=True)
```

I also mentioned earlier that a key part of the approach is to use `setup.py` to copy source files to a directory for each experiment.
This function takes care of running `setup.py build` and copying the result to the correct location.

```python
def clone_src(target_dir: str):
    subprocess.run(f"python setup.py build", shell=True, check=True)
    subprocess.run(f"cp -r build/lib/qb {target_dir}", shell=True, check=True)
```

Since we're generating lots of experiments, its helpful to generate random identifiers.

```python
def random_experiment_id():
    return str(random.randint(1_000_000, 2_000_000))
```

The next bit of code uses SKLearn's parameter grid to create a copy of the `rnn.toml` file/dictionary for each experiment.
This is also where changes could be made to use random sampling or some other procedure for parameter sweeps.

```python
def hyper_to_configs(path: str):
    with open(path) as f:
        # Read the parent config, like the rnn.toml
        hyper_conf = toml.load(f)
    configs = []
    n_trials = hyper_conf.get("n_trials", 1)
    # If it defines a hyper parameter sweep, then generate a config for each one
    if "hyper" in hyper_conf:
        # ParameterGrid takes a list of parameters and converts them to a sweep
        grid = ParameterGrid(hyper_conf["hyper"])
        del hyper_conf["hyper"]
        for params in grid:
            for trial in range(n_trials):
                # Make a deep copy to avoid overwriting old configs
                conf = copy.deepcopy(hyper_conf)
                # Fill in the value of each configuration
                for name, val in params.items():
                    splits = name.split(".")
                    access = conf
                    for part in splits[:-1]:
                        access = access[part]
                    access[splits[-1]] = val
                # Write down which trial this is
                conf["trial"] = trial
                configs.append(conf)
        return configs
    else:
        # if not, just return the original config
        if "hyper" in hyper_conf:
            del hyper_conf["hyper"]
        return [hyper_conf]
```

Then the last part is to combine all this together.
As a preview, running `python hyper.py config/rnn.toml rnn_model.jsonnet rnn` yields the following directories:

1. Directories matching `config/generated/rnn/{random_experiment_id}/{trial}` with contents `qb` (the code copied), `{random_experiment_id}.json` and `{random_experiment_id}.toml`.
2. Empty directories matching `model/generated/rnn/{random_experiment_id}/{trial}` which is where models will get saved.
3. A script `rnn-jobs.sh` that runs all experiments.

The first part of the main function handles creating the directories while the second handles creating the script.
Below is the `hyper.py` script which I've commented since its probably easier to explain inline than interspersing prose and code.

```python
# If you're unfamiliar with click, its a library for making CLIs
# https://click.palletsprojects.com/en/7.x/
@click.command()
@click.option("--slurm-job/--no-slurm-job", is_flag=True, default=True)
@click.argument("hyper_conf_path")
@click.argument("base_json_conf")
@click.argument("name")
def hyper_cli(slurm_job: bool, hyper_conf_path: str, base_json_conf: str, name: str):
    # 1) Generate all the configuration files and directories

    # hyper_conf_path is a toml file defining the hyper parameter sweep
    configs = hyper_to_configs(hyper_conf_path)
    for c in configs:
        conf_name = random_experiment_id()
        trial = c["trial"]

        # This defines the path like config/generated/rnn/{random_experiment_id}/{trial}
        conf_dir = os.path.abspath(os.path.join("config", "generated", name, conf_name, trial))
        allennlp_conf_path = os.path.join(conf_dir, f"{conf_name}.json")
        conf_path = os.path.join(conf_dir, f"{conf_name}.toml")

        # This defines the path like model/generated/rnn/{random_experiment_id}/{trial}
        serialization_dir = os.path.abspath(
            os.path.join("model", "generated", name, conf_name, trial)
        )

        # Save all this information in the new configuration file.
        # My code in particular takes only this file and takes all arguments from it.
        c["generated_id"] = conf_name
        c["name"] = name
        c["allennlp_conf"] = allennlp_conf_path
        c["serialization_dir"] = serialization_dir
        c["conf_dir"] = conf_dir
        c["conf_path"] = conf_path
        c["trial"] = trial
        os.makedirs(os.path.dirname(conf_path), exist_ok=True)
        os.makedirs(serialization_dir, exist_ok=True)
        with open(conf_path, "w") as f:
            toml.dump(c, f)
        args = []
        for key, val in c["params"].items():
            # jsonnet has a quirk the string parameters need --tla-str while other values need tla-code
            if isinstance(val, str):
                args.append(f"--tla-str {key}={val}")
            else:
                args.append(f"--tla-code {key}={val}")
        args = " ".join(args)
        # Generate the json config
        run_jsonnet(base_json_conf, args, allennlp_conf_path)
        # Copy the source using `setup.py` to the experiment directory
        clone_src(conf_dir)

    # 2) Generate the run script, optionally making it a slurm script.
    with open(f"{name}-jobs.sh", "w") as f:
        for c in configs:
            conf_dir = c["conf_dir"]
            conf_path = c["conf_path"]
            # Check if slurm configs are defined, otherwise use some defaults specific to UMD cluster
            if "slurm" in c:
                slurm_time = c["slurm"].get("time", "4-00:00:00")
                slurm_qos = c["slurm"].get("qos", "gpu-long")
            else:
                slurm_time = "4-00:00:00"
                slurm_qos = "gpu-long"

            if slurm_job:
                args = [
                    "sbatch",
                    "--qos",
                    slurm_qos,
                    "--time",
                    slurm_time,
                    "slurm-allennlp.sh",
                    conf_dir,
                    conf_path,
                ]
                f.write(" ".join(args) + "\n")
            else:
                f.write(f"train.sh {conf_dir} {conf_path}\n")


if __name__ == "__main__":
    hyper_cli()
```

Since the slurm script has some UMD cluster specific configuration, instead here is the `train.sh` script which does the same thing locally.

```bash
#!/usr/bin/env bash

# Important to switch to where the code was copied to if you want to use the same version
cd $1
# Replace with your training script, mine assumes that the toml file is by itself a full configuration
python qb/main.py train $2
```

With that, this is how I've been defining and running larger parameter sweeps.
For experiment tracking, I've been using [comet.ml](https://comet.ml) with the [callback trainer](https://github.com/allenai/allennlp/blob/v0.9.0/allennlp/training/callback_trainer.py) which I'll discuss in a future post.
Also for the future, I'd like to look into going beyond grid search by integrating with something like [allentune](https://github.com/allenai/allentune) since I'm already using `allennlp`.
My hunch is that I can push down parameter search down to `allentune` and figure out how to integrate their [ray-based](https://github.com/ray-project/ray) parallelization with the slurm cluster UMD uses.

Thanks for reading and hope this helps someone out there to make natural language processing or machine learning experiments more reproducible.
