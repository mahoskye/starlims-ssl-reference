---
title: "IsGuid"
summary: "Validates whether a string matches the GUID format and returns a boolean result."
id: ssl.function.isguid
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# IsGuid

Validates whether a string matches the GUID format and returns a boolean result.

`IsGuid` returns [`.T.`](../literals/true.md) when `sGuid` matches the expected hyphenated GUID pattern and [`.F.`](../literals/false.md) for non-matching or empty strings. The accepted format is 32 hexadecimal characters grouped as `8-4-4-4-12`, with optional surrounding braces such as `{3F2504E0-4F89-11D3-9A0C-0305E82C3301}`. Hex digits are accepted in either uppercase or lowercase. If `sGuid` is [`NIL`](../literals/nil.md), the function raises an error instead of returning [`.F.`](../literals/false.md).

## When to use

- When input should contain a GUID and you need to validate it before using it.
- When filtering imported values into valid and invalid identifier lists.
- When a value may be missing and you want to guard against the error raised for [`NIL`](../literals/nil.md) input.

## Syntax

```ssl
IsGuid(sGuid)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sGuid` | [string](../types/string.md) | yes | — | String to validate against the GUID format |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when `sGuid` matches the GUID format; otherwise [`.F.`](../literals/false.md)

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sGuid` is [`NIL`](../literals/nil.md). | `IsGuid (Parameter 'sGuid')` |

## Best practices

!!! success "Do"
    - Validate external identifier strings before using them in lookup or save logic.
    - Guard values that may be [`NIL`](../literals/nil.md) before calling `IsGuid`.
    - Accept both uppercase and lowercase GUID text when the format is otherwise valid.

!!! failure "Don't"
    - Assume any non-empty identifier string is valid without checking it.
    - Pass [`NIL`](../literals/nil.md) and expect [`.F.`](../literals/false.md) because the function raises an error for missing input.
    - Reject a GUID only because it uses lowercase hex digits or surrounding braces.

## Caveats

- Empty strings return [`.F.`](../literals/false.md).
- The format must include hyphens in the standard `8-4-4-4-12` layout; a 32-character hex string without hyphens is not accepted.

## Examples

### Validate a user-provided identifier before use

Call `IsGuid` on a single input string and branch on the result to confirm whether it is safe to pass to lookup or save logic. The hardcoded value is a valid GUID, so the true branch executes.

```ssl
:PROCEDURE ValidateGuidInput;
    :DECLARE sUserInput, bIsValid;

    sUserInput := "3F2504E0-4F89-11D3-9A0C-0305E82C3301";

    bIsValid := IsGuid(sUserInput);

    :IF bIsValid;
        UsrMes("Valid GUID: " + sUserInput);
    :ELSE;
        UsrMes("Invalid GUID: " + sUserInput);
    :ENDIF;

    :RETURN bIsValid;
:ENDPROC;

/* Usage;
DoProc("ValidateGuidInput");
```

[`UsrMes`](UsrMes.md) displays:

```text
Valid GUID: 3F2504E0-4F89-11D3-9A0C-0305E82C3301
```

### Filter imported identifiers into valid and invalid groups

Iterate over a mixed list of identifier strings and use `IsGuid` to route each one into a valid or invalid collection. The summary line shows the final counts for both groups.

```ssl
:PROCEDURE FilterValidGuids;
    :DECLARE aRawIdentifiers, aValidGuids, aInvalidIds, sIdentifier, nIndex, sReport;

    aRawIdentifiers := {
        "A45E7F92-8B3D-4D9A-9F3C-2B1A6D8E4C71",
        "NOT_A_GUID",
        "12345678-1234-1234-1234-123456789012",
        "INVALID",
        "B72F3C19-9E2A-4D8B-91F7-3C5D8E6A1924",
        "MISSING_HYPHENS",
        "00000000-0000-0000-0000-000000000000"
    };

    aValidGuids := {};
    aInvalidIds := {};

    :FOR nIndex := 1 :TO ALen(aRawIdentifiers);
        sIdentifier := aRawIdentifiers[nIndex];

        :IF IsGuid(sIdentifier);
            AAdd(aValidGuids, sIdentifier);
        :ELSE;
            AAdd(aInvalidIds, sIdentifier);
        :ENDIF;
    :NEXT;

    sReport := "Valid: " + LimsString(ALen(aValidGuids))
		        + " | Invalid: " + LimsString(ALen(aInvalidIds));
    UsrMes(sReport);

    :RETURN aValidGuids;
:ENDPROC;

/* Usage;
DoProc("FilterValidGuids");
```

[`UsrMes`](UsrMes.md) displays:

```text
Valid: 4 | Invalid: 3
```

### Guard against NIL input with explicit validation and error handling

When `IsGuid` receives a value from an external source that may be [`NIL`](../literals/nil.md) or a non-string type, check for [`NIL`](../literals/nil.md) first and convert to string before calling the function. Wrap the call in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) for any remaining unexpected errors.

```ssl
:PROCEDURE ValidateOptionalGuid;
    :PARAMETERS vGuid;
    :DECLARE sGuid, bIsValid, oErr;

    :IF vGuid == NIL;
        UsrMes("No GUID was provided");
        :RETURN .F.;
    :ENDIF;

    sGuid := LimsString(vGuid);

    :TRY;
        bIsValid := IsGuid(sGuid);

        :IF bIsValid;
            UsrMes("Validated GUID: " + sGuid);
        :ELSE;
            UsrMes("Value is not a GUID: " + sGuid);
        :ENDIF;

        :RETURN bIsValid;
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("GUID validation failed: " + oErr:Description);
        /* Displays on failure: GUID validation failed;
        :RETURN .F.;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ValidateOptionalGuid", {"3F2504E0-4F89-11D3-9A0C-0305E82C3301"});
```

## Related

- [`CreateGUID`](CreateGUID.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
