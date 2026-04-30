---
title: "SetInternal"
summary: "Assigns a value to a named property on a target value and returns NIL."
id: ssl.function.setinternal
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SetInternal

Assigns a value to a named property on a target value and returns [`NIL`](../literals/nil.md).

`SetInternal` takes a target value, a property name, and a value to assign. It raises an error when `oTarget` or `sPropName` is [`NIL`](../literals/nil.md), then delegates the assignment to the target's property-set behavior. The function itself always returns [`NIL`](../literals/nil.md), so it does not report the assigned value or provide a success flag.

## When to use

- When the property name is only known at runtime.
- When you are iterating over property names and assigning values dynamically.
- When direct source syntax such as `oValue:Status := "Active";` is not practical because the member name is stored in a variable.

## Syntax

```ssl
SetInternal(oTarget, sPropName, vPropValue)
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `oTarget` | any | yes | — | Target value whose property will be assigned |
| `sPropName` | [string](../types/string.md) | yes | — | Name of the property to set |
| `vPropValue` | any | yes | — | Value to assign to the named property |

## Returns

**NIL** — Always returns [`NIL`](../literals/nil.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `oTarget` is [`NIL`](../literals/nil.md). | `Argument oTarget cannot be null.` |
| `sPropName` is [`NIL`](../literals/nil.md). | `Argument sPropName cannot be null.` |

## Best practices

!!! success "Do"
    - Check that the target value and property name are available before calling.
    - Use `SetInternal` when the property name is stored in a variable or built dynamically.
    - Read the property back with [`GetInternal`](GetInternal.md) when later logic depends on the assigned value.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `oTarget` or `sPropName`. The function raises an error instead of doing nothing.
    - Expect a confirmation value from `SetInternal`. It always returns [`NIL`](../literals/nil.md).
    - Use `SetInternal` for indexed collection updates. Use [`SetInternalC`](SetInternalC.md) when you need indexed assignment.

## Caveats

- Any additional behavior depends on the target value's own property-set logic.

## Examples

### Update one property using a runtime name

Update a property when the member name is stored in a variable.

```ssl
:PROCEDURE UpdateSampleStatus;
	:DECLARE oSample, sPropName, sStatus;

	oSample := CreateUdObject();
	oSample:Status := "Pending";

	sPropName := "Status";
	sStatus := "Released";

	SetInternal(oSample, sPropName, sStatus);

	UsrMes("Status: " + GetInternal(oSample, sPropName));
:ENDPROC;

/* Usage;
DoProc("UpdateSampleStatus");
```

[`UsrMes`](UsrMes.md) displays:

```text
Status: Released
```

### Apply several dynamic assignments from a field list

Loop through field definitions and assign each value by property name.

```ssl
:PROCEDURE ApplySampleUpdates;
	:DECLARE oSample, aUpdates, sPropName, vPropValue, nIndex;

	oSample := CreateUdObject();
	oSample:SampleID := "LAB-2024-0042";
	oSample:Status := "Pending";
	oSample:Priority := 1;
	oSample:AssignedTo := "";

	aUpdates := {
		{"Status", "Approved"},
		{"Priority", 2},
		{"AssignedTo", "JSMITH"}
	};

	:FOR nIndex := 1 :TO ALen(aUpdates);
		sPropName := aUpdates[nIndex, 1];
		vPropValue := aUpdates[nIndex, 2];

		SetInternal(oSample, sPropName, vPropValue);
	:NEXT;

	UsrMes(
		"Sample " + GetInternal(oSample, "SampleID")
		+ ": status=" + GetInternal(oSample, "Status")
		+ ", priority=" + LimsString(GetInternal(oSample, "Priority"))
		+ ", assigned to=" + GetInternal(oSample, "AssignedTo")
	);

	:RETURN oSample;
:ENDPROC;

/* Usage;
DoProc("ApplySampleUpdates");
```

[`UsrMes`](UsrMes.md) displays:

```text
Sample LAB-2024-0042: status=Approved, priority=2, assigned to=JSMITH
```

## Related

- [`ExecInternal`](ExecInternal.md)
- [`GetInternal`](GetInternal.md)
- [`GetInternalC`](GetInternalC.md)
- [`SetInternalC`](SetInternalC.md)
- [`object`](../types/object.md)
- [`string`](../types/string.md)
