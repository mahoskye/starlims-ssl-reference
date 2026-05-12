---
title: "SSLWsResponse"
summary: "The web-service variant of the response object — adds Value (the structured return) to everything an SSLResponse exposes."
id: ssl.returns.sslwsresponse
element_type: returns
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SSLWsResponse

The web-service variant of the response object — adds `Value` (the structured return) to everything an [`SSLResponse`](SSLResponse.md) exposes.

When an SSL script is invoked as a web service, the [`Response`](../special-forms/response.md) ambient is an `SSLWsResponse` rather than a plain `SSLResponse`. The class adds one new property — `Value` — that holds the script's structured return value to the web-service caller. The runtime serializes whatever you assign to `Value` (a string, number, array, object) and returns it to the caller in the appropriate format for the calling protocol.

For HTML web-service entry points, assigning to `Value` is the normal way to return a result; the inherited `Write` method is rarely needed.

## When to use

- Inside a script invoked as a web service that returns a structured result rather than writing a body.
- When the caller expects a typed return — number, string, array of objects — and you want the runtime to serialize it for you.

## How obtained

| Producer | Call form |
|---|---|
| [`Response`](../special-forms/response.md) ambient (web-service context) | `Response` (just the identifier) |

`Response` is an `SSLWsResponse` only when the script is invoked as a web service. In other endpoint contexts it is a plain [`SSLResponse`](SSLResponse.md).

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `Value` | [any](../types/object.md) | read-write | The script's return value to the web-service caller. The runtime serializes the assigned value into the appropriate response format. |

## Inheritance

**Base class:** [`SSLResponse`](SSLResponse.md)

Every property and method on `SSLResponse` is available on `SSLWsResponse` — `StatusCode`, `ContentType`, `AddHeader`, `Write`, `Redirect`, etc. See the base page for the full surface.

## Best practices

!!! success "Do"
    - Assign the result of the call to `Response:Value` rather than calling `Write` with a serialized string. The runtime handles serialization for you.
    - Set `Response:StatusCode` for error cases (e.g., `400`, `404`, `500`) just as you would on a plain HTTP response.
    - Use `Response:Value` for structured returns; use the inherited `Write` only if you genuinely need raw body output.

!!! failure "Don't"
    - Try to construct an `SSLWsResponse` directly — it is only available as the [`Response`](../special-forms/response.md) ambient when the script runs as a web service.
    - Mix `Response:Value := X` and `Response:Write(...)` in the same script — they target different code paths and combining them is unlikely to produce what you expect.

## Caveats

- `SSLWsResponse` is not directly constructable. Obtain it from the [`Response`](../special-forms/response.md) ambient.
- Whether `Response` is an `SSLWsResponse` or a plain [`SSLResponse`](SSLResponse.md) depends on how the script was invoked. Code that needs to handle both shapes should use the inherited surface only.
- The serialization format applied to `Value` depends on the protocol the call arrived on. For HTML web-service entry points the value is typically returned as JSON.

## Examples

### Return a string from a web-service script

Sets `Value` to the result the caller will receive.

```ssl
:PROCEDURE GetGreeting;
    :DECLARE sName;

    sName := Request:Parameters[1];
    Response:Value := "Hello, " + sName;
:ENDPROC;
```

### Return a structured object

Builds a small object and assigns it to `Value`. The runtime handles serialization.

```ssl
:PROCEDURE GetSampleSummary;
    :DECLARE sSampleId, oResult;

    sSampleId := Request:Parameters[1];

    oResult := CreateUdObject();
    oResult:Id := sSampleId;
    oResult:Status := "complete";
    oResult:Value := 42.5;

    Response:Value := oResult;
:ENDPROC;
```

### Signal a failure with status and a value

Sets a non-success status and a structured error payload.

```ssl
:PROCEDURE GuardedLookup;
    :DECLARE sSampleId, oError;

    sSampleId := Request:Parameters[1];

    :IF Empty(sSampleId);
        oError := CreateUdObject();
        oError:Code := "missing_id";
        oError:Message := "Sample id is required";

        Response:StatusCode := 400;
        Response:Value := oError;
        :RETURN;
    :ENDIF;

    /* ... do the lookup ... ;
:ENDPROC;
```

## Related

- [`SSLResponse`](SSLResponse.md) — base class
- [`Response`](../special-forms/response.md) — the ambient identifier
- [`SSLWsRequest`](SSLWsRequest.md) — the request side for WS contexts
