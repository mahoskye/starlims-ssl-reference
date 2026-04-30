---
title: "ALen"
summary: "Return the number of elements in an array."
id: ssl.function.alen
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ALen

Return the number of elements in an array.

`ALen` returns the current element count of `aTarget`. It accepts a single array argument, returns `0` for an empty array, and raises an error when `aTarget` is [`NIL`](../literals/nil.md).

Use `ALen` when you want the code to make it explicit that the input must be an array.

## When to use

- When you need to test whether an array has any elements before processing it.
- When you need an array count for loop bounds or validation logic.
- When you want array-focused code to read explicitly instead of relying on the broader [`Len`](Len.md) function.

## Syntax

```ssl
ALen(aTarget)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aTarget` | [array](../types/array.md) | yes | — | Array whose current element count to return. |

## Returns

**[number](../types/number.md)** — Number of elements currently in `aTarget`. Returns `0` when the array is empty.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aTarget` is [`NIL`](../literals/nil.md). | `Target array cannot be null.` |

## Best practices

!!! success "Do"
    - Use ALen when you want to make it obvious that the input must be an array.
    - Check the returned count before reading array elements by index.
    - Use the result directly in loop bounds and guard conditions.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) and expect a zero result. ALen raises an error for a null array.
    - Use ALen for strings or other non-array values. It is an array-specific function.
    - Assume a nonzero count means a particular element is valid for your business rule. It only tells you how many elements exist.

## Examples

### Check whether an array is empty

Reads the element count with `ALen` and guards against processing an empty selection before continuing.

```ssl
:PROCEDURE ProcessUserSelection;
    :DECLARE aSelectedItems, nCount;

    aSelectedItems := {"SAMPLE-001", "SAMPLE-002"};
    nCount := ALen(aSelectedItems);

    :IF nCount == 0;
        UsrMes("No items selected.");
        :RETURN;
    :ENDIF;

    UsrMes("Processing " + LimsString(nCount) + " selected item(s)");
:ENDPROC;

/* Usage;
DoProc("ProcessUserSelection");
```

[`UsrMes`](UsrMes.md) displays:

```
Processing 2 selected item(s)
```

### Use ALen as a loop boundary

Passes `ALen` directly to the [`:FOR`](../keywords/FOR.md) upper bound so the loop always iterates the exact number of elements in the array, regardless of how many are present.

```ssl
:PROCEDURE ShowPendingSteps;
    :DECLARE aSteps, nIndex;

    aSteps := {"Login", "Review", "Approve"};

    :FOR nIndex := 1 :TO ALen(aSteps);
        UsrMes("Step " + LimsString(nIndex) + ": " + aSteps[nIndex]);
    :NEXT;
:ENDPROC;

/* Usage;
DoProc("ShowPendingSteps");
```

[`UsrMes`](UsrMes.md) displays:

```
Step 1: Login
Step 2: Review
Step 3: Approve
```

## Related

- [`AAdd`](AAdd.md)
- [`AFill`](AFill.md)
- [`ArrayNew`](ArrayNew.md)
- [`DelArray`](DelArray.md)
- [`Len`](Len.md)
- [`SortArray`](SortArray.md)
- [`array`](../types/array.md)
- [`number`](../types/number.md)
