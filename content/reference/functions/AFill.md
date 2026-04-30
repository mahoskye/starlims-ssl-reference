---
title: "AFill"
summary: "Fill an array element range with the same value and return the same array."
id: ssl.function.afill
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# AFill

Fill an array element range with the same value and return the same array.

AFill updates the original array in place. It starts at a 1-based index and writes the supplied value into each selected element. If you omit `nStart`, the fill begins at element `1`. If you omit `nCount`, AFill uses the current array length as the count, so the operation fills from `nStart` through the end of the array.

AFill does not grow the array. If `nStart + nCount - 1` goes past the last element, filling stops at the end of the array. AFill raises an error when the target array is [`NIL`](../literals/nil.md), when `nStart` or `nCount` is not an integer value, when `nStart` is less than `1` or greater than the array length, or when `nCount` is negative. A `nCount` value of `0` is valid and leaves the array unchanged.

## When to use

- When you need to reset all elements in an existing array to the same value.
- When you need to overwrite a known slice of an array without writing a loop.
- When you need to clear the remaining positions in a work array before reuse.

## Syntax

```ssl
AFill(aTarget, vValue, [nStart], [nCount])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aTarget` | [array](../types/array.md) | yes | — | Array to update. |
| `vValue` | any | yes | — | Value written into each selected element. |
| `nStart` | [number](../types/number.md) | no | `1` | 1-based index of the first element to fill. |
| `nCount` | [number](../types/number.md) | no | `ALen(aTarget)` | Number of elements to fill. If omitted, AFill uses the current array length and fills from `nStart` to the end. If the requested range extends past the end of the array, AFill stops at the last element. |

## Returns

**[array](../types/array.md)** — The same array passed in as `aTarget`, after the fill operation.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aTarget` is [`NIL`](../literals/nil.md). | `Target array cannot be null.` |
| `nStart` is not a whole number. | `Starting index must be an integer value.` |
| `nCount` is not a whole number. | `Count must be an integer value.` |
| `nStart` is outside the valid array range. | `Starting index cannot be less than one or greater than total number of elements in the array.` |
| `nCount < 0`. | `Count cannot be less than zero.` |

## Best practices

!!! success "Do"
    - Use AFill when you want to update the existing array in place.
    - Pass `nStart` and `nCount` when you need to limit the change to a known slice of the array.
    - Validate array bounds before calling AFill when indexes come from user input or calculated positions.

!!! failure "Don't"
    - Use AFill when you need to preserve the original array values. It changes `aTarget` directly.
    - Assume AFill will create missing elements. It only writes within the existing array bounds.
    - Pass fractional, negative, or out-of-range indexes. AFill raises an error instead of adjusting invalid input for you.

## Examples

### Fill every element

Resets every element in a flags array to `"N"` by calling `AFill` with no start or count, then confirms the first and last positions were updated.

```ssl
:PROCEDURE ResetFlags;
    :DECLARE aFlags;

    aFlags := {"Y", "N", "Y", "Y"};

    AFill(aFlags, "N");

    UsrMes("Flag 1: " + aFlags[1]);
    UsrMes("Flag 4: " + aFlags[4]);
:ENDPROC;

/* Usage;
DoProc("ResetFlags");
```

### Fill a selected range

Overwrites elements 2 through 4 with `"REVIEW"` using explicit `nStart` and `nCount` arguments, leaving element 1 (`"NEW"`) and element 5 (`"READY"`) unchanged.

```ssl
:PROCEDURE MarkReviewQueue;
    :DECLARE aSteps;

    aSteps := {"NEW", "NEW", "NEW", "READY", "READY"};

    AFill(aSteps, "REVIEW", 2, 3);

    UsrMes("Step 2: " + aSteps[2]);
    UsrMes("Step 4: " + aSteps[4]);
:ENDPROC;

/* Usage;
DoProc("MarkReviewQueue");
```

## Related

- [`AEval`](AEval.md)
- [`AAdd`](AAdd.md)
- [`ALen`](ALen.md)
- [`AScan`](AScan.md)
- [`array`](../types/array.md)
