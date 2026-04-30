---
title: "GetNETDataSet"
summary: "Executes a SQL command and returns the result either as dataset XML or as a netobject wrapping a dataset."
id: ssl.function.getnetdataset
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetNETDataSet

Executes a SQL command and returns the result either as dataset XML or as a [`netobject`](../types/netobject.md) wrapping a dataset.

`GetNETDataSet` runs the supplied SQL against the connection named by `sConnectionName`, applies positional `?` placeholders from `aValues`, and builds a single-table dataset from the returned result. When `bReturnXml` is omitted or [`.T.`](../literals/true.md), the function returns XML with schema. When `bReturnXml` is [`.F.`](../literals/false.md), it returns a [`netobject`](../types/netobject.md) for .NET interop scenarios. If `sTableName` is a string, that name is assigned to the returned table. If `bR1Compatible` is [`.T.`](../literals/true.md), the returned dataset's columns are adjusted for legacy R1-compatible behavior.

Use positional `?` placeholders with `aValues`. This function does not support `?varName?` substitution.

## When to use

- When you need dataset XML from a SQL query but also want the option to return a dataset object instead.
- When you need to run the query against a named database connection.
- When downstream code needs a stable table name in the returned dataset.
- When legacy R1-compatible column settings are required on the returned dataset object.

## Syntax

```ssl
GetNETDataSet(sCommandString, [sConnectionName], [aValues], [sTableName], [bReturnXml], [bR1Compatible])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCommandString` | [string](../types/string.md) | yes | — | SQL command text to execute. |
| `sConnectionName` | [string](../types/string.md) | no | `"DATABASE"` | Connection name to use. |
| `aValues` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Positional values for `?` placeholders in `sCommandString`. Non-array values are replaced with an empty array. |
| `sTableName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Table name to assign to the returned dataset table. |
| `bReturnXml` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | When [`.T.`](../literals/true.md), returns dataset XML. When [`.F.`](../literals/false.md), returns a [`netobject`](../types/netobject.md) wrapping the dataset. |
| `bR1Compatible` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | When [`.T.`](../literals/true.md), adjusts returned dataset column settings for legacy R1-compatible behavior. |

## Returns

- **[string](../types/string.md)** — Dataset XML with schema. Returned when `bReturnXml` is omitted or [`.T.`](../literals/true.md).
- **[netobject](../types/netobject.md)** — The dataset wrapped for .NET interop. Returned when `bReturnXml` is [`.F.`](../literals/false.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sCommandString` is not a string. | `Argument sCommandString must be a non-empty string.` |
| `sCommandString` is an empty string. | `The command string is null.` |
| `aValues` is multi-dimensional. | `The current array has more than 1 dimension.` |
| The query contains more `?` placeholders than supplied values. | `Parameters count mismatch.` |
| The provider for `sConnectionName` cannot be resolved. | `The provider name: <sConnectionName> not found.` |
| The database collection is unavailable. | `The internal database collection is null.` |
| The database engine name cannot be determined. | `Cannot determine the database engine name.` |
| The query returns a null data table. | `The returned data set is null.` |

## Best practices

!!! success "Do"
    - Use positional `?` placeholders and pass values in the same order in `aValues`.
    - Omit `aValues` entirely when the SQL has no parameters.
    - Pass `sTableName` when downstream code depends on a stable dataset table name.
    - Leave `bReturnXml` at its default when the caller only needs XML output.

!!! failure "Don't"
    - Use `?varName?` syntax with `GetNETDataSet`. That substitution style is for [`SQLExecute`](SQLExecute.md).
    - Pass a nested array in `aValues`. The function expects a single-dimensional values array.
    - Assume `sConnectionName` renames the returned table. Use `sTableName` for that.
    - Request object output unless the caller is prepared to work with a returned netobject.

## Caveats

- Passing extra values beyond the placeholder count does not raise an error; only too few values raises `Parameters count mismatch.`
- XML and object output use the same query path; `bReturnXml` changes only the final return format.

## Examples

### Return dataset XML with the defaults

Runs a query against the default connection with no parameters and displays the length of the returned XML string.

```ssl
:PROCEDURE ExportOpenSamples;
	:DECLARE sSql, sXml;

	sSql := "
	    SELECT sample_id, status
	    FROM sample
	    WHERE status = 'A'
	    ORDER BY sample_id
	";

	sXml := GetNETDataSet(sSql);

	UsrMes("Returned XML length: " + LimsString(Len(sXml)));

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("ExportOpenSamples");
```

[`UsrMes`](UsrMes.md) displays:

```text
Returned XML length: 547
```

### Use positional parameters and set the table name

Passes a status filter through a positional `?` placeholder and assigns a stable table name to the returned XML so downstream code can reference it by name.

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
	sXml := GetNETDataSet(sSql, "DATABASE", aValues, "sample_results");

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("ExportSamplesByStatus", {"A"});
```

### Return a dataset object for .NET interop

Sets `bReturnXml` to [`.F.`](../literals/false.md) to get a [`netobject`](../types/netobject.md) wrapping the dataset instead of XML, and wraps the call in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) to report any query failure.

```ssl
:PROCEDURE LoadSamplesAsObject;
	:PARAMETERS sStatus;
	:DEFAULT sStatus, "A";
	:DECLARE sSql, aValues, oDataSet, oErr;

	sSql := "
	    SELECT sample_id, sample_name, status
	    FROM sample
	    WHERE status = ?
	    ORDER BY sample_id
	";

	aValues := {sStatus};

	:TRY;
		oDataSet := GetNETDataSet(sSql, "DATABASE", aValues,
								  "sample_results", .F., .T.);
		UsrMes("Returned type: " + LimsTypeEx(oDataSet));
		:RETURN oDataSet;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("GetNETDataSet failed: " + oErr:Description);
		:RETURN "";
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("LoadSamplesAsObject", {"A"});
```

[`UsrMes`](UsrMes.md) displays:

```text
Returned type: System.Data.DataSet
```

On failure, [`ErrorMes`](ErrorMes.md) displays a message beginning with:

```text
GetNETDataSet failed: ...
```

## Related

- [`GetDataSet`](GetDataSet.md)
- [`GetDataSetEx`](GetDataSetEx.md)
- [`LimsNETTypeOf`](LimsNETTypeOf.md)
- [`netobject`](../types/netobject.md)
- [`CDataTable`](../classes/CDataTable.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
- [`array`](../types/array.md)
