---
title: "MakeNETObject"
summary: "Converts an SSL value to a .NET interop object."
id: ssl.function.makenetobject
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# MakeNETObject

Converts an SSL value to a .NET interop object.

Use `MakeNETObject` when SSL code needs to pass a value into .NET interop APIs. The function preserves [`NIL`](../literals/nil.md), returns an existing .NET interop object unchanged, and otherwise converts the supplied SSL value for .NET use.

## When to use

- When a .NET interop API expects a .NET object rather than a plain SSL value.
- When you want [`NIL`](../literals/nil.md) to stay [`NIL`](../literals/nil.md) instead of forcing a replacement value.
- When you need a consistent conversion step before passing values into .NET.

## Syntax

```ssl
MakeNETObject(vValue)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vValue` | any | yes | — | SSL value to convert for .NET interop. |

## Returns

**[object](../types/object.md)** — A .NET interop object wrapping the supplied value. Returns [`NIL`](../literals/nil.md) when `vValue` is [`NIL`](../literals/nil.md), or the original object unchanged when `vValue` is already a .NET interop object.

## Best practices

!!! success "Do"
    - Use `MakeNETObject` at the boundary where SSL values are passed into .NET interop code.
    - Preserve [`NIL`](../literals/nil.md) handling explicitly when downstream .NET logic distinguishes null from a real value.
    - Reuse the returned object directly when the input is already a .NET interop object.

!!! failure "Don't"
    - Use `MakeNETObject` for ordinary SSL-only logic that never crosses into .NET interop.
    - Assume `MakeNETObject(NIL)` returns an object; it returns [`NIL`](../literals/nil.md).
    - Add a second conversion step when you already have a .NET interop object.

## Caveats

- This function prepares a value for .NET interop; it is not general-purpose SSL type conversion.

## Examples

### Convert a string for .NET interop

Convert a plain SSL string to a .NET interop object ready to pass into any .NET-facing API.

```ssl
:PROCEDURE ConvertMessageForNet;
	:DECLARE sMessage, oNetValue;

	sMessage := "Sample 1001";
	oNetValue := MakeNETObject(sMessage);

	:RETURN oNetValue;
:ENDPROC;

/* Usage;
DoProc("ConvertMessageForNet");
```

### Preserve [`NIL`](../literals/nil.md) input through conversion

Pass an optional value through `MakeNETObject` and branch on whether the result is [`NIL`](../literals/nil.md). The output message reflects which branch the code took.

```ssl
:PROCEDURE ConvertOptionalValue;
	:PARAMETERS vValue;
	:DECLARE oNetValue, sMessage;

	oNetValue := MakeNETObject(vValue);

	:IF oNetValue = NIL;
		sMessage := "No value was supplied for .NET interop";
	:ELSE;
		sMessage := "Value converted for .NET interop";
	:ENDIF;

	UsrMes(sMessage);

	:RETURN oNetValue;
:ENDPROC;

/* Usage;
DoProc("ConvertOptionalValue", {"Sample 1001"});
```

`UsrMes` displays one of:

```text
No value was supplied for .NET interop
Value converted for .NET interop
```

### Convert a mixed array of values for .NET interop

Build an array containing already-converted objects, plain values, and [`NIL`](../literals/nil.md), then run each element through `MakeNETObject`. Existing interop objects pass through unchanged; [`NIL`](../literals/nil.md) stays [`NIL`](../literals/nil.md); plain values are wrapped.

```ssl
:PROCEDURE PrepareNetInputs;
	:DECLARE aInputs, aNetInputs, nIndex, oNetValue;

	aInputs := {
		MakeNETObject("existing"),
		"plain text",
		42,
		NIL
	};
	aNetInputs := {};

	:FOR nIndex := 1 :TO ALen(aInputs);
		oNetValue := MakeNETObject(aInputs[nIndex]);
		AAdd(aNetInputs, oNetValue);
	:NEXT;

	:RETURN aNetInputs;
:ENDPROC;

/* Usage;
DoProc("PrepareNetInputs");
```

## Related

- [`LimsNETCast`](LimsNETCast.md)
- [`LimsNETConnect`](LimsNETConnect.md)
- [`LimsNETTypeOf`](LimsNETTypeOf.md)
- [`object`](../types/object.md)
