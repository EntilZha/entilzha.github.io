Title: AllenNLP Callback Trainer and CometML
Date: 2020-4-08
Tags: machine learning
Slug: allennlp-callback-trainer-cometml
Author: Pedro Rodriguez

In my [last post](https://www.pedro.ai/blog/2020/03/24/reproducible-ml-and-parameter-sweeps/) on parameter sweeps, I mentioned that I found a nice way to combine [AllenNLP](https://allennlp.org/) and [comet.ml](https://www.comet.ml/).
In this post, I'll share my code that does this via the (experimental) [callback trainer](https://github.com/allenai/allennlp/blob/v0.9.0/allennlp/training/callback_trainer.py).
The `1.0` release of AllenNLP is currently [actively in development](https://github.com/allenai/allennlp/milestone/10) and the callback trainer itself has been changing quite a bit (Issues [3269](https://github.com/allenai/allennlp/issues/3269), [3519](https://github.com/allenai/allennlp/issues/3519), and [3913](https://github.com/allenai/allennlp/issues/3913)).
Given that, everything in this post uses version `0.9.0` of AllenNLP.

The concept of the callback trainer is based on event based programming, and---at least as far as I know---popularized by [keras](https://keras.io/).
I liked the concept enough that when I switched to PyTorch I wrote [my own version](https://github.com/Pinafore/qb/blob/02a9ac953e4bb56f6c863737afbc983959f6a1ab/qanta/torch/__init__.py).
The idea is that during model training, there are a number of important events which multiple pieces of code may be interested. Some of these are:

* When model training starts or ends
* When an epoch starts or ends
* When a batch starts or ends

For example, an early stopping mechanism may be interested in acquiring model predictions at epoch end, or tensorboard may be interested in batch statistics.
Rather than the framework embedding each of these directly in the training loop, the framework instead collects a list of handlers for each event and runs them at the appropriate time.

In my training code, configuring the AllenNLP is as little code as changing the `trainer` key in the `json`/`jsonnet` model configuration:

```python
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
```

This configuration makes it so that:

* `checkpoint`: Models are saved at the end of every epoch
* `track_metrics`: Early stopping is controlled by accuracy allowing for a maximum of three epochs without improvement before stopping
* `log_to_tensorboard`: Log batch statistics to a directory so that it can be visualized in tensorboard.
* `update_learning_rate`: Reduce the learning rate if there is no improvement after two epochs

Although (as far as I know), there isn't much official documentation, I found it quite helpful to look at the [unit test file](https://github.com/allenai/allennlp/blob/v0.9.0/allennlp/tests/training/callback_trainer_test.py) for help

In my code, I also added this callback `{ type: 'log_to_comet', project_name: 'qb-bert' }` which when combined with my custom callback below yields a very useful way to look at experiment results.

![CometML Experiment Table](/static/images/cometml.png)

I make a few assumptions:
* You've followed the [comet.ml docs](https://www.comet.ml/docs/) to install their package and created an account
* The callback configuration provides a comet.ml project name
* If there is a model configuration file, its referenced by the environment variable `MODEL_CONFIG_FILE`
* Similarly, if there is a log file, its referenced by `SLURM_LOG_FILE`
* The configuration file is in [toml](https://github.com/toml-lang/toml), but this could be easily changed.
* The model parameters are stored in a key `params`
* For AllenNLP to find this, the class needs to be imported using `--include-package` in the cli or as a regular python import in your code.

Github gist: [comet_ml_callback.py](https://gist.github.com/EntilZha/763511862c4702b071562f9a0203355c)

```python
from typing import Text
import socket
import os
import comet_ml
import toml
from allennlp.training.callbacks.callback import Callback, handle_event
from allennlp.training.callbacks.events import Events


@Callback.register("log_to_comet")
class LogToComet(Callback):
    def __init__(self, project_name: Text = None):
        self._project_name = project_name
        model_config_file = os.environ.get("MODEL_CONFIG_FILE")
        if project_name is None or model_config_file is None:
            self._experiment = None
            self._conf = None
        else:
            self._experiment = comet_ml.Experiment(project_name=self._project_name)
            slurm_log_file = os.environ.get("SLURM_LOG_FILE")
            if slurm_log_file is not None:
                self._experiment.log_asset(slurm_log_file, overwrite=True)
            model_config_file = os.environ.get("MODEL_CONFIG_FILE")
            if model_config_file is not None:
                self._experiment.log_asset(model_config_file)
                with open(model_config_file) as f:
                    self._conf = toml.load(f)
                for key, val in self._conf["params"].items():
                    self._experiment.log_parameter(key, val)
                self._experiment.add_tag(self._conf["name"])
            self._experiment.log_other("hostname", socket.gethostname())

    @handle_event(Events.TRAINING_END)
    def training_end(self, _):
        if self._experiment is not None:
            self._experiment.add_tag("COMPLETED")

    @handle_event(Events.EPOCH_END)
    def epoch_end_logging(self, trainer):
        if self._experiment is not None:
            epoch = trainer.epoch_number + 1
            for key, val in trainer.train_metrics.items():
                self._experiment.log_metric(f"train_{key}", val, epoch=epoch)

            for key, val in trainer.val_metrics.items():
                self._experiment.log_metric(f"val_{key}", val, epoch=epoch)
            slurm_log_file = os.environ.get("SLURM_LOG_FILE")
            if slurm_log_file is not None:
                self._experiment.log_asset(slurm_log_file, overwrite=True)

    @handle_event(Events.ERROR)
    def mark_run_failure(self, _):
        if self._experiment is not None:
            self._experiment.add_tag("FAILED")
```

The callback trainer will invariably change with AllenNLP `1.0` (excited!) and am hopeful that adapting this code will be straightforward.
Thanks and with the EMNLP deadline coming up ([but extended to June 1st](https://2020.emnlp.org/)) perhaps this will help preserve sanity while running parameter sweeps and comparing results.

Disclaimer: I am using the academic plan on comet.ml, but otherwise have no affiliation or sponsorship.