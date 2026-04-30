# STARLIMS SSL Reference

An unofficial reference site for the **STARLIMS Scripting Language (SSL)**.

Published site: https://mahoskye.github.io/starlims-ssl-reference/

## What this is

This project is the result of many years of personal notes and observations
from working with **STARLIMS version 11**. It collects function signatures,
class members, keyword and operator behavior, type information, and code
examples into a single browsable reference.

## How it was built

Various AI agents were used to generate the documentation in its current
form. I have tried to review everything, but there is bound to be something
that doesn't make sense or doesn't work the way I've represented it.

**Take the content here with a big old grain of salt. Use at your own risk.**

If you spot something wrong, please open an issue or a pull request.

## Disclaimer

This project is **unofficial**. It has no connection to, affiliation with, or
endorsement from STARLIMS, Abbott Informatics, or any related brand or
trademark. It is a personal project that I am making public so other SSL
developers can benefit from the notes I've accumulated.

## Building locally

Requires Python 3.9+.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Then open http://127.0.0.1:8000/.

To build the static site:

```bash
mkdocs build
```

## Deployment

Pushes to `main` are deployed to GitHub Pages automatically via
`.github/workflows/deploy.yml`.
