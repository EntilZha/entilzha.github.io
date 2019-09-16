import json
import datetime
from pelican import signals
from pelican.readers import BaseReader
from plugins.react import compile_jsx
from bibtexparser.bparser import BibTexParser
from jinja2 import Template, Environment


template = """
<h2>Refereed</h2>
<ul>
{% for e in publications %}
<li>
<div>{{ e.authors }}. <b><a href="{{ e.url }}">{{ e.title }}</a></b>. <i>{{ e.source }}</i>, {{ e.year }}. <span class="bibtex" data-entry="{{ e.cite }}"></span></div>
</li>
{% endfor %}
</ul>
<h2>arXiv</h2>
<ul>
{% for e in arxiv %}
<li>
<div>{{ e.authors }}. <b><a href="{{ e.url }}">{{ e.title }}</a></b>. <i>{{ e.source }}</i>, {{ e.year }}.</div>
</li>
{% endfor %}
</ul>
<h2>Workshops</h2>
<ul>
{% for e in workshops %}
<li>
<div>{{ e.authors }}. <b><a href="{{ e.url }}">{{ e.title }}</a></b>. <i>{{ e.source }}</i>, {{ e.year }}.</div>
</li>
{% endfor %}
</ul>
<h2>Non-Refereed</h2>
<ul>
{% for e in non_refereed %}
<li>
<div>{{ e.authors }}. <b><a href="{{ e.url }}">{{ e.title }}</a></b>. <i>{{ e.source }}</i>, {{ e.year }}.</div>
</li>
{% endfor %}
</ul>
<h2>Media</h2>
<ul>
{% for e in media %}
<li>
{{ e.authors }}. <b><a href="{{ e.url }}">{{ e.title }}</a></b>. <i>{{ e.source }}</i>, {{ e.year }}.
</li>
{% endfor %}
</ul>
<h2>Course Projects</h2>
<ul>
{% for e in projects %}
<li>
{{ e.authors }}. <b><a href="{{ e.url }}">{{ e.title }}</a></b>. <i>{{ e.source }}</i>, {{ e.year }}.
</li>
{% endfor %}
</ul>
{{ 'theme/templates/partials/bibtex_entry.jsx' | compile_jsx }}
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
            arxiv = [e for e in entries if e['type'] == 'arxiv']
            workshops = [e for e in entries if e['type'] == 'workshop']
            non_refereed = [e for e in entries if e['type'] == 'non-refereed']
            media = [e for e in entries if e['type'] == 'media']
            projects = [e for e in entries if e['type'] == 'project']
            jinja_env = Environment()
            jinja_env.filters['compile_jsx'] = compile_jsx
            html = jinja_env.from_string(template).render(
                publications=publications,
                media=media,
                arxiv=arxiv,
                non_refereed=non_refereed,
                projects=projects,
                workshops=workshops
            )
        return html, parsed

    def _parse_entry(self, entry):
        authors = [author_format(e) for e in entry['author'].split('and')]
        is_journal = False
        if 'booktitle' in entry:
            source = entry['booktitle']
            volume = ''
        elif 'journal' in entry:
            is_journal = entry['ENTRYTYPE'] == 'article'
            source = entry['journal']
            volume = entry.get('volume', '')
        else:
            source = ''
            volume = ''
        parsed_entry = {
            'authors': comma_join(authors),
            'bib_authors': entry['author'],
            'url': entry['url'],
            'title': entry['title'],
            'year': entry['year'],
            'source': source,
            'volume': volume,
            'type': entry['type'],
            'id': '@' + entry['ID']
        }
        cite = self._entry_to_bibtex(parsed_entry, is_journal)
        parsed_entry['cite'] = cite
        return parsed_entry

    def _entry_to_bibtex(self, entry, is_journal):
        bibtex_key = entry['id']
        if bibtex_key.startswith('@'):
            bibtex_key = bibtex_key[1:]
        if is_journal:
            if entry['type'] == 'arxiv':
                return arxiv_template.format(
                    bibtex_key=bibtex_key,
                    title=entry['title'],
                    author=entry['bib_authors'],
                    journal=entry['source'],
                    year=entry['year'],
                    url=entry['url']
                )
            else:
                return journal_template.format(
                    bibtex_key=bibtex_key,
                    title=entry['title'],
                    author=entry['bib_authors'],
                    journal=entry['source'],
                    year=entry['year'],
                    volume=entry['volume'],
                    url=entry['url']
                )
        else:
            return booktitle_template.format(
                bibtex_key=bibtex_key,
                title=entry['title'],
                author=entry['bib_authors'],
                booktitle=entry['source'],
                year=entry['year'],
                url=entry['url']
            )



journal_template = """@article{{{bibtex_key},
    Title = {{{title}}},
    Author = {{{author}}},
    Journal = {{{journal}}},
    Year = {{{year}}},
    Volume = {{{volume}}},
    Url = {{{url}}},
}}"""

arxiv_template = """@article{{{bibtex_key},
    Title = {{{title}}},
    Author = {{{author}}},
    Year = {{{year}}},
    Url = {{{url}}},
}}"""

booktitle_template = """@inproceedings{{{bibtex_key},
    Title = {{{title}}},
    Author = {{{author}}},
    Booktitle = {{{booktitle}}},
    Year = {{{year}}},
    Url = {{{url}}},
}}"""

online_template = """@online{{{bibtex_key},
    Title = {{{title}}},
    Author = {{{author}}},
    Year = {{{year}}},
    Url = {{{url}}},
}}"""

def add_reader(readers):
    readers.reader_classes['pubs'] = PublicationsReader


def register():
    signals.readers_init.connect(add_reader)
