---
title: "Str"
summary: "Converts a numeric value to a formatted string."
id: ssl.function.str
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Str

Converts a numeric value to a formatted string.

`Str()` returns a character representation of `nNumber` with optional field width and decimal control. The result is space-padded on the left rather than zero-padded, which makes it useful for aligned text output. If you omit both optional parameters, integer values default to a 10-character field with no decimals, while non-integer values default to a 20-character field with 9 decimal places. If the requested format cannot fit the value, the function returns a field of asterisks.

## When to use

- When you need fixed-width numeric text for reports, exports, or aligned output.
- When you want explicit control over the displayed decimal places.
- When you need the same core formatting as [`StrZero`](StrZero.md) but with leading spaces instead of leading zeros.

## Syntax

```ssl
Str(nNumber, [nLength], [nDecimals])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nNumber` | [number](../types/number.md) | yes | — | Numeric value to convert. |
| `nLength` | [number](../types/number.md) | no | depends on call pattern | Total field width. If omitted, the function chooses a default width based on the other arguments and the value. |
| `nDecimals` | [number](../types/number.md) | no | depends on call pattern | Number of decimal places to include. If omitted while `nLength` is supplied, `Str()` keeps as many source decimals as will fit in the field. |

## Returns

**[string](../types/string.md)** — A formatted numeric string, usually left-padded with spaces.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `nNumber` is [`NIL`](../literals/nil.md). | `Argument nNumber cannot be null.` |

## Best practices

!!! success "Do"
    - Specify both `nLength` and `nDecimals` when the output must have a predictable width and precision.
    - Trim the result with [`LTrim`](LTrim.md)`()` if you want the formatted value without the leading padding.
    - Use [`LStr`](LStr.md)`()` when you need a simple trimmed conversion or need to handle [`NIL`](../literals/nil.md) input without an error.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) as `nNumber`. `Str()` raises an error instead of returning a placeholder string.
    - Assume `Str(nNumber)` returns an unpadded value. Default output commonly includes leading spaces.
    - Ignore an all-asterisk result. That indicates the requested field width cannot represent the value.

## Caveats

- If the formatted value does not fit in the requested width, `Str()` returns a string of [`*`](../operators/multiply.md) characters of that width.
- When `nLength` is supplied and `nDecimals` is omitted, the function keeps fractional digits only as long as they fit in the field.
- Negative values are padded so that the minus sign stays immediately before the first visible digit.
- A negative `nLength` uses the current numeric separator settings when formatting the result. See [`SetDecimalSeparator`](SetDecimalSeparator.md) and [`SetGroupSeparator`](SetGroupSeparator.md).

## Examples

### Convert a number and remove the default left padding

Show a simple conversion, then trim the leading spaces for display.

```ssl
:PROCEDURE ShowSampleCount;
    :DECLARE nCount, sRawText, sDisplayText;

    nCount := 42;
    sRawText := Str(nCount);
    sDisplayText := LTrim(sRawText);

    UsrMes("Raw field: [" + sRawText + "]");
    UsrMes("Trimmed value: " + sDisplayText);
:ENDPROC;

/* Usage;
DoProc("ShowSampleCount");
```

[`UsrMes`](UsrMes.md) displays:

```text
Raw field: [        42]
Trimmed value: 42
```

### Format aligned values for a report line

Use explicit width and decimals so numeric columns line up consistently.

```ssl
:PROCEDURE BuildReportLine;
    :DECLARE sSampleID, nResult, nAverage, sLine;

    sSampleID := "S-1024";
    nResult := 7.2;
    nAverage := 12.3456;

    sLine := sSampleID + Replicate(" ", 10 - Len(sSampleID))
        + Str(nResult, 8, 2)
        + Str(nAverage, 10, 3);

    UsrMes("Sample      Result   Average");
    UsrMes(sLine);
:ENDPROC;

/* Usage;
DoProc("BuildReportLine");
```

[`UsrMes`](UsrMes.md) displays:

```text
Sample      Result   Average
S-1024        7.20    12.346
```

### Detect overflow before exporting fixed-width values

Check for the asterisk overflow result before writing fixed-width numeric text.

```ssl
:PROCEDURE ExportReading;
    :DECLARE nReading, sFormatted, sOutput;

    nReading := 123456.789;
    sFormatted := Str(nReading, 8, 2);

    :IF sFormatted == Replicate("*", 8);
        ErrorMes("Reading does not fit in the export field");
        :RETURN .F.;
    :ENDIF;

    sOutput := "READING=" + sFormatted;
    UsrMes(sOutput);

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ExportReading");
```

[`UsrMes`](UsrMes.md) displays:

```text
READING=123456.79
```

If the value does not fit the requested width, [`ErrorMes`](ErrorMes.md) displays `Reading does not fit in the export field` and the procedure returns `.F.`.

## Related

- [`LStr`](LStr.md)
- [`LTransform`](LTransform.md)
- [`StrZero`](StrZero.md)
- [`SetDecimalSeparator`](SetDecimalSeparator.md)
- [`SetGroupSeparator`](SetGroupSeparator.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
