# Getting Started with SSL

The **STARLIMS Scripting Language (SSL)** is the programming language used within the STARLIMS Laboratory Information Management System. This reference documents the functions, classes, keywords, operators, and types available to SSL developers.

## Where SSL code lives and how it runs

SSL is STARLIMS's server-side language — the code that does the heavy lifting behind forms, endpoints, and scheduled work. It is a proprietary language in the xBase family (similar in style to FoxPro), and it runs on STARLIMS's .NET-based application server. That .NET foundation shows through in places: built-in values expose .NET members such as `:ToString()` (see the [type pages](reference/types/index.md)), and several functions exist specifically for .NET interop.

### Code is stored in the dictionary, not files

SSL code is not kept as script files on disk — everything lives in the STARLIMS **dictionary database**. The **Designer**, STARLIMS's IDE, loads code from the dictionary and presents it for editing. You will most often find SSL in four places:

- **Application Server Scripts** — server code belonging to a specific application
- **Global Server Scripts** — shared server code, organized into categories
- **Application Data Sources** and **Global Data Sources** — data-retrieval code written in SSL, or in SQL with access to some SSL-like objects (see [Data Source Files](guides/data-sources.md))

Because code lives in the dictionary, moving it between systems goes through the **package manager**, which exports code as packages. Many developers also copy a script into an external editor to work on it, then paste it back into Designer.

### Running a script and seeing output

From Designer you can execute a server script directly — the quickest feedback loop while learning. In a real system, the same scripts are invoked from forms, client scripts, endpoints, or other scripts.

Two output channels matter:

- **Return values** — when a script ends with [`:RETURN`](reference/keywords/RETURN.md), the returned value appears in the **console pane** below the code workspace.
- **Messages and errors** — [`UsrMes`](reference/functions/UsrMes.md), [`InfoMes`](reference/functions/InfoMes.md), [`ErrorMes`](reference/functions/ErrorMes.md), and runtime errors are written to the **server log files**, which are physical files on the application server. In Designer, open the console pane's **Server Logs** tab and select your user name to view your log. You can refresh the view, and you can delete a log file when it gets too big — but a deleted log cannot be recovered.

A first script to try:

```ssl
:DECLARE sWho;
sWho := MYUSERNAME;
UsrMes("Hello from " + sWho);
:RETURN "Ran as " + sWho;
```

Run it in Designer: the `:RETURN` value shows in the console pane, and the `UsrMes` line lands in the server log under your user name.

### System-provided variables

The runtime predefines some global variables. The one used throughout this reference is `MYUSERNAME` — a string holding the current user's username. Deployments may expose other predefined globals; this reference only relies on what has been verified.

### How scripts address each other

Server code is addressed with a dotted path of two or three segments — `First.Script` or `First.Script.Procedure`. The first segment names one of two trees in Designer:

- A **server-script category** — a directory under the Server Scripts tab. A script `Auth` in category `API_HELPERS` is addressed as `API_HELPERS.Auth`; its procedure `CheckSession` as `API_HELPERS.Auth.CheckSession`.
- An **application** — applications live under an application category and contain their own forms, client scripts, server scripts, and data sources. A server script `SomeServerScript` in application `BBUDDLE` is addressed as `BBUDDLE.SomeServerScript`, or `BBUDDLE.SomeServerScript.Helper` for a specific procedure.

The second segment is the script name; the optional third segment is a procedure inside that script. This is the path form that [`ExecFunction`](reference/functions/ExecFunction.md) and three-segment [`DoProc`](reference/functions/DoProc.md) take — see [Calling procedures](#calling-procedures) below.

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
    UsrMes("Query attempt finished");
    /* :FINALLY runs whether the query succeeded or failed;
:ENDTRY;
```

If the work inside `:TRY` opens a transaction, close it in `:FINALLY` guarded with `IsInTransaction()` — see [SQL Transactions](guides/sql-transactions.md) for the full pattern.

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

[`:PARAMETERS`](reference/keywords/PARAMETERS.md) must appear before any other statements in a script or procedure body, and [`:DEFAULT`](reference/keywords/DEFAULT.md) must immediately follow it. [`:INCLUDE`](reference/keywords/INCLUDE.md) textually inserts another script's contents before the code runs and should appear early. [`:DECLARE`](reference/keywords/DECLARE.md) and [`:PUBLIC`](reference/keywords/PUBLIC.md) can appear anywhere. Recommended order: `:PARAMETERS`, `:DEFAULT`, `:INCLUDE`, `:PUBLIC`, `:DECLARE`. Use one statement per line.

Do not put `:DEFAULT` on the same line as `:DECLARE`.

### Calling procedures

Custom SSL procedures **cannot** be called with bare `Name()` syntax. Use:

- [`DoProc`](reference/functions/DoProc.md)`("ProcName", {args})` — call a procedure in the **same** file.
- [`ExecFunction`](reference/functions/ExecFunction.md)`("Category.Script", {args})` — call another script's entry point.
- [`ExecFunction`](reference/functions/ExecFunction.md)`("Category.Script.ProcName", {args})` — call a specific procedure in another file.

The dotted path is the addressing form described in [How scripts address each other](#how-scripts-address-each-other) — the first segment is a server-script category or an application name.

Inside a [`:CLASS`](reference/keywords/CLASS.md), use [`Me:`](reference/special-forms/me.md)`Method()` to call a method on the same object and [`Base:`](reference/special-forms/base.md)`Method()` to call the parent class's implementation. `DoProc` is a compile-time error inside class methods.

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

- Browse the [SSL Reference](reference/index.md) for specific elements
- Read the [Type System](guides/type-system.md) guide for coercion rules
- See [Error Handling](guides/error-handling.md) for exception patterns
- Review [Naming Conventions](guides/naming-conventions.md) for Hungarian prefixes and casing
- Read [Data Source Files](guides/data-sources.md) if you write SSL or SQL data sources
