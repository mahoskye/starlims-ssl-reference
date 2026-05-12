---
title: "SSLResponse"
summary: "The outgoing HTTP response inside an endpoint script — write content, set status, redirect, add headers and cookies."
id: ssl.returns.sslresponse
element_type: returns
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SSLResponse

The outgoing HTTP response inside an endpoint script — write content, set status, redirect, add headers and cookies.

An `SSLResponse` is the value of the [`Response`](../special-forms/response.md) ambient identifier inside any SSL endpoint script. You set the content type and status code as properties, write the body with `Write` or `WriteFile`, attach headers and cookies, redirect, or terminate the response early.

When the script is invoked as a web service rather than a plain HTTP endpoint, `Response` is typed as the [`SSLWsResponse`](SSLWsResponse.md) subclass, which adds a `Value` property used to return a structured result instead of writing a body.

## When to use

- Inside any endpoint script that needs to send a response body, set a status code, or redirect.
- When you need to attach a cookie or a custom header.
- When you need to control caching behavior for the response.

## How obtained

| Producer | Call form |
|---|---|
| [`Response`](../special-forms/response.md) ambient | `Response` (just the identifier — no construction) |

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `ContentType` | [string](../types/string.md) | read-write | The response `Content-Type` header (e.g., `application/json`, `text/html`). |
| `StatusCode` | [number](../types/number.md) | read-write | The HTTP status code to send (200, 400, 404, 500, etc.). |
| `Tag` | [string](../types/string.md) | read-write | A free-form tag used to associate the response with a cache invalidation key. |
| `CacheRetention` | [number](../types/number.md) | read-write | How long the response may be cached, in seconds. |
| `InvalidateCache` | [boolean](../types/boolean.md) | read-write | When `.T.`, signals that any cached entry for this response should be discarded. |
| `InvalidateCacheByTag` | [string](../types/string.md) | read-write | A tag value; cached entries marked with this tag are discarded. |

## Methods Summary

| Name | Returns | Description |
|------|---------|-------------|
| `Write` | none | Appends text to the response body. |
| `WriteFile` | none | Appends the contents of a file to the response body. |
| `Redirect` | none | Sends a redirect to the given URL. |
| `AddHeader` | none | Adds a custom response header. |
| `AddCookie` | none | Adds a cookie to the response. |
| `SetCookie` | none | Sets (or replaces) a cookie on the response. |
| `Flush` | none | Sends any buffered content immediately. |
| `End` | none | Ends the response — no further content is sent after this call. |
| `DisablePageCaching` | none | Suppresses caching for this response. |
| `Send401` | none | Sends a `401 Unauthorized` status with the appropriate authentication challenge. |

## Methods

### `Write`

Appends text to the response body. Call multiple times to build the response in pieces.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sContent` | [string](../types/string.md) | yes | Text to append. |

### `WriteFile`

Appends the contents of a file on disk to the response body. Useful for sending pre-built HTML, static text, or other on-disk content without reading it into memory first.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sFileName` | [string](../types/string.md) | yes | Path to the file. |

### `Redirect`

Sends a redirect to the URL you supply. Most callers should `:RETURN` from the script immediately after.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sUrl` | [string](../types/string.md) | yes | Target URL. |

### `AddHeader`

Adds a custom response header. Use `ContentType` for `Content-Type` instead of going through `AddHeader`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sName` | [string](../types/string.md) | yes | Header name. |
| `sValue` | [string](../types/string.md) | yes | Header value. |

### `AddCookie`

Adds a cookie to the response.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sName` | [string](../types/string.md) | yes | Cookie name. |
| `sValue` | [string](../types/string.md) | yes | Cookie value. |
| `dExpires` | [date](../types/date.md) | yes | Expiration date. |

### `SetCookie`

Sets (or replaces) a cookie on the response. Same parameters as `AddCookie`. Prefer `SetCookie` when you may be overwriting an existing cookie name; prefer `AddCookie` when accumulating distinct cookies.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sName` | [string](../types/string.md) | yes | Cookie name. |
| `sValue` | [string](../types/string.md) | yes | Cookie value. |
| `dExpires` | [date](../types/date.md) | yes | Expiration date. |

### `Flush`

Sends any buffered content immediately. Useful when streaming a long response in chunks.

### `End`

Ends the response — no further content is sent after this call. Subsequent `Write` calls have no effect on the wire.

### `DisablePageCaching`

Suppresses caching for this response. Equivalent to setting cache-control headers that block downstream caches.

### `Send401`

Sends a `401 Unauthorized` status with an appropriate authentication challenge. Use this from authentication middleware before `:RETURN`ing.

## Best practices

!!! success "Do"
    - Set `ContentType` and `StatusCode` before calling `Write` so the headers go out correctly.
    - `:RETURN` from the script immediately after `Redirect` so the rest of the script does not run.
    - Use `WriteFile` for static or pre-built bodies — it streams the file rather than reading it into a string.
    - Use `End()` when you want to terminate the response early after writing partial content.

!!! failure "Don't"
    - Try to construct an `SSLResponse` directly — it is only available as the [`Response`](../special-forms/response.md) ambient inside endpoint scripts.
    - Reach for `Response` outside an endpoint context. It will not be available — see [`Response`](../special-forms/response.md) for behavior.
    - Use `AddHeader` to set `Content-Type`. Use the `ContentType` property so the runtime can manage it consistently.
    - Continue writing after `End()` and expect the new content to appear on the wire.

## Caveats

- `SSLResponse` is not directly constructable. It is the value of the [`Response`](../special-forms/response.md) ambient, available only in endpoint contexts.
- For web-service contexts, `Response` is the [`SSLWsResponse`](SSLWsResponse.md) subclass; everything documented here is still available, plus the additional `Value` property used to return a structured result.
- `AddCookie` and `SetCookie` both require an explicit expiration date. If you want a session cookie, supply a date in the past or `NIL` per your environment's convention — confirm with a small test in your target environment.

## Examples

### Send a JSON response

Sets the content type and writes a small JSON body.

```ssl
:PROCEDURE SendInstrumentStatus;
    Response:ContentType := "application/json";
    Response:StatusCode := 200;
    Response:Write("{""instrument"":""Acme-1042"",""status"":""ok""}");
:ENDPROC;
```

### Redirect after processing

Performs a side effect, then redirects the client to a confirmation URL.

```ssl
:PROCEDURE FinishOrderAndRedirect;
    :DECLARE sOrderId;

    sOrderId := Request:Forms:OrderId;

    /* ... persist the order ... ;

    Response:Redirect("/Orders/" + sOrderId + "/Confirmation");
    :RETURN;
:ENDPROC;
```

### Reject an unauthenticated request

Issues a `401` and stops processing.

```ssl
:PROCEDURE GuardWithAuth;
    :IF Empty(Request:Headers:Get("Authorization"));
        Response:Send401();
        :RETURN;
    :ENDIF;

    Response:Write("Welcome, " + Request:UserName);
:ENDPROC;
```

## Related

- [`Response`](../special-forms/response.md) — the ambient identifier
- [`SSLWsResponse`](SSLWsResponse.md) — web-service subclass with `Value`
- [`SSLRequest`](SSLRequest.md) — the request side
