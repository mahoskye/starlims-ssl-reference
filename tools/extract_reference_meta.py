#!/usr/bin/env python3
"""Extract structured per-element metadata from the ssl-docs reference site.

Walks ``content/reference/<category>/*.md`` and pulls out:

* YAML frontmatter (``id``, ``element_type``, ``title``, ``summary``)
* The ``## Exceptions`` section, parsed as a list of ``{trigger, message}``
  pairs from its markdown table.
* The ``## Caveats`` section, parsed as a list of bullet items (free prose).
* The ``## Best practices`` section, split into ``do`` and ``dont`` bullet
  lists from the ``!!! success "Do"`` / ``!!! failure "Don't"`` admonitions.

Output: ``content/data/ssl-element-meta.json``. Downstream repositories
(``ssl-style-guide`` -> ``ssl-mcp-server``, ``starlims-lsp``,
``vs-code-ssl-formatter``) vendor this file or consume it transitively.

The extractor is intentionally permissive: missing sections produce empty
lists rather than errors, so partially-documented pages still contribute
their frontmatter without holding up the extraction.

Run from the repository root:

    python3 tools/extract_reference_meta.py

Or set ``OUTPUT`` to write somewhere else.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
REFERENCE_ROOT = REPO_ROOT / "content" / "reference"
DEFAULT_OUTPUT = REPO_ROOT / "content" / "data" / "ssl-element-meta.json"

# Categories we walk. Mirrors the directories under content/reference.
CATEGORIES = (
    "functions",
    "classes",
    "keywords",
    "operators",
    "literals",
    "types",
    "special-forms",
)


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Strip a YAML frontmatter block from the top of ``text``.

    Returns ``(frontmatter_dict, remaining_body)``. We do a minimal YAML
    parse — the frontmatter format used in ssl-docs is simple key/value
    pairs plus one nested ``starlims:`` block — to avoid pulling PyYAML
    into the build dependency graph. If the file has no frontmatter the
    returned dict is empty.
    """
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    block = text[4:end]
    body = text[end + 5:]

    fm: dict[str, Any] = {}
    pending_block: str | None = None
    sub: dict[str, Any] = {}
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[:2] == "  ":
            # Indented child of the most recent block-style key.
            if pending_block is None:
                continue
            k, _, v = raw.strip().partition(":")
            sub[k.strip()] = _coerce_scalar(v.strip())
            continue
        if pending_block is not None:
            fm[pending_block] = sub
            pending_block = None
            sub = {}
        if raw.endswith(":"):
            pending_block = raw[:-1].strip()
            sub = {}
            continue
        k, _, v = raw.partition(":")
        fm[k.strip()] = _coerce_scalar(v.strip())
    if pending_block is not None:
        fm[pending_block] = sub
    return fm, body


def _coerce_scalar(value: str) -> Any:
    """Best-effort YAML scalar coercion: strings, lists of ints/strings."""
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        items = [x.strip() for x in inner.split(",")]
        return [_coerce_scalar(x) for x in items]
    if value.isdigit():
        return int(value)
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


_SECTION_HEADER = re.compile(r"^(##\s+.+)$", re.M)


def split_sections(body: str) -> dict[str, str]:
    """Split a markdown body by ``## ...`` headers into a dict.

    Keys are the lowercased header text (e.g. ``"exceptions"``). Values
    are the section bodies (without the header line itself).
    """
    out: dict[str, str] = {}
    matches = list(_SECTION_HEADER.finditer(body))
    for i, m in enumerate(matches):
        header = m.group(1).lstrip("#").strip().lower()
        start = m.end() + 1  # skip the trailing newline of the header line
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        out[header] = body[start:end].strip()
    return out


_INLINE_LINK = re.compile(r"\[`?([^\]`]+)`?\]\([^\)]+\)")
_INLINE_CODE = re.compile(r"`([^`]+)`")


def strip_inline_markdown(text: str) -> str:
    """Best-effort flattening of inline markdown for plain-text consumption.

    Replaces ``[`X`](path)`` with ``X``, drops backticks around inline code
    spans. Leaves the rest alone — downstream consumers can do their own
    rendering if they want full fidelity.
    """
    text = _INLINE_LINK.sub(r"\1", text)
    text = _INLINE_CODE.sub(r"\1", text)
    return text.strip()


def parse_exceptions_table(section: str) -> list[dict[str, str]]:
    """Parse the standard ``| Trigger | Exception message |`` table.

    Tolerates the rare element that documents exceptions as a bullet list
    (e.g. a single 'None' or 'No documented exceptions.' note) — those
    yield an empty list. Skips the header row and the separator row.
    """
    rows: list[dict[str, str]] = []
    in_table = False
    seen_separator = False
    for line in section.splitlines():
        line = line.rstrip()
        if not line.startswith("|"):
            if in_table:
                break
            continue
        in_table = True
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not seen_separator:
            # First "|---|---|" separator row tells us the table actually started.
            if all(re.fullmatch(r":?-+:?", c) for c in cells):
                seen_separator = True
            continue
        if len(cells) < 2:
            continue
        trigger, message = cells[0], cells[1]
        if not trigger and not message:
            continue
        rows.append({
            "trigger": strip_inline_markdown(trigger),
            "message": strip_inline_markdown(message.strip("`")),
        })
    return rows


_BULLET = re.compile(r"^[-*]\s+(.+?)\s*$")


def parse_bullet_list(section: str) -> list[str]:
    """Pull top-level bullet items out of a section. Sub-bullets are joined
    onto their parent with a leading "; " so we don't lose qualifiers."""
    items: list[str] = []
    current: str | None = None
    for raw in section.splitlines():
        m = _BULLET.match(raw)
        if m:
            if current is not None:
                items.append(strip_inline_markdown(current))
            current = m.group(1)
            continue
        # Sub-bullet (starts with whitespace then a bullet) attaches to current.
        sub = re.match(r"^\s+[-*]\s+(.+?)\s*$", raw)
        if sub and current is not None:
            current = current + "; " + sub.group(1)
    if current is not None:
        items.append(strip_inline_markdown(current))
    return items


_ADMONITION_HEADER = re.compile(r'^!!!\s+(\w+)\s+"([^"]+)"', re.M)


def parse_best_practices(section: str) -> dict[str, list[str]]:
    """Parse the ``!!! success "Do"`` / ``!!! failure "Don't"`` admonitions.

    Each admonition's body is indented with at least 4 spaces (mkdocs
    convention). We collect bullet lines from each block and label them
    by the admonition title (lowercased, with curly apostrophes
    normalized to ``don't``).
    """
    out: dict[str, list[str]] = {}
    matches = list(_ADMONITION_HEADER.finditer(section))
    for i, m in enumerate(matches):
        kind_title = m.group(2).strip().lower().replace("’", "'")
        # Normalize the canonical pair: "Do" -> "do", "Don't" -> "dont".
        if kind_title == "do":
            key = "do"
        elif kind_title in ("don't", "dont"):
            key = "dont"
        else:
            key = kind_title
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(section)
        block = section[start:end]
        # The admonition body is indented; dedent and parse bullets.
        lines = []
        for line in block.splitlines():
            if line.startswith("    "):
                lines.append(line[4:])
            elif line.startswith("\t"):
                lines.append(line[1:])
            else:
                lines.append(line)
        items = parse_bullet_list("\n".join(lines))
        out.setdefault(key, []).extend(items)
    return out


def extract_element(path: Path) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    if not fm.get("id") or not fm.get("element_type"):
        return None
    sections = split_sections(body)
    return {
        "id": fm.get("id", ""),
        "element_type": fm.get("element_type", ""),
        "title": fm.get("title", path.stem),
        "summary": fm.get("summary", ""),
        "doc_status": fm.get("doc_status", ""),
        "source_path": path.relative_to(REPO_ROOT).as_posix(),
        "exceptions": parse_exceptions_table(sections.get("exceptions", "")),
        "caveats": parse_bullet_list(sections.get("caveats", "")),
        "best_practices": parse_best_practices(sections.get("best practices", "")),
    }


def extract_all() -> list[dict[str, Any]]:
    elements: list[dict[str, Any]] = []
    for category in CATEGORIES:
        category_dir = REFERENCE_ROOT / category
        if not category_dir.is_dir():
            continue
        for path in sorted(category_dir.iterdir()):
            if path.suffix != ".md" or path.name == "index.md":
                continue
            element = extract_element(path)
            if element:
                elements.append(element)
    return elements


def main() -> int:
    output = Path(os.environ.get("OUTPUT", DEFAULT_OUTPUT))
    elements = extract_all()
    output.parent.mkdir(parents=True, exist_ok=True)

    counts: dict[str, int] = {}
    has_exceptions = 0
    has_caveats = 0
    has_best_practices = 0
    for el in elements:
        counts[el["element_type"]] = counts.get(el["element_type"], 0) + 1
        if el["exceptions"]:
            has_exceptions += 1
        if el["caveats"]:
            has_caveats += 1
        if el["best_practices"]:
            has_best_practices += 1

    payload = {
        "version": "1.0",
        "source": "ssl-docs/content/reference",
        "totals": {
            "elements": len(elements),
            "by_type": counts,
            "with_exceptions": has_exceptions,
            "with_caveats": has_caveats,
            "with_best_practices": has_best_practices,
        },
        "elements": elements,
    }
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    print(f"Wrote {len(elements)} elements to {output}")
    print(f"  by type: {counts}")
    print(f"  with exceptions:     {has_exceptions}")
    print(f"  with caveats:        {has_caveats}")
    print(f"  with best practices: {has_best_practices}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
