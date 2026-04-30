---
title: "AddProperty"
summary: "Add one or more properties to an object."
id: ssl.function.addproperty
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# AddProperty

Add one or more properties to an object.

AddProperty adds a property to `oTarget` when `vPropName` is a string, or adds multiple properties when `vPropName` is an array of strings. Each new property is created with an initial value of `""`. The function returns [`NIL`](../literals/nil.md).

If `oTarget` is [`NIL`](../literals/nil.md), AddProperty raises an error. If `vPropName` is [`NIL`](../literals/nil.md), it raises an error. If `vPropName` is neither a string nor an array of strings, or if any array element is not a string, it raises `Invalid property`.

Property names must be valid SSL object property identifiers. Names must start with a letter or underscore and can then contain letters, digits, or underscores.

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
| `vPropName` | [string](../types/string.md) or [array](../types/array.md) | yes | — | Property name as a string, or an array of property-name strings. Each name must be a valid property identifier. |

## Returns

**NIL** — Always returns [`NIL`](../literals/nil.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `oTarget` is [`NIL`](../literals/nil.md). | `Argument oTarget cannot be null.` |
| `vPropName` is [`NIL`](../literals/nil.md). | `Argument vPropName cannot be null.` |
| `vPropName` is not a string or an array element is not a string. | `Invalid property` |
| A property name is not a valid identifier. | `Invalid property name: <name>` |

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

## Examples

### Add one property

Creates a user-defined object, adds a single property, and shows that the property starts as an empty string before being assigned a value.

```ssl
:PROCEDURE AddSampleProperty;
	:DECLARE oSample;

	oSample := CreateUdObject();
	AddProperty(oSample, "sample_id");

	UsrMes(oSample:sample_id);  /* Displays: empty string;
	oSample:sample_id := "S-1001";
	UsrMes(oSample:sample_id);  /* Displays: S-1001;
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

[`UsrMes`](UsrMes.md) displays:

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
