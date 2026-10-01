---
title: "AddNameDelimiters"
summary: "Wrap a name in database-specific delimiters."
id: ssl.function.addnamedelimiters
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# AddNameDelimiters

Wrap a name in database-specific delimiters.

AddNameDelimiters returns `sName` wrapped in the identifier delimiters used by the database identified by `sDSN`. If `sDSN` is [`NIL`](../literals/nil.md), it uses an empty string instead. If `sName` is [`NIL`](../literals/nil.md), it also uses an empty string.

Before adding delimiters, the function trims `sName`. If `sDSN` is empty, the function returns the trimmed name without any delimiter characters. A non-empty `sDSN` must name a database connection configured in your environment, such as the default `DATABASE` connection. Any other name raises an error.

The function always returns a string result. It does not modify its inputs.

## When to use

- When building SQL dynamically and identifier quoting must match the target
  database.
- When object names may need delimiters because of reserved words or special
  characters.
- When you want a single helper for identifier formatting instead of embedding delimiter characters in string literals.

## Syntax

```ssl
AddNameDelimiters(sDSN, sName)
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `sDSN` | [string](../types/string.md) | no | `""` | Name of the database connection whose delimiter rules apply, such as `"DATABASE"`. An empty value produces no delimiter characters. A name that is not a configured connection raises an error. |
| `sName` | [string](../types/string.md) | no | `""` | Identifier to wrap in database-specific delimiters. The function trims this value before wrapping it. |

## Returns

**[string](../types/string.md)** — Trimmed and delimited version of `sName`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDSN` is not empty and does not name a configured database connection. | `The provider name: <sDSN> not found.` |

## Best practices

!!! success "Do"
    - Use AddNameDelimiters for individual table, view, or column names.
    - Pass the name of the connection where the SQL will run, such as `"DATABASE"` for the default connection.
    - Use this together with [`AddColDelimiters`](AddColDelimiters.md) when you need both individual identifiers and qualified column arrays.
    - Pass the raw identifier value and let the function trim outer spaces before adding delimiters.

!!! failure "Don't"
    - Assume the same delimiter characters work for every database.
    - Expect this function to modify a variable in place. It returns a new string.
    - Pass [`NIL`](../literals/nil.md) and expect an error. The function falls back to empty strings for missing arguments.
    - Pass a connection name that is not configured in your environment. That raises `The provider name: <sDSN> not found.`

## Examples

### Build a SQL fragment with delimited identifiers

Calls `AddNameDelimiters` twice, once for the table name and once for the column, then joins the results into a SELECT statement. The example uses the default `DATABASE` connection. Replace it with the name of the connection your SQL runs on. The exact delimiters depend on that connection's database type.

```ssl
:PROCEDURE BuildSelectStatement;
	:DECLARE sTableName, sColumnName, sSQL;

	sTableName := AddNameDelimiters("DATABASE", "samples");
	sColumnName := AddNameDelimiters("DATABASE", "sample_id");

	sSQL := "SELECT " + sColumnName + " FROM " + sTableName;
	UsrMes(sSQL);
:ENDPROC;

/* Usage;
DoProc("BuildSelectStatement");
```

[`UsrMes`](UsrMes.md) logs, for a SQL Server connection:

```text
SELECT [sample_id] FROM [samples]
```

### Handle omitted values safely

Omits `sDSN` so that no delimiter characters are applied; the function returns the trimmed name unchanged.

```ssl
:PROCEDURE ShowDefaultDelimiterBehavior;
	:DECLARE sResult;

	sResult := AddNameDelimiters(, "status");

	UsrMes("Delimited name: " + sResult);
:ENDPROC;

/* Usage;
DoProc("ShowDefaultDelimiterBehavior");
```

[`UsrMes`](UsrMes.md) logs:

```text
Delimited name: status
```

## Related

- [`AddColDelimiters`](AddColDelimiters.md)
- [`BuildStringForIn`](BuildStringForIn.md)
- [`GetNoLock`](GetNoLock.md)
- [`GetRdbmsDelimiter`](GetRdbmsDelimiter.md)
- [`string`](../types/string.md)
