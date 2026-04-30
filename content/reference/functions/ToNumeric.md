---
title: "ToNumeric"
summary: "Converts a string to a number, with optional hexadecimal support."
id: ssl.function.tonumeric
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ToNumeric

Converts a string to a number, with optional hexadecimal support.

`ToNumeric` performs strict string-to-number conversion using the current STARLIMS decimal and group separator settings. It accepts values that the runtime can parse as floating-point text with optional thousands separators. If
`bAllowHex` is [`.T.`](../literals/true.md), it also accepts whole hexadecimal strings in `0x...` or `0X...` form.

Leading and trailing whitespace are allowed. `NaN`, positive infinity, negative infinity, empty strings, and other invalid formats raise an error instead of returning a fallback value. Compared with [`Val`](Val.md), `ToNumeric` rejects partial parses rather than stopping at the first invalid character.

## When to use

- When invalid numeric input should fail immediately instead of being tolerated.
- When a field may contain either standard numeric text or optional `0x`
  hexadecimal values.
- When you need a stricter alternative to [`Val`](Val.md) for imported or
  user-entered data.

## Syntax

```ssl
ToNumeric(sNumber, [bAllowHex])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sNumber` | [string](../types/string.md) | yes | — | String to convert. Leading and trailing whitespace are ignored. |
| `bAllowHex` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | When [`.T.`](../literals/true.md), also accepts whole hexadecimal strings such as `0xFF`. Non-boolean values are treated as [`.F.`](../literals/false.md). |

## Returns

**[number](../types/number.md)** — The parsed numeric value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sNumber` is [`NIL`](../literals/nil.md). | `Argument 'sNumber' cannot be null and it must be a string.` |
| `sNumber` is not in a valid numeric format. | `"<value>" does not represent a number in a valid format.` |

## Best practices

!!! success "Do"
    - Validate with [`IsNumeric`](IsNumeric.md) first when invalid input is expected and should be handled without exceptions.
    - Pass `bAllowHex` as [`.T.`](../literals/true.md) only in paths that explicitly allow `0x` hexadecimal values.
    - Use [`:TRY`](../keywords/TRY.md) and [`:CATCH`](../keywords/CATCH.md) when conversion failures are part of normal control flow.

!!! failure "Don't"
    - Assume `ToNumeric` behaves like [`Val`](Val.md). It does not return partial results from mixed text.
    - Assume hexadecimal input is accepted by default. `0x` parsing only happens when `bAllowHex` is [`.T.`](../literals/true.md).
    - Pass unchecked external input unless you are prepared to handle conversion errors.

## Examples

### Strictly convert a validated text value

Convert a known-good numeric string and use the result in a message. This shows the basic call form with no hex support.

```ssl
:PROCEDURE ParseUserInput;
    :DECLARE sUserInput, nParsedValue;

    sUserInput := "42.5";
    nParsedValue := ToNumeric(sUserInput);

    UsrMes("Parsed value: " + LimsString(nParsedValue));
:ENDPROC;

/* Usage;
DoProc("ParseUserInput");
```

[`UsrMes`](UsrMes.md) displays:

```text
Parsed value: 42.5
```

### Accept decimal or hexadecimal input explicitly

Pass `bAllowHex` as [`.T.`](../literals/true.md) only in code paths that explicitly allow `0x` values. This example detects which format was parsed and includes it in the result message.

```ssl
:PROCEDURE ParseNumericInput;
    :PARAMETERS sRawValue;
    :DECLARE nResult, sType;

    nResult := ToNumeric(sRawValue, .T.);

    :IF Left(sRawValue, 2) == "0x" .OR. Left(sRawValue, 2) == "0X";
        sType := "hexadecimal";
    :ELSE;
        sType := "decimal";
    :ENDIF;

    UsrMes(
        "Input " + sRawValue + " parsed as " + sType
        + ": " + LimsString(nResult)
    );

    :RETURN nResult;
:ENDPROC;

/* Usage;
DoProc("ParseNumericInput", {"0xFF"});
```

[`UsrMes`](UsrMes.md) displays:

```text
Input 0xFF parsed as hexadecimal: 255
```

### Handle a failed conversion without accepting partial text

Wrap the call in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the input may be non-numeric. Unlike [`Val`](Val.md), `ToNumeric` raises an error for mixed text rather than stopping at the first non-numeric character.

```ssl
:PROCEDURE ImportNumericField;
    :PARAMETERS sImportedValue;
    :DECLARE nValue, oErr;

    :TRY;
        nValue := ToNumeric(sImportedValue);

        UsrMes("Imported value: " + LimsString(nValue));

        :RETURN nValue;
    :CATCH;
        oErr := GetLastSSLError();

        UsrMes(
            "Could not convert '" + sImportedValue + "': "
            + oErr:Description
        );
        /* Displays on failure: conversion error;

        :RETURN 0;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ImportNumericField", {"123abc"});
```

## Related

- [`IsNumeric`](IsNumeric.md)
- [`Val`](Val.md)
- [`boolean`](../types/boolean.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
