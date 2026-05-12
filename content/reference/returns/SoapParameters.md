---
title: "SoapParameters"
summary: "The parameter list passed to the next SOAP method invocation — add scalar, XML-typed, binary, or by-reference parameters."
id: ssl.returns.soapparameters
element_type: returns
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SoapParameters

The parameter list passed to the next SOAP method invocation — add scalar, XML-typed, binary, or by-reference parameters.

A `SoapParameters` object is reachable as the `Parameters` property of every [`SoapClient`](SoapClient.md). You add the inputs the SOAP method expects, in the order it expects them, and then call [`SoapClient:CallWebService(sMethodName)`](SoapClient.md#callwebservice).

The Add methods come in several forms because SOAP methods accept several shapes of input:

- `Add(sXml)` for a single typed parameter expressed as XML.
- `AddAll(sXml)` for several parameters at once, expressed as a single XML array.
- `AddBinary(sFileName)` for a binary parameter sourced from a file.
- `AddParameter(o)` / `AddParameter2(o, sType)` for SSL values you want passed directly.
- Use the `*ByRef` variants to mark by-reference parameters; the service may modify them, and you'll read the new values from [`SoapResponse:XmlByRef`](SoapResponse.md) after the call.
- `CreateCustomType(sTypeName)` returns an instance of a custom DTO defined in the WSDL, which you can populate and then pass to `AddParameter`.

## When to use

- When you need to pass parameters to a SOAP method.
- When the SOAP method expects a custom DTO defined in its WSDL.
- When the SOAP method has by-reference parameters whose modified values you need to read after the call.

## How obtained

| Producer | Call form |
|---|---|
| [`SoapClient`](SoapClient.md) | `oSoapClient:Parameters` (property access) |

A new, empty `SoapParameters` is created automatically when the client is created. Replace it with another instance only when you need to swap out an entire parameter list at once.

## Methods Summary

| Name | Returns | Description |
|------|---------|-------------|
| `Add` | none | Adds one parameter from an XML representation. |
| `AddAll` | none | Adds several parameters from an XML array. |
| `AddByRef` | none | Like `Add`, and flags the parameter as by-reference. |
| `AddBinary` | none | Adds a binary parameter sourced from a file. |
| `AddBinaryByRef` | none | Like `AddBinary`, and flags the parameter as by-reference. |
| `AddParameter` | none | Adds a parameter from an SSL value directly. |
| `AddParameterByRef` | none | Like `AddParameter`, and flags the parameter as by-reference. |
| `AddParameter2` | none | Adds a parameter from an SSL value with an explicit type name. |
| `AddParameters` | none | Appends every parameter from another `SoapParameters` (preserving by-reference flags). |
| `CreateCustomType` | [object](../types/object.md) | Returns a new instance of a custom DTO defined in the WSDL. |
| `Clear` | none | Removes all parameters and by-reference flags. |

## Methods

### `Add`

Adds one parameter from an XML representation. The XML may be a primitive (`<string>...</string>`, `<int>...</int>`, etc.), a complex object, or a custom DTO type defined in the WSDL.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sXml` | [string](../types/string.md) | yes | XML representation of the parameter. |

### `AddAll`

Adds several parameters at once from a single XML array. Each top-level element of the array becomes one parameter.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sXml` | [string](../types/string.md) | yes | XML array, e.g., `<ArrayOfAnyType>...</ArrayOfAnyType>`. |

### `AddByRef`

Adds one parameter and flags it as by-reference. The SOAP method may modify it; the modified value is reachable after the call via [`SoapResponse:XmlByRef`](SoapResponse.md).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sXml` | [string](../types/string.md) | yes | XML representation of the parameter. |

### `AddBinary`

Adds a binary parameter whose contents are read from a file on disk.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sFileName` | [string](../types/string.md) | yes | Path to the file. |

### `AddBinaryByRef`

Like `AddBinary`, and flags the parameter as by-reference.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sFileName` | [string](../types/string.md) | yes | Path to the file. |

### `AddParameter`

Adds a parameter from an SSL value directly, without a separate XML representation. Use this when you already have the value as an SSL variable.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `oValue` | [any](../types/object.md) | yes | The parameter value. |

### `AddParameterByRef`

Like `AddParameter`, and flags the parameter as by-reference.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `oValue` | [any](../types/object.md) | yes | The parameter value. |

### `AddParameter2`

Adds a parameter from an SSL value with an explicit type name. Use this when the value's SSL type does not match what the SOAP method expects (e.g., passing a string that should be interpreted as a date).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `oValue` | [any](../types/object.md) | yes | The parameter value. |
| `sType` | [string](../types/string.md) | yes | Target type name. |

### `AddParameters`

Appends every parameter from another `SoapParameters` to this one, preserving by-reference flags.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `oOther` | [`SoapParameters`](SoapParameters.md) | yes | The parameters to append. |

### `CreateCustomType`

Returns a new instance of a custom DTO defined in the WSDL. Set its fields, then pass it to `AddParameter`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sTypeName` | [string](../types/string.md) | yes | Name of a type defined in the WSDL. |

**Returns:** [object](../types/object.md) — A new instance of the named type, or `NIL` if no type by that name is defined or the type has no default constructor. On failure, the parent `SoapClient`'s `Error` is set.

### `Clear`

Removes all parameters and by-reference flags. Call this between distinct method invocations on the same `SoapClient` so the second call does not inherit the first call's parameters.

## Best practices

!!! success "Do"
    - Add parameters in the order the SOAP method declares them.
    - Call `Clear` between invocations on the same `SoapClient` unless you intentionally want the parameters carried over.
    - Use `CreateCustomType` to construct DTOs the WSDL defines, populate the fields, then pass the instance to `AddParameter`.
    - Use the `*ByRef` variants only for parameters the SOAP method declares as by-reference; using them on regular parameters has no effect on the call but signals intent that does not match the contract.

!!! failure "Don't"
    - Try to construct a `SoapParameters` directly — obtain it from [`SoapClient:Parameters`](SoapClient.md), or use the empty one created automatically with the client.
    - Rely on `CreateCustomType` for primitive types — use `Add` with the appropriate XML wrapper instead.
    - Mix XML-form (`Add`) and value-form (`AddParameter`) for the same parameter list unless you have a specific reason; pick one form per call site for readability.
    - Forget to `Clear` between calls. Leftover parameters silently corrupt the next invocation.

## Caveats

- `SoapParameters` is not directly constructable. Obtain it from [`SoapClient:Parameters`](SoapClient.md).
- The XML forms (`Add`, `AddAll`, `AddByRef`) require well-formed XML matching the type the SOAP method expects. Malformed XML or a type mismatch sets `Error` on the parent `SoapClient`.
- `CreateCustomType` only works after the client has been configured with a `Use*` method — the WSDL must have been processed first.
- By-reference parameters do not change the SSL variables you passed in. Read the modified values from [`SoapResponse:XmlByRef`](SoapResponse.md) after the call.
- `AddParameter2` interprets the type name as a SOAP-side type, not an SSL type.

## Examples

### Add a primitive parameter as XML

Adds a single string parameter and invokes the method.

```ssl
:PROCEDURE LookupByPrimitiveParam;
    :DECLARE oWebServices, oSoapClient, oResponse;

    oWebServices := WebServices{};
    oSoapClient := oWebServices:CreateSoapClient();
    oSoapClient:UseWebService("https://lims-soap.example/Samples?wsdl");

    oSoapClient:Parameters:Add("<string>SAMP-001</string>");

    oResponse := oSoapClient:CallWebService("LookupSample");
    :IF oResponse != NIL;
        UsrMes(oResponse:Xml);
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("LookupByPrimitiveParam");
```

### Build a custom DTO from the WSDL

Uses `CreateCustomType` to instantiate a DTO defined by the service, populates fields, and passes it to `AddParameter`.

```ssl
:PROCEDURE SubmitOrderViaCustomDto;
    :DECLARE oWebServices, oSoapClient, oOrder, oResponse;

    oWebServices := WebServices{};
    oSoapClient := oWebServices:CreateSoapClient();
    oSoapClient:UseWebService("https://orders-soap.example/Orders?wsdl");

    oOrder := oSoapClient:Parameters:CreateCustomType("OrderRequest");
    :IF oOrder = NIL;
        UsrMes("Custom type unavailable: " + oSoapClient:Error);
        :RETURN;
    :ENDIF;

    oOrder:OrderId := "ORD-2026-0500";
    oOrder:Quantity := 12;

    oSoapClient:Parameters:AddParameter(oOrder);

    oResponse := oSoapClient:CallWebService("SubmitOrder");
    :IF oResponse != NIL;
        UsrMes("Submitted: " + oResponse:Xml);
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("SubmitOrderViaCustomDto");
```

### Read a by-reference output parameter

Flags one parameter as by-reference, invokes the method, then reads the modified value back from the response.

```ssl
:PROCEDURE LookupAndReadByRef;
    :DECLARE oWebServices, oSoapClient, oResponse, sRefXml;

    oWebServices := WebServices{};
    oSoapClient := oWebServices:CreateSoapClient();
    oSoapClient:UseWebService("https://lims-soap.example/Samples?wsdl");

    oSoapClient:Parameters:Add("<string>SAMP-001</string>");
    oSoapClient:Parameters:AddByRef("<string></string>");  /* output parameter — service fills it in;

    oResponse := oSoapClient:CallWebService("LookupSampleWithStatus");
    :IF oResponse != NIL;
        sRefXml := oResponse:XmlByRef;
        UsrMes("By-ref output: " + sRefXml);
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("LookupAndReadByRef");
```

## Related

- [`SoapClient`](SoapClient.md)
- [`SoapResponse`](SoapResponse.md)
- [`WebServices`](../classes/WebServices.md)
