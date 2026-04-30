---
title: "AEvalA"
summary: "Evaluate a code block for each selected array element and write the result back to the same array."
id: ssl.function.aevala
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# AEvalA

Evaluate a code block for each selected array element and write the result back to the same array.

AEvalA iterates an array in order, calls the supplied code block once for each selected element, stores the code block result into that array position, and returns the same array. The code block receives the current element as its argument.

If you omit `nStart`, processing begins at element `1`. If you omit `nCount`, AEvalA processes from `nStart` through the end of the array. When the requested range extends past the end of the array, AEvalA stops at the last available element instead of raising an out-of-bounds error. If `nStart` is beyond the end of the array or `nCount` is `0`, AEvalA makes no updates and returns the original array unchanged.

Use [`AEval`](AEval.md) instead when you want to evaluate each element without replacing the array contents.

## When to use

- When you want to transform existing array values in place.
- When you need to update only part of an array by supplying `nStart` and `nCount`.
- When returning the same array is convenient for follow-on processing.

## Syntax

```ssl
AEvalA(aTarget, fnBlock, [nStart], [nCount])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aTarget` | [array](../types/array.md) | yes | — | Array to process and update. |
| `fnBlock` | [code block](../types/codeblock.md) | yes | — | Code block evaluated for each selected element. Its return value replaces the current element. |
| `nStart` | [number](../types/number.md) | no | `1` | 1-based index of the first element to process. |
| `nCount` | [number](../types/number.md) | no | `ALen(aTarget)` | Number of elements to process. `0` performs no updates. If the requested range extends past the end of the array, AEvalA stops at the last element. |

## Returns

**[array](../types/array.md)** — The same array passed in as `aTarget`, after the selected elements have been updated.

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
    - Use AEvalA when the code block result should replace each processed element.
    - Use `nStart` and `nCount` to limit updates to a known slice of the array.
    - Keep the code block focused on producing the replacement value for the current element.

!!! failure "Don't"
    - Use AEvalA when you need to preserve the original array contents. AEvalA writes each code block result back into the array.
    - Pass fractional values for `nStart` or `nCount`. AEvalA requires integer positions and raises an error for non-integer values.
    - Pass a starting index below `1` or a negative count. AEvalA stops with an error instead of adjusting invalid values for you.

## Examples

### Transform array values in place

Trims whitespace and uppercases each sample ID string in place using a single `AEvalA` call, then confirms all three positions were updated.

```ssl
:PROCEDURE NormalizeSampleIDs;
	:DECLARE aSampleIDs;

	aSampleIDs := {" samp-001 ", " samp-002 ", " samp-003 "};

	AEvalA(aSampleIDs, {|sSampleID| Upper(AllTrim(sSampleID))});

	UsrMes(aSampleIDs[1] + ", " + aSampleIDs[2] + ", " + aSampleIDs[3]);
:ENDPROC;

/* Usage;
DoProc("NormalizeSampleIDs");
```

[`UsrMes`](UsrMes.md) displays:

```text
SAMP-001, SAMP-002, SAMP-003
```

### Update only a slice of an array

Supplies `nStart` and `nCount` to update only elements 3 and 4 with a prefix, leaving element 5 (`"APPROVED"`) unchanged.

```ssl
:PROCEDURE FlagReviewResults;
	:DECLARE aStatuses, nStart, nCount;

	aStatuses := {"NEW", "NEW", "REVIEW", "REVIEW", "APPROVED"};
	nStart := 3;
	nCount := 2;

	AEvalA(aStatuses, {|sStatus| "IN REVIEW: " + sStatus}, nStart, nCount);

	UsrMes(aStatuses[3] + " | " + aStatuses[4] + " | " + aStatuses[5]);
:ENDPROC;

/* Usage;
DoProc("FlagReviewResults");
```

[`UsrMes`](UsrMes.md) displays:

```text
IN REVIEW: REVIEW | IN REVIEW: REVIEW | APPROVED
```

## Related

- [`AEval`](AEval.md)
- [`AFill`](AFill.md)
- [`AScan`](AScan.md)
- [`AScanExact`](AScanExact.md)
- [`array`](../types/array.md)
