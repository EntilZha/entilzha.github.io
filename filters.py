def blog_date_format(value):
    return value.strftime('%B {0}, %Y').format(value.strftime('%d').lstrip('0'))

def default_description(value):
    if value:
        return 'Description: ' + value
    else:
        return ''

def news(_):
    import markdown
    html = markdown.markdown(
"""
* August 3: [Presenting ACL 2021 Paper on Item Response Theory for NLP Leaderboards](https://irt.pedro.ai)
* April 19: [Started as a Research Scientist at Facebook Reality Labs](https://research.fb.com/people/rodriguez-pedro/)
* April 9: Defended PhD Thesis on "Evaluating Machine Intelligence with Question Answering"
* [EMNLP 2020 Paper from FB Internship](https://www.aclweb.org/anthology/2020.emnlp-main.655/)
* [Blog post on AllenNLP Callbacks and CometML](https://www.pedro.ai/blog/2020/04/08/allennlp-callback-trainer-cometml/)
* [Blog post on Reproducible ML](/blog/2020/03/24/reproducible-ml-and-parameter-sweeps/)
* [Blog post on Debugging ML Code](/blog/2019/12/15/debug-ml-code/)
* [arXiv Preprint for Quizbowl](https://arxiv.org/abs/1904.04792)
* [TACL Paper](https://www.pedro.ai/static/publications/2019_tacl_trick.pdf) on Adversarial Question Generation
""")
    return html
