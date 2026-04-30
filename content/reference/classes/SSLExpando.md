---
title: "SSLExpando"
summary: "SSLExpando is a built-in object class for storing named values whose shape is decided at runtime."
id: ssl.class.sslexpando
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SSLExpando

`SSLExpando` is a built-in object class for storing named values whose shape is decided at runtime.

Use `SSLExpando{}` when you need an object that can grow as your script runs. You can add and update dynamic properties by name, check whether a property exists, list the current dynamic properties, and serialize the object to XML. `XmlType` controls the XML root element name and is always treated as an available property. Dynamic property names are matched case-insensitively.

## When to use

- When a script needs to assemble flexible sample, result, or request data.
- When the available property names are not known until runtime.
- When you need XML output for a dynamic object.

## Constructors

### `SSLExpando{}`

Creates an empty `SSLExpando` instance.

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `XmlType` | [string](../types/string.md) | read-write | XML root element name used by `ToString()` and `Serialize()` |

## Methods

| Name | Returns | Description |
|------|---------|-------------|
| `clone` | [object](../types/object.md) | Creates a new `SSLExpando` with the same `XmlType` and current dynamic properties |
| `GetProperty(sProp)` | any | Returns the value of a named property |
| `SetProperty(sProp, vValue)` | none | Sets `XmlType` or a dynamic property |
| `IsProperty(sProp)` | [boolean](../types/boolean.md) | Returns whether a property is available |
| `GetPropList` | [array](../types/array.md) | Returns the current dynamic property names |
| `ToString` | [string](../types/string.md) | Returns the object's XML representation |

### `clone`

Creates a new `SSLExpando` with the same `XmlType` and dynamic properties.

**Returns:** [object](../types/object.md) — New `SSLExpando` instance.

### `GetProperty`

Returns the value of `sProp`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sProp` | [string](../types/string.md) | yes | Property name |

**Returns:** any — Current property value.

**Raises:**
- **When the property does not exist:** `Property not found: <name>.`

### `SetProperty`

Sets `vValue` on `sProp`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sProp` | [string](../types/string.md) | yes | Property name |
| `vValue` | any | yes | Value to store |

**Returns:** none — No return value.

**Raises:**
- **When `sProp` is `XmlType` and `vValue` is neither a string nor [`NIL`](../literals/nil.md):** `The value for property XmlType must be a string`

### `IsProperty`

Checks whether `sProp` is available.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sProp` | [string](../types/string.md) | yes | Property name |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the property exists, otherwise [`.F.`](../literals/false.md).

### `GetPropList`

Returns the current dynamic property names.

**Returns:** [array](../types/array.md) — Array of property names.

### `ToString`

Returns the object as XML.

**Returns:** [string](../types/string.md) — XML string for the current `SSLExpando`.

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Use `SetProperty()` and `GetProperty()` when the property name comes from runtime data.
    - Set `XmlType` before serializing when another system expects a specific root element name.
    - Call `IsProperty()` before `GetProperty()` for optional fields.

!!! failure "Don't"
    - Assume `GetProperty()` returns an empty value for missing fields. It raises `Property not found: <name>.`.
    - Expect `GetPropList()` to include inherited object members. It only returns dynamic properties on the `SSLExpando`.
    - Rely on `clone()` for an independent deep copy of nested arrays or objects. Only the top-level property bag is copied.

## Caveats

- `GetPropList()` returns only dynamic property names. It does not include inherited object members or `XmlType`.
- `IsProperty("XmlType")` is always true, even if you never assigned a custom XML type.
- When `XmlType` is not set, `ToString()` uses `SSLExpando` as the root element name. Setting `XmlType` to [`NIL`](../literals/nil.md) clears any custom value and restores the default.
- `ToString()` returns the same XML content as `Serialize()`.
- `ToString()` returns XML, not a debug-style property dump.

## Examples

### Build a dynamic sample payload

Creates an `SSLExpando`, assigns `XmlType` and three dynamic properties, then reads a property with `GetProperty`, lists the dynamic property count with `GetPropList`, and serializes the object to XML with `ToString`.

```ssl
:PROCEDURE BuildSamplePayload;
	:DECLARE oPayload, aProps, sXml;

	oPayload := SSLExpando{};
	oPayload:XmlType := "SampleRecord";

	oPayload:SetProperty("SampleID", "LAB-2026-0042");
	oPayload:SetProperty("Status", "Logged");
	oPayload:SetProperty("ResultValue", 98.6);

	:IF oPayload:IsProperty("Status");
		UsrMes("Status: " + oPayload:GetProperty("Status"));
	:ENDIF;

	aProps := oPayload:GetPropList();
	UsrMes("Dynamic property count: " + LimsString(ALen(aProps)));

	sXml := oPayload:ToString();
	UsrMes(sXml);  /* Displays XML with root element SampleRecord;
:ENDPROC;

/* Usage;
DoProc("BuildSamplePayload");
```

### Clone before branching

Creates an `SSLExpando` for a release request, clones it twice into separate objects, then changes the `Decision` property on each clone independently to show that `clone()` makes a separate property bag.

```ssl
:PROCEDURE CloneRequestState;
	:DECLARE oRequest, oReviewCopy, oReleaseCopy;

	oRequest := SSLExpando{};
	oRequest:XmlType := "ReleaseRequest";
	oRequest:SetProperty("SampleID", "LAB-2026-0042");
	oRequest:SetProperty("Decision", "Pending");

	oReviewCopy := oRequest:clone();
	oReleaseCopy := oRequest:clone();

	oReviewCopy:SetProperty("Decision", "Review");
	oReleaseCopy:SetProperty("Decision", "Release");

	UsrMes("Original: " + oRequest:GetProperty("Decision"));
	UsrMes("Review copy: " + oReviewCopy:GetProperty("Decision"));
	UsrMes("Release copy: " + oReleaseCopy:GetProperty("Decision"));
:ENDPROC;

/* Usage;
DoProc("CloneRequestState");
```

## Related

- [`object`](../types/object.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
- [`boolean`](../types/boolean.md)
