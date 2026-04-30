---
title: "Val"
summary: "Converts numeric text at the start of a string to a number."
id: ssl.function.val
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Val

Converts numeric text at the start of a string to a number.

`Val` converts `sNumber` to a numeric result. It ignores leading whitespace and uses the current STARLIMS decimal and group separator settings when parsing. When `Val` is operating in its traditional parsing mode, it reads the numeric prefix from left to right and stops when the text stops looking numeric, so a value such as `"12.5 mg"` returns `12.5`.

Passing [`NIL`](../literals/nil.md) or a non-string value raises an error. On systems that use strict numeric parsing for `Val`, invalid numeric text raises the same format error as [`ToNumeric`](ToNumeric.md) instead of returning a partial result.

## When to use

- When you need to extract a leading numeric value from mixed text such as
  `"12.5 mg/L"`.
- When imported values may contain leading whitespace before the numeric text.
- When you want a more tolerant conversion than [`ToNumeric`](ToNumeric.md).

## Syntax

```ssl
Val(sNumber)
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `sNumber` | [string](../types/string.md) | yes | — | String to convert. Leading whitespace is ignored before parsing starts. |

## Returns

**[number](../types/number.md)** — The numeric value produced from `sNumber`.

In the traditional `Val` parsing mode, text with a valid leading numeric portion returns that leading value. If the string does not start with numeric content, the result is `0`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sNumber` is [`NIL`](../literals/nil.md) or not a string. | `Argument 'sNumber' cannot be null and it must be a string.` |
| Strict numeric parsing is enabled and `sNumber` is not a valid numeric string. | `"<value>" does not represent a number in a valid format.` `<value>` is the literal content of `sNumber`. |

## Best practices

!!! success "Do"
    - Use `Val` when you intentionally want the numeric value from the start of a mixed string.
    - Use [`ToNumeric`](ToNumeric.md) instead when the whole string must be valid numeric text.
    - Validate user-entered formats with [`IsNumeric`](IsNumeric.md) first when invalid input is expected and should be handled without exceptions.

!!! failure "Don't"
    - Assume `Val` searches the whole string for a number. It only works from the start of the string.
    - Assume `Val` is always tolerant of invalid text. Some systems use stricter numeric parsing and raise a format error instead.
    - Pass [`NIL`](../literals/nil.md) or unchecked non-string values and expect `0`. Those inputs raise an error.

## Caveats

- In the traditional parsing mode, a string such as `"123ABC"` returns `123` and a string such as `"ABC123"` returns `0`.
- Scientific notation with a leading numeric prefix is accepted, such as `"2.5e2"`.
- Some installations also accept a leading `0x` or `0X` hexadecimal value when `Val` is using its traditional parsing behavior.

## Examples

### Convert a simple numeric string

Convert clean numeric text and use the result in a calculation.

```ssl
:PROCEDURE ConvertSimpleValue;
	:DECLARE sUserInput, nValue;

	sUserInput := "42.5";
	nValue := Val(sUserInput);

	UsrMes("Doubled value: " + LimsString(nValue * 2));
:ENDPROC;

/* Usage;
DoProc("ConvertSimpleValue");
```

[`UsrMes`](UsrMes.md) displays:

```text
Doubled value: 85
```

### Extract the leading number from mixed text

Use `Val` when the number comes first and descriptive text follows. Everything after the numeric prefix is ignored.

```ssl
:PROCEDURE ParseMeasuredResult;
	:DECLARE sReportedValue, nResult;

	sReportedValue := "12.5 mg/L";
	nResult := Val(sReportedValue);

	UsrMes("Numeric result: " + LimsString(nResult));

	:RETURN nResult;
:ENDPROC;

/* Usage;
DoProc("ParseMeasuredResult");
```

[`UsrMes`](UsrMes.md) displays:

```text
Numeric result: 12.5
```

### Choose between tolerant and strict conversion

Pass `bRequireWholeValue = .T.` to require that the entire string be numeric (using [`ToNumeric`](ToNumeric.md)), or [`.F.`](../literals/false.md) to accept a leading numeric prefix (using `Val`). With `"100.0"` and either flag the result is the same.

```ssl
:PROCEDURE ImportQuantityField;
	:PARAMETERS sRawValue, bRequireWholeValue;
	:DEFAULT bRequireWholeValue, .F.;
	:DECLARE nValue;

	:IF bRequireWholeValue;
		nValue := ToNumeric(sRawValue);
	:ELSE;
		nValue := Val(sRawValue);
	:ENDIF;

	UsrMes("Imported quantity: " + LimsString(nValue));

	:RETURN nValue;
:ENDPROC;

/* Usage;
DoProc("ImportQuantityField", {"100.0", .F.});
```

[`UsrMes`](UsrMes.md) displays:

```text
Imported quantity: 100
```

## Related

- [`IsNumeric`](IsNumeric.md)
- [`ToNumeric`](ToNumeric.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
