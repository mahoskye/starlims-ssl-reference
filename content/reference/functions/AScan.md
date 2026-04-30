---
title: "AScan"
summary: "Return the index of the first array element that matches a value or condition."
id: ssl.function.ascan
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# AScan

Return the index of the first array element that matches a value or condition.

AScan searches `aTarget` from a 1-based starting position and returns the index of the first match. You can search by value or by passing a code block. If you omit `nStart`, the scan begins at element `1`. If you omit `nCount`, AScan searches from `nStart` through the end of the array. If no match is found, it returns `0`.

When `vValueOrBlock` is a regular value, AScan compares each element only when the element and the search value have the same type. For strings, AScan uses prefix matching rather than exact matching, so a search for `"APP"` matches `"APPROVED"`. When `vValueOrBlock` is a code block, AScan calls the block for each element and matches the first element whose block result is boolean [`.T.`](../literals/true.md). If `aTarget` is [`NIL`](../literals/nil.md), AScan returns `0`.

## When to use

- When you need the position of the first matching value in an array.
- When you want to search only part of an array by supplying `nStart` and `nCount`.
- When you need predicate-style matching by passing a code block.
- When string prefix matching is acceptable and you do not need exact string
  equality.

## Syntax

```ssl
AScan(aTarget, vValueOrBlock, [nStart], [nCount])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aTarget` | [array](../types/array.md) | yes | — | Array to search. If `aTarget` is [`NIL`](../literals/nil.md), AScan returns `0`. |
| `vValueOrBlock` | any | yes | — | Value to match or code block evaluated for each element. |
| `nStart` | [number](../types/number.md) | no | `1` | 1-based index where the scan begins. |
| `nCount` | [number](../types/number.md) | no | `ALen(aTarget)` | Number of elements to scan from `nStart`. If the requested range extends past the end of the array, AScan stops at the last element. |

## Returns

**[number](../types/number.md)** — 1-based index of the first match, or `0` if no match is found.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `nStart` is not a whole number. | `Starting index must be an integer value.` |
| `nCount` is not a whole number. | `Count must be an integer value.` |
| `nStart < 1`. | `Starting index cannot be less than one.` |
| `nCount < 0`. | `Count cannot be less than zero.` |
| A non-[`NIL`](../literals/nil.md) search value and a scanned element have different types. | `Search value and array elements cannot have different types.` |

## Best practices

!!! success "Do"
    - Use AScan with a code block when the matching rule depends on element content rather than a single literal value.
    - Pass `nStart` and `nCount` when you want the search window to be explicit.
    - Use [`AScanExact`](AScanExact.md) when string matches must be exact instead of prefix-based.

!!! failure "Don't"
    - Expect exact string matching from AScan. `"APP"` matches `"APPROVED"` because string searches use prefix comparison.
    - Pass fractional or negative scan bounds. AScan raises an error for invalid `nStart` or `nCount`.
    - Assume any truthy block result counts as a match. The code block must return boolean [`.T.`](../literals/true.md) for AScan to stop on that element.

## Examples

### Find a value in an array

Searches for `"REJ"` as a prefix, which matches `"REJECTED"` at position 3 because `AScan` uses prefix matching for string searches.

```ssl
:PROCEDURE FindStatus;
	:DECLARE aStatuses, nPosition;

	aStatuses := {"PENDING", "APPROVED", "REJECTED", "COMPLETED"};
	nPosition := AScan(aStatuses, "REJ");

	UsrMes("Matching status found at position " + LimsString(nPosition));
:ENDPROC;

DoProc("FindStatus");
```

[`UsrMes`](UsrMes.md) displays:

```
Matching status found at position 3
```

### Find the first element that satisfies a condition

Passes a code block that tests for even numbers; `AScan` returns the position of `12`, the first element for which the block returns [`.T.`](../literals/true.md).

```ssl
:PROCEDURE FindFirstEven;
	:DECLARE aNumbers, nIndex, fnIsEven;

	aNumbers := {7, 3, 12, 5, 8, 21};
	fnIsEven := {|nValue| nValue % 2 == 0};

	nIndex := AScan(aNumbers, fnIsEven);

	UsrMes("First even number is at position " + LimsString(nIndex));
:ENDPROC;

DoProc("FindFirstEven");
```

[`UsrMes`](UsrMes.md) displays:

```
First even number is at position 3
```

## Related

- [`AEval`](AEval.md)
- [`AEvalA`](AEvalA.md)
- [`AFill`](AFill.md)
- [`AScanExact`](AScanExact.md)
- [`CompArray`](CompArray.md)
- [`array`](../types/array.md)
- [`number`](../types/number.md)
