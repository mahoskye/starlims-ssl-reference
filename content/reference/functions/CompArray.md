---
title: "CompArray"
summary: "Determines whether two arrays are exactly equal."
id: ssl.function.comparray
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CompArray

Determines whether two arrays are exactly equal.

`CompArray` compares `a1` and `a2` element by element. The arrays must have the same number of elements, and each matching position must contain the same value type and the same value. If an element is itself an array, `CompArray` compares that nested array recursively.

The function returns [`.T.`](../literals/true.md) only when both arrays have the same shape and every matching position compares equal. Passing [`NIL`](../literals/nil.md) for either top-level argument raises an exception instead of returning [`.F.`](../literals/false.md).

## When to use

- When you need an exact comparison of two arrays, including nested arrays.
- When element order matters and `{1, 2, 3}` must not be treated as equal to `{3, 2, 1}`.
- When you need to verify that a migrated or transformed array still matches the original structure and values.

## Syntax

```ssl
CompArray(a1, a2)
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `a1` | [array](../types/array.md) | yes | — | First array to compare |
| `a2` | [array](../types/array.md) | yes | — | Second array to compare |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when both arrays have the same length and each corresponding element has the same type and exact value. [`.F.`](../literals/false.md) when the length differs, when matching positions hold different types, or when any value or nested array content differs.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `a1` is [`NIL`](../literals/nil.md). | `First array cannot be null.` |
| `a2` is [`NIL`](../literals/nil.md). | `Second array cannot be null.` |

## Best practices

!!! success "Do"
    - Use `CompArray` when you need exact array equality, not just a value lookup.
    - Validate that both arguments are available before calling when [`NIL`](../literals/nil.md) is possible.
    - Treat a [`.F.`](../literals/false.md) result as a structural or value mismatch and inspect the differing position.
    - Use `CompArray` for nested arrays when the full shape must match, not just the top-level length.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for either argument. The function raises an exception instead of returning [`.F.`](../literals/false.md).
    - Use `CompArray` when you only need to know whether one value exists somewhere in an array.
    - Assume two arrays are equal because they contain similar text values. Matching element types are also required.
    - Assume order does not matter. `CompArray` compares each position directly.

## Caveats

- Two [`NIL`](../literals/nil.md) elements at the same position compare as equal, but [`NIL`](../literals/nil.md) on only one side returns [`.F.`](../literals/false.md).
- String elements are compared exactly, so matching prefixes are not enough.

## Examples

### Compare two simple arrays

Compares two identical string arrays and confirms they match.

```ssl
:PROCEDURE CompareStatusLists;
	:DECLARE aExpected, aActual, bMatches;

	aExpected := {"Logged", "Released", "Approved"};
	aActual := {"Logged", "Released", "Approved"};

	bMatches := CompArray(aExpected, aActual);

	:IF bMatches;
		UsrMes("Statuses match.");
	:ELSE;
		UsrMes("Statuses do not match.");
	:ENDIF;

	:RETURN bMatches;
:ENDPROC;

/* Usage;
DoProc("CompareStatusLists");
```

### Detect a type mismatch in matching positions

Shows that `"1001"` (string) and `1001` (number) are not equal even though they represent the same numeric value, because `CompArray` requires matching types at each position.

```ssl
:PROCEDURE CompareTypedValues;
	:DECLARE aExpected, aActual, bMatches;

	aExpected := {"1001", "QC", .T.};
	aActual := {1001, "QC", .T.};

	bMatches := CompArray(aExpected, aActual);

	:IF !bMatches;
		UsrMes("Arrays differ because the first elements are different types.");
	:ENDIF;

	:RETURN bMatches;
:ENDPROC;

/* Usage;
DoProc("CompareTypedValues");
```

### Verify nested configuration arrays after transformation

Verifies that a transformation preserved a deeply nested configuration array by comparing the original and result structures recursively.

```ssl
:PROCEDURE ValidateConfigTransform;
	:DECLARE aOriginalConfig, aTransformedConfig, bMatches;

	aOriginalConfig := {
		{"Instrument", "GC-MS-001"},
		{"Limits", {0.5, 1.0, 5.0}},
		{"Flags", {.T., .F., .T.}}
	};

	aTransformedConfig := {
		{"Instrument", "GC-MS-001"},
		{"Limits", {0.5, 1.0, 5.0}},
		{"Flags", {.T., .F., .T.}}
	};

	bMatches := CompArray(aOriginalConfig, aTransformedConfig);

	:IF bMatches;
		UsrMes("Transformation preserved the nested configuration.");
	:ELSE;
		UsrMes("Transformation changed the nested configuration.");
	:ENDIF;

	:RETURN bMatches;
:ENDPROC;

/* Usage;
DoProc("ValidateConfigTransform");
```

## Related

- [`AScan`](AScan.md)
- [`AScanExact`](AScanExact.md)
- [`array`](../types/array.md)
- [`boolean`](../types/boolean.md)
