---
title: "CDataColumns"
summary: "Provides access to the column definitions of a CDataTable."
id: ssl.class.cdatacolumns
element_type: class
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CDataColumns

Provides access to the column definitions of a [`CDataTable`](CDataTable.md).

`CDataColumns` represents the columns in a table and lets you retrieve each column definition as a [`CDataColumn`](CDataColumn.md). Use it to inspect column names, types, lengths, and key flags on an existing [`CDataTable`](CDataTable.md). Most scripts obtain this collection from `oTable:Columns` rather than constructing it directly.

## When to use

- When you need to inspect the schema of a [`CDataTable`](CDataTable.md).
- When you need to locate a column by name before reading its metadata.
- When you need to iterate through all columns in a table by position.

## Constructors

### `CDataColumns{oDataTable}`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `oDataTable` | [object](../types/object.md) | yes | The [`CDataTable`](CDataTable.md) whose columns are exposed by the collection. In most scripts, use `oTable:Columns` instead of constructing the collection directly. |

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `Count` | [number](../types/number.md) | read-only | Number of columns in the collection. |
| `ParentTable` | [object](../types/object.md) | write-only | Assigns a parent [`CDataTable`](CDataTable.md) to the collection. The assigned value is not readable from SSL. |

## Methods

| Name | Returns | Description |
|------|---------|-------------|
| `Add(oCol)` | none | Accepts a column argument, but does not add it to the collection. |
| `GetIndex(sColName)` | [number](../types/number.md) | Returns the 1-based position of a named column, or `0` if it is not found. |
| `Set(nIndex, oColumn)` | [`NIL`](../literals/nil.md) | Accepts an index and column argument, but does not update the collection. |
| `Get(vIndex)` | [object](../types/object.md) | Returns a [`CDataColumn`](CDataColumn.md) by name or by 1-based index. |

### `Add`

Accepts a [`CDataColumn`](CDataColumn.md) argument, but does not add it to the collection.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `oCol` | [object](../types/object.md) | yes | Column object to pass to the method. |

**Returns:** none — No return value.

### `GetIndex`

Returns the 1-based position of a column name.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sColName` | [string](../types/string.md) | yes | Column name to locate. |

**Returns:** number — 1-based index of the column, or `0` if the column is not found.

### `Set`

Accepts an index and column object, but does not update the collection.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `nIndex` | [number](../types/number.md) | yes | 1-based column position. |
| `oColumn` | [object](../types/object.md) | yes | Column object to pass to the method. |

**Returns:** [`NIL`](../literals/nil.md) — The method accepts parameters but makes no changes.

### `Get`

Retrieves a column by name or by 1-based index.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `vIndex` | [string](../types/string.md) or [number](../types/number.md) | yes | Column name or 1-based column position. |

**Returns:** [`CDataColumn`](CDataColumn.md) — The matching column object.

**Raises:**

- **When `vIndex` is [`NIL`](../literals/nil.md):** `Argument vIndex cannot be null.`
- **When `vIndex` is not a string or integer:** `Argument vIndex is not string nor integer.`
- **When `vIndex` is an out-of-range integer:** `Index [<n>] is out of range (fields count=<count>)`
- **When `vIndex` names a column that does not exist:** `Column: [<name>] does not exist.`

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Use `oTable:Columns` to work with the collection that belongs to an existing [`CDataTable`](CDataTable.md).
    - Prefer `Get("column_name")` when the script depends on a specific column name.
    - Use `GetIndex()` before numeric access when the column might be missing.
    - Treat numeric access as 1-based when iterating through the collection.

!!! failure "Don't"
    - Assume `Add()` or `Set()` will change the schema — these methods do not update the collection.
    - Use `0` as the first column position — numeric access is 1-based.
    - Assume `Get()` returns an empty value for a missing column — invalid lookups raise errors.
    - Read `ParentTable` — the property is write-only.

## Caveats

- `Get()` raises an error for invalid names, invalid types, [`NIL`](../literals/nil.md), and out-of-range numeric positions.
- Numeric access is 1-based, but the value reported in out-of-range error messages may not match the index you supplied.
- `Add()` and `Set()` are surfaced members, but they do not modify the collection.

## Examples

### Inspect a column by name

Uses `GetIndex` to locate the column first, then retrieves it with `Get`. The `GetIndex` guard avoids the error that `Get` raises for a missing name.

```ssl
:PROCEDURE InspectColumn;
	:DECLARE oImport, oTable, oColumns, oColumn, nIndex, sMsg;

	oImport := TablesImport{"C:/Import"};
	oTable := oImport:GetTable("limsusers");
	oColumns := oTable:Columns;

	nIndex := oColumns:GetIndex("user_name");

	:IF nIndex > 0;
		oColumn := oColumns:Get(nIndex);
		sMsg := "Column " + oColumn:Name;
		sMsg := sMsg + " is at position " + LimsString(nIndex);
		UsrMes(sMsg);
	:ELSE;
		UsrMes("Column user_name was not found");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("InspectColumn");
```

### Inspect a column by position

Accesses the first column using a 1-based numeric index. The `Count` guard ensures the table has at least one column before calling `Get`.

```ssl
:PROCEDURE InspectFirstColumn;
	:DECLARE oImport, oTable, oColumns, oColumn;

	oImport := TablesImport{"C:/Import"};
	oTable := oImport:GetTable("limsusers");
	oColumns := oTable:Columns;

	:IF oColumns:Count > 0;
		oColumn := oColumns:Get(1);
		UsrMes("First column: " + oColumn:Name);
	:ELSE;
		UsrMes("The table has no columns");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("InspectFirstColumn");
```

### Handle a missing column lookup

Demonstrates that `Get` raises an error for a column name that does not exist. Use [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) when looking up columns whose existence is not guaranteed.

```ssl
:PROCEDURE HandleMissingColumn;
	:DECLARE oImport, oTable, oColumns, oErr;

	oImport := TablesImport{"C:/Import"};
	oTable := oImport:GetTable("limsusers");
	oColumns := oTable:Columns;

	:TRY;
		oColumns:Get("missing_column");
	:CATCH;
		oErr := GetLastSSLError();
		UsrMes(oErr:Description);
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("HandleMissingColumn");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Column: [missing_column] does not exist.
```

## Related

- [`CDataColumn`](CDataColumn.md)
- [`CDataTable`](CDataTable.md)
- [`TablesImport`](TablesImport.md)
