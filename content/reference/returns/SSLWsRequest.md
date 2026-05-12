---
title: "SSLWsRequest"
summary: "The web-service variant of the request object — adds Parameters to everything an SSLRequest exposes."
id: ssl.returns.sslwsrequest
element_type: returns
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SSLWsRequest

The web-service variant of the request object — adds `Parameters` to everything an [`SSLRequest`](SSLRequest.md) exposes.

When an SSL script is invoked as a web service, the [`Request`](../special-forms/request.md) ambient is an `SSLWsRequest` rather than a plain `SSLRequest`. The class adds one new property — `Parameters` — that holds the call's positional arguments as an array. For HTML web-service entry points the parameters are typically taken from the JSON body; for other entry points the runtime extracts them from whichever transport the call arrived on.

Everything else inherited from [`SSLRequest`](SSLRequest.md) — query string, headers, body, etc. — works the same here.

## When to use

- Inside a script invoked as a web service that needs the positional parameters the caller supplied.
- Inside a web-service script that also needs request-side details like headers or the authenticated user — read those from the inherited `SSLRequest` surface.

## How obtained

| Producer | Call form |
|---|---|
| [`Request`](../special-forms/request.md) ambient (web-service context) | `Request` (just the identifier) |

`Request` is an `SSLWsRequest` only when the script is invoked as a web service. In other endpoint contexts it is a plain [`SSLRequest`](SSLRequest.md).

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `Parameters` | [array](../types/array.md) | read-only | The positional parameters of the call, in the order the caller supplied them. Empty array when there are no parameters. |

## Inheritance

**Base class:** [`SSLRequest`](SSLRequest.md)

Every property and method on `SSLRequest` is available on `SSLWsRequest` — `HttpMethod`, `BodyAsString`, the six collection properties, `SaveInputStream()`, etc. See the base page for the full surface.

## Best practices

!!! success "Do"
    - Read positional parameters from `Request:Parameters` rather than parsing the body manually. The runtime has already extracted them.
    - Treat `Request` as `SSLWsRequest` only inside web-service scripts. For plain HTTP endpoints, use the base [`SSLRequest`](SSLRequest.md) surface.

!!! failure "Don't"
    - Try to construct an `SSLWsRequest` directly — it is only available as the [`Request`](../special-forms/request.md) ambient when the script runs as a web service.
    - Assume `Parameters` is always populated. Calls with no arguments produce an empty array.

## Caveats

- `SSLWsRequest` is not directly constructable. Obtain it from the [`Request`](../special-forms/request.md) ambient.
- Whether `Request` is an `SSLWsRequest` or a plain [`SSLRequest`](SSLRequest.md) depends on how the script was invoked. Code that needs to handle both shapes should read the inherited surface only.

## Examples

### Read the call's positional parameters

A web-service script that takes a sample ID and a flag.

```ssl
:PROCEDURE LookupSample;
    :DECLARE aParams, sSampleId, bIncludeHistory, oResult;

    aParams := Request:Parameters;

    :IF Len(aParams) < 2;
        Response:Value := "Missing required parameters";
        :RETURN;
    :ENDIF;

    sSampleId := aParams[1];
    bIncludeHistory := aParams[2];

    /* ... do the lookup, build oResult ... ;
    Response:Value := oResult;
:ENDPROC;
```

### Read both parameters and inherited request details

Combines the WS parameters array with the authenticated user's name from the inherited surface.

```ssl
:PROCEDURE AuditedLookup;
    :DECLARE aParams, sSampleId, sUserName, oResult;

    aParams := Request:Parameters;
    sSampleId := aParams[1];
    sUserName := Request:UserName;  /* inherited from SSLRequest ;

    /* ... record the audit, do the lookup ... ;
    Response:Value := oResult;
:ENDPROC;
```

## Related

- [`SSLRequest`](SSLRequest.md) — base class
- [`Request`](../special-forms/request.md) — the ambient identifier
- [`SSLWsResponse`](SSLWsResponse.md) — the response side for WS contexts
