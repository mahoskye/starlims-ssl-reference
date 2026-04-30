---
title: "object"
summary: "Represents SSL object values, including dynamic objects and class instances."
id: ssl.type.object
element_type: type
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# object

## What it is

Represents SSL object values, including dynamic objects and class instances.

The `object` type covers SSL values with named members. In day-to-day SSL code, this includes dynamic objects created with [`CreateLocal`](../functions/CreateLocal.md) as well as instances returned from user-defined or built-in classes.

Dynamic objects are useful when the set of properties is not fixed ahead of time. You can create an empty object, assign members later, or initialize it from a property-definition array. On dynamic objects, member access works naturally with colon syntax such as `oMeta:sampleId` and `oMeta:status := "Logged"`. The same operations are also available through methods such as `GetProperty()`, `SetProperty()`, and `IsProperty()`.

Objects do not support direct indexing of their own members. If an object property contains an array, index the array value after reading it.

The special `XmlType` property controls the root element name used by `Serialize()`. `IsEmpty()` always returns [`.F.`](../literals/false.md) for objects, so use a property-list method when you need to check whether a dynamic object currently has any named properties.

## Creating values

Dynamic objects are created with [`CreateLocal`](../functions/CreateLocal.md) (empty) or [`CreateUdObject`](../functions/CreateUdObject.md) (with initialization):

```ssl
oEmpty := CreateLocal();
oInit := CreateUdObject({{"sampleId", "LAB-0042"}, {"status", "Pending"}});
```

| Attribute | Value |
|---|---|
| Runtime type | `OBJECT` |
| Common construction | [`CreateLocal()`](../functions/CreateLocal.md) |
| Initialized construction | `CreateUdObject({{"prop", value}})` |

## Operators

Objects support identity comparison operators. Arithmetic and relational operators are not supported.

| Operator | Symbol | Returns | Behavior |
|---|---|---|---|
| [`strict-equals`](../operators/strict-equals.md) | [`==`](../operators/strict-equals.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) only when both operands reference the same object instance. |
| [`not-equals`](../operators/not-equals.md) | [`!=`](../operators/not-equals.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) when the operands do not reference the same object instance. |

## Members

| Member | Kind | Parameters | Returns | Description |
|---|---|---|---|---|
| `XmlType` | Property | — | [`string`](string.md) | Gets or sets the XML type name used by `Serialize()`. |
| `AddProperty(sName)` | Method | `sName` ([`string`](string.md)) | [`string`](string.md) | Adds a dynamic property with an empty-string value and returns its name. If the property already exists, it is reset to `""`. |
| `GetProperty(sName)` | Method | `sName` ([`string`](string.md)) | `any` | Returns the named property value. |
| `SetProperty(sName, vValue)` | Method | `sName` ([`string`](string.md)), `vValue` (`any`) | none | Sets the named property value. |
| `IsProperty(sName)` | Method | `sName` ([`string`](string.md)) | [`boolean`](boolean.md) | Returns [`.T.`](../literals/true.md) when the named property exists. `XmlType` is always recognized as a property. |
| `GetPropList()` | Method | none | [`array`](array.md) | Returns property names. On dynamic objects this is the dynamic-property list; on other object values it can also include declared public members. |
| `GetDynPropList()` | Method | none | [`array`](array.md) | Returns only dynamic property names. |
| `Serialize()` | Method | none | [`string`](string.md) | Serializes the object as XML using `XmlType` as the root element name. |
| `Deserialize(sXml, [aTypeMapping])` | Method | `sXml` ([`string`](string.md)), `aTypeMapping` ([`array`](array.md), optional) | `object` | Populates the current object from XML and returns that same object. |
| `IsEmpty()` | Method | none | [`boolean`](boolean.md) | Always returns [`.F.`](../literals/false.md) for object values. |
| `IsMethod(sName)` | Method | `sName` ([`string`](string.md)) | [`boolean`](boolean.md) | Returns [`.T.`](../literals/true.md) when the named method is callable on the object. |
| `InvokeMethod(sName, [aArgs])` | Method | `sName` ([`string`](string.md)), `aArgs` ([`array`](array.md) or [`NIL`](../literals/nil.md)) | `any` | Calls a method by name using dynamic dispatch. |
| `clone()` | Method | none | `object` | Returns a deep copy for dynamic objects created with [`CreateLocal()`](../functions/CreateLocal.md) or [`CreateUdObject()`](../functions/CreateUdObject.md). |
| `ToString()` | Method | none | [`string`](string.md) | On dynamic objects, returns the serialized XML text. |
| `Destroy()` | Method | none | none | Runs object cleanup logic. The base implementation does nothing. |

## Indexing

| Attribute | Value |
|---|---|
| Supported | `false` |
| Behavior | Use member access such as `oValue:propName`; index arrays after reading them from a property |

## Notes for daily SSL work

!!! success "Do"
    - Use colon member access such as `oContext:sampleId` for normal reads and writes on dynamic objects.
    - Check `IsProperty()` before reading optional members that may not exist.
    - Use `clone()` before changing a copied dynamic object when the original must stay unchanged.
    - Set `XmlType` before `Serialize()` when the XML root name matters to downstream code.

!!! failure "Don't"
    - Assume missing properties return an empty value. Reading an unknown property raises an error.
    - Treat object members like array indexes. Objects do not support direct indexing of their own properties.
    - Assume every `object` value supports `clone()` in the same way. The reliable deep-clone behavior is on dynamic objects created with [`CreateLocal()`](../functions/CreateLocal.md) or [`CreateUdObject()`](../functions/CreateUdObject.md).
    - Set `XmlType` to a non-string value. That raises an error.

## Errors and edge cases

- Reading a missing property raises a runtime error with the message `Property not found: <name>.`
- [`AddProperty()`](../functions/AddProperty.md) validates the property name and initializes the new property to `""`.
- `IsEmpty()` is not a property-count check for objects.

## Examples

### Creating and reading a dynamic object

Creates a dynamic object with [`CreateLocal()`](../functions/CreateLocal.md), assigns three named members, and reads them back to build a summary string.

```ssl
:PROCEDURE BuildReviewContext;
    :DECLARE oContext, sSummary;

    oContext := CreateLocal();

    oContext:sampleId := "LAB-0042";
    oContext:status := "Pending";
    oContext:priority := 2;

    sSummary := oContext:sampleId + " / " + oContext:status;
    sSummary := sSummary + " / " + LimsString(oContext:priority);
    UsrMes(sSummary);

    :RETURN oContext;
:ENDPROC;

/* Usage;
DoProc("BuildReviewContext");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
LAB-0042 / Pending / 2
```

### Validating optional fields and cloning safely

Checks for an optional `reviewComment` property, adds it when missing, clones the object before mutating it, and reports the field count and the snapshot's preserved status.

```ssl
:PROCEDURE PrepareApprovalPayload;
    :DECLARE oPayload, oSnapshot, aFields, sMessage;

    oPayload := CreateUdObject({
        {"sampleId", "LAB-0042"},
        {"status", "Logged"}
    });

    :IF !oPayload:IsProperty("reviewComment");
        oPayload:AddProperty("reviewComment");
    :ENDIF;

    oPayload:reviewComment := "Ready for approval";
    oSnapshot := oPayload:clone();

    oPayload:status := "Approved";
    aFields := oPayload:GetDynPropList();

    sMessage := "Fields tracked: " + LimsString(ALen(aFields));
    UsrMes(sMessage);
    UsrMes("Snapshot status: " + oSnapshot:status);

    :RETURN oPayload;
:ENDPROC;

/* Usage;
DoProc("PrepareApprovalPayload");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Fields tracked: 3
Snapshot status: Logged
```

### Serializing and restoring an object tree

Sets `XmlType`, serializes the object to XML, and restores it into a new dynamic object with `Deserialize`.

```ssl
:PROCEDURE RoundTripObjectXml;
    :DECLARE oPayload, oRestored, aTests, sXml;

    oPayload := CreateUdObject({
        {"sampleId", "LAB-0042"},
        {"tests", {"pH", "Conductivity"}},
        {"released", .F.}
    });

    oPayload:XmlType := "SamplePayload";

    sXml := oPayload:Serialize();

    oRestored := CreateLocal();
    oRestored:Deserialize(sXml);
    aTests := oRestored:tests;

    UsrMes("Restored root: " + oRestored:XmlType);
    UsrMes("First test: " + aTests[1]);

    :RETURN oRestored;
:ENDPROC;

/* Usage;
DoProc("RoundTripObjectXml");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Restored root: SamplePayload
First test: pH
```

## Related elements

- [`CreateUdObject`](../functions/CreateUdObject.md)
- [`CreateLocal`](../functions/CreateLocal.md)
- [`SSLExpando`](../classes/SSLExpando.md)
- [`array`](array.md)
- [`netobject`](netobject.md)
