---
title: "BuildArray2"
summary: "Parses text into a two-dimensional array using separate row and column delimiters."
id: ssl.function.buildarray2
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# BuildArray2

Parses text into a two-dimensional array using separate row and column delimiters.

`BuildArray2` returns an array of row arrays. It splits `sText` into rows using `sLineDelimiter`, then splits each row into columns using `sColDelimiter`.

If optional parameters are omitted, these defaults apply: `sLineDelimiter = ";"`, `sColDelimiter = ","`, `bCrlfOk = .F.`, and `bTrimSpaces = .T.`. If `sText` is [`NIL`](../literals/nil.md) or contains only whitespace after trimming, the function returns `{{""}}`.

When `bTrimSpaces` is [`.T.`](../literals/true.md), each returned row token and each returned cell is trimmed with [`AllTrim`](AllTrim.md). When `bCrlfOk` is [`.F.`](../literals/false.md), CR/LF pairs are removed from each row before that row is split into columns. This affects column values only; row splitting still depends on the literal `sLineDelimiter` you pass.

## When to use

- When you need to parse delimited table-style text into rows and columns.
- When you need to convert imported flat-file content into a 2D array you can loop through.
- When you need to handle custom row and column separators without writing nested split logic.

## Syntax

```ssl
BuildArray2(sText, [sLineDelimiter], [sColDelimiter], [bCrlfOk], [bTrimSpaces])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sText` | [string](../types/string.md) | yes | — | Source text to parse. [`NIL`](../literals/nil.md) or whitespace-only input returns `{{""}}`. |
| `sLineDelimiter` | [string](../types/string.md) | no | `";"` | Literal delimiter used to split the source text into rows. |
| `sColDelimiter` | [string](../types/string.md) | no | `","` | Literal delimiter used to split each row into columns. |
| `bCrlfOk` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | When [`.F.`](../literals/false.md), removes CR/LF pairs from each row before splitting it into columns. |
| `bTrimSpaces` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | When [`.T.`](../literals/true.md), trims leading and trailing spaces from each returned cell. |

## Returns

**[array](../types/array.md)** — A two-dimensional array of strings. Each top-level element is a row array.

## Best practices

!!! success "Do"
    - Pass both delimiters explicitly when the source format is known.
    - Pass the actual row separator when parsing newline-delimited text.
    - Leave `bTrimSpaces` enabled unless leading or trailing spaces are meaningful data.
    - Handle the `{{""}}` result when `sText` may be [`NIL`](../literals/nil.md) or whitespace-only.
    - Set `bCrlfOk` to [`.T.`](../literals/true.md) when row text may contain embedded CR/LF that
      must stay inside a column value.

!!! failure "Don't"
    - Assume empty input returns `{}`. `BuildArray2` returns one row with one empty string.
    - Assume CR/LF characters create rows automatically. Rows are split only on `sLineDelimiter`.
    - Assume `bCrlfOk` changes how rows are detected. It affects column splitting within each row.
    - Use `BuildArray2` as a quoted CSV parser. It performs literal delimiter splitting only.
    - Treat the result as a flat array. Each element at the top level is a row array.
    - Assume adjacent delimiters are skipped. They produce empty rows or empty columns in the result.
    - Assume single-character delimiter constraints. Multi-character strings are valid and matched literally.

## Caveats

- When `sLineDelimiter` is not found in `sText`, the result contains one row. When `sColDelimiter` is not found in a row, that row contains one column.

## Examples

### Parse simple row and column data

Uses the default `";"` row delimiter and `","` column delimiter to parse a semicolon-separated table into three rows, each with three fields.

```ssl
:PROCEDURE ParseSimpleTable;
	:DECLARE sTableText, aRows, aRow, nRow, nCol, sMessage;

	sTableText := "Name,Department,Role;Jane Smith,Quality,Analyst;"
				  + "John Davis,Production,Technician";
	aRows := BuildArray2(sTableText);

	sMessage := "Rows parsed: " + LimsString(ALen(aRows));

	:FOR nRow := 1 :TO ALen(aRows);
		aRow := aRows[nRow];
		sMessage := sMessage + Chr(13) + Chr(10)
					+ "Row " + LimsString(nRow) + ": ";

		:FOR nCol := 1 :TO ALen(aRow);
			:IF nCol > 1;
				sMessage := sMessage + " | ";
			:ENDIF;

			sMessage := sMessage + aRow[nCol];
		:NEXT;
	:NEXT;

	UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("ParseSimpleTable");
```

[`UsrMes`](UsrMes.md) displays:

```
Rows parsed: 3
Row 1: Name | Department | Role
Row 2: Jane Smith | Quality | Analyst
Row 3: John Davis | Production | Technician
```

### Use custom delimiters for imported records

Passes `"##"` as the row separator and `"|"` as the column separator to parse an import string where standard delimiters are already in the data.

```ssl
:PROCEDURE ParseImportedRecords;
	:DECLARE sImportText, aRows, aRow, nRow, sSummary;

	sImportText := "S-1001|Logged|25.4##S-1002|Pending|18.3##"
					+ "S-1003|Closed|22.1";
	aRows := BuildArray2(sImportText, "##", "|", .F., .T.);

	sSummary := "Imported records:";

	:FOR nRow := 1 :TO ALen(aRows);
		aRow := aRows[nRow];
		sSummary := sSummary + Chr(13) + Chr(10)
					+ aRow[1] + " -> " + aRow[2] + " -> " + aRow[3];
	:NEXT;

	UsrMes(sSummary);
:ENDPROC;

/* Usage;
DoProc("ParseImportedRecords");
```

[`UsrMes`](UsrMes.md) displays:

```
Imported records:
S-1001 -> Logged -> 25.4
S-1002 -> Pending -> 18.3
S-1003 -> Closed -> 22.1
```

### Preserve embedded CRLF inside a column value

Sets `bCrlfOk := .T.` so that the CR/LF inside the first row's notes column is not stripped, while `"||ROW||"` still splits the two records cleanly.

```ssl
:PROCEDURE ParseRowsWithNotes;
	:DECLARE sBatchText, aRows, aRow, sPreview;

	sBatchText := "S-1001|Logged|First note line" + Chr(13) + Chr(10)
					+ "Second note line"
					+ "||ROW||"
					+ "S-1002|Pending|Single line note";

	aRows := BuildArray2(sBatchText, "||ROW||", "|", .T., .T.);

	aRow := aRows[1];
	sPreview := "Sample: " + aRow[1] + Chr(13) + Chr(10)
				+ "Status: " + aRow[2] + Chr(13) + Chr(10)
				+ "Notes:" + Chr(13) + Chr(10)
				+ aRow[3];

	UsrMes(sPreview);
:ENDPROC;

/* Usage;
DoProc("ParseRowsWithNotes");
```

[`UsrMes`](UsrMes.md) displays:

```
Sample: S-1001
Status: Logged
Notes:
First note line
Second note line
```

## Related

- [`BuildArray`](BuildArray.md)
- [`BuildString`](BuildString.md)
- [`BuildString2`](BuildString2.md)
- [`BuildStringForIn`](BuildStringForIn.md)
- [`ExtractCol`](ExtractCol.md)
- [`PrepareArrayForIn`](PrepareArrayForIn.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
