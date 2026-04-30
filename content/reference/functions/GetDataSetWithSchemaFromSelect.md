---
title: "GetDataSetWithSchemaFromSelect"
summary: "Executes a SQL query and returns the result as XML dataset text with schema always included."
id: ssl.function.getdatasetwithschemafromselect
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetDataSetWithSchemaFromSelect

Executes a SQL query and returns the result as XML dataset text with schema always included.

`GetDataSetWithSchemaFromSelect` is a narrow convenience wrapper around the
same XML-export path used by [`GetDataSetEx`](GetDataSetEx.md). It always
includes both the XML header and the XML schema, and it accepts an optional
connection name plus an optional positional values array for `?`
placeholders in the SQL text.

`aPrimaryKeys` and `aUniqueConstraints` are accepted in the signature but have no effect on the returned XML output.

## When to use

- When you need XML dataset output and schema must always be included.
- When you want the simpler fixed-schema form instead of the more configurable [`GetDataSetEx`](GetDataSetEx.md).
- When you need to run the query against a specific configured connection.
- When your query uses positional `?` placeholders with an explicit values array.

## Syntax

```ssl
GetDataSetWithSchemaFromSelect(sCommandString, [sConnectionName], [aValues], [aPrimaryKeys], [aUniqueConstraints])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCommandString` | [string](../types/string.md) | yes | — | SQL command text to execute. |
| `sConnectionName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Database connection name to run the command against. When [`NIL`](../literals/nil.md), the current default connection is used. |
| `aValues` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Positional values for `?` placeholders in `sCommandString`. Omit when the query has no parameters. |
| `aPrimaryKeys` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Accepted by the function signature, but currently ignored by the implementation. |
| `aUniqueConstraints` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Accepted by the function signature, but currently ignored by the implementation. |

## Returns

**[string](../types/string.md)** — XML dataset output for the query result, with the XML header and schema both included.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sCommandString` is [`NIL`](../literals/nil.md). | `The command string is null.` |
| `aValues` is multi-dimensional. | `The current array has more than 1 dimension.` |
| The query contains more `?` placeholders than supplied values. | `Parameters count mismatch` |
| The database engine name cannot be determined for the chosen connection. | `Cannot determine the database engine name.` |
| The supplied connection name is not configured. | `The provider name: {sConnectionName} not found.` |
| The database collection is unavailable. | `The internal database collection is null` |

## Best practices

!!! success "Do"
    - Use positional `?` placeholders with `aValues` for dynamic values.
    - Omit `aValues` entirely when the query has no parameters.
    - Pass an explicit `sConnectionName` when the query must run against a non-default connection.
    - Use [`GetDataSetEx`](GetDataSetEx.md) instead when you need control over header, schema, table name, null handling, or invariant date columns.

!!! failure "Don't"
    - Use `?varName?` syntax with `GetDataSetWithSchemaFromSelect`. That substitution style is for [`SQLExecute`](SQLExecute.md).
    - Pass a nested array in `aValues`. The function expects a single-dimensional values array.
    - Rely on `aPrimaryKeys` or `aUniqueConstraints` to shape the returned XML. Those arguments have no effect.
    - Choose this function when you need to suppress the XML header or schema. This function always includes both.

## Caveats

- Large result sets can produce very large XML strings and corresponding memory cost.

## Examples

### Export a query result with schema on the default connection

Executes a parameterless query on the default connection and reports the length of the returned XML string, which always includes both the XML header and schema.

```ssl
:PROCEDURE ExportActiveSamples;
	:DECLARE sSql, sXml;

	sSql := "
	    SELECT sample_id, sample_name, status
	    FROM sample
	    WHERE status = 'A'
	    ORDER BY sample_id
	";

	sXml := GetDataSetWithSchemaFromSelect(sSql);

	UsrMes("Returned XML length: " + LimsString(Len(sXml)));

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("ExportActiveSamples");
```

[`UsrMes`](UsrMes.md) displays:

```text
Returned XML length: 2187
```

### Query a named connection with positional parameters

Filters by both status and received date using two `?` placeholders, targeting a named connection rather than the default.

```ssl
:PROCEDURE ExportSamplesByStatus;
	:PARAMETERS sStatus;
	:DEFAULT sStatus, "A";
	:DECLARE sSql, sXml, sConnection, aValues;

	sConnection := "REPORTING";
	sSql := "
	    SELECT sample_id, sample_name, status, received_date
	    FROM sample
	    WHERE status = ?
	      AND received_date >= ?
	    ORDER BY received_date DESC
	";

	aValues := {sStatus, CToD("01/01/2024")};
	sXml := GetDataSetWithSchemaFromSelect(sSql, sConnection, aValues);

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("ExportSamplesByStatus", {"PENDING"});
```

## Related

- [`GetDataSet`](GetDataSet.md)
- [`GetDataSetEx`](GetDataSetEx.md)
- [`GetDataSetXMLFromSelect`](GetDataSetXMLFromSelect.md)
- [`GetNETDataSet`](GetNETDataSet.md)
- [`GetSSLDataset`](GetSSLDataset.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
