---
title: "LimsString"
summary: "Converts a value to a string, returning \"NIL\" when the input is NIL."
id: ssl.function.limsstring
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LimsString

Converts a value to a string, returning `"NIL"` when the input is [`NIL`](../literals/nil.md).

`LimsString` returns the literal string `"NIL"` for a null input. When the input is numeric, it formats the number with the current decimal and group separator settings. For other non-null values, it returns that value's normal string form.

## When to use

- When you need a string value for logging, messaging, or concatenation.
- When a missing value should appear explicitly as `"NIL"` instead of causing special-case handling.
- When converting numeric values to text using the current numeric separator settings.

## Syntax

```ssl
LimsString([vSource])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `vSource` | any | no | [`NIL`](../literals/nil.md) | Value to convert. If omitted or [`NIL`](../literals/nil.md), the function returns `"NIL"`. |

## Returns

**[string](../types/string.md)** — `"NIL"` for null input, a separator-formatted string for numeric input, or the value's normal string form for other non-null input.

## Best practices

!!! success "Do"
    - Use `LimsString` before concatenating numbers or optional values into messages.
    - Expect `"NIL"` when the source value is missing.
    - Use it when numeric text should follow the current decimal and group separator settings.

!!! failure "Don't"
    - Assume a missing value becomes an empty string. `LimsString(NIL)` returns `"NIL"`.
    - Assume numeric output is culture-neutral. It follows the current separator settings.
    - Use `LimsString` when you need a custom numeric mask. Use a formatting function such as [`LTransform`](LTransform.md) instead.

## Examples

### Show an optional value in a message

Convert a possibly missing value to text without special-case branching. When `vResult` is [`NIL`](../literals/nil.md), `LimsString` returns the literal string `"NIL"`.

```ssl
:PROCEDURE ShowOptionalResult;
	:DECLARE vResult, sMessage;

	vResult := NIL;

	sMessage := "Current result: " + LimsString(vResult);

	UsrMes(sMessage);

	:RETURN sMessage;
:ENDPROC;

/* Usage;
DoProc("ShowOptionalResult");
```

[`UsrMes`](UsrMes.md) displays:

```text
Current result: NIL
```

### Build a mixed-value summary line

Iterate over an array containing a string, a number, [`NIL`](../literals/nil.md), and a boolean, converting each element with `LimsString`. The resulting summary shows `"NIL"` for the missing slot and `"True"` for the boolean.

```ssl
:PROCEDURE BuildSummaryLine;
	:DECLARE aValues, sSummary, vValue, nIndex;

	aValues := {"Batch-1042", 27.5, NIL, .T.};
	sSummary := "";

	:FOR nIndex := 1 :TO ALen(aValues);
		vValue := aValues[nIndex];

		:IF nIndex > 1;
			sSummary := sSummary + " | ";
		:ENDIF;

		sSummary := sSummary + LimsString(vValue);
	:NEXT;

	UsrMes("Summary: " + sSummary);

	:RETURN sSummary;
:ENDPROC;

/* Usage;
DoProc("BuildSummaryLine");
```

[`UsrMes`](UsrMes.md) displays:

```text
Summary: Batch-1042 | 27.5 | NIL | True
```

## Related

- [`LStr`](LStr.md)
- [`LTransform`](LTransform.md)
- [`Len`](Len.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
