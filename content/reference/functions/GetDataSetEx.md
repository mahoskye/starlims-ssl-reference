---
title: "GetDataSetEx"
summary: "Executes a SQL command on a specified connection and returns the result as XML dataset text."
id: ssl.function.getdatasetex
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetDataSetEx

Executes a SQL command on a specified connection and returns the result as XML dataset text.

`GetDataSetEx` is the flexible form of [`GetDataSet`](GetDataSet.md). It lets you choose the connection name, control whether the XML declaration and schema are included, override the dataset table name, decide how database nulls are emitted, and mark specific date columns for invariant handling.

When omitted, `bIncludeSchema` defaults to [`.T.`](../literals/true.md), `bIncludeHeader` defaults to [`.T.`](../literals/true.md), `bNullAsBlank` defaults to [`.T.`](../literals/true.md), and `sConnectionName` falls back to the current default connection. If `sTableName` is omitted, the runtime derives a table name from the query and falls back to `Table` when it cannot determine one.

Use positional `?` placeholders with `aValues`. This function does not support `?varName?` substitution.

## When to use

- When you need XML dataset output from a non-default database connection.
- When downstream consumers require control over XML declaration or schema output.
- When you need positional SQL parameters with `?` placeholders.
- When database null handling must be explicit for the XML consumer.
- When specific date columns must use invariant handling in the returned XML.

## Syntax

```ssl
GetDataSetEx(sCommandString, [sConnectionName], [aValues], [bIncludeSchema], [bIncludeHeader], [sTableName], [bNullAsBlank], [aInvariantDateCols])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCommandString` | [string](../types/string.md) | yes | — | SQL command text to execute. |
| `sConnectionName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Database connection name to run the command against. When [`NIL`](../literals/nil.md), the current default connection is used. |
| `aValues` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Positional values for `?` placeholders in `sCommandString`. Omit when the query has no parameters. |
| `bIncludeSchema` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Whether to include XML schema information in the returned string. |
| `bIncludeHeader` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Whether to include the XML declaration/header in the returned string. |
| `sTableName` | [string](../types/string.md) | no | derived from query, else `Table` | Table name to assign to the first dataset table in the XML. |
| `bNullAsBlank` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Whether database nulls should be emitted as blank values in the XML output. |
| `aInvariantDateCols` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Array of 1-based numeric column indexes to treat as invariant-date columns. |

## Returns

**[string](../types/string.md)** — XML dataset output for the command result.

For `SELECT` statements, the XML contains the returned rows. For non-`SELECT` statements, the XML contains a single-row dataset with a status string such as `(3) record(s) affected.`

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
    - Use `?` placeholders with `aValues` for dynamic values.
    - Omit `aValues` entirely when the command has no parameters.
    - Pass an explicit `sTableName` when downstream XML consumers depend on a stable dataset table name.
    - Use numeric 1-based column indexes in `aInvariantDateCols`.

!!! failure "Don't"
    - Use `?varName?` syntax with `GetDataSetEx`. That substitution style is for [`SQLExecute`](SQLExecute.md).
    - Pass a nested array in `aValues`. The function expects a single-dimensional values array.
    - Assume omitted `bNullAsBlank` preserves database nulls. The default is [`.T.`](../literals/true.md).
    - Pass column names in `aInvariantDateCols`. This parameter is index-based.

## Caveats

- For `SELECT` statements that return zero rows, the function still returns a valid XML dataset string.
- Large result sets can produce very large XML strings and corresponding memory cost.

## Examples

### Query a named connection with default XML options

Executes a parameterless query on a named connection and reports the length of the returned XML string.

```ssl
:PROCEDURE ExportActiveSamples;
	:DECLARE sSql, sXml, sConnection;

	sConnection := "REPORTING";
	sSql := "
	    SELECT sample_id, sample_name, status
	    FROM sample
	    WHERE status = 'A'
	    ORDER BY sample_id
	";

	sXml := GetDataSetEx(sSql, sConnection);

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

### Use positional parameters and suppress the XML header

Passes a status value via a `?` placeholder, suppresses the XML declaration and null-as-blank output, and assigns an explicit table name to the returned XML.

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
	sXml := GetDataSetEx(sSql, sConnection, aValues, .T., .F., "sample_results", .F.);

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("ExportSamplesByStatus", {"PENDING"});
```

### Mark date columns for invariant handling

Passes a date parameter and an invariant-date column index array, wrapping the call in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) so a query failure is reported without propagating the exception.

```ssl
:PROCEDURE ExportAuditDataset;
	:PARAMETERS dStartDate;
	:DEFAULT dStartDate, CToD("01/01/2024");
	:DECLARE sSql, sXml, sConnection, aValues, aInvariantDateCols, oErr;

	sConnection := "REPORTING";
	sSql := "
	    SELECT sample_id, sample_name, status, created_date, released_date
	    FROM sample
	    WHERE released_date >= ?
	    ORDER BY released_date
	";

	aValues := {dStartDate};
	aInvariantDateCols := {4, 5};

	:TRY;
		sXml := GetDataSetEx(sSql, sConnection, aValues, .T., .T., "sample_audit", .T., ;
			aInvariantDateCols);
		:RETURN sXml;
	:CATCH;
		oErr := GetLastSSLError();
		/* Displays on failure: Import failed;
		ErrorMes("GetDataSetEx failed: " + oErr:Description);
		:RETURN "";
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ExportAuditDataset", {CToD("03/01/2024")});
```

## Related

- [`GetDataSet`](GetDataSet.md)
- [`GetDataSetWithSchemaFromSelect`](GetDataSetWithSchemaFromSelect.md)
- [`GetDataSetXMLFromSelect`](GetDataSetXMLFromSelect.md)
- [`GetNETDataSet`](GetNETDataSet.md)
- [`GetSSLDataset`](GetSSLDataset.md)
- [`SSLDataset`](../classes/SSLDataset.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
- [`array`](../types/array.md)
