---
title: "Len"
summary: "Returns the number of characters in a string or the element count of an array."
id: ssl.function.len
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Len

Returns the number of characters in a string or the element count of an array.

`Len` accepts a string or an array. For strings, it returns the character count. For arrays, it returns the element count. Passing [`NIL`](../literals/nil.md) or a value that is neither a string nor an array raises an error.

Use [`ALen`](ALen.md) when the input is always an array. `Len` is appropriate when the input is a string, or when the type may be either.

## When to use

- When you need to validate that a text input meets a required minimum or maximum length before storing or processing it.
- When determining if an array or collection has any items before starting further operations.
- When reporting the length of a value for auditing or display purposes.

## Syntax

```ssl
Len(vSource)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vSource` | any | yes | — | The string or array to measure. Must be a string or array — other types raise an error. |

## Returns

**[number](../types/number.md)** — The character count when `vSource` is a string, or the element count when `vSource` is an array.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `vSource` is [`NIL`](../literals/nil.md). | `Argument vSource cannot be null.` |
| `vSource` is neither a string nor an array. | `Invalid type: <type>.` |

## Best practices

!!! success "Do"
    - Check for [`NIL`](../literals/nil.md) before passing a value when the source may be absent.
    - Use `Len` for string length and [`ALen`](ALen.md) when the input is always an array.
    - Treat a zero result as empty and validate further when needed.

!!! failure "Don't"
    - Assume [`NIL`](../literals/nil.md) is handled gracefully — it raises an error.
    - Interpret a length of zero as valid content without further checks.
    - Substitute `Len` for [`ALen`](ALen.md) when the input is always an array — prefer [`ALen`](ALen.md) to make the intent explicit.

## Caveats

- For arrays, only top-level elements are counted — nested arrays are not expanded and their contents are not included in the count.

## Examples

### Validate a password meets minimum length

Check a password string against an 8-character minimum and show the outcome. `"SecurePass1"` is 11 characters, so the valid branch fires.

```ssl
:PROCEDURE ValidatePasswordLength;
	:DECLARE sPassword, nMinLength, nActualLength, bIsValid;

	nMinLength := 8;
	sPassword := "SecurePass1";

	nActualLength := Len(sPassword);
	bIsValid := nActualLength >= nMinLength;

	:IF bIsValid;
		UsrMes("Password is valid. Length: " + LimsString(nActualLength));
	:ELSE;
		UsrMes("Password too short. Minimum: " + LimsString(nMinLength));
	:ENDIF;

	:RETURN bIsValid;
:ENDPROC;

DoProc("ValidatePasswordLength");
```

[`UsrMes`](UsrMes.md) displays:

```text
Password is valid. Length: 11
```

### Scan a string character by character using Len as a loop bound

Use `Len` as the upper bound of a [`:FOR`](../keywords/FOR.md) loop to walk each character of `"LAB-2024-001"` with [`SubStr`](SubStr.md) and count digits. The string contains 7 digit characters.

```ssl
:PROCEDURE CountDigits;
	:DECLARE sValue, nIndex, nDigitCount, sChar;

	sValue := "LAB-2024-001";
	nDigitCount := 0;

	:FOR nIndex := 1 :TO Len(sValue);
		sChar := SubStr(sValue, nIndex, 1);
		:IF sChar >= "0" .AND. sChar <= "9";
			nDigitCount := nDigitCount + 1;
		:ENDIF;
	:NEXT;

	UsrMes("Digits in '" + sValue + "': " + LimsString(nDigitCount));
:ENDPROC;

DoProc("CountDigits");
```

[`UsrMes`](UsrMes.md) displays:

```
Digits in 'LAB-2024-001': 7
```

### Right-pad a label to a fixed column width

Use `Len` to calculate the number of spaces needed to extend `"Sample ID"` (9 characters) to a 15-character column before appending the value. `nColumnWidth - Len(sLabel)` gives the exact padding count.

```ssl
:PROCEDURE BuildFixedWidthLine;
	:DECLARE sLabel, sValue, nColumnWidth, nPadding, sLine, nIndex;

	sLabel := "Sample ID";
	sValue := "LAB-7829";
	nColumnWidth := 15;
	nPadding := nColumnWidth - Len(sLabel);

	sLine := sLabel;
	:FOR nIndex := 1 :TO nPadding;
		sLine := sLine + " ";
	:NEXT;
	sLine := sLine + sValue;

	UsrMes("[" + sLine + "]");
:ENDPROC;

DoProc("BuildFixedWidthLine");
```

[`UsrMes`](UsrMes.md) displays:

```
[Sample ID      LAB-7829]
```

## Related

- [`ALen`](ALen.md)
- [`Left`](Left.md)
- [`SubStr`](SubStr.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
- [`number`](../types/number.md)
