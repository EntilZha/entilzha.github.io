Title: Information Seeking in the Spirit of Learning: a Dataset for Conversational Curiosity
Slug: curiosity
Authors: Pedro Rodriguez
Description: EMNLP 2020 Paper on Conversational Curiosity

![Curiosity dialog diagram](/static/images/curiosity-dialog.png){align=right}

Welcome to the project page for our EMNLP 2020 paper: [Information Seeking in the Spirit of Learning: a Dataset for Conversational Curiosity](https://www.aclweb.org/anthology/2020.emnlp-main.655/).
Our paper introduces the Curiosity dataset which consists of 14K dialogs with fine-grained knowledge groundings, dialog act annotations, and other auxiliary annotations.

You can browse and explore the curiosity dataset at [datasets.pedro.ai/dataset/curiosity](https://datasets.pedro.ai/dataset/curiosity).


## Abstract

Open-ended human learning and information-seeking are increasingly mediated by digital assistants. However, such systems often ignore the user's pre-existing knowledge.
Assuming a correlation between engagement and user responses such as "liking" messages or asking followup questions, we design a Wizard-of-Oz dialog task that tests the hypothesis that engagement increases when users are presented with facts related to what they know.
Through crowd-sourcing of this experiment, we collect and release 14K dialogs (181K utterances) where users and assistants converse about geographic topics like geopolitical entities and locations. This dataset is annotated with pre-existing user knowledge, message-level dialog acts, grounding to Wikipedia, and user reactions to messages. Responses using a user's prior knowledge increase engagement. We incorporate this knowledge into a multi-task model that reproduces human assistant policies and improves over a BERT content model by 13 mean reciprocal rank points.


## Citation

If you cite our paper, please use this citation:

```bib
@inproceedings{rodriguez2020curiosity,
    title = "Information Seeking in the Spirit of Learning: A Dataset for Conversational Curiosity",
    author = "Rodriguez, Pedro  and
      Crook, Paul  and
      Moon, Seungwhan  and
      Wang, Zhiguang",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.655",
    doi = "10.18653/v1/2020.emnlp-main.655",
    pages = "8153--8172",
}
```

## Data

You can download the dataset files in one of two ways:

1. Cloning the [model code](https://github.com/facebookresearch/curiosity) which includes the dataset via [git lfs](https://git-lfs.github.com).
2. Using the direct links below.


### Download Links

* [Curiosity Dialogs (All)](https://obj.umiacs.umd.edu/curiosity/curiosity_dialogs.json)
* [Curiosity Dialogs (Train)](https://obj.umiacs.umd.edu/curiosity/curiosity_dialogs.train.json)
* [Curiosity Dialogs (Val)](https://obj.umiacs.umd.edu/curiosity/curiosity_dialogs.val.json)
* [Curiosity Dialogs (Test)](https://obj.umiacs.umd.edu/curiosity/curiosity_dialogs.test.json)
* [Curiosity Dialogs (Zero-shot)](https://obj.umiacs.umd.edu/curiosity/curiosity_dialogs.test_zero.json)
* [Fact Entity Links](https://obj.umiacs.umd.edu/curiosity/fact_db_links.json)
* [Wikipedia2Vec Embeddings in Model](https://obj.umiacs.umd.edu/curiosity/wiki2vec_entity_100d.txt)
* [Wikipedia Sqlite Fact DB](https://obj.umiacs.umd.edu/curiosity/wiki_sql.sqlite.db)


## Code

We have open sourced our model and paper code at the links below.
Instructions to reproduce our results are in each respective repository.

* Model code: [github.com/facebookresearch/curiosity](https://github.com/facebookresearch/curiosity/)
* Paper code: [github.com/entilzha/publications](https://github.com/entilzha/publications)

## Contact

Please contact <a target="_blank" href="mailto:me@pedro.ai">Pedro Rodriguez at me@pedro.ai</a>
