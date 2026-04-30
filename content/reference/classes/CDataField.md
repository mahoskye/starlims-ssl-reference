---
title: "CDataField"
summary: "Represents one field in a CDataRow."
id: ssl.class.cdatafield
element_type: class
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CDataField

Represents one field in a [`CDataRow`](CDataRow.md).

`CDataField` is the field object returned by `CDataRow:GetField()`. Use it when you need to read or update a single column value, check whether that value is null, or ask for a string, number, or date result explicitly.

For binary columns, `Value` behaves differently from ordinary fields. Reading it writes the current bytes to a file under the table's import folder and returns that file path. Writing it expects a string path to an existing file, then loads that file's contents into the field.

## When to use

- When you need to inspect or update one field in a [`CDataRow`](CDataRow.md).
- When you want an explicit conversion step for a field that should contain a string, number, or date.
- When you need the current value rendered as SQL literal text for ad hoc SQL string-building.
- When working with binary fields exposed through a table import folder.

## Constructors

No standalone SSL constructor is documented for this class.

Obtain `CDataField` instances by calling `GetField()` on a [`CDataRow`](CDataRow.md).

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `IsNull` | [boolean](../types/boolean.md) | read-only | [`.T.`](../literals/true.md) when the field value is null |
| `Value` | any | read-write | Gets or sets the field value. For binary fields, reading returns a file path and writing expects a file path instead of raw bytes. |

## Methods

### `GetSqlFormattedValue`

Returns the current field value as SQL literal text.

- String values are wrapped in single quotes.
- Date values are returned as timestamp literals.
- Other values use their normal string form.

**Returns:** [string](../types/string.md) — SQL literal text for the current value

### `ToDate`

Returns the field value as a date when the value is already a date or when a string value matches `MM/dd/yyyy` or `yyyy-MM-dd` exactly.

**Returns:** [date](../types/date.md) — Converted date, or [`NIL`](../literals/nil.md) when conversion is not possible

### `ToNumber`

Returns the field value as a number when the value is already numeric or when a string value can be parsed as a number.

**Returns:** [number](../types/number.md) — Converted number

### `ToString`

Returns the field value when it is a string.

**Returns:** [string](../types/string.md) — String value, or [`NIL`](../literals/nil.md) for non-string values

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Get `CDataField` instances by calling `GetField()` on a [`CDataRow`](CDataRow.md) so the field stays tied to a real row and column.
    - Check `IsNull` before formatting or converting values that may be null.
    - Use `ToDate()`, `ToNumber()`, or `ToString()` when you want explicit type handling instead of relying on `Value`.
    - Set `Value := NIL` when you want to clear a non-binary field.
    - Make sure the parent table has a valid `ImportFolder` before reading a binary field through `Value`.

!!! failure "Don't"
    - Treat `GetSqlFormattedValue()` as a safe replacement for parameterized SQL — it only formats the current value and does not bind parameters or escape every SQL case.
    - Assume `ToString()` converts every value to text — it returns [`NIL`](../literals/nil.md) for non-string values.
    - Assume `ToDate()` accepts arbitrary date formats — it only parses `MM/dd/yyyy` and `yyyy-MM-dd` strings.
    - Assign a non-string value to a binary field — binary assignment expects a file path and raises an error for the wrong type.
    - Assign a missing file path to a binary field — the assignment fails when the file does not exist.
    - Expect `ToNumber()` to convert arbitrary value types — non-string, non-numeric values can fail instead of returning [`NIL`](../literals/nil.md).

## Caveats

- For non-binary fields, assigning [`NIL`](../literals/nil.md) stores a null value.
- `ToNumber()` may raise an error when the current value is not numeric and is not a parsable string.
- For binary fields, reading `Value` depends on a usable table import folder.
- For binary fields, assigning `Value` requires a string file path that already exists.

## Examples

### Read a field and convert it safely

Get a field from a row, check for null, and convert it only when a value is present.

```ssl
:PROCEDURE ReadUserNameField;
	:DECLARE oImport, oTable, oRow, oField, sUserName;

	oImport := TablesImport{"C:/Import"};
	oTable := oImport:GetTable("limsusers");
	oRow := oTable:Rows[1];
	oField := oRow:GetField("user_name");

	:IF oField:IsNull;
		UsrMes("user_name is null");
		:RETURN NIL;
	:ENDIF;

	sUserName := oField:ToString();
	UsrMes("User name: " + sUserName);

	:RETURN sUserName;
:ENDPROC;

/* Usage;
DoProc("ReadUserNameField");
```

### Update a field value in a row

Write a new value to a field and then read it back from the same row.

```ssl
:PROCEDURE UpdateStatusField;
	:DECLARE oImport, oTable, oRow, oField;

	oImport := TablesImport{"C:/Import"};
	oTable := oImport:GetTable("sample");
	oRow := oTable:Rows[1];
	oField := oRow:GetField("status");

	oField:Value := "Complete";

	UsrMes("Updated status: " + oField:ToString());
	:RETURN oField:Value;
:ENDPROC;

/* Usage;
DoProc("UpdateStatusField");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Updated status: Complete
```

### Work with a binary field through a file path

Read a binary field to a file path, then write updated contents back from a different file.

```ssl
:PROCEDURE CopyBinaryField;
	:DECLARE oImport, oTable, oRow, oField;
	:DECLARE sExportedFile, sReplacementFile;

	oImport := TablesImport{"C:/Import"};
	oTable := oImport:GetTable("attachments");
	oRow := oTable:Rows[1];
	oField := oRow:GetField("attachment_blob");

	sExportedFile := oField:Value;
	UsrMes("Binary field exported to: " + sExportedFile);

	sReplacementFile := "C:/Import/replacement.bin";
	oField:Value := sReplacementFile;

	:RETURN oField:Value;
:ENDPROC;

/* Usage;
DoProc("CopyBinaryField");
```

[`UsrMes`](../functions/UsrMes.md) displays (the filename is derived from the binary content hash):

```text
Binary field exported to: C:/Import/a3f2b1c4d5e6f7890123456789abcdef.bin
```

### Format a field value for SQL string building

Use the helper when you need the current field rendered as a SQL literal.

```ssl
:PROCEDURE BuildFilterFromField;
	:DECLARE oImport, oTable, oRow, oField, sWhere;

	oImport := TablesImport{"C:/Import"};
	oTable := oImport:GetTable("sample");
	oRow := oTable:Rows[1];
	oField := oRow:GetField("sample_id");

	:IF oField:IsNull;
		sWhere := "sample_id IS NULL";
		UsrMes(sWhere);
	:ELSE;
		sWhere := "sample_id = " + oField:GetSqlFormattedValue();
		/* Displays: generated WHERE clause;
		UsrMes(sWhere);
	:ENDIF;

	:RETURN sWhere;
:ENDPROC;

/* Usage;
DoProc("BuildFilterFromField");
```

## Related

- [`CDataColumn`](CDataColumn.md)
- [`CDataRow`](CDataRow.md)
- [`CDataTable`](CDataTable.md)
