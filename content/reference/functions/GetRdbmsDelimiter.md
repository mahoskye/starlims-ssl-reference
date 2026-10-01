---
title: "GetRdbmsDelimiter"
summary: "Returns the identifier delimiter character for the database behind a DSN."
id: ssl.function.getrdbmsdelimiter
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetRdbmsDelimiter

Returns the identifier delimiter character for the database behind a DSN.

`GetRdbmsDelimiter` maps a DSN to the delimiter character used for quoted identifiers. For SQL Server and Sybase, it returns `[` for opening delimiters and `]` for closing delimiters. For Oracle and DB2, it always returns `"` because the same character is used on both sides. If the DSN does not resolve to one of those database types, the function returns an empty string.

If `sDSN` is [`NIL`](../literals/nil.md), SSL converts it to an empty string before the lookup. A non-empty `sDSN` must name a database connection configured in your environment, such as the default `DATABASE` connection. Any other name raises an error. The function returns a string value and does not modify its inputs.

## When to use

- When building SQL or metadata strings that must adapt to the target database.
- When you need the delimiter character itself instead of a helper that wraps a whole identifier for you.
- When the same code may run against SQL Server, Sybase, Oracle, or DB2.
- When you need to build opening and closing delimiters separately.

## Syntax

```ssl
GetRdbmsDelimiter([sDSN], bOpen)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sDSN` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Name of the database connection whose platform determines the delimiter, such as `"DATABASE"`. A name that is not a configured connection raises an error. |
| `bOpen` | [boolean](../types/boolean.md) | yes | — | When [`.T.`](../literals/true.md), returns the opening delimiter. When [`.F.`](../literals/false.md), returns the closing delimiter. |

## Returns

**[string](../types/string.md)** — One delimiter character, or an empty string when no supported mapping is found.

Behavior by database type:

| Database type | `bOpen` = [`.T.`](../literals/true.md) | `bOpen` = [`.F.`](../literals/false.md) |
|---------------|------------------|-----------------|
| SQL Server | `[` | `]` |
| SYBASE | `[` | `]` |
| ORACLE | `"` | `"` |
| DB2 | `"` | `"` |
| Other | `""` | `""` |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDSN` is not empty and does not name a configured database connection. | `The provider name: <sDSN> not found.` |

## Best practices

!!! success "Do"
    - Pass the name of the connection where the SQL will run, such as `"DATABASE"` for the default connection.
    - Call the function twice when you need separate opening and closing delimiters.
    - Handle the empty-string result explicitly when the DSN may point to an unsupported platform.
    - Use [`AddNameDelimiters`](AddNameDelimiters.md) or [`AddColDelimiters`](AddColDelimiters.md) when those higher-level helpers already fit your task.

!!! failure "Don't"
    - Hardcode `[` `]` or `"` when the same logic may run against more than one database platform.
    - Ignore `bOpen`. It matters for SQL Server and Sybase, where opening and closing delimiters are different.
    - Assume every DSN produces a delimiter. Unsupported mappings return an empty string.
    - Pass a connection name that is not configured in your environment. That raises `The provider name: <sDSN> not found.`
    - Use this helper when you actually need a fully wrapped identifier; reach for [`AddNameDelimiters`](AddNameDelimiters.md) instead.

## Caveats

- The function returns only the delimiter character. You must still place it correctly around the identifier.

## Examples

### Wrap an identifier with platform-specific delimiters

Retrieves the opening and closing delimiter characters for the given DSN and wraps a single identifier name, demonstrating the two-call pattern for platforms where the delimiters differ. The usage passes the default `DATABASE` connection. Replace it with the name of the connection your SQL runs on.

```ssl
:PROCEDURE BuildDelimitedIdentifier;
	:PARAMETERS sDSN, sName;
	:DECLARE sOpen, sClose, sIdentifier;

	sOpen := GetRdbmsDelimiter(sDSN, .T.);
	sClose := GetRdbmsDelimiter(sDSN, .F.);
	sIdentifier := sOpen + sName + sClose;

	UsrMes("Delimited identifier: " + sIdentifier);
:ENDPROC;

/* Usage;
DoProc("BuildDelimitedIdentifier", {"DATABASE", "orders"});
```

[`UsrMes`](UsrMes.md) logs, for a SQL Server connection:

```text
Delimited identifier: [orders]
```

### Build a provider-specific SELECT statement

Guards against an unsupported DSN by checking for an empty delimiter before building the query, then assembles a `SELECT` statement where both the table name and column name are quoted with platform-specific delimiters.

```ssl
:PROCEDURE BuildSelectStatement;
	:PARAMETERS sDSN;
	:DECLARE sOpen, sClose, sTable, sColumn, sSQL;

	sOpen := GetRdbmsDelimiter(sDSN, .T.);
	sClose := GetRdbmsDelimiter(sDSN, .F.);

	:IF Empty(sOpen) .OR. Empty(sClose);
		UsrMes("No delimiter mapping is available for this DSN");
		:RETURN "";
	:ENDIF;

	sTable := sOpen + "orders" + sClose;
	sColumn := sOpen + "orderdate" + sClose;
	sSQL := "SELECT " + sColumn + " FROM " + sTable;

	UsrMes(sSQL);
	:RETURN sSQL;
:ENDPROC;

/* Usage;
DoProc("BuildSelectStatement", {"DATABASE"});
```

`UsrMes` logs one of:

```text
No delimiter mapping is available for this DSN
```

```text
SELECT [orderdate] FROM [orders]
```

## Related

- [`AddColDelimiters`](AddColDelimiters.md)
- [`AddNameDelimiters`](AddNameDelimiters.md)
- [`GetNoLock`](GetNoLock.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
