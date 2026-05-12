---
title: "SoapResponse"
summary: "The result of a SOAP call — read scalar values, navigate object fields and arrays, save binary results, or get the result as XML."
id: ssl.returns.soapresponse
element_type: returns
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SoapResponse

The result of a SOAP call — read scalar values, navigate object fields and arrays, save binary results, or get the result as XML.

A `SoapResponse` is the object you receive from [`SoapClient:CallWebService(sMethodName)`](SoapClient.md#callwebservice). It wraps whatever the SOAP method returned — a primitive, a complex object, an array, or binary data — and offers methods to read the value in the form you want.

For complex returns, use `GetObjectField(sName)` to descend into a named field; for array returns, use `GetArrayLength()` and `GetArrayItem(nIndex)` to iterate. Both `GetObjectField` and `GetArrayItem` return another `SoapResponse`, so navigation chains.

## When to use

- When you need a scalar result (number, string, date) from a SOAP call.
- When the result is a complex object and you need to read individual fields.
- When the result is an array and you need to iterate.
- When the result is binary and you want it written to a file.
- When you want the entire result as an XML string for logging or further processing.

## How obtained

| Producer | Call form |
|---|---|
| [`SoapClient`](SoapClient.md) | `oSoapClient:CallWebService(sMethodName)` |
| [`SoapResponse`](SoapResponse.md) | `oResponse:GetObjectField(sName)` (descend into a field) |
| [`SoapResponse`](SoapResponse.md) | `oResponse:GetArrayItem(nIndex)` (descend into an array element) |

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `ValueAsStringDate` | [string](../types/string.md) | read-only | The wrapped value formatted as `YYYY-M-D` when the value is a date. Empty string otherwise. |
| `ValueAsStringTime` | [string](../types/string.md) | read-only | The wrapped value formatted as `HH:MM:SS` (zero-padded) when the value is a date/time. Empty string otherwise. |
| `Xml` | [string](../types/string.md) | read-only | The wrapped value serialized to XML. Empty string when serialization fails; in that case, the parent `SoapClient`'s `Error` property is set. |
| `XmlByRef` | [string](../types/string.md) | read-only | The by-reference parameter values from the call serialized to XML. Empty string when there are none or serialization fails. |

## Methods Summary

| Name | Returns | Description |
|------|---------|-------------|
| `Value` | [object](../types/object.md) | Returns the wrapped value as-is. |
| `UnWrap` | [object](../types/object.md) | Returns the wrapped value, expanding arrays of complex types into arrays of `SoapResponse`. |
| `GetObjectField` | [`SoapResponse`](SoapResponse.md) | Returns a named field of a complex result. |
| `GetArrayItem` | [`SoapResponse`](SoapResponse.md) | Returns an element of an array result. |
| `GetArrayLength` | [number](../types/number.md) | Returns the length of an array result, or `-1` when the result is not an array. |
| `SaveToFile` | [string](../types/string.md) | Writes a binary result to a file. |
| `GetTypeInfo` | [string](../types/string.md) | Returns a name for the wrapped value's type. |
| `GetObjectFieldList` | [string](../types/string.md) | Returns the names and types of all fields on a complex result, as XML. |

## Methods

### `Value`

Returns the wrapped value as-is. Useful when you want the raw value rather than a navigation handle.

**Returns:** [object](../types/object.md) — The wrapped value.

### `UnWrap`

Returns the wrapped value. For arrays of primitives, returns the array as-is. For arrays of complex objects, returns an array of `SoapResponse` wrappers you can navigate.

**Returns:** [object](../types/object.md) — The wrapped value or an array of `SoapResponse`. Returns `NIL` when the call fails; in that case, the parent `SoapClient`'s `Error` is set.

### `GetObjectField`

Returns a named field of a complex result. The returned value is itself a `SoapResponse`, so you can chain navigation.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sName` | [string](../types/string.md) | yes | Field name. |

**Returns:** [`SoapResponse`](SoapResponse.md) — A new response wrapping the field value, or `NIL` if no field by that name exists.

### `GetArrayItem`

Returns an element of an array result. The returned value is itself a `SoapResponse`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `nIndex` | [number](../types/number.md) | yes | Zero-based index. |

**Returns:** [`SoapResponse`](SoapResponse.md) — A new response wrapping the element, or `NIL` when the value is not an array or the index is out of range.

### `GetArrayLength`

Returns the length of an array result. Returns `-1` when the wrapped value is not an array.

**Returns:** [number](../types/number.md) — Array length, or `-1`.

### `SaveToFile`

Writes a binary result to a file. Raises if the wrapped value is not binary.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sFileName` | [string](../types/string.md) | yes | Destination path. |
| `bForceOverride` | [boolean](../types/boolean.md) | yes | When `.T.`, overwrites an existing file at the destination. |

**Returns:** [string](../types/string.md) — The path written to, or empty string on failure (parent `SoapClient`'s `Error` is set).

### `GetTypeInfo`

Returns a short, human-readable name for the wrapped value's type — useful when the call's return shape varies by input.

**Returns:** [string](../types/string.md) — A type name.

### `GetObjectFieldList`

Returns an XML string listing every field on a complex result, with each entry's name and type. Raises if the wrapped value is not a complex type.

**Returns:** [string](../types/string.md) — XML listing the fields. Empty string on failure.

## Best practices

!!! success "Do"
    - Use `GetObjectField` to descend into complex results, and chain calls for nested fields.
    - Use `GetArrayLength` + `GetArrayItem` to iterate array results.
    - Use `Xml` for logging or for handing the result to another system that consumes XML.
    - Use `SaveToFile` for binary results so you do not hold large payloads in memory.

!!! failure "Don't"
    - Try to construct a `SoapResponse` directly — it is only obtainable from a `SoapClient` call or from navigation methods on another `SoapResponse`.
    - Call `SaveToFile` on a non-binary result. It will raise.
    - Rely on `Value` for arrays of complex types — use `UnWrap` to get an array of `SoapResponse` you can iterate.
    - Read `Xml` and assume the result is non-empty without checking — serialization failures return empty string and set `Error` on the parent `SoapClient`.

## Caveats

- `SoapResponse` is not directly constructable. Obtain it from [`SoapClient:CallWebService`](SoapClient.md#callwebservice) or from `GetObjectField` / `GetArrayItem` on another `SoapResponse`.
- `GetArrayItem` uses **zero-based** indexing, unlike most SSL array operations.
- `GetArrayLength` returns `-1` (not `0`) when the wrapped value is not an array. Use this to distinguish "not an array" from "empty array."
- `ValueAsStringDate` and `ValueAsStringTime` return empty strings when the wrapped value is not a date/time. Both are derived from the same underlying value when present.
- Serialization or read errors on `Xml` and `XmlByRef` return empty strings and set the parent `SoapClient`'s `Error` property. Check `Error` after reading these properties when an empty value is unexpected.

## Examples

### Read a scalar result

Reads a single string value from a SOAP method that returns one.

```ssl
:PROCEDURE FetchInstrumentName;
    :DECLARE oWebServices, oSoapClient, oResponse, sName;

    oWebServices := WebServices{};
    oSoapClient := oWebServices:CreateSoapClient();
    oSoapClient:UseWebService("https://lims-soap.example/Instruments?wsdl");
    oSoapClient:Parameters:Add("<int>42</int>");

    oResponse := oSoapClient:CallWebService("GetInstrumentName");

    :IF oResponse != NIL;
        sName := oResponse:Value();
        UsrMes("Instrument name: " + sName);
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("FetchInstrumentName");
```

### Iterate an array result

Reads how many items came back, then walks the array.

```ssl
:PROCEDURE ListRecentSamples;
    :DECLARE oWebServices, oSoapClient, oResponse, oItem, nLen, i;

    oWebServices := WebServices{};
    oSoapClient := oWebServices:CreateSoapClient();
    oSoapClient:UseWebService("https://lims-soap.example/Samples?wsdl");
    oSoapClient:Parameters:Add("<int>10</int>");

    oResponse := oSoapClient:CallWebService("GetRecentSamples");
    :IF oResponse = NIL;
        UsrMes("Call failed: " + oSoapClient:Error);
        :RETURN;
    :ENDIF;

    nLen := oResponse:GetArrayLength();
    :IF nLen <= 0;
        UsrMes("No samples returned");
        :RETURN;
    :ENDIF;

    :FOR i := 0 :TO nLen - 1;
        oItem := oResponse:GetArrayItem(i);
        UsrMes("Sample " + AllTrim(Str(i)) + ": " + oItem:GetObjectField("Id"):Value());
    :NEXT;
:ENDPROC;

/* Usage;
DoProc("ListRecentSamples");
```

### Save a binary result

Calls a method that returns a PDF report and writes it to disk.

```ssl
:PROCEDURE DownloadBatchReport;
    :DECLARE oWebServices, oSoapClient, oResponse, sSavedPath;

    oWebServices := WebServices{};
    oSoapClient := oWebServices:CreateSoapClient();
    oSoapClient:UseWebService("https://reports-soap.example/Reports?wsdl");
    oSoapClient:Parameters:Add("<string>B-1042</string>");

    oResponse := oSoapClient:CallWebService("RenderBatchReport");
    :IF oResponse = NIL;
        UsrMes("Call failed: " + oSoapClient:Error);
        :RETURN;
    :ENDIF;

    sSavedPath := oResponse:SaveToFile("C:\Lims\Inbox\B-1042.pdf", .T.);
    UsrMes("Saved to: " + sSavedPath);
:ENDPROC;

/* Usage;
DoProc("DownloadBatchReport");
```

## Related

- [`SoapClient`](SoapClient.md)
- [`SoapParameters`](SoapParameters.md)
- [`WebServices`](../classes/WebServices.md)
