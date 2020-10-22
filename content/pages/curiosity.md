Title: Information Seeking in the Spirit of Learning: a Dataset for Conversational Curiosity
Slug: curiosity
Authors: Pedro Rodriguez
Description: EMNLP 2020 Paper on Conversational Curiosity

![Curiosity dialog diagram](/static/images/curiosity-dialog.png){align=right}

Welcome to the project page for our EMNLP 2020 paper: [Information Seeking in the Spirit of Learning: a Dataset for Conversational Curiosity](/static/publications/2020_emnlp_curiosity.paper.pdf).
Our paper introduces the Curiosity dataset which consists of 14K dialogs with fine-grained knowledge groundings, dialog act annotations, and other auxiliary annotations.

You can browse and explore the curiosity dataset at [datasets.pedro.ai/dataset/curiosity](https://datasets.pedro.ai/dataset/curiosity).


## Abstract

Open-ended human learning and information-seeking are increasingly mediated by digital assistants. However, such systems often ignore the user's pre-existing knowledge.
Assuming a correlation between engagement and user responses such as "liking" messages or asking followup questions, we design a Wizard-of-Oz dialog task that tests the hypothesis that engagement increases when users are presented with facts related to what they know.
Through crowd-sourcing of this experiment, we collect and release 14K dialogs (181K utterances) where users and assistants converse about geographic topics like geopolitical entities and locations. This dataset is annotated with pre-existing user knowledge, message-level dialog acts, grounding to Wikipedia, and user reactions to messages. Responses using a user's prior knowledge increase engagement. We incorporate this knowledge into a multi-task model that reproduces human assistant policies and improves over a BERT content model by 13 mean reciprocal rank points.


## Citation

If you cite our paper, until EMNLP2020 is in the ACL Anthology please use this citation:

```bib
@inproceedings{rodriguez2020curiosity,
    title = {Information Seeking in the Spirit of Learning: a Dataset for Conversational Curiosity},
    author = {Pedro Rodriguez and Paul Crook and Seungwhan Moon and Zhiguang Wang},
    year = 2020,
    booktitle = {Empirical Methods in Natural Language Processing}
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

Please contact <a target="_blank" href="https://mailhide.io/e/wbfjM">Pedro Rodriguez</a>