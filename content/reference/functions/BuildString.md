---
title: "BuildString"
summary: "Builds one string from array elements using a delimiter."
id: ssl.function.buildstring
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# BuildString

Builds one string from array elements using a delimiter.

`BuildString` reads values from `aTarget`, converts each selected element to
text, trims it with [`AllTrim`](AllTrim.md), and joins the results with `sDelimiter`. If an element is [`NIL`](../literals/nil.md), the function writes the literal text [`NIL`](../literals/nil.md) into the result.

If `nStart` is omitted, the function starts at element `1`. If `nCount` is omitted, the function defaults it to `ALen(aTarget)`, which means the effective range runs from `nStart` to the end of the array. If `sDelimiter` is omitted or [`NIL`](../literals/nil.md), the default delimiter is `","`.

`nStart` and `nCount` must be integer-valued numbers. If `nStart` is greater than the array length, the function clamps the start position to the last valid element for non-empty arrays instead of returning an out-of-range error.

## When to use

- When you need to join array values into one delimited string.
- When you want each element trimmed automatically before joining.
- When you need to serialize only part of an array by start position and count.
- When you want [`NIL`](../literals/nil.md) values to appear explicitly as [`NIL`](../literals/nil.md) in the output.

## Syntax

```ssl
BuildString(aTarget, [nStart], [nCount], [sDelimiter])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aTarget` | [array](../types/array.md) | yes | — | Source array to convert into one delimited string. |
| `nStart` | [number](../types/number.md) | no | `1` | 1-based index of the first element to include. Must be an integer-valued number. |
| `nCount` | [number](../types/number.md) | no | `ALen(aTarget)` | Number of elements to include starting at `nStart`. When omitted, the function uses `ALen(aTarget)`, which effectively includes elements from `nStart` through the end of the array. Must be an integer-valued number. |
| `sDelimiter` | [string](../types/string.md) | no | `","` | Delimiter inserted between output elements. |

## Returns

**[string](../types/string.md)** — A delimited string built from the selected array elements after each element is converted to text and trimmed.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aTarget` is [`NIL`](../literals/nil.md). | `Target array cannot be null.` |
| `nStart` is not an integer-valued number. | `Starting index must be an integer value.` |
| `nCount` is not an integer-valued number. | `Element count must be an integer value.` |
| `nStart` is less than `1`. | `Starting index cannot be less than one.` |
| `nCount` is less than `0`. | `Element count cannot be less than zero.` |

## Best practices

!!! success "Do"
    - Pass `sDelimiter` explicitly when another system expects a specific separator.
    - Use `nStart` and `nCount` when you need a predictable slice of the array.
    - Expect [`NIL`](../literals/nil.md) elements to appear as the literal text [`NIL`](../literals/nil.md) in the output.
    - Use [`BuildStringForIn`](BuildStringForIn.md) or [`PrepareArrayForIn`](PrepareArrayForIn.md) when building SQL `IN` values safely.

!!! failure "Don't"
    - Assume leading or trailing spaces are preserved. `BuildString` trims each element before joining.
    - Assume an out-of-range `nStart` returns an empty string for non-empty arrays. The function clamps it to the last element.
    - Pass fractional values for `nStart` or `nCount`. They raise errors instead of being rounded.
    - Use `BuildString` as SQL quoting or escaping logic. It joins plain text only.

## Caveats

- An empty source array returns an empty string.
- `nCount := 0` returns an empty string.
- For non-empty arrays, `nStart` values greater than the array length use the last element as the starting point.
- Elements are converted to text first, then trimmed. The function does not preserve original surrounding whitespace.
- The function does not quote or escape delimiters that already appear inside element text.

## Examples

### Join a simple list with the default delimiter

Uses the default comma delimiter to create one display string from three status values.

```ssl
:PROCEDURE ShowStatusList;
	:DECLARE aStatuses, sStatusList;

	aStatuses := {"Logged", "Complete", "Pending"};
	sStatusList := BuildString(aStatuses);

	UsrMes(sStatusList);

	:RETURN sStatusList;
:ENDPROC;

/* Usage;
DoProc("ShowStatusList");
```

[`UsrMes`](UsrMes.md) displays:

```text
Logged,Complete,Pending
```

### Join a selected range with a custom delimiter

Selects elements 2 and 3 from a four-element array and joins only those with a pipe separator, showing that leading and trailing spaces are trimmed.

```ssl
:PROCEDURE BuildAuditPreview;
	:DECLARE aFields, sPreview;

	aFields := {"ORD-1001", "  pH  ", "Logged", "admin"};
	sPreview := BuildString(aFields, 2, 2, " | ");

	UsrMes(sPreview);

	:RETURN sPreview;
:ENDPROC;

/* Usage;
DoProc("BuildAuditPreview");
```

[`UsrMes`](UsrMes.md) displays:

```text
pH | Logged
```

### Show [`NIL`](../literals/nil.md) handling and out-of-range start behavior

Demonstrates that [`NIL`](../literals/nil.md) elements become the literal text [`NIL`](../literals/nil.md) in the output, and that an oversized `nStart` on a non-empty array clamps to the last element.

```ssl
:PROCEDURE DemonstrateBuildStringBehavior;
	:DECLARE aValues, sWithNil, sClamped;

	aValues := {"  A  ", NIL, "  C  "};

	sWithNil := BuildString(aValues, 1, 3, "/");
	sClamped := BuildString(aValues, 99, 1, "/");

	UsrMes(sWithNil);  /* Displays: A/NIL/C;
	UsrMes(sClamped);  /* Displays: C;

	:RETURN sClamped;
:ENDPROC;

/* Usage;
DoProc("DemonstrateBuildStringBehavior");
```

## Related

- [`BuildArray`](BuildArray.md)
- [`BuildArray2`](BuildArray2.md)
- [`BuildString2`](BuildString2.md)
- [`BuildStringForIn`](BuildStringForIn.md)
- [`PrepareArrayForIn`](PrepareArrayForIn.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
