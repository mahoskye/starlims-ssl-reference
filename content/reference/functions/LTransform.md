---
title: "LTransform"
summary: "Formats a numeric expression as a string by applying a picture string."
id: ssl.function.ltransform
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LTransform

Formats a numeric expression as a string by applying a picture string.

If `vExpression` is [`NIL`](../literals/nil.md), `LTransform` returns an empty string. If `vExpression` is not numeric, it returns the value's string representation and does not apply the picture. For numeric input, `sPicture` is applied after converting both [`#`](../operators/hash.md) and `9` placeholders to `0`, so those placeholder characters behave the same in this function.

After formatting a numeric value, `LTransform` replaces leading zeroes with spaces until it reaches the digit immediately before the decimal point. For negative values, the minus sign is moved so it appears just before the first non-space digit.

## When to use

- When you need a numeric value displayed with a fixed mask rather than the default string conversion.
- When report or export output needs aligned numeric columns with predictable spacing.
- When you want a non-numeric fallback to pass through as plain text without a separate conversion step.

## Syntax

```ssl
LTransform(vExpression, sPicture)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vExpression` | any | yes | — | Value to convert. Numeric values use the picture; non-numeric values are returned as plain text. |
| `sPicture` | [string](../types/string.md) | yes | — | Numeric picture string used when `vExpression` is numeric. In `LTransform`, [`#`](../operators/hash.md) and `9` are treated the same as `0`. |

## Returns

**[string](../types/string.md)** — A formatted string for numeric input, the plain string value for non-numeric input, or an empty string when `vExpression` is [`NIL`](../literals/nil.md).

## Best practices

!!! success "Do"
    - Use `LTransform` when you need a specific numeric display mask instead of a generic conversion.
    - Choose a picture string that matches the width and decimal precision you actually need in the output.
    - Handle mixed-type input deliberately when the picture should apply only to numeric values.

!!! failure "Don't"
    - Assume [`#`](../operators/hash.md) and `9` behave differently in `LTransform`. Both are converted to `0` before formatting.
    - Expect `sPicture` to affect strings, dates, or other non-numeric values. Non-numeric input is returned as plain text.
    - Assume a [`NIL`](../literals/nil.md) input will be preserved as `"NIL"` or raise an error. `LTransform` returns an empty string instead.

## Examples

### Format a value with fixed decimals

Format a single numeric result for display. `LTransform(1234.5, "9999.00")` replaces leading zeros with spaces; `1234.5` has no leading zeros in a four-digit integer field, so the result is `"1234.50"`.

```ssl
:PROCEDURE ShowFormattedResult;
	:DECLARE nResult, sFormatted;

	nResult := 1234.5;
	sFormatted := LTransform(nResult, "9999.00");

	UsrMes("Formatted result: [" + sFormatted + "]");

	:RETURN sFormatted;
:ENDPROC;

/* Usage;
DoProc("ShowFormattedResult");
```

[`UsrMes`](UsrMes.md) displays:

```text
Formatted result: [1234.50]
```

### Align positive and negative values

Use the same picture string so multiple numeric values line up consistently. Leading zeros become spaces, and the minus sign is moved immediately before the first non-space digit.

```ssl
:PROCEDURE ShowAlignedValues;
	:DECLARE aValues, aLines, nIndex, nValue, sLine, sOutput;

	aValues := {12.5, (0 - 3.25), 0.5};
	aLines := {};

	:FOR nIndex := 1 :TO ALen(aValues);
		nValue := aValues[nIndex];
		sLine := "[" + LTransform(nValue, "9999.00") + "]";
		AAdd(aLines, sLine);
	:NEXT;

	sOutput := aLines[1] + Chr(13) + Chr(10);
	sOutput := sOutput + aLines[2] + Chr(13) + Chr(10);
	sOutput := sOutput + aLines[3];

	UsrMes(sOutput);

	:RETURN sOutput;
:ENDPROC;

/* Usage;
DoProc("ShowAlignedValues");
```

[`UsrMes`](UsrMes.md) displays:

```text
[  12.50]
[  -3.25]
[   0.50]
```

### Apply the picture only to numeric items

Guard mixed input so numbers are formatted with `LTransform` and other values keep their plain text form. [`NIL`](../literals/nil.md) items produce an empty slot; the minus sign on `-7.0` is placed immediately before the first non-space digit.

```ssl
:PROCEDURE FormatMixedValues;
	:DECLARE aValues, aOutput, nIndex, vValue, sValue, sMessage;

	aValues := {1250.5, "Pending", NIL, (0 - 7.0)};
	aOutput := {};

	:FOR nIndex := 1 :TO ALen(aValues);
		vValue := aValues[nIndex];

		:IF Empty(vValue);
			sValue := "";
		:ELSE;
			:IF LimsTypeEx(vValue) == "NUMERIC";
				sValue := LTransform(vValue, "9999.00");
			:ELSE;
				sValue := LimsString(vValue);
			:ENDIF;
		:ENDIF;

		AAdd(aOutput, sValue);
	:NEXT;

	sMessage := aOutput[1] + " | " + aOutput[2] + " | " + aOutput[3];
	sMessage := sMessage + " | " + aOutput[4];

	UsrMes(sMessage);

	:RETURN sMessage;
:ENDPROC;

/* Usage;
DoProc("FormatMixedValues");
```

[`UsrMes`](UsrMes.md) displays:

```text
1250.50 | Pending |  |   -7.00
```

## Related

- [`LStr`](LStr.md)
- [`Str`](Str.md)
- [`StrZero`](StrZero.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
