---
title: "CDataColumn"
summary: "Provides metadata for a single column in a CDataTable."
id: ssl.class.cdatacolumn
element_type: class
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CDataColumn

Provides metadata for a single column in a [`CDataTable`](CDataTable.md).

`CDataColumn` lets you inspect a column's name, length, type information, primary-key membership, and whether the column stores binary data. Use it when you need schema-aware logic before reading, transforming, or exporting table rows.

## When to use

- When you need to inspect column names, lengths, or types before processing table data.
- When you need to identify primary key columns in a [`CDataTable`](CDataTable.md).
- When you need to detect binary columns before reading or exporting values.
- When you intentionally want to rename a column or change its maximum length.

## Constructors

`CDataColumn` is typically obtained from other APIs rather than created directly in SSL.

Common sources are:

- `oTable:Columns:Get(nIndex)`
- `oTable:Columns:Get("column_name")`
- `oTable:PkColumns[nIndex]`

## Properties

| Name | Type | Access | Description |
| --- | --- | --- | --- |
| `DBType` | [number](../types/number.md) | read-only | Numeric type code for the column. Unknown types return `0`. |
| `FType` | [string](../types/string.md) | read-only | Type label for the column, such as `SQL_INTEGER`, `SQL_VARCHAR`, `SQL_DATE`, or `SQL_BINARY`. Unknown types return an empty string. |
| `IsBlob` | [boolean](../types/boolean.md) | read-only | [`.T.`](../literals/true.md) when the column stores binary data. |
| `IsPk` | [boolean](../types/boolean.md) | read-only | [`.T.`](../literals/true.md) when the column is part of the table's current primary key. |
| `Length` | [number](../types/number.md) | read-write | Maximum length for the column. |
| `Name` | [string](../types/string.md) | read-write | Column name. |
| `Scale` | [number](../types/number.md) | read-only | Always returns `0`. |

Known type mappings for `DBType` and `FType`:

| Data kind | `DBType` | `FType` |
| --- | --- | --- |
| Boolean | `-7` | `SQL_BIT` |
| Byte | `-6` | `SQL_TINYINT` |
| Date | `9` | `SQL_DATE` |
| Decimal | `8` | `SQL_DOUBLE` |
| Double | `6` | `SQL_FLOAT` |
| Short integer | `5` | `SQL_SMALLINT` |
| Integer | `4` | `SQL_INTEGER` |
| Long integer | `-5` | `SQL_BIGINT` |
| Float | `7` | `SQL_REAL` |
| String | `12` | `SQL_VARCHAR` |
| Binary | `-2` | `SQL_BINARY` |

## Methods

`CDataColumn` does not expose methods. Use its properties to inspect or update column metadata.

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Check `IsPk` when you need to identify key columns instead of inferring keys from names.
    - Check `IsBlob` before treating a column's values as text.
    - Use `DBType` or `FType` when branching on column type in import or transformation logic.
    - Update `Name` and `Length` only when you intentionally want to change the table definition.

!!! failure "Don't"
    - Assume every familiar column name is part of the primary key — `IsPk` exposes that directly.
    - Treat binary columns as text — `IsBlob` marks columns that need binary-safe handling.
    - Rely on `Scale` for numeric precision — it always returns `0`.
    - Expect assignments to `DBType`, `FType`, `IsBlob`, `IsPk`, or `Scale` to change column metadata.

## Caveats

- Changing `Name` or `Length` updates column metadata, not existing row values.

## Examples

### Inspect columns from a table

This example loops through a table's columns and reports the metadata exposed by each `CDataColumn`.

```ssl
:PROCEDURE DisplayColumnInfo;
	:DECLARE oTablesImport, oTable, oColumns, oColumn;
	:DECLARE nColCount, nIndex, sColInfo;

	oTablesImport := TablesImport{"C:/Import"};
	oTable := oTablesImport:GetTable("limsusers");
	oColumns := oTable:Columns;
	nColCount := oColumns:Count;
	nIndex := 1;

	:WHILE nIndex <= nColCount;
		oColumn := oColumns:Get(nIndex);
		sColInfo := oColumn:Name + " | " + oColumn:FType;
		sColInfo := sColInfo + " | Len=" + LimsString(oColumn:Length);

		:IF oColumn:IsPk;
			sColInfo := sColInfo + " | PK";
		:ENDIF;

		:IF oColumn:IsBlob;
			sColInfo := sColInfo + " | BLOB";
		:ENDIF;

		UsrMes(sColInfo);
		nIndex++;
	:ENDWHILE;
:ENDPROC;

/* Usage;
DoProc("DisplayColumnInfo");
```

[`UsrMes`](../functions/UsrMes.md) displays (one line per column; actual names and types depend on the table):

```text
user_id | SQL_INTEGER | Len=10 | PK
username | SQL_VARCHAR | Len=50
created_date | SQL_DATE | Len=-1
photo | SQL_BINARY | Len=-1 | BLOB
```

### Rename a column and adjust its length

This example retrieves one column by name, updates the writable metadata, and logs the result.

```ssl
:PROCEDURE UpdateColumnMetadata;
	:DECLARE oTablesImport, oTable, oColumn;
	:DECLARE sOldName;

	oTablesImport := TablesImport{"C:/Import"};
	oTable := oTablesImport:GetTable("limsusers");
	oColumn := oTable:Columns:Get("username");

	:IF oColumn:IsPk;
		ErrorMes("Column Error", "username is a primary key column");
		:RETURN .F.;
	:ENDIF;

	sOldName := oColumn:Name;
	oColumn:Name := "user_name";
	oColumn:Length := 80;

	UsrMes("Updated " + sOldName + " to " + oColumn:Name 
			+ " with length " + LimsString(oColumn:Length));

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("UpdateColumnMetadata");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Updated username to user_name with length 80
```

## Related

- [`CDataColumns`](CDataColumns.md)
- [`CDataTable`](CDataTable.md)
- [`TablesImport`](TablesImport.md)
