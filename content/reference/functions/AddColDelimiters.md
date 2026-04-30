---
title: "AddColDelimiters"
summary: "Qualify each column in an array as table.column with database-specific identifier delimiters."
id: ssl.function.addcoldelimiters
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# AddColDelimiters

Qualify each column in an array as `table.column` with database-specific identifier delimiters.

AddColDelimiters updates `aCols` in place. For each element, it builds a value in the form `table.column`, wrapping both parts with the delimiter characters for the database identified by `sDSN`.

If `sDSN` is [`NIL`](../literals/nil.md), the function uses empty delimiters. If `aCols` is [`NIL`](../literals/nil.md) or `sTable` is [`NIL`](../literals/nil.md), the function leaves the array unchanged and returns no value. The function trims `sTable` before building the qualified names.

## When to use

- When you need an existing array of column names converted to qualified `table.column` names.
- When SQL must adapt to the identifier delimiter rules of the target database.
- When you want to prepare a column array in place before building a SELECT list or export query.

## Syntax

```ssl
AddColDelimiters(sDSN, aCols, sTable)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sDSN` | [string](../types/string.md) | no | `""` | Data source name used to determine delimiter rules. |
| `aCols` | [array](../types/array.md) | yes | — | Array of column names to update in place. Each element is replaced with a qualified name. |
| `sTable` | [string](../types/string.md) | yes | — | Table name used to qualify each column. The function trims this value before using it. |

## Returns

**none** — No return value. The function updates `aCols` directly.

## Best practices

!!! success "Do"
    - Call `AddColDelimiters` before joining `aCols` into a SELECT list or export statement.
    - Pass the same DSN the SQL will use so the delimiter style matches the target database.
    - Copy the array first if you need to keep the original unqualified column names.
    - Use [`AddNameDelimiters`](AddNameDelimiters.md) when you need to delimit one identifier instead of an entire column array.

!!! failure "Don't"
    - Expect a new array back. The existing `aCols` array is modified in place.
    - Pass [`NIL`](../literals/nil.md) for `aCols` or `sTable` and expect partial output. The function does nothing in that case.
    - Hardcode brackets or quotes when the DSN can vary by database.
    - Assume the function trims column names. It uses each column value as provided.

## Examples

### Qualify a list of columns

Adds table qualification and database-specific delimiters to each column name in place. The exact delimiter characters depend on the DBMS type for the given DSN (for example, `[` and `]` for SQL Server).

```ssl
:PROCEDURE BuildQualifiedColumns;
	:DECLARE aColumns, nIndex;

	aColumns := {"sample_id", "sample_name", "status"};

	AddColDelimiters("LIMS", aColumns, "samples");

	:FOR nIndex := 1 :TO ALen(aColumns);
		UsrMes(aColumns[nIndex]);
	:NEXT;
:ENDPROC;

/* Usage;
DoProc("BuildQualifiedColumns");
```

[`UsrMes`](UsrMes.md) displays (SQL Server example):

```text
[samples].[sample_id]
[samples].[sample_name]
[samples].[status]
```

### Prepare columns before joining them into SQL

Qualifies the column array in place, then joins the result into a SELECT list using [`BuildString`](BuildString.md).

```ssl
:PROCEDURE BuildSelectList;
	:DECLARE aColumns, sSelectList;

	aColumns := {"sample_id", "analysis_date", "status_code"};

	AddColDelimiters("LIMS", aColumns, "samples");

	sSelectList := BuildString(aColumns,,, ", ");

	UsrMes("SELECT " + sSelectList + " FROM samples");
:ENDPROC;

/* Usage;
DoProc("BuildSelectList");
```

[`UsrMes`](UsrMes.md) displays (SQL Server example):

```text
SELECT [samples].[sample_id], [samples].[analysis_date], [samples].[status_code] FROM samples
```

### Qualify columns without database-specific wrappers

Passes [`NIL`](../literals/nil.md) for `sDSN` so that no delimiter characters are added and the result uses plain `table.column` notation.

```ssl
:PROCEDURE BuildPlainQualifiedColumns;
	:DECLARE aColumns, nIndex;

	aColumns := {"sample_id", "result_value"};

	AddColDelimiters(, aColumns, "results");

	:FOR nIndex := 1 :TO ALen(aColumns);
		UsrMes(aColumns[nIndex]);
	:NEXT;
:ENDPROC;

/* Usage;
DoProc("BuildPlainQualifiedColumns");
```

[`UsrMes`](UsrMes.md) displays:

```text
results.sample_id
results.result_value
```

## Related

- [`AddNameDelimiters`](AddNameDelimiters.md)
- [`GetNoLock`](GetNoLock.md)
- [`GetRdbmsDelimiter`](GetRdbmsDelimiter.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
