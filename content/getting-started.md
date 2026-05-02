# Getting Started with SSL

The **STARLIMS Scripting Language (SSL)** is the programming language used within the STARLIMS Laboratory Information Management System. This reference documents every function, class, keyword, operator, and type available to SSL developers.

## How to read this reference

Each element page follows a consistent structure:

- **Summary** — one-sentence purpose
- **Description** — detailed behavioral explanation with edge cases
- **Parameters** — name, type, required/optional, defaults
- **Returns** — type and description of the return value
- **Exceptions** — conditions that cause errors, with exact messages
- **Best practices** — do/don't guidance with rationale
- **Caveats** — gotchas and non-obvious behavior
- **Examples** — representative SSL code
- **Related** — links to related elements

## SSL basics

### Variables and declarations

```ssl
:DECLARE sName, nCount, aItems;
sName := "Sample-001";
nCount := 42;
aItems := {"A", "B", "C"};
```

These are top-level statements — in a procedure body they would be indented.

### Control flow

```ssl
:IF nCount > 0;
    UsrMes("Processing " + LimsString(nCount) + " items");
:ELSE;
    UsrMes("No items to process");
:ENDIF;
:FOR nIndex := 1 :TO ALen(aItems);
    UsrMes(aItems[nIndex]);
:NEXT;
```

### Error handling

```ssl
:DECLARE oResult;
:TRY;
    oResult := RunSQL("SELECT * FROM samples");
:CATCH;
    UsrMes("Query failed: " + GetLastSSLError():Description);
:FINALLY;
    EndLimsTransaction();
:ENDTRY;
```

### Procedures

```ssl
:PROCEDURE CalculateAverage;
    :PARAMETERS aValues;
    :DECLARE nSum, nIndex;
    nSum := 0;
    :FOR nIndex := 1 :TO ALen(aValues);
        nSum := nSum + aValues[nIndex];
    :NEXT;
    :RETURN nSum / ALen(aValues);
:ENDPROC;
```

## Key language rules

A few rules are non-obvious and worth internalizing before writing any SSL.

### Case sensitivity

- **Colon-prefixed keywords** (`:IF`, `:PROCEDURE`, `:TRY`, ...) are **case-sensitive** and must be UPPERCASE.
- **Identifiers and built-in function names** are case-insensitive — `sMyVar` is the same as `SMYVAR`.
- **Literals and class-context forms** ([`NIL`](reference/literals/nil.md), [`.T.`](reference/literals/true.md), [`.F.`](reference/literals/false.md), `Me`, `Base`, `Constructor`) are case-insensitive.

### Semicolons in comments

Almost every statement, including comments, must end with `;`. Comments use `/* ...;` and **terminate at the first `;`**. Embedding a semicolon inside comment text closes the comment early — the remaining text becomes executable code.

```ssl
/* Don't do this; the rest after the colon becomes code;
/* Safe — no semicolons inside the comment text;
```

### Declaration ordering

[`:PARAMETERS`](reference/keywords/PARAMETERS.md) must appear before any other statements in a script or procedure body, and [`:DEFAULT`](reference/keywords/DEFAULT.md) must immediately follow it. [`:INCLUDE`](reference/keywords/INCLUDE.md) is a lexer-level textual inclusion and should appear early. [`:DECLARE`](reference/keywords/DECLARE.md) and [`:PUBLIC`](reference/keywords/PUBLIC.md) can appear anywhere. Recommended order: `:PARAMETERS`, `:DEFAULT`, `:INCLUDE`, `:PUBLIC`, `:DECLARE`. Use one statement per line.

Do not put `:DEFAULT` on the same line as `:DECLARE`.

### Calling procedures

Custom SSL procedures **cannot** be called with bare `Name()` syntax. Use:

- [`DoProc`](reference/functions/DoProc.md)`("ProcName", {args})` — call a procedure in the **same** file.
- [`ExecFunction`](reference/functions/ExecFunction.md)`("Category.Script", {args})` — call another script's entry point.
- [`ExecFunction`](reference/functions/ExecFunction.md)`("Category.Script.ProcName", {args})` — call a specific procedure in another file.

Inside a [`:CLASS`](reference/keywords/CLASS.md), use `Me:Method()` and `Base:Method()` for sibling and inherited calls. `DoProc` is a compile-time error inside class methods.

Built-in functions (e.g., [`Len`](reference/functions/Len.md), [`ALen`](reference/functions/ALen.md)) are called directly with normal syntax. Omit trailing optional parameters rather than passing empty values: `GetDataSet(sQuery)` not `GetDataSet(sQuery, {})`. For skipped middle parameters, use adjacent commas: `DoProc("MyProc", {p1,,p3})`.

### Built-in vs user-defined classes

- **Built-in classes** instantiate with curly braces only: `Email{}`, `SSLDataset{}`. They cannot be created via `CreateUdObject`.
- **User-defined classes** (`:CLASS` files) instantiate via [`CreateUdObject`](reference/functions/CreateUdObject.md)`("ClassName")` or `CreateUdObject("ClassName", {args})`.
- `CreateUdObject()` with no argument creates an empty dynamic object (`SSLExpando`).

### Case fall-through

[`:BEGINCASE`](reference/keywords/BEGINCASE.md) is not a value-matching switch — each [`:CASE`](reference/keywords/CASE.md) evaluates its own boolean. Without [`:EXITCASE;`](reference/keywords/EXITCASE.md), later `:CASE` expressions are still evaluated and additional matching bodies may execute. End each `:CASE` and `:OTHERWISE` block with `:EXITCASE;` unless multi-match behavior is intentional.

### String equality

The [`=`](reference/operators/equals.md) operator on strings does **prefix matching**: `"abcdef" = "abc"` is `.T.`. Use [`==`](reference/operators/strict-equals.md) for exact equality, or [`$`](reference/operators/dollar.md) for containment. See the [Type System guide](guides/type-system.md) for the full table.

## Core types

| Type | Example | Description |
|------|---------|-------------|
| [`number`](reference/types/number.md) | `42`, `3.14` | Integer and decimal values |
| [`string`](reference/types/string.md) | `"hello"` | Text sequences, 1-based indexing |
| [`boolean`](reference/types/boolean.md) | [`.T.`](reference/literals/true.md), [`.F.`](reference/literals/false.md) | True/false values |
| [`date`](reference/types/date.md) | [`Today()`](reference/functions/Today.md) | Calendar dates |
| [`array`](reference/types/array.md) | `{1, 2, 3}` | Ordered collections, 1-based indexing |
| [`object`](reference/types/object.md) | [`CreateLocal()`](reference/functions/CreateLocal.md) | Dynamic property bags |
| [`NIL`](reference/literals/nil.md) | [`NIL`](reference/literals/nil.md) | Absence of value |

## Next steps

- Browse the [API Reference](reference/index.md) for specific elements
- Read the [Type System](guides/type-system.md) guide for coercion rules
- See [Error Handling](guides/error-handling.md) for exception patterns
- Review [Naming Conventions](guides/naming-conventions.md) for Hungarian prefixes and casing
- Read [Data Source Files](guides/data-sources.md) if you write SSL or SQL data sources
