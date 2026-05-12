---
title: "HttpRequest"
summary: "A configurable outbound HTTP request — method, headers, content type, body, and timeout."
id: ssl.returns.httprequest
element_type: returns
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# HttpRequest

A configurable outbound HTTP request — method, headers, content type, body, and timeout.

An `HttpRequest` is the object you receive from [`HttpClient:CreateHttpRequest(sUrl)`](HttpClient.md#createhttprequest). It starts as an unauthenticated GET for the URL you passed. Set its properties and call `SetContent` (or `AddHeader`, `SetContentFromFile`) before passing it to [`HttpClient:GetResponse`](HttpClient.md#getresponse).

A new request authenticates with default credentials unless a user and password are supplied at creation time, in which case it authenticates as that user.

## When to use

- When you need to set headers or change the request method (POST, PUT, DELETE).
- When you need to send a body — text, binary, or multipart form.
- When you need to set a custom timeout for a slow endpoint.

## How obtained

| Producer | Call form |
|---|---|
| [`HttpClient`](HttpClient.md) | `oHttpClient:CreateHttpRequest(sUrl)` |

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `UserAgent` | [string](../types/string.md) | read-write | The `User-Agent` header value. |
| `Timeout` | [number](../types/number.md) | read-write | Maximum wait, in milliseconds, for the response. |
| `ContentType` | [string](../types/string.md) | read-write | The `Content-Type` header for the request body (e.g., `application/json`). |
| `ContentLength` | [number](../types/number.md) | read-write | Byte length of the request body. Set automatically by `SetContent`; assign explicitly only when streaming bodies you build by hand. |
| `Method` | [string](../types/string.md) | read-write | HTTP method (`GET`, `POST`, `PUT`, `DELETE`, etc.). Defaults to `GET`. |
| `Accept` | [string](../types/string.md) | read-write | The `Accept` header value. |

`Timeout` is in **milliseconds**. A value of `30000` waits up to 30 seconds.

## Methods Summary

| Name | Returns | Description |
|------|---------|-------------|
| `AddHeader` | none | Adds a custom request header. |
| `SetContent` | none | Sets the request body. Multiple forms accept text, binary, or multipart content. |
| `SetContentFromFile` | none | Sets the request body to the contents of a file. |
| `CreateHttpForm` | object | Returns a multipart form object you can populate and pass to `SetContent`. |

## Methods

### `AddHeader`

Adds a custom request header. Each call appends one header — `Content-Type` and `Accept` are set through their dedicated properties instead.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sName` | [string](../types/string.md) | yes | Header name. |
| `sValue` | [string](../types/string.md) | yes | Header value. |

### `SetContent`

Sets the request body. The body must be set before the request is sent. Forms:

- `SetContent(sValue)` — body is the text you pass, encoded as UTF-8.
- `SetContent(aBytes)` — body is an array of bytes.
- `SetContent(oForm)` — body is a multipart form (built with `CreateHttpForm`). Sends the request as a POST with a multipart body.
- `SetContent(oMultipart)` — body is a generic multipart object. Sends as a POST.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sValue` / `aBytes` / `oForm` / `oMultipart` | varies | yes | The body content. |

The multipart object surfaces (`HttpForm`, `HttpMultipart`) are documented in a separate batch.

### `SetContentFromFile`

Sets the request body to the contents of a file on disk.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sFileName` | [string](../types/string.md) | yes | Path to the file whose contents become the request body. |

### `CreateHttpForm`

Returns a multipart form object you can populate and pass back to `SetContent`. Use this for `multipart/form-data` POSTs that include named parts.

**Returns:** [object](../types/object.md) — A multipart form. Its surface is documented in a separate batch.

## Best practices

!!! success "Do"
    - Set `Method`, `ContentType`, and `Accept` before calling `SetContent` so the request is fully configured before it is sent.
    - Use a finite `Timeout` (in milliseconds) when calling endpoints that may stall; otherwise the runtime default applies.
    - Use `SetContentFromFile` for large bodies rather than reading the file into a string and passing it to `SetContent`.

!!! failure "Don't"
    - Try to construct an `HttpRequest` directly — it is only obtainable via [`HttpClient:CreateHttpRequest`](HttpClient.md#createhttprequest).
    - Set `ContentLength` manually after calling `SetContent`. The byte length is already configured.
    - Use `AddHeader` to set `Content-Type` or `Accept`. Use the dedicated properties so the runtime can manage them consistently.

## Caveats

- `HttpRequest` is not directly constructable. Obtain it from [`HttpClient:CreateHttpRequest`](HttpClient.md#createhttprequest).
- `Timeout` is in milliseconds. Setting a value of `30` waits 30 milliseconds, not 30 seconds.
- `SetContent(sValue)` encodes text as UTF-8. If you need a different encoding, build the byte array yourself and pass it to the bytes form.
- The multipart forms of `SetContent` (and `CreateHttpForm`) are usable today, but the multipart object surfaces are documented in a separate, forthcoming batch.

## Examples

### POST a JSON body

Sets the method, content type, and accept header before posting a small JSON payload.

```ssl
:PROCEDURE NotifyBatchComplete;
    :DECLARE oWebServices, oHttpClient, oRequest, oResponse;

    oWebServices := WebServices{};
    oHttpClient := oWebServices:CreateHttpClient();

    oRequest := oHttpClient:CreateHttpRequest("https://notifier.example/api/batch");
    oRequest:Method := "POST";
    oRequest:ContentType := "application/json";
    oRequest:Accept := "application/json";
    oRequest:SetContent("{""batch"":""B-1042"",""status"":""complete""}");

    oResponse := oHttpClient:GetResponse(oRequest);
    UsrMes(oResponse:GetValueAsString());
:ENDPROC;

/* Usage;
DoProc("NotifyBatchComplete");
```

### Add a custom auth header and a longer timeout

Adds an `Authorization` header and gives the request 60 seconds before timing out.

```ssl
:PROCEDURE FetchWithBearer;
    :DECLARE oWebServices, oHttpClient, oRequest, sBody;

    oWebServices := WebServices{};
    oHttpClient := oWebServices:CreateHttpClient();

    oRequest := oHttpClient:CreateHttpRequest("https://lims-data.example/api/v2/samples/recent");
    oRequest:AddHeader("Authorization", "Bearer abcdef0123456789");
    oRequest:Timeout := 60000;
    oRequest:Accept := "application/json";

    sBody := oHttpClient:GetText(oRequest);
    UsrMes(sBody);
:ENDPROC;

/* Usage;
DoProc("FetchWithBearer");
```

### Upload a file as the request body

Uses `SetContentFromFile` to send a binary file as a `PUT` request body.

```ssl
:PROCEDURE UploadResultArchive;
    :DECLARE oWebServices, oHttpClient, oRequest, oResponse;

    oWebServices := WebServices{};
    oHttpClient := oWebServices:CreateHttpClient();

    oRequest := oHttpClient:CreateHttpRequest("https://archive.example/api/results/B-1042");
    oRequest:Method := "PUT";
    oRequest:ContentType := "application/zip";
    oRequest:SetContentFromFile("C:\Lims\Outbox\B-1042.zip");

    oResponse := oHttpClient:GetResponse(oRequest);
    UsrMes("Server responded: " + oResponse:GetValueAsString());
:ENDPROC;

/* Usage;
DoProc("UploadResultArchive");
```

## Related

- [`HttpClient`](HttpClient.md)
- [`HttpResponse`](HttpResponse.md)
- [`HttpException`](HttpException.md)
- [`WebServices`](../classes/WebServices.md)
