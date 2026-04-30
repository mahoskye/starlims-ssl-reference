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
