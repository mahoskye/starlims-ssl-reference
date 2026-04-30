---
title: "SSLDataset"
summary: "Represents dataset results so SSL code can work with query output as an object, convert the first table to an array, export XML, or pass the dataset handle to APIs that expect one."
id: ssl.class.ssldataset
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SSLDataset

Represents dataset results so SSL code can work with query output as an object, convert the first table to an array, export XML, or pass the dataset handle to APIs that expect one.

`SSLDataset` is usually obtained from [`GetSSLDataset`](../functions/GetSSLDataset.md) or from [`RunDS`](../functions/RunDS.md) with the `"ssldataset"` return type. An empty `SSLDataset{}` starts with no loaded data. `ToArray()` reads only the first table and returns an empty array when no table is available. [`ToXml()`](../functions/ToXml.md) exports the current dataset as XML with schema and an XML declaration. `ToDataSet()` returns the current dataset handle in object form for APIs that specifically expect it.

## When to use

- When you need the first table of a dataset as a plain SSL array.
- When you need XML output from a dataset, including schema information.
- When you need to keep a dataset result in object form and choose how nulls are represented in `ToArray()` output.

## Constructors

### `SSLDataset{}`

Creates an empty dataset object with no loaded data.

### `SSLDataset{oData, bNullAsBlank}`

Creates an `SSLDataset` from an existing dataset handle.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `oData` | [object](../types/object.md) | yes | Existing dataset handle. |
| `bNullAsBlank` | [boolean](../types/boolean.md) | yes | Controls how `ToArray()` represents null values from the first table. Pass [`.T.`](../literals/true.md) to convert nulls to blank values, or [`.F.`](../literals/false.md) to preserve nulls. |

## Methods

| Name | Returns | Description |
|------|---------|-------------|
| [`ToXml`](../functions/ToXml.md) | [string](../types/string.md) | Serializes the current dataset to XML with schema and an XML declaration. |
| `ToArray` | [array](../types/array.md) | Returns the first table as an array of rows. |
| `ToDataSet` | [object](../types/object.md) | Returns the current dataset handle in object form. |

### [`ToXml`](../functions/ToXml.md)

Serializes the current dataset to XML.

**Returns:** [string](../types/string.md) — XML for the current dataset, including schema and an XML declaration.

### `ToArray`

Returns the first table in the dataset as an array of rows. If no dataset is loaded or the dataset has no tables, the result is an empty array.

**Returns:** [array](../types/array.md) — Rows from the first table, or an empty array when no table is available.

### `ToDataSet`

Returns the current dataset handle in object form.

**Returns:** [object](../types/object.md) — Dataset handle for APIs that work with dataset objects.

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Prefer [`GetSSLDataset`](../functions/GetSSLDataset.md) or [`RunDS`](../functions/RunDS.md) with `"ssldataset"` when you need a populated `SSLDataset`.
    - Pass `bNullAsBlank` explicitly when wrapping an existing dataset handle so the `ToArray()` behavior is clear.
    - Check `ALen(oDataset:ToArray())` before assuming the first table contains rows.
    - Use `ToDataSet()` only when the next API specifically expects a dataset object instead of an SSL array or XML string.

!!! failure "Don't"
    - Assume `ToArray()` includes every table in a multi-table dataset. It only returns the first table.
    - Treat `bNullAsBlank` as optional in `SSLDataset{xData, xNullAsBlank}`. The wrapping constructor expects both arguments.
    - Call [`ToXml()`](../functions/ToXml.md) on an empty `SSLDataset{}`. Load data first.
    - Use `ToDataSet()` unless the next API specifically needs a dataset handle. `ToArray()` or [`ToXml()`](../functions/ToXml.md) are usually clearer in SSL code.

## Caveats

- The `bNullAsBlank` setting affects `ToArray()` output, not the underlying dataset itself.
- [`ToXml()`](../functions/ToXml.md) requires loaded dataset content. An empty `SSLDataset{}` does not provide a safe XML export.

## Examples

### Read the first table as rows

Runs a query with [`GetSSLDataset`](../functions/GetSSLDataset.md), converts the first table to an array with `ToArray()`, then iterates over each row to display the result columns.

```ssl
:PROCEDURE ReviewRecentTasks;
	:DECLARE oDataset, aRows, nIndex;

	oDataset := GetSSLDataset("
	    SELECT ordno, testcode, status
	    FROM ordtask
	    WHERE status = 'Pending'
	    ORDER BY ordno
	");

	aRows := oDataset:ToArray();

	:FOR nIndex := 1 :TO ALen(aRows);
		UsrMes(
			aRows[nIndex, 1] + " / "
			+ aRows[nIndex, 2] + " / "
			+ aRows[nIndex, 3]
		);
		/* Displays pending task row;
	:NEXT;
:ENDPROC;

/* Usage;
DoProc("ReviewRecentTasks");
```

### Wrap a dataset handle before exporting XML

Uses the two-argument constructor to wrap an existing dataset handle from [`RunDS`](../functions/RunDS.md), controlling null handling with `bNullAsBlank`, then exports the result to XML with [`ToXml()`](../functions/ToXml.md).

```ssl
:PROCEDURE ExportPendingOrdersXml;
	:DECLARE oData, oDataset, sXml;

	oData := RunDS("QA.PendingOrders",, "dataset");
	oDataset := SSLDataset{oData, .F.};
	sXml := oDataset:ToXml();

	UsrMes(
		"Prepared XML payload with "
		+ LimsString(Len(sXml))
		+ " characters"
	);
	/* Displays XML payload length;
:ENDPROC;

/* Usage;
DoProc("ExportPendingOrdersXml");
```

## Related

- [`GetSSLDataset`](../functions/GetSSLDataset.md)
- [`RunDS`](../functions/RunDS.md)
- [`GetDataSet`](../functions/GetDataSet.md)
- [`CDataTable`](CDataTable.md)
- [`object`](../types/object.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
