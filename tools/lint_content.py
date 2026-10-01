#!/usr/bin/env python3
"""Content lint for the SSL reference pages.

Checks the mechanical conventions that have drifted before (see issue #23),
so CI can stop them from drifting again:

1. No bare code fences — output blocks use ```text, code uses a language.
2. No dangling ``:=`` at end of line inside ```ssl fences (orphaned string
   literals on the next line).
3. Usage-trailer comments use the canonical ``/* Usage;`` form (the
   descriptive ``/* Usage: ...;`` form is allowed). Any ```ssl block that
   calls ``DoProc``/``ExecFunction`` after its last ``:ENDPROC;`` must open
   that trailer with a single-line ``/* Usage;`` comment, with no bare
   ``/*`` or lone ``;`` lines, so multi-line and prose variants are caught.
4. A file's ```ssl fences indent consistently — tabs or spaces, not both.
5. Reference-page frontmatter carries no vestigial ``category:``/``tags:``.
6. No link whose text was turned into a placeholder, such as ``<date>(../types/date.md)``.

Run from the repository root:

    python3 tools/lint_content.py

Exits non-zero if any check fails.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT = REPO_ROOT / "content"

FENCE_OPEN = re.compile(r"^```([a-zA-Z0-9_-]*)[ \t]*$")
BAD_TRAILER = re.compile(
    r"^/\* (?:Usage example|Example call|Run the procedure|Call the procedure[^;]*);", re.M
)
CANON_TRAILER = re.compile(r"^/\* Usage(?:: [^;\n]+)?;\n")
TRAILER_CALL = re.compile(r"\b(?:DoProc|ExecFunction)\(")
TRAILER_JUNK = re.compile(r"^\s*;\s*$|^\s*/\*\s*$", re.M)
DANGLING_ASSIGN = re.compile(r":=[ \t]*$")
BROKEN_LINK = re.compile(r"<[A-Za-z][\w ]*>\((?:\.\./|\./)?[\w./-]+\.md(?:#[\w-]+)?\)")


def ssl_blocks(text: str) -> list[str]:
    return re.findall(r"^```ssl[ \t]*\n(.*?)^```", text, re.M | re.S)


def trailer_problem(block: str) -> str | None:
    """Return the offending trailer text if a block's usage trailer is non-canonical."""
    if ":ENDPROC;" not in block:
        return None
    tail = block[block.rindex(":ENDPROC;") + len(":ENDPROC;"):].strip()
    if not TRAILER_CALL.search(tail):
        return None
    if CANON_TRAILER.match(tail + "\n") and not TRAILER_JUNK.search(tail):
        return None
    return tail.split("\n", 1)[0]


def main() -> int:
    problems: list[str] = []
    for path in sorted(CONTENT.rglob("*.md")):
        rel = path.relative_to(REPO_ROOT)
        text = path.read_text(encoding="utf-8")

        # 1. bare opening fences
        state = 0
        for i, line in enumerate(text.split("\n"), start=1):
            m = FENCE_OPEN.match(line)
            if not m:
                continue
            if state == 0:
                if m.group(1) == "":
                    problems.append(f"{rel}:{i}: bare code fence (use ```text for output)")
                state = 1
            else:
                state = 0

        # 2. dangling := inside ssl fences
        for block in ssl_blocks(text):
            for line in block.splitlines():
                if DANGLING_ASSIGN.search(line):
                    problems.append(f"{rel}: dangling ':=' at end of line in ```ssl block")
                    break

        # 3. non-canonical usage trailers
        for m in BAD_TRAILER.finditer(text):
            problems.append(f"{rel}: non-canonical usage trailer {m.group(0)!r} (use '/* Usage;')")
        for block in ssl_blocks(text):
            first = trailer_problem(block)
            if first is not None:
                problems.append(
                    f"{rel}: usage trailer starting {first!r} is not a single-line '/* Usage;' comment"
                )

        # 4. mixed indentation within the file's ssl fences
        tabs = spaces = 0
        for block in ssl_blocks(text):
            for line in block.splitlines():
                if line.startswith("\t"):
                    tabs += 1
                elif line.startswith("    "):
                    spaces += 1
        if tabs and spaces:
            problems.append(f"{rel}: ```ssl blocks mix tab ({tabs}) and space ({spaces}) indentation")

        # 5. vestigial frontmatter keys on reference pages
        if "reference" in rel.parts:
            fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            if fm and re.search(r"^(category|tags):", fm.group(1), re.M):
                problems.append(f"{rel}: vestigial 'category:'/'tags:' frontmatter")

        # 6. placeholder-mangled links
        for m in BROKEN_LINK.finditer(text):
            problems.append(f"{rel}: link text replaced by a placeholder: {m.group(0)!r}")

    if problems:
        print(f"{len(problems)} content lint problem(s):")
        for p in problems:
            print(f"  {p}")
        return 1
    print("content lint: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
