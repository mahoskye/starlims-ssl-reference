---
title: "DelArray"
summary: "Removes an element from an array at a specified one-based index and returns the same array."
id: ssl.function.delarray
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DelArray

Removes an element from an array at a specified one-based index and returns the same array.

`DelArray` removes the element at `nIndex` from `aTarget`, updates the same array in place, and returns that array. If `nIndex` is greater than the number of elements, the array is returned unchanged. The call raises an error when `aTarget` is [`NIL`](../literals/nil.md), `nIndex` is [`NIL`](../literals/nil.md), `nIndex` is not an integer-valued number, or `nIndex` is less than `1`.

## When to use

- When you need to remove a specific element from an array by its index.
- When cleaning up an array after deleting or processing one of its items.
- When adjusting an array by position without reconstructing it from scratch.

## Syntax

```ssl
DelArray(aTarget, nIndex)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aTarget` | [array](../types/array.md) | yes | — | The array to modify. |
| `nIndex` | [number](../types/number.md) | yes | — | One-based position of the element to remove. Must be an integer-valued number. |

## Returns

**[array](../types/array.md)** — The same target array after removal. When `nIndex` is within bounds, the element is removed and later elements shift left. When `nIndex` exceeds the array length, the array is returned unchanged.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aTarget` is [`NIL`](../literals/nil.md). | `Target array cannot be null.` |
| `nIndex` is [`NIL`](../literals/nil.md). | `Element index cannot be null.` |
| `nIndex` is not an integer-valued number. | `Element index must be an integer value.` |
| `nIndex` is less than `1`. | `Element index cannot be less than one.` |

## Best practices

!!! success "Do"
    - Always check that the array and index are valid before removal.
    - Use [`ALen`](ALen.md) when you need to calculate or validate the one-based index before removal.
    - Use `DelArray` when you want to remove by position without rebuilding the array yourself.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md), a non-integer index, or an index less than one. These cases raise errors.
    - Assume the function creates a copy. `DelArray` modifies the target array you pass in.
    - Rebuild the array manually when you only need to remove one element by position.

## Examples

### Remove an item by index

Displays the array contents before and after removing the element at a given index, showing how later elements shift left.

```ssl
:PROCEDURE RemoveArrayElement;
	:DECLARE aValues, nIndex, sResult;

	aValues := {"Red", "Green", "Blue", "Yellow"};
	nIndex := 2;

	sResult := "Array before deletion: " + BuildString(aValues);
	UsrMes(sResult);

	aValues := DelArray(aValues, nIndex);

	sResult := "Array after removing index " + LimsString(nIndex)
				+ ": " + BuildString(aValues);
	UsrMes(sResult);
:ENDPROC;
```

[`UsrMes`](UsrMes.md) displays:

```text
Array before deletion: Red,Green,Blue,Yellow
Array after removing index 2: Red,Blue,Yellow
```

### Remove matching entries by iterating backwards

Iterates in reverse order to safely remove all entries except a target value, collecting removed items in a separate array without index-shift errors.

```ssl
:PROCEDURE ProcessPendingSamples;
	:DECLARE aPendingSamples, aProcessedSamples;
	:DECLARE sSampleID, nIndex;

	aPendingSamples := {
		"SAMPLE-001", "SAMPLE-002", "SAMPLE-003", "SAMPLE-004", "SAMPLE-005"
	};
	aProcessedSamples := {};

	:FOR nIndex := ALen(aPendingSamples) :TO 1 :STEP (0 - 1);
		sSampleID := aPendingSamples[nIndex];

		:IF !(sSampleID == "SAMPLE-003");
			aPendingSamples := DelArray(aPendingSamples, nIndex);
			AAdd(aProcessedSamples, sSampleID);
		:ENDIF;
	:NEXT;

	UsrMes("Processed: " + BuildString(aProcessedSamples));
	UsrMes("Still pending: " + BuildString(aPendingSamples));
:ENDPROC;
```

[`UsrMes`](UsrMes.md) displays:

```
Processed: SAMPLE-005,SAMPLE-004,SAMPLE-002,SAMPLE-001
Still pending: SAMPLE-003
```

### Remove a pre-specified list of positions

Removes multiple elements by supplying positions in descending order so that each removal does not shift the remaining target indices.

```ssl
:PROCEDURE RemoveMultipleEntries;
	:DECLARE aSampleList, aPositions, nIdx, nRemoved, nIndex, sResult;

	aSampleList := {"Alpha", "Beta", "Gamma", "Delta", "Epsilon"};
	aPositions := {5, 4, 2};
	nRemoved := 0;

	:FOR nIndex := 1 :TO ALen(aPositions);
		nIdx := aPositions[nIndex];

		:IF nIdx >= 1 .AND. nIdx <= ALen(aSampleList);
			aSampleList := DelArray(aSampleList, nIdx);
			nRemoved += 1;
		:ENDIF;
	:NEXT;

	sResult := "Removed " + LimsString(nRemoved)
				+ " entries. Remaining: " + BuildString(aSampleList);
	UsrMes(sResult);

	:RETURN aSampleList;
:ENDPROC;
```

[`UsrMes`](UsrMes.md) displays:

```
Removed 3 entries. Remaining: Alpha,Gamma
```

## Related

- [`AAdd`](AAdd.md)
- [`ALen`](ALen.md)
- [`ArrayCalc`](ArrayCalc.md)
- [`SortArray`](SortArray.md)
- [`array`](../types/array.md)
- [`number`](../types/number.md)
