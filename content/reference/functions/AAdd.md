---
title: "AAdd"
summary: "Appends an element to the end of an array and returns the appended element."
id: ssl.function.aadd
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# AAdd

Appends an element to the end of an array and returns the appended element.

`AAdd` appends one value to an existing array. It updates the target array in place and returns the appended value. If the target array is [`NIL`](../literals/nil.md), the call raises an error.

## When to use

- When you are building an array one value at a time.
- When you need to collect values during a loop.
- When you want to append a value without rebuilding the whole array.

## Syntax

```ssl
AAdd(aTarget, vElement)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aTarget` | [array](../types/array.md) | yes | — | Existing array to modify. |
| `vElement` | any | yes | — | Value to append as the new last element. |

## Returns

**any** — The appended value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aTarget` is [`NIL`](../literals/nil.md). | `Target array cannot be null.` |

## Best practices

!!! success "Do"
    - Initialize the array before appending, for example with an array literal such as `{}` or with [`ArrayNew`](ArrayNew.md).
    - Use `AAdd` inside loops when you need to collect matching values into one result array.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) as the target array. `AAdd` only works with an existing array and raises `Target array cannot be null.` when the target is [`NIL`](../literals/nil.md).
    - Assume the return value is the updated array. `AAdd` returns the appended value, so code that needs the array should keep using `aTarget`.

## Examples

### Append only matching values

Iterates a two-column array of order numbers and statuses, appending each open order number to a results array with `AAdd`. The returned array contains only the entries that matched.

```ssl
:PROCEDURE CollectOpenOrders;
	:DECLARE aOrderRows, aOpenOrdnos, nIndex;

	aOrderRows := {
		{"ORD-1001", "Open"},
		{"ORD-1002", "Closed"},
		{"ORD-1003", "Open"}
	};
	aOpenOrdnos := {};

	:FOR nIndex := 1 :TO ALen(aOrderRows);
		:IF aOrderRows[nIndex, 2] == "Open";
			AAdd(aOpenOrdnos, aOrderRows[nIndex, 1]);
		:ENDIF;
	:NEXT;

	:RETURN aOpenOrdnos;
:ENDPROC;

/* Usage;
DoProc("CollectOpenOrders");
```

### Capture the appended value

Appends one batch ID to an existing array and stores the return value of `AAdd` to confirm which value was added.

```ssl
:PROCEDURE AddSelectedBatch;
	:DECLARE aBatchIds, sAddedBatch;

	aBatchIds := {"B-100", "B-200"};
	sAddedBatch := AAdd(aBatchIds, "B-300");

	UsrMes("Added batch " + sAddedBatch);
:ENDPROC;

/* Usage;
DoProc("AddSelectedBatch");
```

[`UsrMes`](UsrMes.md) displays:

```
Added batch B-300
```

## Related

- [`ALen`](ALen.md)
- [`ArrayNew`](ArrayNew.md)
- [`DelArray`](DelArray.md)
- [`array`](../types/array.md)
