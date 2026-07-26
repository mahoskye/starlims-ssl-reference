"""MkDocs hooks for the SSL API reference site."""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pygments.lexers import _mapping
import pygments.lexers as _lex_mod
from ssl_lexer import SSLLexer


def on_startup(**kwargs):
    _mapping.LEXERS["SSLLexer"] = (
        "ssl_lexer",
        SSLLexer.name,
        tuple(SSLLexer.aliases),
        tuple(SSLLexer.filenames),
        (),
    )
    if hasattr(_lex_mod, "_lexer_cache"):
        _lex_mod._lexer_cache.clear()


def on_page_markdown(markdown, page, config, files):
    """Use each page's summary as its meta description for search engines."""
    if "description" not in page.meta and page.meta.get("summary"):
        page.meta["description"] = page.meta["summary"]
    return markdown


def on_page_content(html, page, config, files):
    """Mark exception tables for styling; keep code blocks out of search.

    Code examples dominated the search index (~3.3MB) while adding noise —
    searching an identifier surfaced every example using it ahead of the
    element's own page. ``data-search-exclude`` drops ``<pre>`` block
    contents from the index; titles and prose remain searchable.
    """
    html = re.sub(
        r'(<h2 id="exceptions">.*?</h2>\s*)<table>',
        (
            r'\1<table data-ssl-table="exceptions">'
            r'<colgroup><col><col></colgroup>'
        ),
        html,
        flags=re.DOTALL,
    )
    return html.replace("<pre>", "<pre data-search-exclude>")
