---
title: "SetInternalC"
summary: "Assigns a value through a chained index path on a target value and returns NIL."
id: ssl.function.setinternalc
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SetInternalC

Assigns a value through a chained index path on a target value and returns [`NIL`](../literals/nil.md).

`SetInternalC` requires a target value `oTarget`, a non-null `sCollectionName`, a value to assign, and a non-null first index. It then walks the supplied index path from `vArg1` through `vArg6` and writes `vValue` at the last supplied step. For example, if only `vArg1` and `vArg2` are provided, the function assigns through a two-step path. If more index arguments are supplied, the assignment happens deeper in the nested structure.

`SetInternalC` raises an error when `oTarget`, `sCollectionName`, or `vArg1` is [`NIL`](../literals/nil.md) and always returns [`NIL`](../literals/nil.md) after the assignment attempt. Any other runtime behavior depends on how the target value handles indexed access.

## When to use

- When the index path is built at runtime rather than written directly in code.
- When you need to update a nested array or other indexable value at variable
  depth.
- When direct source syntax is not practical because the path segments are held
  in variables.

## Syntax

```ssl
SetInternalC(oTarget, sCollectionName, vValue, vArg1, [vArg2], [vArg3], [vArg4], [vArg5], [vArg6])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `oTarget` | any | yes | — | Target value that receives the indexed assignment |
| `sCollectionName` | [string](../types/string.md) | yes | — | Required non-null string. Its value is not used in the index chain; pass a descriptive label by convention. |
| `vValue` | any | yes | — | Value assigned at the final index step |
| `vArg1` | any | yes | — | First index in the assignment path |
| `vArg2` | any | no | — | Second index in the assignment path |
| `vArg3` | any | no | — | Third index in the assignment path |
| `vArg4` | any | no | — | Fourth index in the assignment path |
| `vArg5` | any | no | — | Fifth index in the assignment path |
| `vArg6` | any | no | — | Sixth index in the assignment path |

## Returns

**NIL** — Always returns [`NIL`](../literals/nil.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `oTarget` is [`NIL`](../literals/nil.md). | `Argument oTarget cannot be null.` |
| `sCollectionName` is [`NIL`](../literals/nil.md). | `Argument sCollectionName cannot be null.` |
| `vArg1` is [`NIL`](../literals/nil.md). | `Argument vArg1 cannot be null.` |

## Best practices

!!! success "Do"
    - Pass only the index depth you actually need, and omit unused trailing arguments.
    - Read the current value with [`GetInternalC`](GetInternalC.md) first when overwriting a nested location matters.
    - Validate that each earlier step in the path is valid for the target value before assigning deeper into it.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `oTarget`, `sCollectionName`, or `vArg1`. Those inputs raise an immediate error.
    - Supply deeper index arguments unless the target really supports that full path.
    - Expect `SetInternalC` to return the assigned value or a success flag. It always returns [`NIL`](../literals/nil.md).

## Caveats

- `SetInternalC` writes at the last supplied non-null index argument.
- Any failure beyond the null checks on `oTarget`, `sCollectionName`, and `vArg1`
  depends on the target value's indexed access behavior.

## Examples

### Update one value in a two-dimensional array

Replace a single matrix cell by supplying two index arguments.

```ssl
:PROCEDURE UpdateMatrixCell;
	:DECLARE aMatrix, sValue;

	aMatrix := {
		{"Pending", "Pending"},
		{"Pending", "Pending"}
	};

	SetInternalC(aMatrix, "Matrix", "Released", 2, 1);
	sValue := GetInternalC(aMatrix, "Matrix", 2, 1);

	UsrMes("Updated value: " + sValue);

	:RETURN sValue;
:ENDPROC;

/* Usage;
DoProc("UpdateMatrixCell");
```

[`UsrMes`](UsrMes.md) displays:

```text
Updated value: Released
```

### Update a nested metric inside a row structure

Write through a three-step path where one element contains another array.

```ssl
:PROCEDURE UpdateBatchMetric;
	:DECLARE aBatches, nPending;

	aBatches := {
		{"Batch-001", {12, 3}},
		{"Batch-002", {9, 1}}
	};

	SetInternalC(aBatches, "Batches", 4, 1, 2, 2);
	nPending := GetInternalC(aBatches, "Batches", 1, 2, 2);

	UsrMes("Batch-001 pending count: " + LimsString(nPending));

	:RETURN nPending;
:ENDPROC;

/* Usage;
DoProc("UpdateBatchMetric");
```

[`UsrMes`](UsrMes.md) displays:

```text
Batch-001 pending count: 4
```

### Verify the current value before updating a deeper path

Read a four-step path, update it only when needed, and catch a bad lookup or assignment path.

```ssl
:PROCEDURE ApproveNestedResult;
	:DECLARE aRuns, sCurrentStatus, sFinalStatus, oErr;

	aRuns := {
		{"Batch-001", {
			{"pH", 7.2, "P"},
			{"Conductivity", 1420, "P"}
		}}
	};
	sFinalStatus := "";

	:TRY;
		sCurrentStatus := GetInternalC(aRuns, "Runs", 1, 2, 2, 3);

		:IF !(sCurrentStatus == "A");
			SetInternalC(aRuns, "Runs", "A", 1, 2, 2, 3);
		:ENDIF;

		sFinalStatus := GetInternalC(aRuns, "Runs", 1, 2, 2, 3);
	:CATCH;
		oErr := GetLastSSLError();
		sFinalStatus := "Update failed: " + oErr:Description;
	:ENDTRY;

	UsrMes(sFinalStatus);

	:RETURN sFinalStatus;
:ENDPROC;

/* Usage;
DoProc("ApproveNestedResult");
```

[`UsrMes`](UsrMes.md) displays:

```text
A
```

## Related

- [`ExecInternal`](ExecInternal.md)
- [`GetInternal`](GetInternal.md)
- [`GetInternalC`](GetInternalC.md)
- [`SetInternal`](SetInternal.md)
- [`array`](../types/array.md)
