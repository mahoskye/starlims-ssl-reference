---
title: "Integer"
summary: "Returns the whole-number portion of a numeric value by truncating the fractional part toward zero."
id: ssl.function.integer
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Integer

Returns the whole-number portion of a numeric value by truncating the fractional
part toward zero.

`Integer` takes one numeric argument and returns a numeric result. It does not round to the nearest value. Positive numbers are truncated downward toward zero, and negative numbers are truncated upward toward zero.

## When to use

- When you need truncation rather than rounding.
- When you need to remove the fractional part before storing or displaying a whole-number value.
- When you want predictable toward-zero behavior for negative numbers.

## Syntax

```ssl
Integer(nValue)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nValue` | [number](../types/number.md) | yes | — | Numeric value to truncate |

## Returns

**[number](../types/number.md)** — The input value with any fractional part removed.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `nValue` is [`NIL`](../literals/nil.md). | `Value cannot be null. (Parameter 'nValue')` |

## Best practices

!!! success "Do"
    - Use `Integer` when you specifically want truncation toward zero.
    - Validate string input before converting it to a number and passing it to `Integer`.
    - Use [`Round`](Round.md) instead when you need rounding rather than truncation.

!!! failure "Don't"
    - Treat `Integer` as a rounding function. It removes the fractional part instead.
    - Pass [`NIL`](../literals/nil.md) and expect a blank or default numeric result.
    - Assume `Integer(-2.7)` behaves like floor logic. It returns `-2`, not `-3`.

## Caveats

- If you are starting from text input, convert it to a number first.

## Examples

### Remove the fractional part from a price

Call `Integer` on a positive decimal to get the whole-number portion without
any rounding.

```ssl
:DECLARE nPrice, nWholePrice, sMessage;

nPrice := 99.95;
nWholePrice := Integer(nPrice);

sMessage := "Original: " + LimsString(nPrice)
		    + ", Integer: " + LimsString(nWholePrice);

UsrMes(sMessage);
```

[`UsrMes`](UsrMes.md) displays:

```
Original: 99.95, Integer: 99
```

### Truncate a negative value toward zero

`Integer(-2.7)` returns `-2`, not `-3`, because truncation moves toward zero
rather than toward negative infinity.

```ssl
:DECLARE nRawValue, nTruncValue, sMessage;

nRawValue := -2.7;
nTruncValue := Integer(nRawValue);

sMessage := "Original: " + LimsString(nRawValue)
		    + ", Integer: " + LimsString(nTruncValue);

UsrMes(sMessage);
```

[`UsrMes`](UsrMes.md) displays:

```
Original: -2.7, Integer: -2
```

### Validate text input before truncating

Validate user-supplied text with [`IsNumeric`](IsNumeric.md) before converting it with [`Val`](Val.md) and truncating, so that a bad input produces a clear message rather than a runtime error.

```ssl
:PROCEDURE SubmitWholeNumber;
	:PARAMETERS sRawValue;
	:DECLARE nConvertedValue;

	:IF Empty(sRawValue) .OR. !IsNumeric(sRawValue);
		UsrMes("Enter a numeric value before calling Integer.");
		:RETURN;
	:ENDIF;

	nConvertedValue := Integer(Val(sRawValue));
	UsrMes("Submitting whole-number value: " + LimsString(nConvertedValue));
:ENDPROC;

DoProc("SubmitWholeNumber", {"3.7"});
```

[`UsrMes`](UsrMes.md) displays:

```text
Submitting whole-number value: 3
```

## Related

- [`Round`](Round.md)
- [`Val`](Val.md)
- [`IsNumeric`](IsNumeric.md)
- [`number`](../types/number.md)
