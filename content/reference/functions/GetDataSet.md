---
title: "GetDataSet"
summary: "Executes a SQL query on the default database connection and returns the result as an XML dataset string."
id: ssl.function.getdataset
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetDataSet

Executes a SQL query on the default database connection and returns the result as an XML dataset string.

`GetDataSet` is the convenience form of [`GetDataSetEx`](GetDataSetEx.md) for the current default connection. It accepts a SQL command string plus optional positional parameter values and XML-shaping options, then returns the result as XML with the XML header included. When `bIncludeSchema` is omitted, it defaults to [`.T.`](../literals/true.md) for this function. When `bNullAsBlank` is omitted, it defaults to [`.T.`](../literals/true.md). If `sTableName` is omitted, the runtime derives a table name from the query and falls back to `Table` when it cannot determine one.

Use `?` placeholders with `aValues`. This function does not use `?varName?` substitution.

## When to use

- When you need XML output from a query and the default database connection is the correct target.
- When you want positional SQL parameters without supplying a connection name.
- When downstream code expects dataset XML rather than an [`SSLDataset`](../classes/SSLDataset.md) object.
- When you want schema included by default and do not need control over the XML header flag.

## Syntax

```ssl
GetDataSet(sCommandString, [aValues], [bIncludeSchema], [sTableName], [bNullAsBlank], [aInvariantDateCols])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCommandString` | [string](../types/string.md) | yes | — | SQL command text to execute on the default connection. |
| `aValues` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Positional values for `?` placeholders in `sCommandString`. Omit when the query has no parameters. |
| `bIncludeSchema` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Whether to include XML schema information in the returned string. |
| `sTableName` | [string](../types/string.md) | no | derived from query, else `Table` | Table name to assign in the returned dataset XML. |
| `bNullAsBlank` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Whether database nulls should be emitted as blank values in the dataset output. |
| `aInvariantDateCols` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Array of 1-based column indexes to treat as invariant-date columns. |

## Returns

**[string](../types/string.md)** — XML dataset output for the query result.

The returned XML always includes the XML header. If you need control over header inclusion or need to target a non-default connection, use [`GetDataSetEx`](GetDataSetEx.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sCommandString` is [`NIL`](../literals/nil.md). | `The command string is null.` |
| `aValues` is multi-dimensional. | `The current array has more than 1 dimension.` |
| The query contains more `?` placeholders than supplied values. | `Parameters count mismatch` |
| The database engine name cannot be determined for the default connection. | `Cannot determine the database engine name.` |
| The resolved default connection is not configured. | `The provider name: {name} not found.` |
| The database collection is unavailable. | `The internal database collection is null` |

## Best practices

!!! success "Do"
    - Use `?` placeholders with `aValues` for dynamic values.
    - Omit `aValues` entirely when the query has no parameters.
    - Pass an explicit `sTableName` when downstream XML consumers depend on a stable dataset table name.
    - Use numeric 1-based column indexes in `aInvariantDateCols`.

!!! failure "Don't"
    - Use `?varName?` syntax with `GetDataSet`. That substitution style is for [`SQLExecute`](SQLExecute.md), not `GetDataSet`.
    - Pass a nested array in `aValues`. The function expects a single-dimensional values array.
    - Assume omitted `bNullAsBlank` preserves database nulls. The default is [`.T.`](../literals/true.md).
    - Pass column names in `aInvariantDateCols`. This parameter is index-based.

## Caveats

- Large result sets can produce very large XML strings and corresponding memory cost.

## Examples

### Run a simple query on the default connection

Executes a parameterless query on the default connection and reports the length of the returned XML string.

```ssl
:PROCEDURE ExportActiveSamples;
	:DECLARE sSql, sXml;

	sSql := "
	    SELECT sample_id, sample_name, status
	    FROM sample
	    WHERE status = 'A'
	    ORDER BY sample_id
	";

	sXml := GetDataSet(sSql);

	UsrMes("Returned XML length: " + LimsString(Len(sXml)));

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("ExportActiveSamples");
```

[`UsrMes`](UsrMes.md) displays:

```
Returned XML length: 1243
```

### Use positional parameters with custom XML options

Passes a status value through a `?` placeholder, disables schema and null-as-blank output, and assigns an explicit table name to the returned XML.

```ssl
:PROCEDURE ExportSamplesByStatus;
	:PARAMETERS sStatus;
	:DEFAULT sStatus, "A";
	:DECLARE sSql, sXml, aValues;

	sSql := "
	    SELECT sample_id, sample_name, status, received_date
	    FROM sample
	    WHERE status = ?
	    ORDER BY received_date DESC
	";

	aValues := {sStatus};
	sXml := GetDataSet(sSql, aValues, .F., "sample_results", .F.);

	UsrMes("Export complete for status " + sStatus);

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("ExportSamplesByStatus", {"PENDING"});
```

[`UsrMes`](UsrMes.md) displays:

```
Export complete for status PENDING
```

### Mark specific date columns as invariant

Passes a date parameter and an invariant-date column index array, wrapping the call in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) so a query failure is reported without propagating the exception.

```ssl
:PROCEDURE ExportReportDataset;
	:PARAMETERS dStartDate;
	:DEFAULT dStartDate, CToD("01/01/2024");
	:DECLARE sSql, sXml, aValues, aInvariantDateCols, oErr;

	sSql := "
	    SELECT sample_id, sample_name, status, created_date, released_date
	    FROM sample
	    WHERE released_date >= ?
	    ORDER BY released_date
	";

	aValues := {dStartDate};
	aInvariantDateCols := {4, 5};

	:TRY;
		sXml := GetDataSet(sSql, aValues, .T., "sample_report",
						   .T., aInvariantDateCols);
		:RETURN sXml;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("GetDataSet failed: " + oErr:Description);
		:RETURN "";
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ExportReportDataset", {CToD("03/01/2024")});
```

On failure, [`ErrorMes`](ErrorMes.md) displays a message beginning with:

```text
GetDataSet failed: ...
```

## Related

- [`GetDataSetEx`](GetDataSetEx.md)
- [`GetDataSetWithSchemaFromSelect`](GetDataSetWithSchemaFromSelect.md)
- [`GetDataSetXMLFromSelect`](GetDataSetXMLFromSelect.md)
- [`GetNETDataSet`](GetNETDataSet.md)
- [`GetSSLDataset`](GetSSLDataset.md)
- [`SSLDataset`](../classes/SSLDataset.md)
- [`XmlExportSql`](XmlExportSql.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
- [`array`](../types/array.md)
