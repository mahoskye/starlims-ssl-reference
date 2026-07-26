# SSL Reference

An unofficial reference for the **STARLIMS Scripting Language (SSL)** as implemented in **STARLIMS version 11** — functions, classes, keywords, operators, types, and language constructs, with behavior notes and code examples.

## What's here

| Section | Count | Description |
|---------|-------|-------------|
| [Functions](reference/functions/index.md) | 330 | Built-in functions for strings, arrays, dates, database, files, and more |
| [Classes](reference/classes/index.md) | 29 | Object types for data tables, dictionaries, regex, email, and system services |
| [Obtained Objects](reference/returns/index.md) | 12 | Objects you obtain from another call rather than construct — the HTTP/SOAP client cluster and endpoint runtime objects |
| [Keywords](reference/keywords/index.md) | 38 | Language keywords for control flow, declarations, and error handling |
| [Operators](reference/operators/index.md) | 32 | Arithmetic, comparison, logical, bitwise, and assignment operators |
| [Types](reference/types/index.md) | 8 | Core SSL types: number, string, boolean, date, array, object, codeblock, netobject |
| [Literals](reference/literals/index.md) | 3 | Boolean and null literals: [`.T.`](reference/literals/true.md), [`.F.`](reference/literals/false.md), [`NIL`](reference/literals/nil.md) |
| [Special Forms](reference/special-forms/index.md) | 8 | Language constructs: constructor, `Base:`, `Me:`, code blocks, access modifiers, code organization, and the `Request`/`Response` endpoint objects |

## Guides

- [Getting Started](getting-started.md) — orientation for new SSL developers
- [Type System](guides/type-system.md) — types, coercion rules, and null semantics
- [Error Handling](guides/error-handling.md) — structured and legacy error handling patterns
- [Working with SQL](guides/sql-queries.md) — parameterized queries, IN clauses, and choosing the right SQL function
- [SQL & Transactions](guides/sql-transactions.md) — transaction control, nesting, isolation levels, and error handling
- [Naming Conventions](guides/naming-conventions.md) — Hungarian prefixes, casing rules, and constants
- [Data Source Files](guides/data-sources.md) — SSL and SQL data source syntax and directives

## About this reference

Element pages document parameters, return types, known exception messages, do/don't guidance, and code examples — the exact sections vary by category.

This site is **unofficial** and was drafted with the help of AI tools from the maintainer's working notes, then reviewed. It aims to be useful to SSL developers working in STARLIMS v11 environments, but it will contain mistakes — when a page disagrees with what your system does, trust your system and [report the difference](https://github.com/mahoskye/starlims-ssl-reference/issues). See [About This Reference](about.md) for provenance, version scope, and license details.
