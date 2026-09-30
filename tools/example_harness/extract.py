#!/usr/bin/env python3
"""Inventory every ```ssl example on the site for the example-testing harness.

Walks ``content/**/*.md`` and writes one JSON record per ```ssl fence to
``tools/example_harness/examples.json``. Each record says where the example
lives, what kind of block it is, how it is meant to be called, what output
the page promises, and what it depends on, so a runner can pick out the
examples it is able to execute and check them against the page.

Record fields:

* ``id`` -- ``<path relative to content>#<n>``, ``n`` being the 1-based
  index of the ```ssl fence within its page.
* ``page``, ``line`` -- the page path (relative to the repository root) and
  the 1-based line of the opening fence.
* ``heading`` -- nearest ``###`` or ``##`` heading above the block;
  ``section`` -- nearest ``##`` heading above it.
* ``kind`` -- ``syntax`` (inside ``## Syntax`` or a one-line signature),
  ``class`` (contains ``:CLASS``), ``procedure`` (defines ``:PROCEDURE``),
  otherwise ``fragment``.
* ``procedures`` -- procedure names the block defines.
* ``entry`` -- the statements in the usage trailer after the last
  ``:ENDPROC;`` that call ``DoProc``/``ExecFunction`` (e.g.
  ``DoProc("Name", {args});`` or ``:RETURN DoProc(...);``).
* ``expected_output`` / ``expected_prose`` -- the first ```text fence that
  follows the block (before the next ```ssl fence or heading) when the prose
  in between says the example logs or returns something, and that prose
  line. ``expected_alternatives`` holds further ```text fences in the same
  span that are introduced the same way or with "or" (pages that say
  "logs either ... or").
* ``depends`` -- ``db_tables`` (tables named in SQL string literals, best
  effort), ``db`` (calls a database function), ``external`` (integration
  families such as ``ftp``, ``email``, ``file-io``), ``helpers``
  (``DoProc``/``ExecFunction`` targets not defined in the block;
  ``<dynamic>`` when the target is computed from a ``Category.Script``
  style literal) and
  ``classes`` (string targets of ``CreateUdObject``).
* ``runnable`` -- ``pure``, ``db``, ``helper``, ``class``, ``external`` or
  ``not-runnable``; see ``classify_runnable``.

``examples.json`` is generated and not committed (it is listed in
``.gitignore``). Regenerate it from the repository root with:

    python3 tools/example_harness/extract.py

Pass ``--output PATH`` to write it somewhere else. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CONTENT = REPO_ROOT / "content"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "examples.json"

FENCE = re.compile(r"^([ \t]*)```([A-Za-z0-9_-]*)[ \t]*$")
HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
PROC_DEF = re.compile(r"^[ \t]*:PROCEDURE[ \t]+([A-Za-z_][A-Za-z0-9_]*)", re.I | re.M)
CLASS_DEF = re.compile(r"^[ \t]*:CLASS\b", re.I | re.M)
ENDPROC = re.compile(r":ENDPROC[ \t]*;", re.I)
PROC_CALL = re.compile(r"\b(DoProc|ExecFunction)[ \t]*\(", re.I)
UDOBJECT_CALL = re.compile(r"\bCreateUdObject[ \t]*\([ \t]*([\"'])([^\"']+)\1", re.I)
DYNAMIC_TARGET = re.compile(r"(?<![:\w.])(?:DoProc|ExecFunction)[ \t]*\([ \t]*[^\"'\s]", re.I)
SCRIPT_PATH = re.compile(r"^[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*\.(?:[A-Za-z_]\w*)?$")
PROC_TARGET = re.compile(r"\b(?:DoProc|ExecFunction)[ \t]*\([ \t]*([\"'])([^\"']+)\1", re.I)
EXPECT_PROSE = re.compile(
    r"\b(?:logs?|logged|returns?|returned|output|prints?|displays?|shows?)\b", re.I
)

# --- dependency vocabularies -------------------------------------------------

DB_FUNCTIONS = {
    "RunSQL", "SQLExecute", "LSelect", "LSelect1", "LSelectC", "LSearch",
    "GetDataSet", "GetDataSetEx", "GetDataSetWithSchemaFromSelect",
    "GetDataSetXMLFromSelect", "GetNETDataSet", "GetSSLDataset",
    "BeginLimsTransaction", "EndLimsTransaction", "RunDS", "GetDSParameters",
    "XmlExportSql", "UpdLong", "RetrieveLong", "LimsSetCounter",
    "LimsSqlConnect", "LimsSqlDisconnect", "GetConnectionByName",
    "GetConnectionStrings", "IsTable", "IsTableFld", "TableFldLst", "GetTables",
    "CreateORMSession", "IsDBConnected", "GetDBMSName", "GetDBMSProviderName",
    "LimsRecordsAffected", "ArrayToTVP", "ChkPassword", "ChkNewPassword",
    "SetUserPassword", "DetectSqlInjections", "IsInTransaction",
    "GetTransactionsCount",
}
DB_CLASSES = {"Sequence", "SQLConnection"}

EXTERNAL_FUNCTIONS: dict[str, set[str]] = {
    "ftp": {
        "CheckOnFtp", "CopyToFtp", "DeleteDirOnFtp", "DeleteFromFtp",
        "GetDirFromFtp", "GetFromFtp", "MakeDirOnFtp", "MoveInFtp",
        "ReadFromFtp", "RenameOnFtp", "SendToFtp", "WriteToFtp",
    },
    "ldap": {"LDAPAuth", "LDAPAuthEX", "SearchLDAPUser"},
    "email": {"SendLimsEmail", "SendOutlookReminder", "SendFromOutbox", "SendToOutbox"},
    "file-io": {
        "ReadText", "WriteText", "FileSupport", "CreateZip", "ExtractZip",
        "LDir", "Directory", "ReadBytesBase64", "WriteBytesBase64",
        "CombineFiles", "DosSupport", "GetFileVersion", "ConvertReport",
    },
    "dotnet": {"LimsNETConnect", "MakeNETObject", "LimsOleConnect", "EndLimsOleConnect"},
    "printers": {"GetPrinters"},
    "batch": {"SubmitToBatch", "SubmitToBatchEx", "RunApp", "LimsExec"},
}
EXTERNAL_CLASSES: dict[str, str] = {
    "Email": "email",
    "FtpsClient": "ftp",
    "AzureStorage": "azure",
    "SDMS": "sdms",
    "SDMSDocUploader": "sdms",
    "WebServices": "web",
    "PdfSupport": "file-io",
    "HtmlConverter": "file-io",
    "EnterpriseExporter": "file-io",
    "TablesImport": "file-io",
    "RegSetup": "file-io",
    "PatcherSupport": "web",
    "BatchSupport": "batch",
}
DOCUMENTUM_CALL = re.compile(r"\bDoc[A-Z][A-Za-z]*[ \t]*\(")
SFTP_HINT = re.compile(r"\bsftp\b", re.I)
# Web-service scripts read the host-supplied Request and Response objects.
HTTP_HOST_OBJECT = re.compile(r"(?<![:\w.])(?:Request|Response)[ \t]*:", re.I)

# --- SQL table detection -------------------------------------------------------

SQL_SHAPE = re.compile(
    r"\bSELECT\b[\s\S]*\bFROM\b|\bINSERT\s+INTO\b|\bUPDATE\s+\S+\s+SET\b|\bDELETE\s+FROM\b"
    r"|\bMERGE\s+INTO\b",
    re.I,
)
SQL_TABLE = re.compile(
    r"\b(?:FROM|JOIN|INTO|UPDATE|DELETE\s+FROM)\s+([A-Za-z_#@][\w.$#@]*)", re.I
)
SQL_NOT_TABLES = {"select", "set", "dual", "values", "where", "lateral"}


def scan_ssl(block: str) -> tuple[str, list[str]]:
    """Split a block into code with comments and strings blanked, plus its string literals.

    SSL comments run from ``/*`` to the next ``;``. Double- and single-quoted
    strings are recognized; bracketed strings are too ambiguous with indexing
    to be worth guessing at here.
    """
    code: list[str] = []
    strings: list[str] = []
    i, n = 0, len(block)
    while i < n:
        ch = block[i]
        if ch in "\"'":
            end = block.find(ch, i + 1)
            if end < 0:
                end = n - 1
            strings.append(block[i + 1:end])
            code.append(ch + re.sub(r"[^\n]", " ", block[i + 1:end]) + ch)
            i = end + 1
        elif block.startswith("/*", i):
            end = block.find(";", i + 2)
            if end < 0:
                end = n - 1
            code.append(re.sub(r"[^\n]", " ", block[i:end + 1]))
            i = end + 1
        else:
            code.append(ch)
            i += 1
    return "".join(code), strings


def called(code: str, names: set[str]) -> set[str]:
    """Names from ``names`` that ``code`` calls (case-insensitive, as SSL is)."""
    found = set()
    lowered = {name.lower(): name for name in names}
    for m in re.finditer(r"(?<![:\w.])([A-Za-z_][A-Za-z0-9_]*)[ \t]*\(", code):
        name = lowered.get(m.group(1).lower())
        if name:
            found.add(name)
    return found


def instantiated(code: str, names: set[str]) -> set[str]:
    """Built-in classes from ``names`` that ``code`` creates with ``Name{...}``."""
    found = set()
    lowered = {name.lower(): name for name in names}
    for m in re.finditer(r"(?<![:\w.])([A-Za-z_][A-Za-z0-9_]*)[ \t]*\{", code):
        name = lowered.get(m.group(1).lower())
        if name:
            found.add(name)
    return found


def statements_after_last_endproc(block: str) -> list[str]:
    """Trailer statements after the last ``:ENDPROC;`` that call DoProc/ExecFunction."""
    ends = list(ENDPROC.finditer(block))
    if not ends:
        return []
    tail = block[ends[-1].end():]
    code, _ = scan_ssl(tail)
    entries: list[str] = []
    start = 0
    depth = 0
    for i, ch in enumerate(code):
        if ch in "({":
            depth += 1
        elif ch in ")}":
            depth -= 1
        elif ch == ";" and depth <= 0:
            if PROC_CALL.search(code[start:i]):
                # Skip leading whitespace and comments (blanked in ``code``).
                lead = len(code[start:i + 1]) - len(code[start:i + 1].lstrip())
                stmt = tail[start + lead:i + 1].strip()
                entries.append(stmt)
            start = i + 1
    return entries


def is_signature(block: str) -> bool:
    lines = [ln.strip() for ln in scan_ssl(block)[0].splitlines() if ln.strip()]
    return len(lines) == 1 and not lines[0].endswith(";")


def classify_kind(block: str, section: str | None, heading: str | None) -> str:
    if (section or "").strip().lower() == "syntax" or (heading or "").strip().lower() == "syntax":
        return "syntax"
    code, _ = scan_ssl(block)
    if CLASS_DEF.search(code):
        return "class"
    if PROC_DEF.search(code):
        return "procedure"
    if is_signature(block):
        return "syntax"
    return "fragment"


def dependencies(block: str, procedures: list[str]) -> dict[str, Any]:
    code, strings = scan_ssl(block)

    tables: list[str] = []
    for s in strings:
        if not SQL_SHAPE.search(s):
            continue
        for m in SQL_TABLE.finditer(s):
            table = m.group(1).rstrip(".")
            if table.lower() in SQL_NOT_TABLES or table.startswith("?"):
                continue
            if table not in tables:
                tables.append(table)

    db = bool(called(code, DB_FUNCTIONS) or instantiated(code, DB_CLASSES))

    external: set[str] = set()
    if DOCUMENTUM_CALL.search(code):
        external.add("documentum")
    for family, names in EXTERNAL_FUNCTIONS.items():
        if called(code, names):
            external.add(family)
    for cls in instantiated(code, set(EXTERNAL_CLASSES)):
        external.add(EXTERNAL_CLASSES[cls])
    if "ftp" in external and any(SFTP_HINT.search(s) for s in strings):
        external.add("sftp")
    if HTTP_HOST_OBJECT.search(code):
        external.add("web")

    defined = {p.lower() for p in procedures}
    helpers: list[str] = []
    for m in PROC_TARGET.finditer(block):
        # Skip matches inside comments: the same span must be live code.
        if code[m.start():m.start() + 6].lower() not in ("doproc", "execfu"):
            continue
        target = m.group(2)
        if target.lower() not in defined and target not in helpers:
            helpers.append(target)

    # A name computed at runtime that is built from a "Category.Script" style
    # literal dispatches outside the block.
    if DYNAMIC_TARGET.search(code) and any(SCRIPT_PATH.match(s) for s in strings):
        helpers.append("<dynamic>")

    classes: list[str] = []
    for m in UDOBJECT_CALL.finditer(block):
        if code[m.start():m.start() + 14].lower() != "createudobject":
            continue
        if m.group(2) not in classes:
            classes.append(m.group(2))

    return {
        "db_tables": tables,
        "db": db,
        "external": sorted(external),
        "helpers": helpers,
        "classes": classes,
    }


def classify_runnable(kind: str, deps: dict[str, Any]) -> str:
    if kind in ("syntax", "fragment"):
        return "not-runnable"
    if kind == "class":
        return "class"
    if deps["external"]:
        return "external"
    if deps["classes"]:
        return "class"
    if deps["helpers"]:
        return "helper"
    if deps["db"]:
        return "db"
    return "pure"


def dedent(lines: list[str], indent: str) -> str:
    """Strip an admonition's indentation from a fenced block's lines."""
    out = []
    for ln in lines:
        if ln.startswith(indent):
            out.append(ln[len(indent):])
        else:
            out.append(ln if ln.strip() else "")
    return "\n".join(out) + "\n"


def parse_page(path: Path) -> list[dict[str, Any]]:
    """Return one record per ```ssl fence in ``path``."""
    lines = path.read_text(encoding="utf-8").split("\n")
    rel_content = path.relative_to(CONTENT).as_posix()
    rel_repo = path.relative_to(REPO_ROOT).as_posix()

    records: list[dict[str, Any]] = []
    section: str | None = None
    heading: str | None = None
    open_record: dict[str, Any] | None = None  # ssl record still collecting output
    prose: list[str] = []  # prose lines since the last ssl fence
    in_frontmatter = bool(lines) and lines[0] == "---"

    i = 0
    while i < len(lines):
        line = lines[i]
        if in_frontmatter:
            if i > 0 and line == "---":
                in_frontmatter = False
            i += 1
            continue

        fence = FENCE.match(line)
        if fence:
            indent, lang = fence.group(1), fence.group(2).lower()
            j = i + 1
            while j < len(lines) and not re.match(rf"^{re.escape(indent)}```[ \t]*$", lines[j]):
                j += 1
            body = dedent(lines[i + 1:j], indent)
            if lang == "ssl":
                n = len(records) + 1
                procedures = PROC_DEF.findall(scan_ssl(body)[0])
                kind = classify_kind(body, section, heading)
                deps = dependencies(body, procedures)
                record = {
                    "id": f"{rel_content}#{n}",
                    "page": rel_repo,
                    "line": i + 1,
                    "heading": heading,
                    "section": section,
                    "kind": kind,
                    "procedures": procedures,
                    "entry": statements_after_last_endproc(body),
                    "expected_output": None,
                    "expected_prose": None,
                    "expected_alternatives": [],
                    "depends": deps,
                    "runnable": classify_runnable(kind, deps),
                    "source": body,
                }
                records.append(record)
                open_record = record
                prose = []
            elif lang == "text" and open_record is not None:
                if open_record["expected_output"] is None:
                    said = next((p for p in reversed(prose) if p.strip()), "")
                    if any(EXPECT_PROSE.search(p) for p in prose):
                        open_record["expected_output"] = body.rstrip("\n")
                        open_record["expected_prose"] = said.strip()
                    else:
                        open_record = None
                elif any(EXPECT_PROSE.search(p) or re.match(r"\s*or\b", p, re.I) for p in prose):
                    open_record["expected_alternatives"].append(body.rstrip("\n"))
                prose = []
            i = j + 1
            continue

        head = HEADING.match(line)
        if head:
            level, title = len(head.group(1)), head.group(2)
            if level == 2:
                section = heading = title
            elif level == 3:
                heading = title
            open_record = None
            prose = []
        elif line.strip():
            prose.append(line)
        i += 1
    return records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)

    records: list[dict[str, Any]] = []
    for path in sorted(CONTENT.rglob("*.md")):
        records.extend(parse_page(path))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    kinds = ["procedure", "class", "syntax", "fragment"]
    runnables = ["pure", "db", "helper", "class", "external", "not-runnable"]
    table = Counter((r["kind"], r["runnable"]) for r in records)
    width = max(len(k) for k in kinds + ["kind", "total"])
    print(f"{len(records)} ```ssl examples -> {args.output.relative_to(REPO_ROOT) if args.output.is_relative_to(REPO_ROOT) else args.output}")
    print()
    header = f"{'kind':<{width}} " + " ".join(f"{r:>12}" for r in runnables) + f" {'total':>7}"
    print(header)
    print("-" * len(header))
    for k in kinds:
        row = [table[(k, r)] for r in runnables]
        print(f"{k:<{width}} " + " ".join(f"{c:>12}" for c in row) + f" {sum(row):>7}")
    totals = [sum(table[(k, r)] for k in kinds) for r in runnables]
    print("-" * len(header))
    print(f"{'total':<{width}} " + " ".join(f"{c:>12}" for c in totals) + f" {sum(totals):>7}")
    with_output = sum(1 for r in records if r["expected_output"] is not None)
    print()
    print(f"{with_output} examples carry expected output.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
