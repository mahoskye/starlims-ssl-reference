---
title: "AddProperty"
summary: "Adds one or more properties to an object."
id: ssl.function.addproperty
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# AddProperty

Adds one or more properties to an object.

AddProperty adds a property to `oTarget` when `vPropName` is a string, or adds multiple properties when `vPropName` is an array of strings. Each new property is created with an initial value of `""`. The function returns [`NIL`](../literals/nil.md).

If `oTarget` is [`NIL`](../literals/nil.md), AddProperty raises an error. If `vPropName` is [`NIL`](../literals/nil.md), it raises an error. If `vPropName` is neither a string nor an array of strings, or if any array element is not a string, it raises `Invalid property`.

Use valid SSL identifiers for property names: start with a letter or underscore, then use letters, digits, or underscores. The runtime does not enforce this (see [Caveats](#caveats)).

## When to use

- When you need to extend a user-defined object with additional properties at runtime.
- When you want to add several properties in one call by passing an array of names.
- When object shape is data-driven and property names are not all fixed in advance.

## Syntax

```ssl
AddProperty(oTarget, vPropName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `oTarget` | [object](../types/object.md) | yes | — | Object that receives the new property or properties. |
| `vPropName` | [string](../types/string.md) or [array](../types/array.md) | yes | — | Property name as a string, or an array of property-name strings. Use valid SSL identifiers. |

## Returns

**NIL** — Always returns [`NIL`](../literals/nil.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `oTarget` is [`NIL`](../literals/nil.md). | `Argument o cannot be null. AddProperty()` |
| `vPropName` is [`NIL`](../literals/nil.md). | `Argument propName cannot be null. AddProperty()` |
| `vPropName` is not a string or an array element is not a string. | `Invalid property` |

## Best practices

!!! success "Do"
    - Pass an array of strings when you need to add several properties at once.
    - Keep property-name generation separate from the AddProperty call so type issues are easier to diagnose.
    - Add properties before code that assumes they already exist on the object.
    - Use property names that follow SSL identifier rules so the object can accept them.

!!! failure "Don't"
    - Pass mixed-type arrays as `vPropName`. Every element must be a string.
    - Expect a return value you can use in further expressions. The function always returns [`NIL`](../literals/nil.md).
    - Pass [`NIL`](../literals/nil.md) for the target object or property name. Both are required.
    - Use spaces, hyphens, or leading digits in property names.

## Caveats

- Property names are not checked against identifier rules. In observed runtime behavior, `AddProperty(o, "1 bad")` adds the property and returns [`NIL`](../literals/nil.md) instead of raising an error.

## Examples

### Add one property

Creates a user-defined object, adds a single property, and shows that the property starts as an empty string before being assigned a value.

```ssl
:PROCEDURE AddSampleProperty;
	:DECLARE oSample;

	oSample := CreateUdObject();
	AddProperty(oSample, "sample_id");

	UsrMes(oSample:sample_id);  /* Logs: empty string;
	oSample:sample_id := "S-1001";
	UsrMes(oSample:sample_id);  /* Logs: S-1001;
:ENDPROC;

/* Usage;
DoProc("AddSampleProperty");
```

### Add several properties at once

Passes an array of names to add all three properties in a single call, then assigns values and reads back the last one.

```ssl
:PROCEDURE PrepareImportObject;
	:DECLARE oImportRecord, aFieldNames;

	oImportRecord := CreateUdObject();
	aFieldNames := {"sample_id", "sample_name", "status"};

	AddProperty(oImportRecord, aFieldNames);

	oImportRecord:sample_id := "LAB-0042";
	oImportRecord:sample_name := "Composite sample";
	oImportRecord:status := "Pending";
	UsrMes(oImportRecord:status);
:ENDPROC;

/* Usage;
DoProc("PrepareImportObject");
```

[`UsrMes`](UsrMes.md) logs:

```text
Pending
```

## Related

- [`GetByName`](GetByName.md)
- [`HasProperty`](HasProperty.md)
- [`SetByName`](SetByName.md)
- [`object`](../types/object.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
