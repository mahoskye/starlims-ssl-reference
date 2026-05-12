---
title: "HttpClient"
summary: "Entry point for outbound HTTP requests — builds requests, fetches responses, and retrieves text, XML, or files."
id: ssl.returns.httpclient
element_type: returns
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# HttpClient

Entry point for outbound HTTP requests — builds requests, fetches responses, and retrieves text, XML, or files.

An `HttpClient` is the object you receive from [`WebServices{}:CreateHttpClient()`](../classes/WebServices.md). It is the top of the HTTP call stack: from one `HttpClient` you can either issue convenience calls (`GetText`, `GetXmlDom`, `SaveFile`) that take a URL and return the body in the form you want, or build an [`HttpRequest`](HttpRequest.md) when you need to set headers, change the method, or attach a request body.

When a request fails, the underlying error is recorded on the client and is reachable through [`GetLastServerException`](#getlastserverexception) until the next successful call clears it.

## When to use

- When you need to fetch a URL and return the body as a string, XML DOM, or saved file.
- When you need full control over the request — headers, method, body, content type — before sending it.
- When you need to inspect the server's response details after a failed call.

## How obtained

| Producer | Call form |
|---|---|
| [`WebServices`](../classes/WebServices.md) | `WebServices{}:CreateHttpClient()` |

## Methods Summary

| Name | Returns | Description |
|------|---------|-------------|
| `CreateHttpRequest` | [`HttpRequest`](HttpRequest.md) | Creates a configurable request for the given URL. |
| `GetResponse` | [`HttpResponse`](HttpResponse.md) | Sends a request and returns the response. |
| `GetLastServerException` | [`HttpException`](HttpException.md) | Returns the most recent failure, or `NIL` if the last call succeeded. |
| `GetText` | [string](../types/string.md) | Sends a request and returns the body as text. |
| `GetXmlDom` | [object](../types/object.md) | Sends a request and returns the body as an XML DOM object. |
| `SaveFile` | [string](../types/string.md) | Sends a request and writes the body to a file. |

## Methods

### `CreateHttpRequest`

Creates a configurable request for the given URL. The returned [`HttpRequest`](HttpRequest.md) defaults to an unauthenticated GET — set its properties and call `SetContent` before passing it to `GetResponse` if you need anything else.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sUrl` | [string](../types/string.md) | yes | Target URL. |

**Returns:** [`HttpRequest`](HttpRequest.md) — A request you can configure and pass to `GetResponse`.

### `GetResponse`

Sends a request and returns the response. Two forms are available.

`GetResponse(oRequest)` sends a request you have already built with `CreateHttpRequest`:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `oRequest` | [`HttpRequest`](HttpRequest.md) | yes | A request previously built with `CreateHttpRequest`. |

`GetResponse(sUrl)` is a shortcut that builds a default GET request for the URL and sends it:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sUrl` | [string](../types/string.md) | yes | Target URL. |

**Returns:** [`HttpResponse`](HttpResponse.md) — The response. On failure, an [`HttpException`](HttpException.md) is raised and the same exception is also reachable via `GetLastServerException` until the next successful call.

### `GetLastServerException`

Returns the most recent failure recorded by this client. The value is set whenever `GetResponse` (or any method that delegates to it) fails, and is cleared on the next successful response.

**Returns:** [`HttpException`](HttpException.md) — The last failure, or `NIL` if no failure has occurred since the last successful call.

### `GetText`

Sends a request and returns the body as text. Two forms:

`GetText(oRequest)` uses a request you have already built; `GetText(sUrl)` builds a default GET for the URL.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `oRequest` | [`HttpRequest`](HttpRequest.md) | yes (first form) | Request to send. |
| `sUrl` | [string](../types/string.md) | yes (second form) | Target URL. |

**Returns:** [string](../types/string.md) — The response body decoded to text. Compressed responses are returned in their decompressed form.

### `GetXmlDom`

Sends a request and parses the response body as XML. Two forms — request or URL — same as `GetText`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `oRequest` | [`HttpRequest`](HttpRequest.md) | yes (first form) | Request to send. |
| `sUrl` | [string](../types/string.md) | yes (second form) | Target URL. |

**Returns:** [object](../types/object.md) — XML DOM object. See [`netobject`](../types/netobject.md) for the surface available for navigating it.

### `SaveFile`

Sends a request and writes the response body to a file.

`SaveFile(sUrl)` writes to a file path chosen by the runtime; `SaveFile(sUrl, sLocalFile)` writes to the path you specify.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sUrl` | [string](../types/string.md) | yes | Target URL. |
| `sLocalFile` | [string](../types/string.md) | no | Destination path. When omitted, the runtime chooses a path. |

**Returns:** [string](../types/string.md) — The path the file was written to.

## Best practices

!!! success "Do"
    - Use the URL-only forms (`GetText(sUrl)`, `GetResponse(sUrl)`, `GetXmlDom(sUrl)`, `SaveFile(sUrl)`) for simple, unauthenticated GETs.
    - Build an [`HttpRequest`](HttpRequest.md) when you need to set headers, change the method, or attach a body.
    - Check `GetLastServerException` after a failure to see the server's response body.

!!! failure "Don't"
    - Try to construct an `HttpClient` directly — it is only obtainable via [`WebServices{}:CreateHttpClient()`](../classes/WebServices.md).
    - Reuse the value returned by `GetLastServerException` after a successful call. The next success clears it.
    - Assume `GetXmlDom` will succeed on non-XML bodies. It will raise.

## Caveats

- `HttpClient` is not directly constructable. Obtain it from [`WebServices{}:CreateHttpClient()`](../classes/WebServices.md).
- A failed request raises an [`HttpException`](HttpException.md). The same exception is also recorded for retrieval through `GetLastServerException`.
- The two-argument `SaveFile` writes to the path you give it. The one-argument form writes to a runtime-chosen path; capture the returned path if you need to find the file later.

## Examples

### Fetch a JSON endpoint as text

Builds an HTTP client and fetches a small JSON endpoint, returning the body as a string.

```ssl
:PROCEDURE FetchInstrumentStatus;
    :DECLARE oWebServices, oHttpClient, sBody;

    oWebServices := WebServices{};
    oHttpClient := oWebServices:CreateHttpClient();

    sBody := oHttpClient:GetText("https://lims-instruments.example/api/status");

    UsrMes(sBody);
:ENDPROC;

/* Usage;
DoProc("FetchInstrumentStatus");
```

### Build a configured request and send it

Creates an `HttpRequest`, sets the method and an `Accept` header, sends it, then reads the response body.

```ssl
:PROCEDURE PostBatchNotification;
    :DECLARE oWebServices, oHttpClient, oRequest, oResponse, sBody;

    oWebServices := WebServices{};
    oHttpClient := oWebServices:CreateHttpClient();

    oRequest := oHttpClient:CreateHttpRequest("https://notifier.example/api/batch");
    oRequest:Method := "POST";
    oRequest:ContentType := "application/json";
    oRequest:Accept := "application/json";
    oRequest:SetContent("{""batch"":""B-1042"",""status"":""complete""}");

    oResponse := oHttpClient:GetResponse(oRequest);
    sBody := oResponse:GetValueAsString();

    UsrMes(sBody);
:ENDPROC;

/* Usage;
DoProc("PostBatchNotification");
```

### Inspect the server's response after a failed call

Catches a failure and reads the server's error body via `GetLastServerException`.

```ssl
:PROCEDURE TryFetchAndReport;
    :DECLARE oWebServices, oHttpClient, sBody, oError;

    oWebServices := WebServices{};
    oHttpClient := oWebServices:CreateHttpClient();

    :TRY;
        sBody := oHttpClient:GetText("https://lims-instruments.example/api/status");
        UsrMes(sBody);
    :CATCH;
        oError := oHttpClient:GetLastServerException();
        :IF oError != NIL;
            UsrMes("Status " + oError:Status + " — " + oError:MessageDetails);
        :ENDIF;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("TryFetchAndReport");
```

## Related

- [`WebServices`](../classes/WebServices.md)
- [`HttpRequest`](HttpRequest.md)
- [`HttpResponse`](HttpResponse.md)
- [`HttpException`](HttpException.md)
- [`netobject`](../types/netobject.md)
