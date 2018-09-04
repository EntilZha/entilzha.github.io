import datetime
from pelican import signals
from pelican.readers import BaseReader
from bibtexparser.bparser import BibTexParser
from jinja2 import Template


template = """
<h2>Refereed Publications</h2>
<ul>
{% for e in publications %}
<li>
{{ e.authors }}. <b><a href="{{ e.url }}">{{ e.title }}</a></b>. <i>{{ e.source }}</i>, {{ e.year }}
</li>
{% endfor %}
</ul>
<h2>Media</h2>
<ul>
{% for e in media %}
<li>
{{ e.authors }}. <b><a href="{{ e.url }}">{{ e.title }}</a></b>. <i>{{ e.source }}</i>, {{ e.year }}
</li>
{% endfor %}
</ul>
"""

def author_format(author):
    author = author.strip()
    if author.lower() == 'pedro rodriguez':
        return '<b>' + author + '</b>'
    else:
        return author

def comma_join(authors):
    if not authors:
        return ""
    elif len(authors) == 1:
        return authors[0]
    else:
        return ', '.join(authors[:-1]) + ", and " + authors[-1]


class PublicationsReader(BaseReader):
    enabled = True
    file_extensions = ['bib']

    def read(self, filename):
        metadata = {
            'title': 'Publications',
            'category': 'Publications',
            'date': str(datetime.datetime.now())
        }
        parsed = {}
        for key, value in metadata.items():
            parsed[key] = self.process_metadata(key, value)
        with open(filename) as f:
            parser = BibTexParser()
            parser.ignore_nonstandard_types = False
            db = parser.parse_file(f)
            entries = [self._parse_entry(e) for e in db.entries]
            publications = [e for e in entries if e['type'] == 'publication']
            media = [e for e in entries if e['type'] == 'media']
            html = Template(template).render(publications=publications, media=media)
        return html, parsed

    def _parse_entry(self, entry):
        authors = [author_format(e) for e in entry['author'].split('and')]
        if 'booktitle' in entry:
            source = entry['booktitle']
        elif 'journal' in entry:
            source = entry['journal']
        else:
            source = ''
        return {
            'authors': comma_join(authors),
            'url': entry['url'],
            'title': entry['title'],
            'year': entry['year'],
            'source': source,
            'type': entry['type']
        }


def add_reader(readers):
    readers.reader_classes['pubs'] = PublicationsReader

def register():
    signals.readers_init.connect(add_reader)
