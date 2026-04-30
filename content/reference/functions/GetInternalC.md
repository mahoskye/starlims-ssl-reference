---
title: "GetInternalC"
summary: "Retrieves a value by applying a chained series of index operations to a root value."
id: ssl.function.getinternalc
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetInternalC

Retrieves a value by applying a chained series of index operations to a root value.

`GetInternalC` requires a root value, a non-null `sCollectionName`, and a non-null first index. It then applies `vArg1` through `vArg6` in order, stopping at the last supplied index. For example, if only `vArg1` and `vArg2` are provided, the function returns the result of indexing the root value twice. The function does not modify the target value.

## When to use

- When the path you need to read is built at runtime rather than written
  directly in source.
- When you need to read beyond a single property or index lookup.
- When the same code may stop at different depths depending on how many index
  values are available.

## Syntax

```ssl
GetInternalC(oTarget, sCollectionName, vArg1, [vArg2], [vArg3], [vArg4], [vArg5], [vArg6])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `oTarget` | [object](../types/object.md) | yes | — | Root value to read from |
| `sCollectionName` | [string](../types/string.md) | yes | — | Required non-null string. Its value is not used in the index chain; pass a descriptive label by convention. |
| `vArg1` | any | yes | — | First index applied to the root value |
| `vArg2` | any | no | [`NIL`](../literals/nil.md) | Second index in the chain |
| `vArg3` | any | no | [`NIL`](../literals/nil.md) | Third index in the chain |
| `vArg4` | any | no | [`NIL`](../literals/nil.md) | Fourth index in the chain |
| `vArg5` | any | no | [`NIL`](../literals/nil.md) | Fifth index in the chain |
| `vArg6` | any | no | [`NIL`](../literals/nil.md) | Sixth index in the chain |

## Returns

**any** — The value reached after applying the supplied index chain.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `oTarget` is [`NIL`](../literals/nil.md). | `Argument oTarget cannot be null.` |
| `sCollectionName` is [`NIL`](../literals/nil.md). | `Argument sCollectionName cannot be null.` |
| `vArg1` is [`NIL`](../literals/nil.md). | `Argument vArg1 cannot be null.` |

## Best practices

!!! success "Do"
    - Pass only the depth you actually need. Omit trailing optional index arguments when the lookup ends earlier.
    - Validate or control the index path before calling when the target structure may vary.
    - Use [`GetInternal`](GetInternal.md) instead when you only need one named property lookup.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `oTarget`, `sCollectionName`, or `vArg1`. Those inputs raise an error immediately.
    - Supply deeper index arguments unless every earlier step is valid for the target structure.
    - Assume a failed nested lookup will quietly return an empty value. The
      indexed value may raise its own runtime error.

## Caveats

- The function only checks `oTarget`, `sCollectionName`, and `vArg1` for [`NIL`](../literals/nil.md); a [`NIL`](../literals/nil.md) value in `vArg2`–`vArg6` simply terminates the chain rather than raising an exception.
- Any later failure depends on how the target value handles indexing at that step.

## Examples

### Read a value with two index steps

Read a nested value from a two-dimensional array.

```ssl
:PROCEDURE ReadMatrixValue;
	:DECLARE aMatrix, sValue;

	aMatrix := {
		{"A1", "A2"},
		{"B1", "B2"}
	};

	sValue := GetInternalC(aMatrix, "Matrix", 2, 1);

	UsrMes("Selected value: " + sValue);

	:RETURN sValue;
:ENDPROC;

/* Usage;
DoProc("ReadMatrixValue");
```

[`UsrMes`](UsrMes.md) displays:

```text
Selected value: B1
```

### Stop at different depths based on the path you need

Use the same nested structure to return either an entire sub-array or one final value from inside it.

```ssl
:PROCEDURE ReadBatchMetrics;
	:DECLARE aBatches, aMetrics, nReleased, nPending;

	aBatches := {
		{"Batch-001", {12, 3}},
		{"Batch-002", {9, 1}}
	};

	aMetrics := GetInternalC(aBatches, "Batches", 1, 2);
	nReleased := GetInternalC(aBatches, "Batches", 1, 2, 1);
	nPending := GetInternalC(aBatches, "Batches", 1, 2, 2);

	UsrMes(
		"Batch-001 metrics: released="
		+ LimsString(nReleased)
		+ ", pending="
		+ LimsString(nPending)
	);

	:RETURN aMetrics;
:ENDPROC;

/* Usage;
DoProc("ReadBatchMetrics");
```

[`UsrMes`](UsrMes.md) displays:

```text
Batch-001 metrics: released=12, pending=3
```

### Catch a lookup failure when the path is not safe

Handle a runtime error from a deeper lookup when the requested path does not exist in the current structure.

```ssl
:PROCEDURE ReadOptionalMetric;
	:DECLARE aBatches, vValue, oErr, sMessage;

	aBatches := {
		{"Batch-001", {12, 3}},
		{"Batch-002", {9, 1}}
	};
	sMessage := "";

	:TRY;
		vValue := GetInternalC(aBatches, "Batches", 3, 2, 1);
		sMessage := "Metric: " + LimsString(vValue);
	:CATCH;
		oErr := GetLastSSLError();
		sMessage := "Lookup failed: " + oErr:Description;
	:ENDTRY;

	UsrMes(sMessage);

	:RETURN sMessage;
:ENDPROC;

/* Usage;
DoProc("ReadOptionalMetric");
```

[`UsrMes`](UsrMes.md) displays a runtime-specific failure message, such as:

```text
Lookup failed: Subscript out of range
```

## Related

- [`ExecInternal`](ExecInternal.md)
- [`GetInternal`](GetInternal.md)
- [`SetInternal`](SetInternal.md)
- [`SetInternalC`](SetInternalC.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
