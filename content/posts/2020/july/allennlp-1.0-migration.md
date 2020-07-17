Title: AllenNLP 1.0 Migration
Date: 2020-7-05
Tags: nlp
Slug: allennlp-1.0-migration
Author: Pedro Rodriguez

AI2 [recently released](https://medium.com/ai2-blog/allennlp-1-0-df0327445509) version `1.0` of its excellent [AllenNLP library](https://allennlp.org/).
The goal of this (living) blog post is to list code and configuration changes I've made in my own code to migrate from `0.9.0` to `1.0`.
While I was writing this, I also found that the developers added a more exhaustive migration guide in the [1.0 release notes](https://github.com/allenai/allennlp/releases/tag/v1.0.0) so be sure to check that too; thus my focus is how I changed my code.
At least in the first iteration of this blog post, most of the changes come from updating some [FEVER](https://fever.ai/) baselines I've written at [github.com/entilzha/fever](https://github.com/EntilZha/fever).

# Configuration Changes

In the `jsonnet` configuration file, it seems like `iterator` has been replaced by `data_loader` and its simpler to define the `bucket` sampler.
Additionally, `num_serialized_models_to_keep` has moved out of the `trainer`, but more importantly now has a default value of 2 instead of the much higher number.
I'm ok with keeping 2 models around over the much larger number in the prior version of `allennlp`.

Here is my configuration file before:

```jsonnet
function(lr=0.0001) {
  dataset_reader: {
    type: 'fever',
  },
  train_data_path: 'data/train.jsonl',
  validation_data_path: 'data/shared_task_dev.jsonl',
  model: {
    type: 'claim_only',
    dropout: 0.25,
    pool: 'mean',
  },
  iterator: {
    type: 'bucket',
    sorting_keys: [['text', 'num_tokens']],
    batch_size: 32,
  },
  trainer: {
    optimizer: {
      type: 'adam',
      lr: lr,
    },
    validation_metric: '+accuracy',
    num_serialized_models_to_keep: 1,
    num_epochs: 50,
    patience: 2,
    cuda_device: 0,
  },
}
```

And after

```jsonnet
local transformer = "roberta-base";

function(lr=0.0001) {
  dataset_reader: {
    type: 'fever',
    transformer: transformer
  },
  train_data_path: 'data/train.jsonl',
  validation_data_path: 'data/shared_task_dev.jsonl',
  model: {
    type: 'claim_only',
    dropout: 0.5,
    pool: 'cls',
    transformer: transformer
  },
  data_loader: {
    batch_sampler: {
      type: 'bucket',
      sorting_keys: ['claim_tokens'],
      batch_size: 32
    },
  },
  trainer: {
    optimizer: {
      type: 'adam',
      lr: lr,
    },
    validation_metric: '+accuracy',
    num_epochs: 50,
    patience: 1,
    cuda_device: 0,
  },
}
```

# Dataset Changes

In dataset readers, the main changes I encountered were updating transformer tokenizers/indexers.
In my prior code, I manually defined `start_tokens` and `end_tokens` since I noticed that the `[CLS]` and other special tokens were being used twice.

For reference, [this was my code before](https://github.com/EntilZha/fever/blob/73776fceaad1085bf4150caa4dfaa7e2c2538abb/src/snif/dataset.py) and [after the changes](https://github.com/EntilZha/fever/blob/3d34efa7b7cfe20581d06fb493ef1d2b56a1ba07/serene/dataset.py)

Here is a shortlist of changes to make:

* Imports: `allennlp.data.token_indexers.wordpiece_indexer.PretrainedBertIndexer` to `allennlp.data.token_indexers.PretrainedTransformerIndexer`
* In the class: `{'text': PretrainedBertIndexer(transformer)}` to `{"text": PretrainedTransformerIndexer(transformer)}`
* In the class: `PretrainedTransformerTokenizer('bert-base-uncased', do_lowercase=True, start_tokens=[], end_tokens=[])` to `PretrainedTransformerTokenizer(transformer)`

# Model Changes

The primary model changes were in how to define and use transformer models.
For reference, [this is what my code looked like before](https://github.com/EntilZha/fever/blob/73776fceaad1085bf4150caa4dfaa7e2c2538abb/src/snif/model.py).
The 1.0 version changes some names around and [looks like this](https://github.com/EntilZha/fever/blob/3d34efa7b7cfe20581d06fb493ef1d2b56a1ba07/serene/model.py)

Here is a shortlist of changes to make:

* Imports: `allennlp.modules.token_embedders.bert_token_embedder.PretrainedBertEmbedder` to `allennlp.modules.token_embedders.pretrained_transformer_embedder.PretrainedTransformerEmbedder`
* When using in a class: `PretrainedBertEmbedder(transformer_name)` to `PretrainedTransformerEmbedder(transformer_name)`

# Summary

That's all I've got so far since it appears many changes are non-user facing.
In the next weeks, I'm also looking forward to using new features like native pytorch distributed training to speed up my experiments!