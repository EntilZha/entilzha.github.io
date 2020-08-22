Title: Literature Review Tricks
Date: 2020-8-22
Tags: research,writing
Slug: literature-review-tricks
Author: Pedro Rodriguez


Conducting a thorough literature review for a new idea is a critical yet difficult research skill to learn.
Even now, for areas I'd like to think I have a good grasp on, its difficult not to miss something important; multiple times, I've done a literature review only to find a couple weeks later I missed a paper or two.
In this post, I will share some of the tricks I've learned for making literature reviews easier.

I've found the most helpful tricks are (1) using scholar tools like [Semantic Scholar](https://www.semanticscholar.org/), (2) following authors who frequently publish papers relevant to your area of interest, (3) exposing yourself to social groups that share papers, (4) knowing how to ask for help, and (5) using a system for managing papers/references.
These combined will passively and actively increase the quality of literature reviews while making them more easier to do.

I view literature review as an iterative queue-building and writing process that bounces between depth first search, breadth first search, and writing.
In the breadth first search phase, I am looking to add as many separate papers to my queue.
For example, I might use scholar tools or google search to find a set of papers that seem relevant and add them to my queue.
In the depth first search phase, I read or skim papers to check for (1) relevance to the review and (2) find which of the paper's references I should add to my queue.
If I believe a paper is relevant, I'll do a second skim, copy the bibtex entry to my bibfile, and write a placeholder comment + citation in my latex document that I'll expand later.

This basic process should capture many papers, but there are a few specific tricks that I find very useful.

## General Tips

1. Conference tutorials are good starting places since they provide an overview of an area and should reference the most important papers in that area.
2. One useful view of literature review is as a graph traversal along citations/references. You should aim to iteratively find new loosely connected components and fully explore known connected components.
3. Have a system for managing papers.

## Semantic Scholar for Paper Citations

One of Semantic Scholar's most useful features is to list all the papers that cite a specific paper.
For example, to find a list of papers citing [Pathologies of Neural Models Make Interpretation Difficult](https://www.semanticscholar.org/paper/Pathologies-of-Neural-Models-Make-Interpretation-Feng-Wallace/74e9053d6f44f4507bd40bbea999ee65f0cbefb2) I can click the "citations" tab.
This trick is especially helpful for searches intents like:

1. Finding the most recent research on a specific dataset/task.
2. Finding all uses of a specific method

This trick is extremely effective if there is a specific paper that you believe all/most papers in your literature review would cite.
For example, if I am doing a literature review of [SQuAD models](https://rajpurkar.github.io/SQuAD-explorer/) then I can be fairly sure that any relevant papers will cite the SQuAD paper.
The main drawback of this approach---as is apparent for SQuAD or ImageNet---is that this list of papers might be huge; such is life though.

## Following Authors and Social Groups

There are two easy ways to follow authors: via the "follow author" feature on Semantic Scholar and via Twitter.
The first easy easy enough: as you read papers, if you like reading someone's work then follow their profile on Semantic Scholar.
While this by construction won't represent a diverse set of papers, its very useful if specific researchers consistently publish papers you enjoy reading or are relevant to your subject area.
Similarly, you should also sign up for notifications for when someone cites one of your papers since those papers are likely relevant to you.

This leads me to the topic of Twitter.
Say what you will about Twitter, but I have found it to be a consistent source of papers that tend to interest me.
To get to this point though, you will need to put conscious effort to continually expand who you follow.
I view Twitter as a sort of filter on the arXiv/conference proceedings firehose that is most helpful in passively exposing me to recent research.

On a similar note, you should look to build or join social groups that share and/or read papers.
For example, the [UMD CLIP](https://wiki.umiacs.umd.edu/clip/index.php/Main_Page) has a Slack workspace where we post about papers of general NLP interest and papers in specific areas (e.g., question answering).
Similarly, there is usually at least one reading group which is another way to gain exposure to papers.

## Asking for Help

Once you've done all the above and either can't find more or are stuck, then you should ask for help.
But, you should be smart about how you ask for help.
When I ask for help, I typically aim to establish: (1) what specific topic/question am I interested in, (2) which papers have I looked at which are most similar, and (3) how I've tried thus far to find these papers.

As a recent example, I was trying to find papers discussing neural model calibration.
In this area, nearly all papers cite at least [On Calibration of Modern Neural Networks](http://proceedings.mlr.press/v70/guo17a.html).
Thus far, my searches had focused around finding various rephrasing of calibration and traversing the citation graph.
My advisor suggested I try searching for "posterior calibration" which led to finding another cluster of relevant papers.

Although I haven't tried this, I have seen similar approaches to asking the Twitterverse for references.

## Reference Managers

The last important trick for literature review is to use and maintain (1) a system for saving and reading papers, and (2) a bibfile for citing papers.
While these may be one and the same, I'd recommend keeping them separate.
The most important thing I look for in a paper manager is that it is easy enough to use that I actually use it consistently.
I used to use [Zotero](https://www.zotero.org/), but found that I didn't use it consistently.
For reasons that are difficult to pinpoint, after switching to paid [Paperpile](https://paperpile.com/app) I have been much better about making sure anything I read or plan to read is imported.
My suspicion is that the combination of intuitive labels, folders, shared folders, and easy bib reference copying made the software useful enough in my daily workflow to use consistently which in turn massively increased its usefulness.
Unsurprisingly, keeping good track of papers you read (or intended to read) will make it easier to do a literature review on that topic later.

Along similar lines, maintaining a single, nice bibfile makes the writing process easier.
My personal preference is to make all citation keys follow the format: authorYYYYkeyword.
This has several benefits: (1) you become more familiar with some of the authors in the field, (2) when citing papers you can cite in year order correctly, and (3) keywords make it easy to remember which paper is which.
Having a single bib file also makes it easier to maintain and update references (e.g., if an arXiv paper is published).

## Conclusion

While these set of tricks is certainly not exhaustive, I hope it helps anyone setting out on new literature reviews!
If you have more ideas on how to make literature reviews easier or improve their quality, please let me know on [Twitter](https://twitter.com/EntilZhaPR)!
