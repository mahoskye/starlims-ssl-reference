---
title: "Upper"
summary: "Converts all characters in a string to uppercase."
id: ssl.function.upper
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Upper

Converts all characters in a string to uppercase.

`Upper` returns a new string with `sSource` converted to uppercase. Use it when you need consistent case normalization before exact comparisons, validation, storage, or display. If `sSource` is an empty string, the result is also empty. If `sSource` is [`NIL`](../literals/nil.md), the function raises an error.

## When to use

- When normalizing user input before an exact string comparison.
- When preparing codes, IDs, or statuses for case-insensitive matching.
- When formatting text for display or export in a consistent uppercase form.
- When combining case normalization with [`AllTrim`](AllTrim.md) or [`Trim`](Trim.md) for cleaner input handling.

## Syntax

```ssl
Upper(sSource)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSource` | [string](../types/string.md) | yes | — | The string to convert to uppercase. |

## Returns

**[string](../types/string.md)** — The uppercase form of `sSource`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSource` is [`NIL`](../literals/nil.md). | `Argument sSource cannot be null.` |

## Best practices

!!! success "Do"
    - Normalize both values before an exact string comparison when case should not matter.
    - Combine `Upper` with [`AllTrim`](AllTrim.md) when input may contain extra spaces.
    - Use `Upper` when you want a normalized display or storage form without changing other characters.

!!! failure "Don't"
    - Assume `Upper` handles [`NIL`](../literals/nil.md) input silently. It raises an error instead.
    - Expect `Upper` to trim or remove whitespace. It changes case only.
    - Compare mixed-case strings directly when the match should be case-insensitive.

## Caveats

- Case conversion follows the runtime's uppercase rules, so some characters can uppercase differently in different locales.

## Examples

### Normalize user input for case-insensitive comparison

Ensure user-provided codes match expected values regardless of case. [`LimsString`](LimsString.md) converts the boolean result to its string form for display.

```ssl
:PROCEDURE NormalizeCodeForCompare;
    :DECLARE sUserInput, sExpectedCode, sNormalizedInput, bMatch;

    sUserInput := "abc";
    sExpectedCode := "ABC";

    sNormalizedInput := Upper(sUserInput);
    bMatch := sNormalizedInput == sExpectedCode;

    UsrMes("Codes match: " + LimsString(bMatch));

    :RETURN bMatch;
:ENDPROC;

/* Usage;
DoProc("NormalizeCodeForCompare");
```

[`UsrMes`](UsrMes.md) displays:

```
Codes match: .T.
```

### Normalize a list of mixed-case codes

Convert multiple values to a consistent uppercase form before later validation or storage.

```ssl
:PROCEDURE NormalizeCodes;
    :DECLARE aRawCodes, aUpperCodes, nIndex;

    aRawCodes := {"Abc-01", "def-02", "GhI-03"};
    aUpperCodes := {};

    :FOR nIndex := 1 :TO ALen(aRawCodes);
        AAdd(aUpperCodes, Upper(aRawCodes[nIndex]));
    :NEXT;

    :RETURN aUpperCodes;
:ENDPROC;

/* Usage;
DoProc("NormalizeCodes");
```

### Trim and normalize before membership checks

Clean incoming values, convert them to uppercase, and compare them against a normalized allowed list. Both conditional branches produce visible output so the caller knows whether the code was accepted or rejected.

```ssl
:PROCEDURE ValidateStatusCode;
    :PARAMETERS sStatusCode;
    :DECLARE sNormalizedStatus, aValidStatuses, bIsValid;

    sNormalizedStatus := Upper(AllTrim(sStatusCode));
    aValidStatuses := {"ACTIVE", "PENDING", "CLOSED"};

    bIsValid := AScan(aValidStatuses, sNormalizedStatus) > 0;

    :IF bIsValid;
        UsrMes("Accepted status: " + sNormalizedStatus);
    :ELSE;
        UsrMes("Invalid status: " + sStatusCode);
    :ENDIF;

    :RETURN bIsValid;
:ENDPROC;

/* Usage;
DoProc("ValidateStatusCode", {"Active"});
```

## Related

- [`AllTrim`](AllTrim.md)
- [`LLower`](LLower.md)
- [`LTrim`](LTrim.md)
- [`Lower`](Lower.md)
- [`Trim`](Trim.md)
- [`string`](../types/string.md)
