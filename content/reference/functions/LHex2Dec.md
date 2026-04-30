---
title: "LHex2Dec"
summary: "Converts a hexadecimal string to its decimal string representation."
id: ssl.function.lhex2dec
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LHex2Dec

Converts a hexadecimal string to its decimal string representation.

`LHex2Dec()` takes a string containing a hexadecimal number and returns the equivalent decimal value as a string. If `sSource` is [`NIL`](../literals/nil.md), the function raises an error. Invalid input is not sanitized or repaired before conversion, so this function is best used after input has already been validated.

## When to use

- When you need a decimal string version of a hexadecimal identifier or code.
- When upstream logic stores numeric values as hex text but later steps expect decimal text.
- When you validate external input with [`IsHex`](IsHex.md) before converting it.

## Syntax

```ssl
LHex2Dec(sSource)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSource` | [string](../types/string.md) | yes | — | Hexadecimal text to convert |

## Returns

**[string](../types/string.md)** — The decimal string produced from `sSource`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSource` is [`NIL`](../literals/nil.md). | `Source string cannot be null.` |

## Best practices

!!! success "Do"
    - Validate external input before calling `LHex2Dec()`.
    - Normalize incoming values first when your input may contain surrounding whitespace or mixed casing.
    - Use [`IsHex`](IsHex.md) when you want to reject non-hex content before conversion.

!!! failure "Don't"
    - Assume invalid input is corrected automatically. Bad input still fails during conversion.
    - Pass [`NIL`](../literals/nil.md) to `LHex2Dec()`. The function raises an error for [`NIL`](../literals/nil.md) input.
    - Use `LHex2Dec()` when you need byte-to-text decoding. Use [`LFromHex`](LFromHex.md) for that.

## Examples

### Convert a validated hex value

Pass a known-valid uppercase hex string to get the decimal representation. `"1A7F"` in hex is `6783` in decimal.

```ssl
:PROCEDURE ConvertHexValue;
    :DECLARE sHexValue, sDecimalValue;

    sHexValue := "1A7F";
    sDecimalValue := LHex2Dec(sHexValue);

    UsrMes("Decimal value: " + sDecimalValue);

    :RETURN sDecimalValue;
:ENDPROC;

/* Usage;
DoProc("ConvertHexValue");
```

[`UsrMes`](UsrMes.md) displays:

```text
Decimal value: 6783
```

### Normalize input before conversion

Trim whitespace and convert to uppercase before validating with [`IsHex`](IsHex.md), then pass the cleaned value to `LHex2Dec()`. For input `"1a7f"` the normalized value is `"1A7F"` and the result is `"6783"`.

```ssl
:PROCEDURE NormalizeAndConvertHex;
    :PARAMETERS sInput;
    :DECLARE sHexValue, sDecimalValue;

    sHexValue := Upper(AllTrim(sInput));

    :IF Empty(sHexValue) .OR. !IsHex(sHexValue);
        /* Displays invalid-input message with the original value;
        UsrMes("Input is not a valid hexadecimal value: " + sInput);
        :RETURN "";
    :ENDIF;

    sDecimalValue := LHex2Dec(sHexValue);

    /* Displays the normalized hex value and converted decimal value;
    UsrMes("Converted " + sHexValue + " to " + sDecimalValue);

    :RETURN sDecimalValue;
:ENDPROC;

/* Usage;
DoProc("NormalizeAndConvertHex", {"1a7f"});
```

### Convert a batch of validated values

Process a list of incoming hex values, trimming and normalizing each one before validation. With the five inputs, `"GG"` is invalid and four others pass, so the batch yields four converted values and one skip.

```ssl
:PROCEDURE ConvertHexBatch;
    :DECLARE aInput, aDecimalValues, aInvalidValues, sHexValue, nIndex;

    aInput := {"1A", "FF", "7B", "GG", " 2C "};
    aDecimalValues := {};
    aInvalidValues := {};

    :FOR nIndex := 1 :TO ALen(aInput);
        sHexValue := Upper(AllTrim(aInput[nIndex]));

        :IF Empty(sHexValue) .OR. !IsHex(sHexValue);
            AAdd(aInvalidValues, aInput[nIndex]);
            :LOOP;
        :ENDIF;

        AAdd(aDecimalValues, LHex2Dec(sHexValue));
    :NEXT;

    /* Displays the number of successfully converted values;
    UsrMes("Converted values: " + LimsString(ALen(aDecimalValues)));

    :IF ALen(aInvalidValues) > 0;
        /* Displays the number of skipped invalid values;
        UsrMes("Skipped invalid values: " + LimsString(ALen(aInvalidValues)));
    :ENDIF;

    :RETURN aDecimalValues;
:ENDPROC;

/* Usage;
DoProc("ConvertHexBatch");
```

## Related

- [`IsHex`](IsHex.md)
- [`LFromHex`](LFromHex.md)
- [`LToHex`](LToHex.md)
- [`string`](../types/string.md)
