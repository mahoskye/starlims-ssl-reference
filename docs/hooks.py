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


def on_page_content(html, page, config, files):
    """Mark exception tables so column widths can be styled consistently."""
    return re.sub(
        r'(<h2 id="exceptions">.*?</h2>\s*)<table>',
        (
            r'\1<table data-ssl-table="exceptions">'
            r'<colgroup><col><col></colgroup>'
        ),
        html,
        flags=re.DOTALL,
    )
