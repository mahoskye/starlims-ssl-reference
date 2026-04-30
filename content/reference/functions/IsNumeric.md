---
title: "IsNumeric"
summary: "Determines whether a string is a valid numeric value, with optional support for hexadecimal input."
id: ssl.function.isnumeric
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# IsNumeric

Determines whether a string is a valid numeric value, with optional support for hexadecimal input.

`IsNumeric` checks whether `sNumber` can be interpreted as a number using the current STARLIMS decimal and group separator settings. It returns [`.T.`](../literals/true.md) for values that the runtime accepts as floating-point text with optional thousands separators, and [`.F.`](../literals/false.md) for strings that do not match that format. If `bAllowHex` is [`.T.`](../literals/true.md), the function also accepts whole hexadecimal strings in `0x...` or `0X...` form.

Leading and trailing whitespace are allowed. Empty strings, `NaN`, positive infinity, and negative infinity return [`.F.`](../literals/false.md). Passing [`NIL`](../literals/nil.md) or a non-string value raises an error instead of returning [`.F.`](../literals/false.md).

## When to use

- When you need to validate a string before calling [`ToNumeric`](ToNumeric.md).
- When imported or user-entered values may include group separators.
- When hexadecimal input should be accepted only in specific paths.

## Syntax

```ssl
IsNumeric(sNumber, [bAllowHex])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sNumber` | [string](../types/string.md) | yes | — | String to validate. |
| `bAllowHex` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | When [`.T.`](../literals/true.md), also accepts whole hexadecimal strings such as `0xFF`. Non-boolean values are treated as [`.F.`](../literals/false.md). |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when `sNumber` is a valid decimal value under the current numeric settings, or a valid `0x...` or `0X...` hexadecimal string when `bAllowHex` is enabled; otherwise [`.F.`](../literals/false.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sNumber` is [`NIL`](../literals/nil.md) or not a string. | `Value cannot be null. (Parameter 'sNumber')` |

## Best practices

!!! success "Do"
    - Use `IsNumeric` before [`ToNumeric`](ToNumeric.md) when invalid input should be handled without exceptions.
    - Pass `bAllowHex` as [`.T.`](../literals/true.md) only when `0x`-prefixed values are valid for that input.
    - Keep user input as a string until validation is complete.

!!! failure "Don't"
    - Assume [`NIL`](../literals/nil.md) or non-string values return [`.F.`](../literals/false.md). They raise an error instead.
    - Assume hexadecimal strings are accepted by default. They only pass when `bAllowHex` is [`.T.`](../literals/true.md).
    - Use `IsNumeric` when you need the parsed numeric value. Use [`ToNumeric`](ToNumeric.md) or [`Val`](Val.md) after validation.

## Caveats

- `NaN`, positive infinity, and negative infinity return [`.F.`](../literals/false.md).
- Hexadecimal support is limited to whole values in `0x...` or `0X...` form.

## Examples

### Validate a text field before conversion

Check a user-entered value before converting it to a number. The input `"1,234.50"` is valid with a thousands separator, so `IsNumeric` returns [`.T.`](../literals/true.md), the early-return branch is skipped, and [`ToNumeric`](ToNumeric.md) converts the string to `1234.5`.

```ssl
:PROCEDURE ValidateNumericInput;
    :DECLARE sUserInput, bIsNumeric, nValue;

    sUserInput := "1,234.50";
    bIsNumeric := IsNumeric(sUserInput);

    :IF !bIsNumeric;
        UsrMes("Enter a valid number.");
        :RETURN .F.;
    :ENDIF;

    nValue := ToNumeric(sUserInput);
    UsrMes("Accepted value: " + LimsString(nValue));
    /* Displays converted numeric value on success;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ValidateNumericInput");
```

### Distinguish decimal and hexadecimal input

Check the same value against both decimal and hex modes to route it into the correct conversion path. For `"0xFF"`, the decimal check fails and the hex check succeeds, so [`ToNumeric`](ToNumeric.md) is called with `bAllowHex` [`.T.`](../literals/true.md) and returns `255`.

```ssl
:PROCEDURE ParseConfigValue;
    :DECLARE sConfigValue, bIsDecimal, bIsHex, nValue;

    sConfigValue := "0xFF";
    bIsDecimal := IsNumeric(sConfigValue, .F.);
    bIsHex := IsNumeric(sConfigValue, .T.);

    :IF bIsDecimal;
        nValue := ToNumeric(sConfigValue);
        UsrMes("Decimal value: " + LimsString(nValue));
        /* Displays parsed decimal value;
        :RETURN nValue;
    :ENDIF;

    :IF bIsHex;
        nValue := ToNumeric(sConfigValue, .T.);
        UsrMes("Hex value: " + LimsString(nValue));
        /* Displays parsed hexadecimal value;
        :RETURN nValue;
    :ENDIF;

    UsrMes("Config value is not numeric.");

    :RETURN 0;
:ENDPROC;

/* Usage;
DoProc("ParseConfigValue");
```

### Filter imported rows and collect invalid IDs for review

Iterate over a batch of imported rows, use `IsNumeric` to classify each record ID, and collect failures separately for follow-up. The `bAllowHex` parameter is forwarded so callers can opt in to hex IDs without changing the validation logic.

```ssl
:PROCEDURE CleanImportedSampleData;
    :PARAMETERS aImportedRows, bAllowHex;
    :DEFAULT bAllowHex, .F.;
    :DECLARE aCleanRows, aInvalidRows, sRecordId, nIndex;

    aCleanRows := {};
    aInvalidRows := {};

    :FOR nIndex := 1 :TO ALen(aImportedRows);
        sRecordId := aImportedRows[nIndex, 1];

        :IF IsNumeric(sRecordId, bAllowHex);
            AAdd(aCleanRows, aImportedRows[nIndex]);
        :ELSE;
            AAdd(aInvalidRows, {sRecordId, nIndex});
        :ENDIF;
    :NEXT;

    UsrMes("Valid rows: " + LimsString(ALen(aCleanRows)));
    /* Displays valid row count;
    UsrMes("Invalid rows: " + LimsString(ALen(aInvalidRows)));
    /* Displays invalid row count;

    :RETURN aCleanRows;
:ENDPROC;

/* Usage;
DoProc("CleanImportedSampleData", {{{"001", "Sample A"}, {"0xFF", "Sample B"}, {"bad_id", "Sample C"}}, .T.});
```

## Related

- [`ToNumeric`](ToNumeric.md)
- [`Val`](Val.md)
- [`ValidateNumeric`](ValidateNumeric.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
