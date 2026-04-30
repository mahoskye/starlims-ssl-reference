---
title: "IsHex"
summary: "Validates whether a string contains only uppercase hexadecimal characters."
id: ssl.function.ishex
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# IsHex

Validates whether a string contains only uppercase hexadecimal characters.

`IsHex` returns [`.T.`](../literals/true.md) when `sSource` contains only the characters `0-9` and `A-F`. The check is case-sensitive, so lowercase `a-f` characters return [`.F.`](../literals/false.md). The function also accepts the empty string, which returns [`.T.`](../literals/true.md) because it contains no non-hex characters. If `sSource` is [`NIL`](../literals/nil.md), the function raises an error.

## When to use

- When validating input before passing it to other hex-processing logic.
- When checking whether a value contains only uppercase hexadecimal digits.
- When normalizing mixed-case input with [`Upper`](Upper.md) and then validating it.

## Syntax

```ssl
IsHex(sSource)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSource` | [string](../types/string.md) | yes | — | String to validate against the uppercase hexadecimal character set `0-9` and `A-F`. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when `sSource` contains only uppercase hexadecimal characters; otherwise [`.F.`](../literals/false.md)

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSource` is [`NIL`](../literals/nil.md). | `Source string cannot be null.` |

## Best practices

!!! success "Do"
    - Check that `sSource` is not [`NIL`](../literals/nil.md) before calling `IsHex`.
    - Use [`Upper`](Upper.md) first when your input may contain lowercase `a-f`.
    - Add a length check when the next step requires at least one hex digit.
    - Validate untrusted hex input before sending it to downstream conversion logic.

!!! failure "Don't"
    - Assume [`NIL`](../literals/nil.md) input returns [`.F.`](../literals/false.md). It raises an error instead.
    - Assume lowercase `a-f` is accepted. `IsHex` only accepts uppercase `A-F`.
    - Skip validation when later logic expects a hex-only string.

## Caveats

- Lowercase `a-f` is rejected. Use [`Upper`](Upper.md) first if you want to accept mixed-case input.
- Leading prefixes such as `0x`, whitespace, and punctuation cause the check to fail.
- The empty string returns [`.T.`](../literals/true.md). Add a separate length check when at least one hex digit is required before conversion.

## Examples

### Check whether a string contains only uppercase hex characters

Call `IsHex` on a hardcoded value and branch on the result. The input `"A3F7"` contains only valid uppercase hex digits, so the true branch executes.

```ssl
:PROCEDURE ValidateHexCode;
    :DECLARE sUserInput, bIsValidHex, sStatus;

    sUserInput := "A3F7";
    bIsValidHex := IsHex(sUserInput);

    :IF bIsValidHex;
        sStatus := "Valid uppercase hex value";
        UsrMes(sStatus);
        :RETURN .T.;
    :ELSE;
        sStatus := "Value contains non-hex characters";
        UsrMes(sStatus);
        :RETURN .F.;
    :ENDIF;
:ENDPROC;
```

Call with `DoProc("ValidateHexCode")`.

### Normalize mixed-case input before validating

Trim whitespace and convert to uppercase before calling `IsHex`, so that values like `" a3f7 "` pass validation rather than failing on case or whitespace. Calling with `"a3f7"` produces `"A3F7"` after normalization, which is valid; calling with `"not hex"` produces `"NOT HEX"`, which is not.

```ssl
:PROCEDURE NormalizeAndValidateHex;
    :PARAMETERS sInput;
    :DECLARE sHexValue, bIsValidHex;

    sHexValue := Upper(AllTrim(sInput));
    bIsValidHex := IsHex(sHexValue);

    :IF bIsValidHex;
        UsrMes("Normalized value is valid: " + sHexValue);
        /* Displays normalized valid message;
    :ELSE;
        UsrMes("Normalized value is not valid hex: " + sHexValue);
        /* Displays normalized invalid message;
    :ENDIF;

    :RETURN bIsValidHex;
:ENDPROC;
```

Call with `DoProc("NormalizeAndValidateHex", {"a3f7"})`.

### Filter and convert a batch of hex strings

Use `IsHex` as a gate before calling [`LHex2Dec`](LHex2Dec.md), so that only valid uppercase hex strings are converted. From the five inputs, `"ab"` (lowercase), `"0x10"` (prefix), and `"FF"`, `"1A"`, and `"7B"` (valid) demonstrate how the filter works. Three values pass and two are silently skipped.

```ssl
:PROCEDURE ConvertValidHexBatch;
    :DECLARE aRawValues, aDecimalValues, sHexValue, nDecimalValue, nIndex;

    aRawValues := {"1A", "FF", "ab", "0x10", "7B"};
    aDecimalValues := {};

    :FOR nIndex := 1 :TO ALen(aRawValues);
        sHexValue := aRawValues[nIndex];

        :IF IsHex(sHexValue);
            nDecimalValue := LHex2Dec(sHexValue);
            AAdd(aDecimalValues, nDecimalValue);
        :ENDIF;
    :NEXT;

    :RETURN aDecimalValues;
:ENDPROC;
```

Call with `DoProc("ConvertValidHexBatch")`.

## Related

- [`LFromHex`](LFromHex.md)
- [`LHex2Dec`](LHex2Dec.md)
- [`LToHex`](LToHex.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
