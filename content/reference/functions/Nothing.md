---
title: "Nothing"
summary: "Returns .T. when vValue is NIL, empty by SSL rules, or stringifies to the exact value \"0\"; otherwise returns .F.."
id: ssl.function.nothing
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Nothing

Returns [`.T.`](../literals/true.md) when `vValue` is [`NIL`](../literals/nil.md), empty by SSL rules, or stringifies to the exact value `"0"`; otherwise returns [`.F.`](../literals/false.md).

`Nothing()` is a broader absence check than [`Empty`](Empty.md). The function first returns [`.T.`](../literals/true.md) for [`NIL`](../literals/nil.md), then returns [`.T.`](../literals/true.md) for anything that [`Empty`](Empty.md) already considers empty, and finally returns [`.T.`](../literals/true.md) when `LimsString(vValue)` is exactly `"0"`. Any other value returns [`.F.`](../literals/false.md).

## When to use

- When blank input and the literal string `"0"` should both count as no value.
- When normalizing imported text fields that may use `"0"` as a placeholder.
- When you want one check that covers [`NIL`](../literals/nil.md), SSL-empty values, and `"0"`.
- When screening loosely typed values before continuing with business logic.

## Syntax

```ssl
Nothing(vValue)
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `vValue` | any | yes | — | Value to test for [`NIL`](../literals/nil.md), SSL-empty state, or the exact stringified value `"0"`. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when `vValue` is [`NIL`](../literals/nil.md), empty by [`Empty`](Empty.md), or stringifies to `"0"`; otherwise [`.F.`](../literals/false.md).

| Input | Result | Why |
| --- | --- | --- |
| [`NIL`](../literals/nil.md) | [`.T.`](../literals/true.md) | Returns [`.T.`](../literals/true.md) immediately for [`NIL`](../literals/nil.md) input. |
| `""` or whitespace-only string | [`.T.`](../literals/true.md) | [`Empty`](Empty.md) handles trimmed-empty strings. |
| `0` | [`.T.`](../literals/true.md) | `Empty(0)` is true. |
| [`.F.`](../literals/false.md) | [`.T.`](../literals/true.md) | `Empty(.F.)` is true. |
| `"0"` | [`.T.`](../literals/true.md) | `LimsString(vValue) == "0"` matches exactly. |
| `"00"` | [`.F.`](../literals/false.md) | The final check is exact `"0"`, not a numeric parse. |
| `"0.0"` | [`.F.`](../literals/false.md) | The stringified value is not exactly `"0"`. |
| `"ABC"` | [`.F.`](../literals/false.md) | It is neither empty nor exactly `"0"`. |

## Best practices

!!! success "Do"
    - Use `Nothing()` when your input rules explicitly treat `"0"` as missing data.
    - Use `Nothing()` on mixed-type values when [`NIL`](../literals/nil.md), blank input, `0`, and [`.F.`](../literals/false.md) should all stop processing.
    - Prefer [`Empty`](Empty.md) instead when `"0"` is a meaningful text value that must be preserved.

!!! failure "Don't"
    - Use `Nothing()` when the literal string `"0"` is a valid code, quantity, or response in your workflow.
    - Assume `Nothing()` only extends [`Empty()`](Empty.md) for numeric zero. The extra behavior is the exact stringified value `"0"`.
    - Treat `Nothing()`, [`Empty`](Empty.md), and [`IsDefined`](IsDefined.md) as interchangeable. They answer different questions.

## Examples

### Reject a placeholder response of `"0"`

Treat a form value of `"0"` as missing instead of as a real answer.

```ssl
:PROCEDURE ValidateFormResponse;
    :DECLARE sUserResponse, bIsMissing;

    sUserResponse := "0";
    bIsMissing := Nothing(sUserResponse);

    :IF bIsMissing;
        UsrMes("Response is required");
    :ELSE;
        UsrMes("Response recorded: " + sUserResponse);
        /* Displays recorded response with submitted value;
    :ENDIF;

    :RETURN bIsMissing;
:ENDPROC;

/* Usage;
DoProc("ValidateFormResponse");
```

### Normalize imported values to [`NIL`](../literals/nil.md)

Use `Nothing()` to collapse multiple placeholder forms into one missing-value state during import.

```ssl
:PROCEDURE NormalizeImportedValue;
    :PARAMETERS vValue;
    :DECLARE vNormalized;

    :IF Nothing(vValue);
        vNormalized := NIL;
    :ELSE;
        vNormalized := vValue;
    :ENDIF;

    :RETURN vNormalized;
:ENDPROC;

:PROCEDURE NormalizeImportRow;
    :DECLARE aRow, aCleanRow, nIndex;

    aRow := {"", "0", "0.0", "Approved", NIL};
    aCleanRow := {};

    :FOR nIndex := 1 :TO ALen(aRow);
        AAdd(aCleanRow, DoProc("NormalizeImportedValue", {aRow[nIndex]}));
    :NEXT;

    :RETURN aCleanRow;
:ENDPROC;

/* Usage;
DoProc("NormalizeImportRow");
```

### Keep only meaningful queue values

Filter a mixed queue so that only values with real business meaning continue to the next step.

```ssl
:PROCEDURE CollectMeaningfulValues;
    :DECLARE aInput, aKept, vValue, nIndex;

    aInput := {NIL, "", "0", "00", 0, .F., "Ready", 12, .T.};
    aKept := {};

    :FOR nIndex := 1 :TO ALen(aInput);
        vValue := aInput[nIndex];

        :IF Nothing(vValue);
            :LOOP;
        :ENDIF;

        AAdd(aKept, vValue);
    :NEXT;

    :RETURN aKept;
:ENDPROC;

/* Usage;
DoProc("CollectMeaningfulValues");
```

## Related

- [`Empty`](Empty.md)
- [`IsDefined`](IsDefined.md)
- [`boolean`](../types/boolean.md)
