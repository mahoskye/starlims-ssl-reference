---
title: "GetDataSetXMLFromSelect"
summary: "Executes a SQL query and returns the result as XML dataset text."
id: ssl.function.getdatasetxmlfromselect
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetDataSetXMLFromSelect

Executes a SQL query and returns the result as XML dataset text.

`GetDataSetXMLFromSelect` is the configurable XML-export form behind
[`GetDataSet`](GetDataSet.md) and related helpers. It runs the SQL against a
database connection, applies positional `?` parameter values when supplied, and
serializes the returned dataset as XML.

When omitted, `sConnectionName` falls back to the current default connection, `bIncludeHeader` defaults to [`.T.`](../literals/true.md), `bIncludeSchema` defaults to [`.F.`](../literals/false.md), and `bNullAsBlank` defaults to [`.T.`](../literals/true.md). If `sTableName` is omitted, the runtime tries to derive a table name from the SQL text and falls back to `Table`.

Use positional `?` placeholders with `aValues`. This function does not support `?varName?` substitution.

## When to use

- When you need XML dataset output and want direct control over header and
  schema inclusion.
- When you need to run the query against a specific configured connection.
- When downstream code expects XML text instead of an [`SSLDataset`](../classes/SSLDataset.md) or another dataset object form.
- When you need to control dataset table naming, null handling, or invariant
  date columns.

## Syntax

```ssl
GetDataSetXMLFromSelect(sCommandString, [sConnectionName], [bIncludeHeader], [aValues], [bIncludeSchema], [sTableName], [bNullAsBlank], [aInvariantDateCols])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCommandString` | [string](../types/string.md) | yes | — | SQL command text to execute. |
| `sConnectionName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Database connection name to run the command against. When [`NIL`](../literals/nil.md), the current default connection is used. |
| `bIncludeHeader` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Whether to include the XML declaration/header in the returned string. |
| `aValues` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Positional values for `?` placeholders in `sCommandString`. Omit when the query has no parameters. |
| `bIncludeSchema` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Whether to include XML schema information in the returned string. |
| `sTableName` | [string](../types/string.md) | no | derived from query, else `Table` | Table name to assign to the first dataset table in the XML. |
| `bNullAsBlank` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Whether database nulls should be emitted as blank values in the XML output. |
| `aInvariantDateCols` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Array of 1-based numeric column indexes to treat as invariant-date columns. |

## Returns

**[string](../types/string.md)** — XML dataset output for the query result.

If `bIncludeHeader` is [`.F.`](../literals/false.md), the function returns the XML body without the XML declaration. If `bIncludeSchema` is [`.T.`](../literals/true.md), the returned XML includes schema information.

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
    - Pass an explicit `sConnectionName` when the query must run against a non-default connection.
    - Set `bIncludeHeader` and `bIncludeSchema` explicitly when another system depends on a specific XML shape.
    - Use numeric 1-based column indexes in `aInvariantDateCols`.

!!! failure "Don't"
    - Use `?varName?` syntax with `GetDataSetXMLFromSelect`. That substitution style is for [`SQLExecute`](SQLExecute.md).
    - Pass a nested array in `aValues`. The function expects a single-dimensional values array.
    - Treat `sConnectionName` as a display label for the XML. It is the database connection name.
    - Assume schema is included by default. This function defaults `bIncludeSchema` to [`.F.`](../literals/false.md).

## Caveats

- Large result sets can produce very large XML strings and corresponding memory cost.

## Examples

### Export query results as XML on the default connection

Executes a parameterless query on the default connection using all default output flags and reports the length of the returned XML string.

```ssl
:PROCEDURE ExportActiveSamples;
	:DECLARE sSql, sXml;

	sSql := "
	    SELECT sample_id, sample_name, status
	    FROM sample
	    WHERE status = 'A'
	    ORDER BY sample_id
	";

	sXml := GetDataSetXMLFromSelect(sSql);

	UsrMes("Returned XML length: " + LimsString(Len(sXml)));

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("ExportActiveSamples");
```

[`UsrMes`](UsrMes.md) displays:

```text
Returned XML length: 1243
```

### Query a named connection with parameters and schema

Passes a status parameter via a `?` placeholder to a named connection, with header and schema both enabled in the returned XML.

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
	    ORDER BY received_date DESC
	";

	aValues := {sStatus};
	sXml := GetDataSetXMLFromSelect(sSql, sConnection, .T., aValues, .T.);

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("ExportSamplesByStatus", {"PENDING"});
```

### Control table name, null handling, and invariant date columns

Suppresses the XML header, assigns a custom table name, enables null-as-blank, and marks two date columns as invariant. The example wraps the export in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) to report failures.

```ssl
:PROCEDURE ExportAuditFragment;
	:PARAMETERS dStartDate;
	:DEFAULT dStartDate, CToD("01/01/2024");
	:DECLARE sSql, sXml, sConnection, aValues, aInvariantDateCols, oErr;

	sConnection := "REPORTING";
	sSql := "
	    SELECT sample_id, sample_name, created_date, released_date
	    FROM sample
	    WHERE released_date >= ?
	    ORDER BY released_date
	";

	aValues := {dStartDate};
	aInvariantDateCols := {3, 4};

	:TRY;
		sXml := GetDataSetXMLFromSelect(sSql, sConnection, .F., aValues, .T.,
			"sample_audit", .T., aInvariantDateCols);
		:RETURN sXml;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("GetDataSetXMLFromSelect failed: " + oErr:Description);
		:RETURN "";
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ExportAuditFragment", {CToD("03/01/2024")});
```

`ErrorMes` displays on failure:

```text
GetDataSetXMLFromSelect failed: <database error description>
```

## Related

- [`GetDataSet`](GetDataSet.md)
- [`GetDataSetEx`](GetDataSetEx.md)
- [`GetDataSetWithSchemaFromSelect`](GetDataSetWithSchemaFromSelect.md)
- [`GetNETDataSet`](GetNETDataSet.md)
- [`GetSSLDataset`](GetSSLDataset.md)
- [`XmlExportSql`](XmlExportSql.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
- [`array`](../types/array.md)
