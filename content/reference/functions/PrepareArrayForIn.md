---
title: "PrepareArrayForIn"
summary: "Prepares an array for SQL IN clause helpers by mutating it in place."
id: ssl.function.preparearrayforin
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# PrepareArrayForIn

Prepares an array for SQL `IN` clause helpers by mutating it in place.

`PrepareArrayForIn` has two distinct behaviors.

If `aTarget` is empty, it appends one type-appropriate sentinel value so downstream SQL-building logic can still produce a valid `IN (...)` clause that matches no real rows. The sentinel type is chosen based on `sItemType`: `"string"`, `"numeric"`, or `"date"`.

If `aTarget` already has elements, the function does not apply typed defaults. Instead, it only replaces elements that are exactly the empty string `""` with the string sentinel value.

The function returns the same array after mutation. Passing [`NIL`](../literals/nil.md) for `aTarget` raises an argument-null error, and passing a non-array value raises an argument error.

## When to use

- When you need an empty array to become a safe non-matching `IN` filter.
- When you want empty-string elements in an existing array replaced with a non-matching sentinel.
- When you are pairing the result with helpers such as [`BuildStringForIn`](BuildStringForIn.md) or with positional `?` placeholders built to match the array length.

## Syntax

```ssl
PrepareArrayForIn(aTarget, sItemType)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aTarget` | [array](../types/array.md) | yes | — | Array to modify in place before building an SQL `IN` clause. |
| `sItemType` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Type name used only when `aTarget` is empty. Recognized values are [`string`](../types/string.md), `numeric`, and [`date`](../types/date.md), case-insensitively. |

## Returns

**[array](../types/array.md)** — The same array after preparation. Empty input receives one sentinel element based on `sItemType`. Non-empty input keeps its length with `""` elements replaced by the string sentinel.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aTarget` is not [`NIL`](../literals/nil.md) and not an array. | `Argument must be an array` |
| `aTarget` is [`NIL`](../literals/nil.md). | `Value cannot be null.` |

## Best practices

!!! success "Do"
    - Pass `"string"`, `"numeric"`, or `"date"` explicitly when an empty array is possible.
    - Treat the function as an in-place mutator and continue using the same variable afterward.
    - Use it before generating placeholder lists or literal `IN (...)` text so empty input still produces valid SQL.

!!! failure "Don't"
    - Assume it normalizes every kind of empty value in a populated array. It only replaces elements that are exactly `""`.
    - Expect `sItemType` to affect populated arrays. Typed sentinels are only
      used when the array starts empty.
    - Pass numeric type codes such as `1` or undocumented strings and expect typed behavior.

## Caveats

- A non-string `sItemType` is treated like `"string"` when the array is empty.
- An empty-string `sItemType` also falls back to `"string"`.
- If `sItemType` is an unrecognized string, no fallback element is appended to an empty array.
- In a populated array, [`NIL`](../literals/nil.md), [`.F.`](../literals/false.md), `0`, and strings such as `"   "` are not replaced unless the value is exactly `""`.

## Examples

### Prepare an empty array for an `IN (...)` filter

`PrepareArrayForIn` adds a string sentinel to the empty array so [`BuildStringForIn`](BuildStringForIn.md) still produces a valid `IN (...)` clause that matches no real rows.

```ssl
:PROCEDURE BuildEmptySampleFilter;
	:DECLARE aSampleIDs, sInClause, sSQL;

	aSampleIDs := {};
	PrepareArrayForIn(aSampleIDs, "string");

	sInClause := BuildStringForIn(aSampleIDs);
	sSQL :=
		"
	    SELECT sampleid, samplename
	    FROM sample
	    WHERE sampleid IN
	" + sInClause;

	/* Displays the SQL statement with one sentinel value in the IN clause;
	UsrMes(sSQL);

	:RETURN sInClause;
:ENDPROC;

/* Usage;
DoProc("BuildEmptySampleFilter");
```

### Replace empty-string elements in a populated array

The array already has elements, so `PrepareArrayForIn` only replaces the `""` entry with the string sentinel. The `"numeric"` type argument has no effect on a populated array.

```ssl
:PROCEDURE NormalizeExistingFilter;
	:DECLARE aSampleIDs, sInClause;

	aSampleIDs := {"SAM-001", "", "SAM-003"};
	PrepareArrayForIn(aSampleIDs, "numeric");

	sInClause := BuildStringForIn(aSampleIDs);
	/* Displays the IN clause with the empty string replaced by the sentinel;
	UsrMes(sInClause);

	:RETURN aSampleIDs;
:ENDPROC;

/* Usage;
DoProc("NormalizeExistingFilter");
```

### Keep a parameterized `IN` query valid when the input array is empty

When `aOrderIDs` arrives empty, `PrepareArrayForIn` adds a numeric sentinel (`-2147483648`) so the placeholder list has exactly one `?`. The resulting query executes but matches no rows.

```ssl
:PROCEDURE GetOrdersByIDList;
	:PARAMETERS aOrderIDs;
	:DECLARE sTemp, sPlaceholders, sSQL, aResults;

	PrepareArrayForIn(aOrderIDs, "numeric");
	sTemp := Replicate("?,", ALen(aOrderIDs));
	sPlaceholders := Left(sTemp, Len(sTemp) - 1);

	sSQL :=
		"
	    SELECT orderid, ordno, status
	    FROM orders
	    WHERE orderid IN (
	" + sPlaceholders
		+ ")";

	aResults := LSelect1(sSQL,, aOrderIDs);

	:RETURN aResults;
:ENDPROC;

/* Usage;
DoProc("GetOrdersByIDList", {{1001, 1002}});
```

## Related

- [`AddNameDelimiters`](AddNameDelimiters.md)
- [`BuildArray`](BuildArray.md)
- [`BuildArray2`](BuildArray2.md)
- [`BuildString`](BuildString.md)
- [`BuildString2`](BuildString2.md)
- [`BuildStringForIn`](BuildStringForIn.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
