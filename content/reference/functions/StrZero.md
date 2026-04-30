---
title: "StrZero"
summary: "Formats a number as a zero-padded string, with optional total width and decimal precision."
id: ssl.function.strzero
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# StrZero

Formats a number as a zero-padded string, with optional total width and decimal precision.

`StrZero` is used when you need a fixed-width numeric string for display, export, or identifiers. It pads the integer portion with leading zeroes and can include a fixed number of decimal places. When `nLength` and `nDecimals` are both omitted, integers default to a 10-character field and non-integers to a 20-character field with up to 9 decimal places. When the requested width cannot hold the formatted value, the function returns a string of [`*`](../operators/multiply.md) characters of that width.

## When to use

- When aligning numbers with leading zeros for output in reports, lists, or documents.
- When formatting identifiers, reference numbers, or serial codes that require a fixed length containing zeros.
- When exporting numeric data to external systems that mandate a specific width or decimal precision.
- When displaying financial values with uniform width and consistent decimal places for readability.

## Syntax

```ssl
StrZero(nNumber, [nLength], [nDecimals])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `nNumber` | [number](../types/number.md) | yes | — | Number to format. |
| `nLength` | [number](../types/number.md) | no | depends on call pattern | Total output width. |
| `nDecimals` | [number](../types/number.md) | no | depends on call pattern | Number of decimal places. |

## Returns

**[string](../types/string.md)** — The formatted number, left-padded with zeros to the requested width. Returns a string of [`*`](../operators/multiply.md) characters when the value overflows the requested width.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `nNumber` is [`NIL`](../literals/nil.md) and at least one optional argument is supplied. | `nNumber argument cannot be null.` |

## Best practices

!!! success "Do"
    - Specify `nLength` and `nDecimals` explicitly when an export or interface requires a fixed format.
    - Check for an all-asterisk result when the value might not fit the requested width.
    - Validate that `nNumber` is not [`NIL`](../literals/nil.md) before calling `StrZero`.

!!! failure "Don't"
    - Rely on the default width when downstream code expects a specific field size.
    - Treat an all-asterisk result as valid formatted data.
    - Pass [`NIL`](../literals/nil.md) for `nNumber`; depending on the other arguments, the function either raises or returns an empty string.

## Caveats

- If all three arguments are [`NIL`](../literals/nil.md), `StrZero` returns an empty string without raising.
- If both `nLength` and `nDecimals` are negative, `StrZero` falls back to the default width and decimal behavior.
- When `nDecimals` is supplied, the output uses the current SSL decimal separator setting.

## Examples

### Pad an invoice number to a fixed width

Display invoice numbers as zero-padded 8-character strings for consistent visual alignment.

```ssl
:PROCEDURE FormatInvoiceCode;
	:DECLARE nInvoiceNum, sInvoiceCode;

	nInvoiceNum := 4528;
	sInvoiceCode := StrZero(nInvoiceNum, 8);

	UsrMes("Invoice code: " + sInvoiceCode);
:ENDPROC;

/* Usage;
DoProc("FormatInvoiceCode");
```

[`UsrMes`](UsrMes.md) displays:

```text
Invoice code: 00004528
```

### Format a measurement value for export

Export a numeric result with a fixed total width and three decimal places.

```ssl
:PROCEDURE FormatMeasurementForExport;
	:DECLARE nMeasurement, nLength, nDecimals, sFormatted, sOutputLine, sSampleID;

	nMeasurement := 12.37658;
	nLength := 10;
	nDecimals := 3;
	sSampleID := "LAB-2024-0042";

	sFormatted := StrZero(nMeasurement, nLength, nDecimals);
	sOutputLine := sSampleID + "," + sFormatted;

	UsrMes(sOutputLine);

	:RETURN sFormatted;
:ENDPROC;

/* Usage;
DoProc("FormatMeasurementForExport");
```

[`UsrMes`](UsrMes.md) displays:

```text
LAB-2024-0042,000012.377
```

### Detect and report overflow before export

Detect the documented overflow case where `StrZero` returns an all-asterisk string.

```ssl
:PROCEDURE FormatResultValue;
	:PARAMETERS nValue, nWidth, nDecimals;
	:DEFAULT nWidth, 8;
	:DEFAULT nDecimals, 2;
	:DECLARE sFormatted, sOverflow;

	sFormatted := StrZero(nValue, nWidth, nDecimals);
	sOverflow := Replicate("*", nWidth);

	:IF sFormatted == sOverflow;
		ErrorMes(
			"Formatted value overflowed width "
			+ LimsString(nWidth)
			+ " for value "
			+ LimsString(nValue)
		);
		:RETURN "";
	:ENDIF;

	:RETURN sFormatted;
:ENDPROC;

/* Usage;
DoProc("FormatResultValue", {123456.78, 8, 2});
```

## Related

- [`LStr`](LStr.md)
- [`LTransform`](LTransform.md)
- [`Str`](Str.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
