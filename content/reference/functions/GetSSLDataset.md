---
title: "GetSSLDataset"
summary: "Executes a SQL statement and returns the result as an SSLDataset."
id: ssl.function.getssldataset
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetSSLDataset

Executes a SQL statement and returns the result as an [`SSLDataset`](../classes/SSLDataset.md).

`GetSSLDataset` runs SQL against a database connection and wraps the result in an [`SSLDataset`](../classes/SSLDataset.md). Use it when you want dataset behavior in SSL rather than XML text or a plain array.

When `sDsn` is omitted, the function uses `DATABASE`. When `sTableName` is omitted, the runtime tries to derive the first table name from the SQL text and falls back to `__TableName__` if it cannot determine one. When `bNullAsBlank` is omitted, it defaults to [`.T.`](../literals/true.md).

## When to use

- When you want an [`SSLDataset`](../classes/SSLDataset.md) object rather than XML text from [`GetDataSet`](GetDataSet.md) or [`GetDataSetEx`](GetDataSetEx.md).
- When you need explicit named parameter binding with separate `aParamNames`
  and `aParamValues` arrays.
- When downstream code will call dataset methods such as `ToArray()` or [`ToXml()`](ToXml.md).
- When you need to control null handling or mark date columns as invariant.

## Syntax

```ssl
GetSSLDataset(sSql, [sDsn], [aParamNames], [aParamValues], [sTableName], [bNullAsBlank], [aInvariantDateCols])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSql` | [string](../types/string.md) | yes | — | SQL command text to execute. |
| `sDsn` | [string](../types/string.md) | no | `DATABASE` | Database connection name. |
| `aParamNames` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Array of parameter names to bind. Parameter binding only happens when both `aParamNames` and `aParamValues` are supplied. |
| `aParamValues` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Array of values corresponding to `aParamNames`. |
| `sTableName` | [string](../types/string.md) | no | first table in `sSql`, else `__TableName__` | Table name assigned to the first table in the returned dataset. |
| `bNullAsBlank` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Whether database nulls should be converted to blank values in the returned [`SSLDataset`](../classes/SSLDataset.md) view. |
| `aInvariantDateCols` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Array of invariant date columns. Pass either column names or zero-based column ordinals, and keep the whole array in one form. |

## Returns

**[SSLDataset](../classes/SSLDataset.md)** — Dataset wrapper for the command result.

For `SELECT` statements, the first table contains the returned rows. For non-`SELECT` statements, the returned dataset still contains a first table, with one status row such as `(3) record(s) affected.`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSql` is [`NIL`](../literals/nil.md). | `sSql parameter cannot be null.` |
| `sSql` is an empty string. | `The command string is null.` |
| `aParamNames` has more entries than `aParamValues`. | `Not enough values provided for parameters.` |
| The connection name is not configured. | `The provider name: <name> not found.` |
| The database collection is unavailable. | `The internal database collection is null.` |

## Best practices

!!! success "Do"
    - Supply both `aParamNames` and `aParamValues` when using bound parameters.
    - Use a stable `sTableName` when downstream code depends on the dataset table name.
    - Set `bNullAsBlank` to [`.F.`](../literals/false.md) when your logic must distinguish database nulls from blank strings.
    - Use one consistent form in `aInvariantDateCols`: all names or all zero-based ordinals.

!!! failure "Don't"
    - Assume `GetSSLDataset` uses `?varName?` substitution like [`SQLExecute`](SQLExecute.md). This function binds explicit parameter names and values arrays.
    - Pass only one of `aParamNames` or `aParamValues`. If either is missing, no parameters are bound.
    - Assume omitted `sTableName` falls back to `Table`. This function falls back to `__TableName__` when it cannot derive a table name.
    - Mix column names and numeric ordinals in the same `aInvariantDateCols` array.

## Caveats

- Placeholder syntax in `sSql` must match the target provider. In practice that is typically `:name` for Oracle and `@name` for non-Oracle providers.
- If `aParamValues` contains more entries than `aParamNames`, the extra values are ignored.
- `bNullAsBlank` affects how the returned [`SSLDataset`](../classes/SSLDataset.md) exposes values, especially through methods such as `ToArray()`.

## Examples

### Read query results as an SSLDataset

Runs a simple SELECT against the default connection, converts the result to an array with `ToArray()`, and iterates over each row to display the three columns separated by slashes.

```ssl
:PROCEDURE ReviewActiveSamples;
	:DECLARE sSql, oDataset, aRows, nIndex;

	sSql := "
	    SELECT sample_id, sample_name, status
	    FROM sample
	    WHERE status = 'A'
	    ORDER BY sample_id
	";

	oDataset := GetSSLDataset(sSql);
	aRows := oDataset:ToArray();

	:FOR nIndex := 1 :TO ALen(aRows);
		UsrMes(aRows[nIndex, 1] + " / " + aRows[nIndex, 2] + " / " + aRows[nIndex, 3]);
		/* Displays one row per active sample;
	:NEXT;

	:RETURN ALen(aRows);
:ENDPROC;

/* Usage;
DoProc("ReviewActiveSamples");
```

### Bind named parameters and set the dataset table name

Passes a bound `:status` parameter and assigns the stable table name `orders_by_status` so that downstream code can reference the table by name regardless of how the SQL is phrased.

```ssl
:PROCEDURE LoadOrdersByStatus;
	:PARAMETERS sStatus;
	:DEFAULT sStatus, "PENDING";
	:DECLARE sSql, aParamNames, aParamValues, oDataset, aRows;

	sSql := "
	    SELECT order_id, customer_name, status
	    FROM orders
	    WHERE status = :status
	    ORDER BY order_id
	";

	aParamNames := {":status"};
	aParamValues := {sStatus};
	oDataset := GetSSLDataset(sSql, "DATABASE", aParamNames, aParamValues,
		"orders_by_status");

	aRows := oDataset:ToArray();
	UsrMes("Loaded " + LimsString(ALen(aRows)) + " order rows");

	:RETURN oDataset;
:ENDPROC;

/* Usage;
DoProc("LoadOrdersByStatus", {"PENDING"});
```

[`UsrMes`](UsrMes.md) displays:

```
Loaded 12 order rows
```

### Preserve nulls and mark date columns as invariant

Sets `bNullAsBlank` to [`.F.`](../literals/false.md) so database nulls stay distinct, marks `review_date` as invariant to prevent locale-based date conversion, and exports the result as XML via [`ToXml()`](ToXml.md).

```ssl
:PROCEDURE ExportAuditDataset;
	:PARAMETERS sStatus;
	:DEFAULT sStatus, "ACTIVE";
	:DECLARE sSql, aParamNames, aParamValues, aInvariantDateCols;
	:DECLARE oDataset, sXml, oErr;

	sSql := "
	    SELECT sample_id, reviewer, review_date, comments
	    FROM sample_audit
	    WHERE status = :status
	    ORDER BY review_date
	";

	aParamNames := {":status"};
	aParamValues := {sStatus};
	aInvariantDateCols := {"review_date"};

	:TRY;
		oDataset := GetSSLDataset(sSql, "DATABASE", aParamNames, aParamValues,
			"sample_audit", .F., aInvariantDateCols);
		sXml := oDataset:ToXml();
		:RETURN sXml;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("GetSSLDataset failed: " + oErr:Description);
		/* Displays on failure: GetSSLDataset failed;
		:RETURN "";
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ExportAuditDataset", {"ACTIVE"});
```

## Related

- [`GetDataSet`](GetDataSet.md)
- [`GetDataSetEx`](GetDataSetEx.md)
- [`GetDataSetWithSchemaFromSelect`](GetDataSetWithSchemaFromSelect.md)
- [`GetDataSetXMLFromSelect`](GetDataSetXMLFromSelect.md)
- [`GetNETDataSet`](GetNETDataSet.md)
- [`SSLDataset`](../classes/SSLDataset.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
- [`array`](../types/array.md)
