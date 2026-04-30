---
title: "AEval"
summary: "Evaluate a code block for each array element and return the same array."
id: ssl.function.aeval
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# AEval

Evaluate a code block for each array element and return the same array.

AEval iterates an array in order, calls the supplied code block once for each selected element, and returns the original array. The code block receives the current element as its argument. AEval ignores the code block's return value, so it is intended for side effects such as logging, updating external variables, or calling other routines while walking an array.

If you omit `nStart`, iteration begins at element `1`. If you omit `nCount`, the count defaults to the array length. When the requested range extends past the end of the array, AEval stops at the last available element instead of raising an out-of-bounds error. If `nStart` is beyond the end of the array or `nCount` is `0`, AEval performs no code block calls and returns the original array unchanged.

Use [`AEvalA`](AEvalA.md) instead when you want the code block result written back into each array position.

## When to use

- When you need for-each style iteration over an array and the code block is performing side effects rather than producing replacement values.
- When you want to process only part of an array by supplying `nStart` and `nCount`.
- When you want a compact alternative to an explicit loop for per-element work.

## Syntax

```ssl
AEval(aTarget, fnBlock, [nStart], [nCount])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `aTarget` | [array](../types/array.md) | yes | — | Array to iterate. |
| `fnBlock` | [code block](../types/codeblock.md) | yes | — | Code block evaluated for each selected element. It receives the current element as its argument. |
| `nStart` | [number](../types/number.md) | no | `1` | 1-based index of the first element to process. |
| `nCount` | [number](../types/number.md) | no | `ALen(aTarget)` | Number of elements to process. `0` performs no iterations. If the requested range extends past the end of the array, AEval stops at the last element. |

## Returns

**[array](../types/array.md)** — The same array passed in as `aTarget`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aTarget` is [`NIL`](../literals/nil.md). | `Target array cannot be null.` |
| `nStart` is not a whole number. | `Starting index must be an integer value.` |
| `nCount` is not a whole number. | `Count must be an integer value.` |
| `nStart < 1`. | `Starting index cannot be less than one.` |
| `nCount < 0`. | `Count cannot be less than zero.` |

## Best practices

!!! success "Do"
    - Use AEval when the purpose of the code block is side effects such as logging, accumulation, or calling another routine for each element.
    - Use `nStart` and `nCount` when you need to limit processing to a known slice of the array.
    - Use [`AEvalA`](AEvalA.md) instead when you want each code block result to replace the current array element.

!!! failure "Don't"
    - Use AEval as a transformation function. It ignores the code block's return value, so `AEval(aValues, {|n| n * 2})` leaves the array contents unchanged.
    - Pass fractional values for `nStart` or `nCount`. AEval requires integer positions and raises an error for non-integer values.
    - Pass negative counts or a starting index below `1`. AEval stops with an error instead of adjusting invalid values for you.

## Examples

### Call a routine for each element

Passes a code block to `AEval` that calls [`UsrMes`](UsrMes.md) for each sample ID, printing one line per element in array order.

```ssl
:PROCEDURE LogSamples;
	:DECLARE aSampleIDs;

	aSampleIDs := {"SAMP-001", "SAMP-002", "SAMP-003"};

	AEval(aSampleIDs, {|sSampleID| UsrMes("Processing " + sSampleID)});
:ENDPROC;

/* Usage;
DoProc("LogSamples");
```

[`UsrMes`](UsrMes.md) displays:

```text
Processing SAMP-001
Processing SAMP-002
Processing SAMP-003
```

### Process a slice of an array

Supplies `nStart` and `nCount` to limit iteration to elements 3 and 4 (the two `"REVIEW"` entries), leaving the rest of the array untouched.

```ssl
:PROCEDURE LogReviewQueue;
	:DECLARE aStatuses, nStart, nCount;

	aStatuses := {"NEW", "NEW", "REVIEW", "REVIEW", "APPROVED"};
	nStart := 3;
	nCount := 2;

	AEval(aStatuses,
          {|sStatus| UsrMes("Queue status: " + sStatus)},
          nStart,
          nCount
         );
:ENDPROC;

/* Usage;
DoProc("LogReviewQueue");
```

[`UsrMes`](UsrMes.md) displays:

```text
Queue status: REVIEW
Queue status: REVIEW
```

## Related

- [`AEvalA`](AEvalA.md)
- [`AFill`](AFill.md)
- [`AScan`](AScan.md)
- [`AScanExact`](AScanExact.md)
- [`array`](../types/array.md)
