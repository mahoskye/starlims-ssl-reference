---
title: "ToXml"
summary: "Converts a value to an XML string."
id: ssl.function.toxml
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ToXml

Converts a value to an XML string.

`ToXml` always returns a string that starts with an XML declaration. It can
serialize primitive values, arrays, [`NIL`](../literals/nil.md), and dynamic objects. If serialization fails, `ToXml` does not raise an exception — it returns XML containing an `<error>` element instead. Use [`FromXml`](FromXml.md) to deserialize XML produced in the built-in format.

## When to use

- When you need a text XML representation of a value, array, or dynamic object.
- When you need to send SSL data to another system that expects XML text.
- When you want XML that can later be read back with [`FromXml`](FromXml.md).

## Syntax

```ssl
ToXml(vValue)
ToXml(vValue, sTypeName)
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `vValue` | any | yes | — | Value to serialize. [`NIL`](../literals/nil.md), primitive values, arrays, and dynamic objects are supported. |
| `sTypeName` | [string](../types/string.md) | no | inferred from `vValue` when applicable | Optional XML type or tag name. For primitive values it replaces the inferred tag name. For arrays it becomes the `type` attribute on `<complexType>`. For dynamic objects it is ignored. |

## Returns

**[string](../types/string.md)** — XML text for the input value.

Common result shapes:

- Primitive values: `<?xml version='1.0' ?>` followed by a single element such as `<string>...</string>` or `<double>...</double>`.
- Arrays: `<?xml version='1.0' ?>` followed by `<complexType>` with a `length` attribute and, for typed arrays other than object arrays, a `type` attribute.
- [`NIL`](../literals/nil.md): `<?xml version='1.0' ?>` followed by `<null/>`.
- Dynamic objects: `<?xml version='1.0' ?>` followed by `<dto>...</dto>`.
- Serialization failure: `<?xml version='1.0' ?>` followed by `<error>...</error>`.

## Best practices

!!! success "Do"
    - Use `ToXml` and [`FromXml`](FromXml.md) together when you want the built-in XML round trip.
    - Check the returned XML for `<error>` when serializing data from variable or external sources.
    - Use a supported built-in `sTypeName` value such as `"string"`, `"bool"`, `"double"`, or `"date"` when you need predictable tags for primitive values or typed arrays.

!!! failure "Don't"
    - Assume `sTypeName` renames every result. Arrays still serialize as `<complexType>`, and dynamic objects still serialize as `<dto>`.
    - Assume `ToXml` raises a catchable error when serialization fails. The failure is encoded in the returned XML.
    - Use an arbitrary custom `sTypeName` if you expect [`FromXml`](FromXml.md) to restore the original type automatically.

## Caveats

- The return value always starts with the XML declaration `<?xml version='1.0' ?>`.
- For whitespace-only strings, the output element includes `xml:space='preserve'`.
- Numeric values are formatted using culture-invariant formatting.

## Examples

### Serialize a string with the inferred tag

Serialize a scalar string value without supplying a type name. The runtime
infers `<string>` as the element tag.

```ssl
:PROCEDURE ExportStatus;
	:DECLARE sStatus, sXml;

	sStatus := "Logged";
	sXml := ToXml(sStatus);

	UsrMes(sXml);

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("ExportStatus");
```

[`UsrMes`](UsrMes.md) displays:

```text
<?xml version='1.0' ?>
<string>Logged</string>
```

### Serialize a typed array for round-trip use

Pass `"double"` as `sTypeName` to tag the array elements explicitly so the XML can be deserialized back to the correct numeric type with [`FromXml`](FromXml.md).

```ssl
:PROCEDURE ExportResults;
	:DECLARE aResults, sXml;

	aResults := {7.1, 7.3, 7.0};
	sXml := ToXml(aResults, "double");

	UsrMes(sXml);

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("ExportResults");
```

[`UsrMes`](UsrMes.md) displays:

```text
<?xml version='1.0' ?>
<complexType type='double'  length='3'>
	<double>7.1</double>
	<double>7.3</double>
	<double>7</double>
</complexType>
```

### Check for embedded serialization errors

Inspect the returned XML for an `<error>` element rather than relying on [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md). This pattern is necessary because `ToXml` encodes failures in the XML string instead of raising an exception.

```ssl
:PROCEDURE ExportSamplePayload;
	:DECLARE oPayload, sXml;

	oPayload := CreateUdObject();
	oPayload:sampleId := "S-1001";
	oPayload:status := "Logged";
	oPayload:resultValue := 7.2;

	sXml := ToXml(oPayload);

	:IF "<error>" $ sXml;
		ErrorMes("Sample payload XML serialization failed");
		:RETURN "";
	:ENDIF;

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("ExportSamplePayload");
```

## Related

- [`FromXml`](FromXml.md)
- [`array`](../types/array.md)
- [`object`](../types/object.md)
- [`string`](../types/string.md)
