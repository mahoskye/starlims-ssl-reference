---
title: "AScanExact"
summary: "Return the index of the first array element that matches a value or condition exactly."
id: ssl.function.ascanexact
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# AScanExact

Return the index of the first array element that matches a value or condition exactly.

AScanExact searches `aTarget` from a 1-based starting position and returns the index of the first match. You can search by value or by passing a code block. If you omit `nStart`, the scan begins at element `1`. If you omit `nCount`, AScanExact searches from `nStart` through the end of the array. If no match is found, it returns `0`.

When `vValueOrBlock` is a regular value, AScanExact compares each element by exact value and only compares non-[`NIL`](../literals/nil.md) elements whose type matches the search value. Unlike [`AScan`](AScan.md), it does not use string prefix matching. When `vValueOrBlock` is a code block, AScanExact calls the block for each element and matches the first element whose block result is boolean [`.T.`](../literals/true.md). If `aTarget` is [`NIL`](../literals/nil.md), AScanExact returns `0`. If the requested search range runs past the end of the array, the scan stops at the last element.

## When to use

- When you need exact string matching instead of [`AScan`](AScan.md) prefix matching.
- When you need the first exact value match in an array.
- When you want to search only part of an array by supplying `nStart` and `nCount`.
- When you need predicate-style matching by passing a code block.

## Syntax

```ssl
AScanExact(aTarget, vValueOrBlock, [nStart], [nCount])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aTarget` | [array](../types/array.md) | yes | — | Array to search. If `aTarget` is [`NIL`](../literals/nil.md), AScanExact returns `0`. |
| `vValueOrBlock` | any | yes | — | Value to match or code block evaluated for each element. |
| `nStart` | [number](../types/number.md) | no | `1` | 1-based index where the scan begins. |
| `nCount` | [number](../types/number.md) | no | `ALen(aTarget)` | Number of elements to scan from `nStart`. If the requested range extends past the end of the array, AScanExact stops at the last element. |

## Returns

**[number](../types/number.md)** — 1-based index of the first exact match, or `0` if no match is found.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `nStart` is not a whole number. | `Starting index must be an integer value.` |
| `nCount` is not a whole number. | `Count must be an integer value.` |
| `nStart < 1`. | `Starting index cannot be less than one.` |
| `nCount < 0`. | `Count cannot be less than zero.` |
| A non-[`NIL`](../literals/nil.md) search value and a scanned non-[`NIL`](../literals/nil.md) element in the scanned range have different types. | `Search value and array elements cannot have different types.` |

## Best practices

!!! success "Do"
    - Use AScanExact when string values must match completely.
    - Pass `nStart` and `nCount` when you want the search window to be explicit.
    - Use a code block when matching depends on a condition instead of a single literal value.

!!! failure "Don't"
    - Use AScanExact when prefix string matching is acceptable. In that case, [`AScan`](AScan.md) is the better fit.
    - Pass fractional or negative scan bounds. AScanExact raises an error for invalid `nStart` or `nCount`.
    - Assume any truthy block result counts as a match. The code block must return boolean [`.T.`](../literals/true.md) for AScanExact to stop on that element.

## Examples

### Find an exact string match

Searches for `"APP"` exactly in an array that also contains `"APPROVED"`. Unlike [`AScan`](AScan.md), `AScanExact` matches only position 1 and skips `"APPROVED"`.

```ssl
:PROCEDURE FindStatusExact;
	:DECLARE aStatuses, nPosition;

	aStatuses := {"APP", "APPROVED", "REJECTED"};
	nPosition := AScanExact(aStatuses, "APP");

	UsrMes("Exact match found at position " + LimsString(nPosition));
:ENDPROC;

/* Usage;
DoProc("FindStatusExact");
```

[`UsrMes`](UsrMes.md) displays:

```text
Exact match found at position 1
```

### Match [`NIL`](../literals/nil.md) values exactly

Scans an array for the first [`NIL`](../literals/nil.md) element by passing [`NIL`](../literals/nil.md) as the search value, which `AScanExact` compares by exact type and value.

```ssl
:PROCEDURE FindFirstNilValue;
	:DECLARE aValues, nPosition;

	aValues := {"READY", NIL, "DONE", NIL};
	nPosition := AScanExact(aValues, NIL);

	UsrMes("First NIL value is at position " + LimsString(nPosition));
:ENDPROC;

/* Usage;
DoProc("FindFirstNilValue");
```

[`UsrMes`](UsrMes.md) displays:

```text
First NIL value is at position 2
```

## Related

- [`AEval`](AEval.md)
- [`AEvalA`](AEvalA.md)
- [`ALen`](ALen.md)
- [`AScan`](AScan.md)
- [`CompArray`](CompArray.md)
- [`array`](../types/array.md)
- [`number`](../types/number.md)
