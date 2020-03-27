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
* [Blog post on Reproducible ML](/blog/2020/03/24/reproducible-ml-and-parameter-sweeps/)
* [Blog post on Debugging ML Code](/blog/2019/12/15/debug-ml-code/)
* Finished [Google AI](https://ai.google/research/)-Zurich winter research internship!
* Finished [Facebook Conversational AI](https://ai.facebook.com/) summer research internship
* [TACL Paper](https://www.pedro.ai/static/publications/2019_tacl_trick.pdf) on Adversarial Question Generation
""")
    return html
