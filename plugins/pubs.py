import datetime
import copy
from pelican import signals
from pelican.readers import BaseReader
from plugins.react import compile_jsx
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bparser import BibTexParser
from bibtexparser.bibdatabase import BibDatabase
from jinja2 import Environment


template = """
<h3>PhD Thesis</h3>
<ul>
{% for e in thesis %}
<li>
<div>{{ e.authors }}. <b><a href="{{ e.url }}">{{ e.title }}</a></b>. <i>{{ e.source }}</i>, {{ e.year }}. <span class="bibtex" data-entry="{{ e.cite }}"></span></div>
</li>
{% endfor %}
</ul>
<h3>Conference and Journal Papers</h3>
<ul>
{% for e in publications %}
<li>
<div>{{ e.authors }}. <b><a href="{{ e.url }}">{{ e.title }}</a></b>. <i>{{ e.source }}</i>, {{ e.year }}. <span class="bibtex" data-entry="{{ e.cite }}"></span></div>
</li>
{% endfor %}
</ul>
<h3>arXiv</h3>
<ul>
{% for e in arxiv %}
<li>
<div>{{ e.authors }}. <b><a href="{{ e.url }}">{{ e.title }}</a></b>. <i>{{ e.source }}</i>, {{ e.year }}.</div>
</li>
{% endfor %}
</ul>
<h3>Workshop Papers</h3>
<ul>
{% for e in workshops %}
<li>
<div>{{ e.authors }}. <b><a href="{{ e.url }}">{{ e.title }}</a></b>. <i>{{ e.source }}</i>, {{ e.year }}.</div>
</li>
{% endfor %}
</ul>
<h3>Non-Refereed</h3>
<ul>
{% for e in non_refereed %}
<li>
<div>{{ e.authors }}. <b><a href="{{ e.url }}">{{ e.title }}</a></b>. <i>{{ e.source }}</i>, {{ e.year }}.</div>
</li>
{% endfor %}
</ul>
<h3>Media</h3>
<ul>
{% for e in media %}
<li>
{{ e.authors }}. <b><a href="{{ e.url }}">{{ e.title }}</a></b>. <i>{{ e.source }}</i>, {{ e.year }}.
</li>
{% endfor %}
</ul>
<h3>Course Projects</h3>
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
    if author.lower() == "pedro rodriguez":
        return "<b>" + author + "</b>"
    else:
        return author


def comma_join(authors):
    if not authors:
        return ""
    elif len(authors) == 1:
        return authors[0]
    else:
        return ", ".join(authors[:-1]) + ", and " + authors[-1]


def extract_citation(entry):
    entry = copy.deepcopy(entry)
    del entry["type"]
    single_entry_db = BibDatabase()
    single_entry_db.entries = [entry]
    writer = BibTexWriter()
    return bibtexparser.dumps(single_entry_db, writer).strip()


class PublicationsReader(BaseReader):
    enabled = True
    file_extensions = ["bib"]

    def read(self, filename):
        metadata = {
            "title": "Publications",
            "category": "Publications",
            "date": str(datetime.datetime.now()),
        }
        parsed = {}
        for key, value in metadata.items():
            parsed[key] = self.process_metadata(key, value)
        with open(filename) as f:
            parser = BibTexParser()
            parser.ignore_nonstandard_types = False
            db = parser.parse_file(f)
            entries = [self._parse_entry(e) for e in db.entries]

            thesis = []
            publications = []
            arxiv = []
            workshops = []
            non_refereed = []
            media = []
            projects = []

            thesis = [e for e in entries if e["type"] == "thesis"]
            publications = [e for e in entries if e["type"] == "publication"]
            arxiv = [e for e in entries if e["type"] == "arxiv"]
            workshops = [e for e in entries if e["type"] == "workshop"]
            non_refereed = [e for e in entries if e["type"] == "non-refereed"]
            media = [e for e in entries if e["type"] == "media"]
            projects = [e for e in entries if e["type"] == "project"]
            for e in entries:
                del e["type"]
            jinja_env = Environment()
            jinja_env.filters["compile_jsx"] = compile_jsx
            html = jinja_env.from_string(template).render(
                thesis=thesis,
                publications=publications,
                media=media,
                arxiv=arxiv,
                non_refereed=non_refereed,
                projects=projects,
                workshops=workshops,
            )
        return html, parsed

    def _parse_entry(self, entry):
        authors = [author_format(e) for e in entry["author"].split(" and ")]
        if "booktitle" in entry:
            source = entry["booktitle"]
            volume = ""
        elif "journal" in entry:
            source = entry["journal"]
            volume = entry.get("volume", "")
        elif "school" in entry:
            source = entry["school"]
            volume = ""
        else:
            source = ""
            volume = ""
        parsed_entry = {
            "authors": comma_join(authors),
            "bib_authors": entry["author"],
            "url": entry["url"],
            "title": entry["title"].replace("{", "").replace("}", ""),
            "year": entry["year"],
            "source": source,
            "volume": volume,
            "type": entry["type"],
            "id": "@" + entry["ID"],
        }
        cite = extract_citation(entry)
        parsed_entry["cite"] = cite
        return parsed_entry


def add_reader(readers):
    readers.reader_classes["pubs"] = PublicationsReader


def register():
    signals.readers_init.connect(add_reader)
