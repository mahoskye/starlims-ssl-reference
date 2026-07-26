# Contributing

Thanks for helping improve the SSL Reference. This page covers the things
that are not obvious from looking at the repo — read it before your first
change, because several conventions here are load-bearing for tooling.

## Repository layout (not the MkDocs default)

| Path | What it is |
|------|------------|
| `content/` | **The documentation pages.** This repo sets `docs_dir: content` in `mkdocs.yml` — the conventional `docs/` directory is *not* where pages live. |
| `docs/` | Build hooks only (`hooks.py`). Do not add pages here; MkDocs will not see them. |
| `content/data/ssl-element-meta.json` | **Generated** — never edit by hand. See [Regenerating the metadata JSON](#regenerating-the-metadata-json). |
| `tools/extract_reference_meta.py` | The generator for that JSON. |
| `ssl_lexer.py` | Custom Pygments lexer registered by `docs/hooks.py`, which is what makes ` ```ssl ` code fences highlight. |
| `mkdocs.yml` | Site config **and the full hand-maintained nav** — every page must be listed there. |

## Building locally

Linux/macOS:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdocs serve
```

Then open http://127.0.0.1:8000/. `mkdocs build` produces the static site in
`_site/`.

## Page conventions the tooling depends on

Reference pages are parsed by machines as well as read by people. Two tools
match pages **by exact heading and admonition text**, and both fail silently
when the text drifts:

- `docs/hooks.py` styles exception tables by matching the rendered
  `<h2 id="exceptions">` heading. Rename `## Exceptions` and the styling
  quietly disappears.
- `tools/extract_reference_meta.py` parses the `## Exceptions` table, the
  `## Caveats` bullets, and the `!!! success "Do"` / `!!! failure "Don't"`
  admonitions into `ssl-element-meta.json`. Reword those headings or
  admonition titles and the page's data silently drops out of the JSON.

So: keep the section skeleton of existing pages in the same category, and
keep the `Do` / `Don't` admonition titles exactly as they are.

Two section vocabularies exist **by deliberate per-category convention**:
functions, classes, and keywords use `When to use` / `Best practices` /
`Exceptions` / `Caveats` / `Related`; operators, types, literals, and most
special forms use `When to use it` / `Notes for daily SSL work` /
`Errors and edge cases` / `Related elements`. The extractor recognizes both
(`Errors and edge cases` feeds `caveats`, `Notes for daily SSL work` feeds
`best_practices`) — follow whichever vocabulary the page's category uses.

Every reference page carries frontmatter:

```yaml
---
title: "PageTitle"
summary: "One-sentence description — also used as the page's meta description."
id: ssl.<category>.<slug>
element_type: function | class | keyword | operator | literal | type | special_form | returns
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---
```

The `summary` matters more than it looks: it feeds the category index tables,
search, and the extracted JSON.

## Adding a page

1. Create the `.md` file under the right `content/reference/<category>/`
   directory, following an existing page in that category as a template.
2. Add it to the `nav:` in `mkdocs.yml`. The nav is fully hand-maintained.
   Functions are grouped by category (matching the sections of
   `content/reference/functions/index.md`) — add the entry to the right
   group, in alphabetical order.
3. Add a row to the category's `index.md` table and update any counts that
   page states.
4. Regenerate the metadata JSON (next section), and run
   `python3 tools/lint_content.py` — CI runs it too; it enforces the
   mechanical conventions (```text output fences, no dangling `:=`,
   canonical `/* Usage;` trailers, consistent fence indentation per file).
5. Build and check: CI runs `mkdocs build --strict`, so a page missing from
   the nav or a broken link fails the pull request rather than deploying
   broken.

## Regenerating the metadata JSON

`content/data/ssl-element-meta.json` is generated from the reference pages'
frontmatter and sections:

```bash
python3 tools/extract_reference_meta.py
```

Run it after **any** edit to a reference page and commit the JSON alongside
your change. CI verifies the JSON matches the pages and fails the PR if it
has drifted.

This file has consumers beyond this site: downstream repositories
(`ssl-style-guide` → `ssl-mcp-server`, `starlims-lsp`,
`vs-code-ssl-formatter`) vendor it or consume it transitively. Treat its
shape as an interface — if you need to change what the extractor emits,
coordinate with those projects.

## Content ground rules

- **Verify before documenting.** Behavior claims should match STARLIMS v11
  as actually observed; when something is observed-but-not-vendor-documented,
  say "in observed runtime behavior".
- **Write for SSL developers, not for the doc pipeline.** No build/pipeline
  narration, internal tool names, or style-rule IDs in `content/`.
- **Unofficial site** — see `README.md` for the disclaimer and license
  (CC BY 4.0).

## Reporting problems

Found something wrong but can't fix it yourself? [Open an
issue](https://github.com/mahoskye/starlims-ssl-reference/issues) with the
page and the behavior you observed.
