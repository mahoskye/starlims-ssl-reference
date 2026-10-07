---
title: "AddColDelimiters"
summary: "Qualify each column in an array as table.column with database-specific identifier delimiters."
id: ssl.function.addcoldelimiters
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# AddColDelimiters

Qualify each column in an array as `table.column` with database-specific identifier delimiters.

AddColDelimiters updates `aCols` in place. For each element, it builds a value in the form `table.column`, wrapping both parts with the delimiter characters for the database identified by `sDSN`.

If `sDSN` is [`NIL`](../literals/nil.md), the function uses empty delimiters. If `aCols` is [`NIL`](../literals/nil.md) or `sTable` is [`NIL`](../literals/nil.md), the function leaves the array unchanged and returns no value. The function trims `sTable` before building the qualified names.

!!! warning "Not callable from SSL"
    On STARLIMS v11, every call to `AddColDelimiters` from SSL code fails to compile with `Compile-time error: … Invalid prototype for built-in function: AddColDelimiters`, whatever arguments are passed. Sixteen argument shapes were tested, from no arguments to four. Build qualified names with [`AddNameDelimiters`](AddNameDelimiters.md) instead, as in the example below.

## When to use

- Not from SSL code: calls are rejected at compile time. To qualify columns for a specific database, apply [`AddNameDelimiters`](AddNameDelimiters.md) to the table and to each column name.

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

## Exceptions

| Trigger | Exception message |
| --- | --- |
| Any call from SSL code, with any arguments. | `Compile-time error: <line>:<column> Invalid prototype for built-in function: AddColDelimiters` |

## Best practices

!!! success "Do"
    - Qualify column names with [`AddNameDelimiters`](AddNameDelimiters.md), applied to the table name and to each column name.
    - Pass the same connection name the SQL will use, so the delimiter style matches the target database.

!!! failure "Don't"
    - Call `AddColDelimiters` from SSL code. It does not compile.
    - Hardcode brackets or quotes when the connection can vary by database.

## Examples

### Qualify a list of columns with AddNameDelimiters

Builds `table.column` names for a SELECT list by delimiting the table name and each column name with [`AddNameDelimiters`](AddNameDelimiters.md), then joins them with [`BuildString`](BuildString.md).

```ssl
:PROCEDURE QualifyColumns;
    :PARAMETERS sDSN, sTable, aCols;
    :DECLARE aQualified, sPrefix, nIndex;

    aQualified := {};
    sPrefix := AddNameDelimiters(sDSN, sTable) + ".";

    :FOR nIndex := 1 :TO ALen(aCols);
        AAdd(aQualified, sPrefix + AddNameDelimiters(sDSN, aCols[nIndex]));
    :NEXT;

    UsrMes(BuildString(aQualified, 1, ALen(aQualified), ", "));

    :RETURN aQualified;
:ENDPROC;

/* Usage;
DoProc("QualifyColumns", {"DATABASE", "sample", {"sample_id", "status"}});
```

On SQL Server, [`UsrMes`](UsrMes.md) logs:

```text
[sample].[sample_id], [sample].[status]
```

## Related

- [`AddNameDelimiters`](AddNameDelimiters.md)
- [`GetNoLock`](GetNoLock.md)
- [`GetRdbmsDelimiter`](GetRdbmsDelimiter.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
