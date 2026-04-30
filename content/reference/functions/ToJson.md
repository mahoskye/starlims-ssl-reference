---
title: "ToJson"
summary: "Serializes a value to a JSON string."
id: ssl.function.tojson
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ToJson

Serializes a value to a JSON string.

`ToJson()` returns a string representation of the supplied value in JSON form. It supports normal SSL values such as strings, numbers, booleans, dates, arrays, and objects. [`NIL`](../literals/nil.md) is returned as the literal string `null`.

## When to use

- When you need to send SSL data to a web API or another JSON-based interface.
- When you want a string form of an array or object for logging, storage, or transport.
- When you need JSON output from a value before passing it to another system.

## Syntax

```ssl
ToJson(vValue)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vValue` | any | yes | — | Value to serialize. |

## Returns

**[string](../types/string.md)** — JSON text representing `vValue`.

Behavior depends on the input value:

| Input | JSON result |
|------|-------------|
| [`NIL`](../literals/nil.md) | `null` |
| String | Quoted JSON string with escaping applied |
| Number | JSON number |
| Boolean | `true` or `false` |
| Date | Quoted timestamp string, or `null` for an empty date |
| Array | JSON array with each element serialized recursively |
| Object | JSON object containing the object's properties and an `XmlType` field |
| Supported external dataset object | JSON generated from the dataset contents |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| Passing an unsupported external object. | `Objects of type: <type> cannot be serialized to json` |

## Best practices

!!! success "Do"
    - Serialize values as late as practical, close to the API call, file write, or log step that needs JSON.
    - Expect object output to include the object's properties plus `XmlType`.
    - Wrap serialization in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the value may come from an external source.

!!! failure "Don't"
    - Assume every external object can be serialized.
    - Assume an empty date becomes an empty string; it becomes `null`.
    - Treat the JSON text as identical to SSL source syntax for arrays or objects.

## Caveats

- Date output format depends on the date kind: local dates include an offset, UTC dates include `Z`, and unspecified dates omit a zone suffix.

## Examples

### Serialize a simple object

Build a small dynamic object and serialize it to JSON. The output includes the object's three properties followed by the required `XmlType` field that all serialized objects carry.

```ssl
:PROCEDURE BuildSampleJson;
	:DECLARE oSample, sJson;

	oSample := CreateUdObject({
		{"sampleId", "SAMP-1001"},
		{"status", "Logged"},
		{"approved", .F.}
	});

	sJson := ToJson(oSample);

	:RETURN sJson;
:ENDPROC;

/*
Usage
DoProc("BuildSampleJson")
;
```

Expected JSON:

```text
{"sampleId":"SAMP-1001","status":"Logged","approved":false,"XmlType":"SSLExpando"}
```

### Serialize nested data for an API payload

Build a nested payload with a child object, an array, a date, and a number, then serialize the whole structure. This shows how `ToJson` recurses into nested objects and arrays automatically.

```ssl
:PROCEDURE BuildOrderPayload;
	:DECLARE oPayload, oCustomer, aTests, sJson, dRequested;

	dRequested := Today();
	aTests := {"pH", "Conductivity", "Turbidity"};

	oCustomer := CreateUdObject();
	oCustomer:customerId := "C-2048";
	oCustomer:name := "North Plant";

	oPayload := CreateUdObject();
	oPayload:orderNo := "ORD-2026-0042";
	oPayload:requestedDate := dRequested;
	oPayload:customer := oCustomer;
	oPayload:tests := aTests;
	oPayload:priority := 2;

	sJson := ToJson(oPayload);

	:RETURN sJson;
:ENDPROC;

/*
Usage
DoProc("BuildOrderPayload")
;
```

### Handle values that may not be serializable

Wrap `ToJson` in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the caller cannot guarantee the value comes from a supported type. Unsupported external objects raise an exception; this pattern surfaces the message and returns an empty string instead of letting the error propagate.

```ssl
:PROCEDURE SerializeSafely;
	:PARAMETERS vValue;
	:DECLARE sJson, oErr;

	:TRY;
		sJson := ToJson(vValue);
		:RETURN sJson;

	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes(oErr:Description);
		:RETURN "";
	:ENDTRY;
:ENDPROC;

/*
Usage
DoProc("SerializeSafely", {CreateUdObject()})
;
```

## Related

- [`FromJson`](FromJson.md)
- [`array`](../types/array.md)
- [`object`](../types/object.md)
- [`string`](../types/string.md)
