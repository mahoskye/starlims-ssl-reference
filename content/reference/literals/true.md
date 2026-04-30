---
title: "true"
summary: "The .T. literal represents the boolean value true in SSL and is case-insensitive."
id: ssl.literal.true
element_type: literal
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# true

## What it does

The `.T.` literal represents the boolean value true in SSL. It is case-insensitive — `.T.` and `.t.` are both valid. Use `.T.` in logical expressions, assignments, comparisons, and conditional statements wherever a boolean true is required.

Equality checks on `.T.` require both operands to be booleans. Comparing `.T.` to a number (for example `.T. = 1`) raises a runtime error. Unlike [`.F.`](false.md), `.T.` is **not** considered empty — `IsEmpty(.T.)` returns [`.F.`](false.md).

## Syntax

`.T.`

- **Type:** boolean
- **Case:** case-insensitive

## Comparison behavior

| Expression | Result | Notes |
|------------|--------|-------|
| `.T. = .T.` | `.T.` | |
| `.T. = .F.` | [`.F.`](false.md) | |
| `.T. = 1` | runtime error | Boolean equality requires both operands to be booleans |
| `.T. = 0` | runtime error | Same — use explicit type checking instead |
| `IsEmpty(.T.)` | [`.F.`](false.md) | `.T.` is not empty (unlike [`.F.`](false.md) which is) |

## Type coercion

| Target | Result |
|--------|--------|
| [string](../types/string.md) | `".T."` |
| [number](../types/number.md) | `1` |
| JSON ([`ToJson`](../functions/ToJson.md)) | `"true"` (a string value, not a JSON boolean token) |

## Notes for daily SSL work

!!! success "Do"
    - Use `.T.` to clearly represent positive or true conditions.
    - Explicitly pass `.T.` as arguments for boolean parameters.
    - Use `.T.` with [`.F.`](false.md) for toggling and switching state.

!!! failure "Don't"
    - Assign `1` or any other numeric value when a boolean is required. SSL has strict boolean typing.
    - Assume "truthy" values (non-empty strings, non-zero numbers) behave like `.T.` in comparisons. SSL does not have truthy/falsy semantics.
    - Use string representations (`"TRUE"`, `"true"`) in boolean operations. They are strings, not booleans.

## Errors and edge cases

- User input arrives as strings — `"TRUE"` is not the same as `.T.` unless explicitly converted.

## Examples

### Boolean flag in a conditional

Initializes `bValidationEnabled` to `.T.` and enters the conditional body because the flag is true, displaying the processing message.

```ssl
:PROCEDURE ProcessWithValidation;
    :DECLARE bValidationEnabled, sSampleId, sStatus;

    bValidationEnabled := .T.;
    sSampleId := "LAB-2024-0042";
    sStatus := "";

    :IF bValidationEnabled;
        sStatus := "Validation enabled — processing " + sSampleId;
        UsrMes(sStatus);
    :ENDIF;

    :RETURN sStatus;
:ENDPROC;

/* Usage;
DoProc("ProcessWithValidation");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Validation enabled — processing LAB-2024-0042
```

### Loop with a boolean sentinel

Starts `bAllValid` at `.T.` and flips it to [`.F.`](false.md) on the first empty sample ID. With three non-empty IDs, the flag stays `.T.` and the all-valid message displays.

```ssl
:PROCEDURE ValidateBatch;
    :PARAMETERS aSampleIds;
    :DECLARE bAllValid, nIndex, sSampleId;

    bAllValid := .T.;

    :FOR nIndex := 1 :TO ALen(aSampleIds);
        sSampleId := aSampleIds[nIndex];

        :IF Empty(sSampleId);
            ErrorMes("Validation", "Empty sample ID at position " + LimsString(nIndex));
            bAllValid := .F.;
        :ENDIF;
    :NEXT;

    :IF bAllValid;
        UsrMes("All " + LimsString(ALen(aSampleIds)) + " samples valid");
    :ELSE;
        UsrMes("Batch has invalid entries");
    :ENDIF;

    :RETURN bAllValid;
:ENDPROC;

/* Usage;
DoProc("ValidateBatch", {{"LAB-001", "LAB-002", "LAB-003"}});
```

## Related elements

- [`false`](false.md)
- [`nil`](nil.md)
