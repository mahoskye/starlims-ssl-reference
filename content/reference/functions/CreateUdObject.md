---
title: "CreateUdObject"
summary: "Creates a dynamic object or instantiates a user-defined class."
id: ssl.function.createudobject
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CreateUdObject

Creates a dynamic object or instantiates a user-defined [`:CLASS`](../keywords/CLASS.md).

`CreateUdObject` has three distinct call modes:

- **No-argument form** — creates an empty dynamic object with no properties.
- **Property-definition form** — creates a dynamic object with a pre-defined set of properties. Each element of `aPropertyDefs` must be either a property name string or a two-element array of `{propertyName, initialValue}`.
- **Class-name form** — instantiates a user-defined [`:CLASS`](../keywords/CLASS.md) by name, optionally passing constructor arguments as a single array.

## When to use

- When you need an empty dynamic object that you will populate step by step.
- When you want to create a dynamic object from a data-driven list of properties.
- When you need to instantiate a user-defined [`:CLASS`](../keywords/CLASS.md) by name.
- When object shape is not fixed at design time and named properties are a better fit than array indexes.

## Syntax

```ssl
CreateUdObject()
CreateUdObject(aPropertyDefs)
CreateUdObject(sClassName, [aArgs])
```

## Parameters

| Name | Form | Type | Required | Default | Description |
|------|------|------|----------|---------|-------------|
| `aPropertyDefs` | property-def | [array](../types/array.md) | conditional | — | Property definitions for the dynamic object. Each element must be either a property name string or a two-element array of `{propertyName, initialValue}`. A bare property name creates the property with an empty-string value. |
| `sClassName` | class-name | [string](../types/string.md) | conditional | — | Name of a user-defined [`:CLASS`](../keywords/CLASS.md) to instantiate. Not for built-in classes such as `Email{}` or `SSLDataset{}`. |
| `aArgs` | class-name | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Constructor arguments for the class-name form. Pass all arguments as one array in call order, even when there is only one argument. |

Only one form is used per call. `aPropertyDefs` and `sClassName` are both the first positional argument — they are distinguished by type (array vs. string).

## Returns

**[object](../types/object.md)** — The returned object depends on the call form:

- `CreateUdObject()` returns an empty [`SSLExpando`](../classes/SSLExpando.md).
- `CreateUdObject(aPropertyDefs)` returns an [`SSLExpando`](../classes/SSLExpando.md) with the requested properties already created.
- `CreateUdObject(sClassName, [aArgs])` returns an instance of the named user-defined class.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| The first argument is neither a string nor an array. | `Argument must be an array` |
| The second argument in the class-name form is not an array. | `Wrong parameters for <className>` |
| A property-definition element is neither a string nor a two-element array. | `Invalid property definition. Property#: <index>` |
| A property name is empty or not a string. | `Property name must be a non-empty string. Property#: <index>` |
| A property name is not a valid SSL identifier. | `Invalid property name. Property#: <index>` |
| A property named `XmlType` is assigned a non-string value. | `The value for property XmlType must be a string` |

## Best practices

!!! success "Do"
    - Use the no-argument or property-definition form when the set of properties is only known at runtime.
    - Use the class-name form only for user-defined [`:CLASS`](../keywords/CLASS.md) files.
    - Build `aPropertyDefs` as either `{"PropName"}` style entries for empty-string defaults or `{{"PropName", vValue}}` pairs for initialized values.
    - Validate property names before building `aPropertyDefs` from imported or user-supplied data.

!!! failure "Don't"
    - Use `CreateUdObject` to instantiate built-in classes. Use curly-brace construction such as `Email{}` or `SSLDataset{}` instead.
    - Pass constructor arguments as separate parameters. The class-name form expects one array argument list.
    - Use empty property names or names that contain spaces, hyphens, or leading digits.
    - Assume a bare property-name entry gives you a custom default value. It creates the property with `""`.

## Caveats

- An empty `aPropertyDefs` array is valid and returns an empty dynamic object.
- If the same property name appears more than once in `aPropertyDefs`, the last value wins.
- `XmlType` is a special property name on dynamic objects and must receive a string value when you set it through `aPropertyDefs`.

## Examples

### Create an empty dynamic object and populate it later

Creates an empty dynamic object using the no-argument form and assigns three properties individually after construction.

```ssl
:PROCEDURE BuildSampleContext;
	:DECLARE oContext, sSummary;

	oContext := CreateUdObject();
	oContext:sampleId := "LAB-0042";
	oContext:status := "Pending";
	oContext:priority := 2;

	sSummary := oContext:sampleId + " / " + oContext:status;
	sSummary := sSummary + " / " + LimsString(oContext:priority);
	UsrMes(sSummary);

	:RETURN oContext;
:ENDPROC;

/* Usage;
DoProc("BuildSampleContext");
```

[`UsrMes`](UsrMes.md) displays:

```text
LAB-0042 / Pending / 2
```

### Build a dynamic object from property definitions

Creates a dynamic object from a runtime-assembled list of property definitions. The last entry in `aPropertyDefs` is a bare name string, which creates the property with an empty-string value that is then assigned separately.

```ssl
:PROCEDURE BuildImportRow;
	:DECLARE aPropertyDefs, oRow, sMessage;

	aPropertyDefs := {
		{"sampleId", "LAB-0105"},
		{"status", "Logged"},
		{"replicateCount", 3},
		"reviewer"
	};

	oRow := CreateUdObject(aPropertyDefs);
	oRow:reviewer := MYUSERNAME;

	sMessage := oRow:sampleId + " reviewed by " + oRow:reviewer;
	sMessage := sMessage + " (" + LimsString(oRow:replicateCount) + " replicates)";
	UsrMes(sMessage);

	:RETURN oRow;
:ENDPROC;

/* Usage;
DoProc("BuildImportRow");
```

[`UsrMes`](UsrMes.md) displays (username varies by session):

```text
LAB-0105 reviewed by jsmith (3 replicates)
```

### Instantiate a user-defined class with constructor arguments

Instantiates a user-defined class by name, passing constructor arguments as an array. The class definition and usage must live in separate scripts.

!!! note "One class per script"
    A [`:CLASS`](../keywords/CLASS.md) definition lives in its own script. The class definition and the usage example are shown separately here because they would not appear in the same SSL file.

Class definition:

```ssl
:CLASS SampleTicket;

:DECLARE sSampleID, nPriority;

:PROCEDURE Describe;
	:RETURN sSampleID + " priority " + LimsString(nPriority);
:ENDPROC;

:PROCEDURE Constructor;
	:PARAMETERS sNewSampleID, nNewPriority;

	sSampleID := sNewSampleID;
	nPriority := nNewPriority;
:ENDPROC;
```

Usage:

```ssl
:PROCEDURE CreateSampleTicket;
	:DECLARE oTicket, sMessage;

	oTicket := CreateUdObject("Samples.SampleTicket", {"LAB-0042", 2});
	sMessage := oTicket:Describe();
	UsrMes(sMessage);

	:RETURN oTicket;
:ENDPROC;

/* Usage;
DoProc("CreateSampleTicket");
```

[`UsrMes`](UsrMes.md) displays:

```text
LAB-0042 priority 2
```

## Related

- [`AddProperty`](AddProperty.md)
- [`SSLExpando`](../classes/SSLExpando.md)
- [`CLASS`](../keywords/CLASS.md)
- [`object`](../types/object.md)
- [`array`](../types/array.md)
