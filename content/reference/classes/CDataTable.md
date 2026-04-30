---
title: "CDataTable"
summary: "Provides an in-memory table object for working with rows, columns, XML, and database persistence from SSL."
id: ssl.class.cdatatable
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CDataTable

Provides an in-memory table object for working with rows, columns, XML, and database persistence from SSL.

`CDataTable` is typically used for table data that already has a schema, such as tables returned by [`TablesImport:GetTable()`](TablesImport.md) or tables loaded with [`FromXml()`](../functions/FromXml.md). It exposes column metadata through `Columns`, row objects through `Rows`, plain array data through `ToArray()`, and SQL or persistence helpers such as `GetInsertSql()`, `GetUpdateSql()`, and `SaveToDb()`.

## When to use

- When you need to inspect or update imported tabular data in memory.
- When you need row objects for field-by-field edits before persisting changes.
- When you need generated `INSERT` or `UPDATE` SQL that matches the table's current schema.
- When you need to move a table between SSL and XML while preserving its schema.

## Constructors

### `CDataTable{}`

Creates an empty table.

### `CDataTable{oDataTable, sImportFolder}`

Wraps an existing table object and associates an import folder with it.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `oDataTable` | [object](../types/object.md) | yes | Existing table handle. |
| `sImportFolder` | [string](../types/string.md) | yes | Folder used for imported table assets such as extracted binary values. |

### `CDataTable{sName, nColCount}`

Creates an empty named table.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sName` | [string](../types/string.md) | yes | Table name. |
| `nColCount` | [number](../types/number.md) | yes | Accepted by the constructor, but it does not define the schema. |

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `Columns` | [object](../types/object.md) | read-only | [`CDataColumns`](CDataColumns.md) collection for the current schema. |
| `ErrMsg` | [string](../types/string.md) | read-only | Error text property exposed by the class. The documented methods on this page do not populate it. |
| `ImportFolder` | [string](../types/string.md) | read-write | Folder associated with imported content and extracted binary values. Setting it to [`NIL`](../literals/nil.md) clears it to an empty string. |
| `InnerTable` | [object](../types/object.md) | read-only | Underlying table handle for advanced integration scenarios. |
| `IsSystem` | [boolean](../types/boolean.md) | read-write | Controls whether generated SQL and persistence target system-table context. |
| `Name` | [string](../types/string.md) | read-write | Table name. |
| `NullAsBlank` | [boolean](../types/boolean.md) | read-write | Controls whether null values are converted to blank or default values in array and XML conversions. |
| `PkColumns` | [array](../types/array.md) | read-only | Array of [`CDataColumn`](CDataColumn.md) objects that make up the primary key. |
| `Rows` | [array](../types/array.md) | read-only | Array of [`CDataRow`](CDataRow.md) objects for all rows in the table. |
| `RowsCount` | [number](../types/number.md) | read-only | Number of rows in the table. |

## Methods

| Name | Returns | Description |
|------|---------|-------------|
| `AddPK(vPks)` | [boolean](../types/boolean.md) | Assigns one or more columns as the table's primary key. |
| `AddRow(oRow)` | none | Appends an existing [`CDataRow`](CDataRow.md) to the table. |
| `NewRow()` | [object](../types/object.md) | Creates a new unattached [`CDataRow`](CDataRow.md) for this table. |
| `GetInsertSql()` | [string](../types/string.md) | Returns an `INSERT` statement for the current schema, excluding binary columns. |
| `GetUpdateSql()` | [string](../types/string.md) | Returns an `UPDATE` statement for the current schema, using primary-key columns in the `WHERE` clause and excluding binary columns. |
| `SaveToDb(bOverwrite, aWhereFields, aFieldsValues, bDoAudit, aSkipColumns)` | [boolean](../types/boolean.md) | Persists current rows, or a selected subset of current rows, to the database. |
| `Select(vWhereFields, aFieldsValues)` | [array](../types/array.md) | Returns matching [`CDataRow`](CDataRow.md) objects. |
| `ToArray()` | [array](../types/array.md) | Returns the table as a 2D array of values. |
| [`ToXml()`](../functions/ToXml.md) | [string](../types/string.md) | Serializes the table, including schema, to XML. |
| `UpdateField(sFieldName, vNewValue, vOldValue)` | [boolean](../types/boolean.md) | Replaces one field value across matching rows. |
| `UpdateFieldFromArray(sFieldName, aValues)` | [boolean](../types/boolean.md) | Replaces field values by key lookup from an array of `{newValue, key}` pairs. |
| `FromXml(sXml)` | [`NIL`](../literals/nil.md) | Replaces the current table with the first table read from XML. |

### `AddPK`

Registers one column name or an array of column names as the primary key.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `vPks` | [string](../types/string.md) or [array](../types/array.md) | yes | Column name, or array of column names, to assign as primary-key columns. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the key assignment succeeds.

**Raises:**

- **When `vPks` contains an unrecognised column name:** `Invalid column name: [<name>].`

### `AddRow`

Appends a row created for this table.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `oRow` | [object](../types/object.md) | yes | [`CDataRow`](CDataRow.md) to add to the table. |

**Returns:** none — No return value.

### `NewRow`

Creates a new row with this table's schema. The row is not added to the table until you pass it to `AddRow()`.

**Returns:** [`CDataRow`](CDataRow.md) — New row for this table.

### `GetInsertSql`

Returns an `INSERT` statement for the current table schema. Binary columns are excluded from the statement.

**Returns:** [string](../types/string.md) — Positional-parameter `INSERT` statement, or an empty string when the table has no columns.

### `GetUpdateSql`

Returns an `UPDATE` statement for the current table schema. Binary columns are excluded from the statement, and primary-key columns are used in the `WHERE` clause.

**Returns:** [string](../types/string.md) — Positional-parameter `UPDATE` statement, or an empty string when the table has no columns.

### `SaveToDb`

Persists rows from the current table to the database.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `bOverwrite` | [boolean](../types/boolean.md) | no | When [`.T.`](../literals/true.md), existing database rows with matching primary keys are updated. When [`.F.`](../literals/false.md), existing matches are skipped. Defaults to [`.T.`](../literals/true.md) when omitted or [`NIL`](../literals/nil.md). |
| `aWhereFields` | [array](../types/array.md) | no | Field names used to select which in-memory rows should be persisted. |
| `aFieldsValues` | [array](../types/array.md) | no | Array of value arrays aligned with `aWhereFields`. |
| `bDoAudit` | [boolean](../types/boolean.md) | no | Accepted parameter. It does not affect the method's behavior. Defaults to [`.T.`](../literals/true.md) when omitted or [`NIL`](../literals/nil.md). |
| `aSkipColumns` | [array](../types/array.md) | no | Column names to omit from generated insert or update commands. Matching is case-insensitive. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) after processing the selected rows.

**Raises:**

- `count is null.` — the row-count lookup returned null during persist.

### `Select`

Returns rows that match either a filter string or aligned field/value criteria.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `vWhereFields` | [string](../types/string.md) or [array](../types/array.md) | yes | Filter string, or array of field names. |
| `aFieldsValues` | [array](../types/array.md) | no | Required when `vWhereFields` is an array. Each entry must be an array of candidate values for the field at the same position. |

**Returns:** [array](../types/array.md) — Array of [`CDataRow`](CDataRow.md) objects.

**Raises:**

- **When `vWhereFields` is [`NIL`](../literals/nil.md) or not an array:** `An array of names is expected!`
- **When `aFieldsValues` entries are not arrays:** `An array of arrays, with values is expected`

### `ToArray`

Returns the table as a plain 2D array of field values in row order.

**Returns:** [array](../types/array.md) — Each row is an array of values in column order.

### [`ToXml`](../functions/ToXml.md)

Serializes the table, including schema and data, to XML.

**Returns:** [string](../types/string.md) — XML string for the current table.

### `UpdateField`

Updates one column across matching rows. Passing [`NIL`](../literals/nil.md) for `vOldValue` updates every row in the table.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sFieldName` | [string](../types/string.md) | yes | Column to update. |
| `vNewValue` | any | yes | Replacement value. Use [`NIL`](../literals/nil.md) to write a null value. |
| `vOldValue` | any | yes | Current value to match. Pass [`NIL`](../literals/nil.md) to update all rows. |

**Returns:** [boolean](../types/boolean.md) — Always [`.T.`](../literals/true.md) if the method completes.

**Raises:**

- `Column: [<name>] does not exist.`

### `UpdateFieldFromArray`

Updates one field by looking up each row's current field value in an array of `{newValue, key}` pairs.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sFieldName` | [string](../types/string.md) | yes | Column to update. |
| `aValues` | [array](../types/array.md) | yes | Array of two-item arrays in the form `{newValue, key}`. The lookup is case-insensitive. |

**Returns:** [boolean](../types/boolean.md) — Always [`.T.`](../literals/true.md) if the method completes.

**Raises:**

- `Argument 'sFieldName' cannot be null nor empty string.`
- `Argument 'aValues' must be a non null array.`
- `Invalid values. Index: <n>`

### [`FromXml`](../functions/FromXml.md)

Loads the first table from an XML string and replaces the current table.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sXml` | [string](../types/string.md) | yes | XML string that includes table schema and data. |

**Returns:** [`NIL`](../literals/nil.md) — Replaces the current table contents with those from the XML string.

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Use `GetTable()` from [`TablesImport`](TablesImport.md) or [`FromXml()`](../functions/FromXml.md) when you need a `CDataTable` with a working schema already in place.
    - Call `AddPK()` before using `GetUpdateSql()` or relying on update behavior in `SaveToDb()`.
    - Use `Select({fieldNames}, {valueArrays})` when you want predictable exact field/value matching from SSL code.
    - Use `Rows` when you want every row in the table, and `ToArray()` when you want plain value arrays instead of [`CDataRow`](CDataRow.md) objects.
    - Set `NullAsBlank` deliberately before exporting to arrays or XML so null handling matches your script's expectations.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) as the first argument to `Select()` to mean "all rows" — that raises `An array of names is expected!`.
    - Assume `ToArray()` returns [`CDataRow`](CDataRow.md) objects — it returns a plain 2D array of field values.
    - Expect `SaveToDb()` to audit changes just because you passed `bDoAudit` — that parameter does not change the method's behavior.
    - Rely on `ErrMsg` for method failures on this class — the documented methods raise errors directly and do not populate that property.
    - Expect `CDataTable{sName, nColCount}` to build the schema — the constructor only sets the table name.

## Caveats

- Setting `IsSystem`, `Name`, or `NullAsBlank` to [`NIL`](../literals/nil.md) raises an error.
- Setting `ImportFolder` to [`NIL`](../literals/nil.md) clears it to an empty string.
- `Select({}, {})` returns an empty result set, not all rows.
- `GetInsertSql()` and `GetUpdateSql()` skip binary columns.
- `SaveToDb()` can still include binary columns unless you omit them with `aSkipColumns`.
- `UpdateFieldFromArray()` returns [`.T.`](../literals/true.md) even when no row values match the provided keys.

## Examples

### Select rows by field values

This example demonstrates loading a table with `GetTable()`, filtering rows using `Select()` with field-name and value-array criteria, and reading a field value from the first matching row.

```ssl
:PROCEDURE FindPendingRows;
	:DECLARE oImport, oTable, aRows, oRow, sSampleId;

	oImport := TablesImport{"C:/Import"};
	oTable := oImport:GetTable("sample");
	aRows := oTable:Select({"status"}, {{"Pending"}});

	:IF ALen(aRows) == 0;
		UsrMes("No pending rows found");
		:RETURN;
	:ENDIF;

	oRow := aRows[1];
	sSampleId := oRow:GetField("sample_id"):Value;

/* Displays matching sample id when a pending row exists;
	UsrMes("First pending sample: " + sSampleId);
:ENDPROC;

/* Usage;
DoProc("FindPendingRows");
```

### Update matching rows and persist them

This example demonstrates assigning a primary key with `AddPK()`, updating a field across matching rows using `UpdateField()`, then persisting only those updated rows to the database with `SaveToDb()`.

```ssl
:PROCEDURE CompletePendingRows;
	:DECLARE oImport, oTable, bSaved;

	oImport := TablesImport{"C:/Import"};
	oTable := oImport:GetTable("sample");

	oTable:AddPK("sample_id");
	oTable:UpdateField("status", "Complete", "Pending");
	bSaved := oTable:SaveToDb(.T., {"status"}, {{"Complete"}});

	:IF bSaved;
		UsrMes("Completed rows were saved");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("CompletePendingRows");
```

`UsrMes` displays:

```text
Completed rows were saved
```

## Related

- [`CDataColumns`](CDataColumns.md)
- [`CDataRow`](CDataRow.md)
- [`SSLDataset`](SSLDataset.md)
- [`TablesImport`](TablesImport.md)
