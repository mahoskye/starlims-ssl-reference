---
title: "BuildString2"
summary: "Builds one string from a two-dimensional array using separate row and column delimiters."
id: ssl.function.buildstring2
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# BuildString2

Builds one string from a two-dimensional array using separate row and column delimiters.

`BuildString2` treats each top-level element of `aTarget` as a row array. It joins the values inside each row with `sColDelimiter`, then joins those row strings with `sLineDelimiter`.

If `sLineDelimiter` is omitted or [`NIL`](../literals/nil.md), the default row delimiter is `";"`. If `sColDelimiter` is omitted or [`NIL`](../literals/nil.md), the default column delimiter is `","`.

Each row is processed with the same behavior as [`BuildString`](BuildString.md): values are converted to text, trimmed with [`AllTrim`](AllTrim.md), and [`NIL`](../literals/nil.md) cell values are written as the literal text [`NIL`](../literals/nil.md).

## When to use

- When you need to serialize a two-dimensional array into one string.
- When you need rows and columns to use different delimiters.
- When you want the same trimming and [`NIL`](../literals/nil.md) rendering behavior as [`BuildString`](BuildString.md) applied to each row.
- When you need to export or log simple table-like data.

## Syntax

```ssl
BuildString2(aTarget, [sLineDelimiter], [sColDelimiter])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aTarget` | [array](../types/array.md) | yes | — | Two-dimensional source array. Each top-level element must be a row array. |
| `sLineDelimiter` | [string](../types/string.md) | no | `";"` | Delimiter inserted between row strings. |
| `sColDelimiter` | [string](../types/string.md) | no | `","` | Delimiter inserted between values inside each row. |

## Returns

**[string](../types/string.md)** — A string built by joining each row with `sLineDelimiter` after each row is joined with `sColDelimiter`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aTarget` is [`NIL`](../literals/nil.md). | `Target array cannot be null.` |
| Any top-level element is [`NIL`](../literals/nil.md) or not an array. | `Target array cannot be null.` |

## Best practices

!!! success "Do"
    - Pass a real two-dimensional array where every top-level element is a row array.
    - Choose row and column delimiters that do not appear in the data when the result will be parsed later.
    - Use [`BuildString`](BuildString.md) directly when you only need to join a one-dimensional array.
    - Expect row values to be trimmed and [`NIL`](../literals/nil.md) cells to appear as the literal text [`NIL`](../literals/nil.md).

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `aTarget`. The function raises an error immediately.
    - Mix row arrays with scalar top-level values or [`NIL`](../literals/nil.md) rows. Row serialization fails because each top-level element must be an array.
    - Assume delimiters are escaped or quoted in the output. The function only joins text.
    - Use `BuildString2` when you need SQL-safe quoting. Use helpers such as [`BuildStringForIn`](BuildStringForIn.md) or [`PrepareArrayForIn`](PrepareArrayForIn.md) for that use case.

## Caveats

- An empty top-level array returns an empty string.
- An empty row array contributes an empty row segment.
- [`NIL`](../literals/nil.md) cell values inside a row become the literal text [`NIL`](../literals/nil.md).
- Row values are trimmed before joining because each row is processed through [`BuildString`](BuildString.md).
- The function accepts jagged row arrays. It does not require every row to have the same length.

## Examples

### Join a small grid with the default delimiters

Uses the default `";"` row delimiter and `","` column delimiter to serialize a header-plus-data grid into one string.

```ssl
:PROCEDURE ShowGridAsText;
	:DECLARE aGrid, sResult;

	aGrid := {{"Product", "Qty"}, {"Widget", 5}, {"Gadget", 3}};
	sResult := BuildString2(aGrid);

	UsrMes(sResult);

	:RETURN sResult;
:ENDPROC;

/* Usage;
DoProc("ShowGridAsText");
```

[`UsrMes`](UsrMes.md) displays:

```
Product,Qty;Widget,5;Gadget,3
```

### Use custom row and column delimiters

Formats three instrument readings for a system that expects one record per line and pipe-separated columns, by passing `Chr(13) + Chr(10)` as the row delimiter.

```ssl
:PROCEDURE ExportInstrumentRows;
	:DECLARE aRows, sExport, sLineDelimiter, sColDelimiter;

	aRows := {
		{"SAM-1001", "pH", 7.2},
		{"SAM-1002", "Cond", 15.8},
		{"SAM-1003", "Temp", 22.4}
	};

	sLineDelimiter := Chr(13) + Chr(10);
	sColDelimiter := "|";

	sExport := BuildString2(aRows, sLineDelimiter, sColDelimiter);

	UsrMes(sExport);

	:RETURN sExport;
:ENDPROC;

/* Usage;
DoProc("ExportInstrumentRows");
```

[`UsrMes`](UsrMes.md) displays:

```
SAM-1001|pH|7.2
SAM-1002|Cond|15.8
SAM-1003|Temp|22.4
```

### Show trimming, [`NIL`](../literals/nil.md) cells, and empty rows

Demonstrates trimming, [`NIL`](../literals/nil.md) cell handling, and empty-row behavior inherited from [`BuildString`](BuildString.md) using a jagged input with a [`NIL`](../literals/nil.md) middle cell and an empty row array.

```ssl
:PROCEDURE ShowBuildString2Behavior;
	:DECLARE aRows, sResult;

	aRows := {
		{"  A  ", NIL, "  C  "},
		{},
		{"  D  ", "E"}
	};

	sResult := BuildString2(aRows, "|", "/");

	UsrMes(sResult);

	:RETURN sResult;
:ENDPROC;

/* Usage;
DoProc("ShowBuildString2Behavior");
```

[`UsrMes`](UsrMes.md) displays:

```
A/NIL/C||D/E
```

## Related

- [`BuildArray`](BuildArray.md)
- [`BuildArray2`](BuildArray2.md)
- [`BuildString`](BuildString.md)
- [`BuildStringForIn`](BuildStringForIn.md)
- [`ExtractCol`](ExtractCol.md)
- [`PrepareArrayForIn`](PrepareArrayForIn.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
