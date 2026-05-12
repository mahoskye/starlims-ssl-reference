---
title: "SoapClient"
summary: "Calls SOAP web services — configures the endpoint from a WSDL, supplies credentials, invokes methods."
id: ssl.returns.soapclient
element_type: returns
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SoapClient

Calls SOAP web services — configures the endpoint from a WSDL, supplies credentials, invokes methods.

A `SoapClient` is the object you receive from [`WebServices{}:CreateSoapClient()`](../classes/WebServices.md). The typical workflow is: point it at a WSDL with `UseWebService` (or `UseWebServiceWithCredentials`), populate its [`Parameters`](SoapParameters.md) with the inputs the SOAP method expects, then call `CallWebService(sMethodName)` to invoke the operation. The result comes back as a [`SoapResponse`](SoapResponse.md).

Configuration methods return `.F.` on failure rather than raising — read `Error` for the reason instead of catching an exception. Check the return value of every `Use*` call.

## When to use

- When you need to call a SOAP web service from SSL.
- When the service is described by a WSDL (file path, URL, or inline XML).
- When you need to authenticate to the service with explicit credentials or with the calling process's defaults.

## How obtained

| Producer | Call form |
|---|---|
| [`WebServices`](../classes/WebServices.md) | `WebServices{}:CreateSoapClient()` |

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `Error` | [string](../types/string.md) | read-write | The reason the most recent configuration step failed. Empty string when the last step succeeded. |
| `TimeOut` | [number](../types/number.md) | read-write | Maximum wait, in milliseconds, for a `CallWebService` invocation. Values `<= 0` disable the timeout. |
| `Parameters` | [`SoapParameters`](SoapParameters.md) | read-write | The parameter list passed to the next `CallWebService` invocation. Replace it with another instance, or call its add methods directly. |
| `AcceptCookies` | [boolean](../types/boolean.md) | read-write | When `.T.` (the default), the client retains cookies set by the service across calls. |
| `UseDefaultCredentials` | [boolean](../types/boolean.md) | read-write | When `.T.`, calls authenticate with the calling process's default credentials. Falls back to `GlobalUseDefaultCredentials` when not set explicitly on the client. |
| `GlobalUseDefaultCredentials` | [boolean](../types/boolean.md) | read-write | Class-wide default for `UseDefaultCredentials`. Affects every `SoapClient` that has not set the property locally. |
| `WsAssembly` | [object](../types/object.md) | read-only | Advanced — a handle to the generated proxy types for the configured WSDL. Used internally by [`Parameters:CreateCustomType`](SoapParameters.md#createcustomtype) and [`GetWSType`](#getwstype); rarely needed directly. |

## Methods Summary

| Name | Returns | Description |
|------|---------|-------------|
| `UseWebService` | [boolean](../types/boolean.md) | Configures the client from a WSDL location, with no credentials. |
| `UseWebServiceWithCredentials` | [boolean](../types/boolean.md) | Configures the client from a WSDL location with explicit user/password. |
| `UseProxy` | [boolean](../types/boolean.md) | Advanced — configures the client from a pre-built proxy file. |
| `CallWebService` | [`SoapResponse`](SoapResponse.md) | Invokes a SOAP method on the configured service. |
| `GetWSType` | [object](../types/object.md) | Advanced — returns a handle to a named proxy type. |

## Methods

### `UseWebService`

Configures the client from a WSDL. Accepts a URL, a `.wsdl` file path, or an inline WSDL XML string.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sWsdlLocation` | [string](../types/string.md) | yes | URL, file path, or inline WSDL XML. |

**Returns:** [boolean](../types/boolean.md) — `.T.` on success; `.F.` when the WSDL cannot be retrieved or processed. Read `Error` for the reason.

### `UseWebServiceWithCredentials`

Same as `UseWebService` but authenticates the WSDL fetch and subsequent calls with the user/password you supply.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sWsdlLocation` | [string](../types/string.md) | yes | URL, file path, or inline WSDL XML. |
| `sUser` | [string](../types/string.md) | yes | Username. May be domain-prefixed (`DOMAIN\\user`). Pass an empty string to fall back to default credentials. |
| `sPassword` | [string](../types/string.md) | yes | Password. |

**Returns:** [boolean](../types/boolean.md) — `.T.` on success; `.F.` when configuration fails. Read `Error` for the reason.

### `UseProxy`

Advanced — configures the client from a pre-built proxy file you have generated yourself, instead of fetching a WSDL. Use this when the service is unreachable for WSDL fetch or when you need a specific generated client.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sAssemblyLocation` | [string](../types/string.md) | yes | Full path to the proxy file. |
| `sClassName` | [string](../types/string.md) | yes | Name of the proxy class within the file. |

**Returns:** [boolean](../types/boolean.md) — `.T.` on success; `.F.` when the file cannot be found or loaded. Read `Error` for the reason.

### `CallWebService`

Invokes a SOAP method on the configured service. Add inputs to `Parameters` first.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sMethodName` | [string](../types/string.md) | yes | Name of the SOAP method to invoke. |

**Returns:** [`SoapResponse`](SoapResponse.md) — The response, or `NIL` when the call fails. On failure, `Error` is set; on success, `Error` is cleared.

### `GetWSType`

Advanced — returns a handle to a named proxy type. Useful when working with custom DTOs whose shape is defined in the WSDL.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sTypeName` | [string](../types/string.md) | yes | Name of the proxy type. |

**Returns:** [object](../types/object.md) — A handle to the named type, or `NIL` when no type by that name is found.

## Best practices

!!! success "Do"
    - Configure the client with one of the `Use*` methods exactly once before calling `CallWebService`.
    - Check the return value of `Use*` and read `Error` when it returns `.F.`.
    - Populate `Parameters` in the order the SOAP method expects them, and call `Parameters:Clear()` between distinct invocations on the same client.
    - Use `UseWebService` (no credentials) only for services that allow anonymous access or when default credentials are appropriate.
    - Set `TimeOut` (in milliseconds) for slow services so a stalled call does not block indefinitely.

!!! failure "Don't"
    - Try to construct a `SoapClient` directly — it is only obtainable via [`WebServices{}:CreateSoapClient()`](../classes/WebServices.md).
    - Reuse `Parameters` across calls without clearing it between invocations — leftover parameters are silently passed to the next method.
    - Use `UseProxy` unless you know exactly what proxy file you need; `UseWebService` from the WSDL is the normal path.
    - Treat `Error` as a one-shot value. It is cleared on the next successful step and overwritten on the next failure; capture its content immediately.

## Caveats

- `SoapClient` is not directly constructable. Obtain it from [`WebServices{}:CreateSoapClient()`](../classes/WebServices.md).
- `Use*` methods return `.F.` on failure rather than raising — always check the return value and `Error`.
- `CallWebService` returns `NIL` on failure rather than raising. Check the return value before reading the response.
- `TimeOut` is in milliseconds. Values `<= 0` disable the timeout entirely.
- The configuration step caches results based on the WSDL content. Calling `UseWebService` repeatedly with the same WSDL is cheap; switching WSDLs on the same client is supported but may rebuild the proxy.
- `UseDefaultCredentials` falls back to `GlobalUseDefaultCredentials` only when the local property has not been set. Once you assign to it, the local value wins regardless of the global value.

## Examples

### Call a SOAP method that takes one parameter

Configures the client from a WSDL URL, adds one parameter, and invokes the method.

```ssl
:PROCEDURE LookupSampleViaSoap;
    :DECLARE oWebServices, oSoapClient, oResponse, sResultXml;

    oWebServices := WebServices{};
    oSoapClient := oWebServices:CreateSoapClient();

    :IF .NOT. oSoapClient:UseWebService("https://lims-soap.example/Samples?wsdl");
        UsrMes("Configuration failed: " + oSoapClient:Error);
        :RETURN;
    :ENDIF;

    oSoapClient:Parameters:Add("<string>SAMP-001</string>");

    oResponse := oSoapClient:CallWebService("LookupSample");

    :IF oResponse = NIL;
        UsrMes("Call failed: " + oSoapClient:Error);
        :RETURN;
    :ENDIF;

    sResultXml := oResponse:Xml;
    UsrMes(sResultXml);
:ENDPROC;

/* Usage;
DoProc("LookupSampleViaSoap");
```

### Authenticate with explicit credentials and a longer timeout

Uses `UseWebServiceWithCredentials` and bumps `TimeOut` to 60 seconds for a slow service.

```ssl
:PROCEDURE InvokeSecureSoapMethod;
    :DECLARE oWebServices, oSoapClient, oResponse;

    oWebServices := WebServices{};
    oSoapClient := oWebServices:CreateSoapClient();

    :IF .NOT. oSoapClient:UseWebServiceWithCredentials( ;
            "https://secure-soap.example/Reports?wsdl", ;
            "LIMSDOMAIN\\reports_user", ;
            "********");
        UsrMes("Auth/config failed: " + oSoapClient:Error);
        :RETURN;
    :ENDIF;

    oSoapClient:TimeOut := 60000;
    oSoapClient:Parameters:Add("<string>2026-05-01</string>");

    oResponse := oSoapClient:CallWebService("DailySummary");

    :IF oResponse = NIL;
        UsrMes("Call failed: " + oSoapClient:Error);
    :ELSE;
        UsrMes(oResponse:Xml);
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("InvokeSecureSoapMethod");
```

### Reuse one client for several calls

Clears `Parameters` between calls so the second invocation does not inherit the first one's inputs.

```ssl
:PROCEDURE LookupSeveralSamples;
    :DECLARE oWebServices, oSoapClient, oResponse, aIds, i;

    oWebServices := WebServices{};
    oSoapClient := oWebServices:CreateSoapClient();

    :IF .NOT. oSoapClient:UseWebService("https://lims-soap.example/Samples?wsdl");
        UsrMes("Configuration failed: " + oSoapClient:Error);
        :RETURN;
    :ENDIF;

    aIds := {"SAMP-001", "SAMP-002", "SAMP-003"};

    :FOR i := 1 :TO Len(aIds);
        oSoapClient:Parameters:Clear();
        oSoapClient:Parameters:Add("<string>" + aIds[i] + "</string>");

        oResponse := oSoapClient:CallWebService("LookupSample");
        :IF oResponse != NIL;
            UsrMes(aIds[i] + " => " + oResponse:Xml);
        :ELSE;
            UsrMes(aIds[i] + " failed: " + oSoapClient:Error);
        :ENDIF;
    :NEXT;
:ENDPROC;

/* Usage;
DoProc("LookupSeveralSamples");
```

## Related

- [`WebServices`](../classes/WebServices.md)
- [`SoapResponse`](SoapResponse.md)
- [`SoapParameters`](SoapParameters.md)
