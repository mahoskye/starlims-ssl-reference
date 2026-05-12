---
title: "SSLRequest"
summary: "The incoming HTTP request inside an endpoint script — method, URL, headers, query string, cookies, forms, body, and uploaded files."
id: ssl.returns.sslrequest
element_type: returns
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SSLRequest

The incoming HTTP request inside an endpoint script — method, URL, headers, query string, cookies, forms, body, and uploaded files.

An `SSLRequest` is the value of the [`Request`](../special-forms/request.md) ambient identifier inside any SSL endpoint script. You read scalar properties (`HttpMethod`, `RawUrl`, `UserAgent`, `UserName`, etc.), drill into name/value collections (`QueryString`, `Headers`, `Cookies`, `Forms`, `ServerVariables`, `ClientCertificate`) for header- or parameter-style lookups, or pull the request body as text or binary content.

When the script is invoked as a web service rather than a plain HTTP endpoint, `Request` is typed as the [`SSLWsRequest`](SSLWsRequest.md) subclass, which adds a `Parameters` array on top of everything documented here.

## When to use

- Inside any endpoint script (REST handler, custom URL handler, web-service implementation) that needs to read details of the incoming request.
- When you need a query parameter, header, cookie, form field, or server variable.
- When you need the request body — as text for JSON/XML/form-encoded payloads, or as binary for file uploads and binary protocols.

## How obtained

| Producer | Call form |
|---|---|
| [`Request`](../special-forms/request.md) ambient | `Request` (just the identifier — no construction) |

## Properties

### Scalar properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `IsJson` | [boolean](../types/boolean.md) | read-only | `.T.` when the `Content-Type` indicates JSON. |
| `IsHTMLWsRequest` | [boolean](../types/boolean.md) | read-only | `.T.` when the request was issued from the HTML web-service entry point. |
| `ContentType` | [string](../types/string.md) | read-only | The request `Content-Type` header. |
| `HttpMethod` | [string](../types/string.md) | read-only | HTTP method (`GET`, `POST`, `PUT`, `DELETE`, etc.). |
| `RequestType` | [string](../types/string.md) | read-only | Same as `HttpMethod` for HTTP requests; web-service entry points may report a service-specific label. |
| `IsSecureConnection` | [boolean](../types/boolean.md) | read-only | `.T.` when the request arrived over HTTPS. |
| `IsClientCertificatePresent` | [boolean](../types/boolean.md) | read-only | `.T.` when a client certificate was supplied. |
| `RawUrl` | [string](../types/string.md) | read-only | The full request URL as received, including query string. |
| `UserAgent` | [string](../types/string.md) | read-only | The `User-Agent` header. |
| `UserHostAddress` | [string](../types/string.md) | read-only | The client's IP address. |
| `UserHostName` | [string](../types/string.md) | read-only | The client's host name (or IP, if no name resolution is available). |
| `PhysicalApplicationPath` | [string](../types/string.md) | read-only | The filesystem path of the application. |
| `ApplicationPath` | [string](../types/string.md) | read-only | The application's virtual path. |
| `UserName` | [string](../types/string.md) | read-only | The authenticated user's name. |
| `ActionId` | [string](../types/string.md) | read-only | The action identifier the script was invoked under. |
| `BodyAsString` | [string](../types/string.md) | read-only | The request body decoded as text. `NIL` when the body is empty. |
| `BodyAsBinary` | [object](../types/object.md) | read-only | The request body as binary content, wrapped as a [`netobject`](../types/netobject.md). `NIL` when no body is present. |
| `Files` | [array](../types/array.md) | read-only | Uploaded files attached to the request. Empty array when none. |

### Collection properties (each returns an [`SSLNameValueContainer`](SSLNameValueContainer.md))

| Name | What it contains |
|------|------|
| `QueryString` | URL query parameters. |
| `Cookies` | Cookies sent by the client. |
| `Forms` | URL-encoded form fields posted in the request body. |
| `Headers` | Request headers. |
| `ServerVariables` | Server-side request metadata (host, port, paths, protocol, etc.). |
| `ClientCertificate` | Fields from the client certificate, when one is supplied. |

Read each collection with the expando form (`Request:QueryString:UserName`) for fixed keys, or with `:Get(sName)` for dynamic keys. See [`SSLNameValueContainer`](SSLNameValueContainer.md) for the full surface.

## Methods Summary

| Name | Returns | Description |
|------|---------|-------------|
| `SaveInputStream` | [string](../types/string.md) | Saves the request body to a file and returns the path. |

## Methods

### `SaveInputStream`

Saves the request body to a file on the server and returns the path. Useful for large bodies you don't want to materialize as a string or hold in memory.

**Returns:** [string](../types/string.md) — The path the body was written to.

## Best practices

!!! success "Do"
    - Reach for `Request:QueryString:Foo` (expando form) when you know the parameter name; reach for `:Get(sName)` when the name is dynamic.
    - Check `IsJson` before treating `BodyAsString` as JSON.
    - Use `SaveInputStream()` for large or binary bodies rather than loading them into a variable.
    - Treat `Request` as read-only — the values reflect what the client sent.

!!! failure "Don't"
    - Try to construct an `SSLRequest` directly — it is only available as the [`Request`](../special-forms/request.md) ambient inside endpoint scripts.
    - Reach for `Request` outside an endpoint context (e.g., from a script invoked through `DoProc` from an interactive session). It will not be available — see [`Request`](../special-forms/request.md) for behavior.
    - Use `BodyAsString` for binary uploads. Use `BodyAsBinary` or `SaveInputStream()` instead.
    - Modify values on the collection properties expecting the incoming request to change. The values are read-only views.

## Caveats

- `SSLRequest` is not directly constructable. It is the value of the [`Request`](../special-forms/request.md) ambient, available only in endpoint contexts.
- `BodyAsString` returns `NIL` (not an empty string) when the body is empty. Test with `Empty()` or compare to `NIL`.
- `BodyAsBinary` returns `NIL` when the body is empty.
- For web-service contexts, `Request` is the [`SSLWsRequest`](SSLWsRequest.md) subclass; everything documented here is still available, plus the additional `Parameters` array.

## Examples

### Branch on HTTP method, read query parameters

Distinguishes a `GET` from a `POST`, then handles each.

```ssl
:PROCEDURE HandleSampleRequest;
    :DECLARE sMethod, sId;

    sMethod := Request:HttpMethod;

    :IF sMethod = "GET";
        sId := Request:QueryString:Id;
        Response:Write("Lookup sample: " + sId);
    :ELSEIF sMethod = "POST";
        Response:Write("Create from body: " + Request:BodyAsString);
    :ELSE;
        Response:StatusCode := 405;
        Response:Write("Method not allowed");
    :ENDIF;
:ENDPROC;
```

### Read an `Authorization` header

Pulls a single header value to authenticate the call.

```ssl
:PROCEDURE RequireBearerToken;
    :DECLARE sAuth;

    sAuth := Request:Headers:Get("Authorization");

    :IF Empty(sAuth) .OR. .NOT. ("Bearer " $ sAuth);
        Response:StatusCode := 401;
        Response:Write("Authorization required");
        :RETURN;
    :ENDIF;

    Response:Write("Authenticated as " + Request:UserName);
:ENDPROC;
```

### Save a binary upload to a file

Writes a binary request body to disk for later processing, instead of holding it in memory.

```ssl
:PROCEDURE ReceiveBinaryUpload;
    :DECLARE sSavedPath;

    :IF Request:HttpMethod != "POST";
        Response:StatusCode := 405;
        :RETURN;
    :ENDIF;

    sSavedPath := Request:SaveInputStream();
    Response:Write("Saved to: " + sSavedPath);
:ENDPROC;
```

## Related

- [`Request`](../special-forms/request.md) — the ambient identifier
- [`SSLWsRequest`](SSLWsRequest.md) — web-service subclass with `Parameters`
- [`SSLResponse`](SSLResponse.md) — the response side
- [`SSLNameValueContainer`](SSLNameValueContainer.md) — collection-property surface
- [`netobject`](../types/netobject.md) — wraps the binary body
