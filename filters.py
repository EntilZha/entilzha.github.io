def blog_date_format(value):
    return value.strftime('%B {0}, %Y').format(value.strftime('%d').lstrip('0'))
