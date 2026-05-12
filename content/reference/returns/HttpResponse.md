---
title: "HttpResponse"
summary: "An HTTP response — content metadata, headers, and the body as text, XML, or a saved file."
id: ssl.returns.httpresponse
element_type: returns
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# HttpResponse

An HTTP response — content metadata, headers, and the body as text, XML, or a saved file.

An `HttpResponse` is the object you receive from [`HttpClient:GetResponse`](HttpClient.md#getresponse). It exposes the response headers and content metadata as properties, and offers methods to consume the body in the form you want — text, XML DOM, or a file written to disk.

You can call only one value-extraction method per response — the body is consumed by the first call.

## When to use

- When you need the response body as a string.
- When the body is XML and you want a DOM you can navigate.
- When the body is binary or large and you want it saved to a file rather than held in memory.
- When you need to read response headers (`Content-Type`, custom server headers) before deciding how to handle the body.

## How obtained

| Producer | Call form |
|---|---|
| [`HttpClient`](HttpClient.md) | `oHttpClient:GetResponse(oRequest)` or `oHttpClient:GetResponse(sUrl)` |

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `ContentLength` | [number](../types/number.md) | read-only | Length of the response body in bytes, as reported by the server. |
| `ContentEncoding` | [string](../types/string.md) | read-only | The `Content-Encoding` header value (e.g., `gzip`). |
| `ContentType` | [string](../types/string.md) | read-only | The `Content-Type` header value. |
| `HeaderNames` | [array](../types/array.md) | read-only | All response header names, as an array of strings. Use with `GetHeader` to read individual values. |

## Methods Summary

| Name | Returns | Description |
|------|---------|-------------|
| `GetHeader` | [string](../types/string.md) | Returns the value of a named response header. |
| `GetValueAsString` | [string](../types/string.md) | Returns the response body as text. |
| `GetValueAsXmlDom` | [object](../types/object.md) | Returns the response body parsed as an XML DOM object. |
| `SaveValueToFile` | [string](../types/string.md) | Writes the response body to a file and returns the path. |

## Methods

### `GetHeader`

Returns the value of a named response header. Returns an empty string when the header is not present.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sName` | [string](../types/string.md) | yes | Header name to look up. |

**Returns:** [string](../types/string.md) — The header value, or `""` when the header is not in the response.

### `GetValueAsString`

Returns the response body as text. Compressed responses are returned in their decompressed form.

**Returns:** [string](../types/string.md) — The response body decoded to text.

### `GetValueAsXmlDom`

Reads the response body as text, then parses it as XML.

**Returns:** [object](../types/object.md) — XML DOM object. See [`netobject`](../types/netobject.md) for the surface available for navigating it. Raises if the body is not well-formed XML.

### `SaveValueToFile`

Writes the response body to a file. Two forms:

`SaveValueToFile()` writes to a runtime-chosen path; `SaveValueToFile(sPath)` writes to the path you specify.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sPath` | [string](../types/string.md) | no | Destination path. When omitted, the runtime chooses a path. |

**Returns:** [string](../types/string.md) — The path the file was written to.

## Best practices

!!! success "Do"
    - Choose one of `GetValueAsString`, `GetValueAsXmlDom`, or `SaveValueToFile` per response — each consumes the body.
    - Inspect `ContentType` before choosing how to consume the body (parse XML only when the type indicates XML).
    - Use `SaveValueToFile` for large or binary bodies; it avoids loading them into memory.

!!! failure "Don't"
    - Try to construct an `HttpResponse` directly — it is only obtainable via [`HttpClient:GetResponse`](HttpClient.md#getresponse).
    - Call `GetValueAsString` and then `GetValueAsXmlDom` on the same response. The body is consumed by the first call.
    - Assume `GetValueAsXmlDom` will return a DOM for non-XML responses. It will raise.

## Caveats

- `HttpResponse` is not directly constructable. Obtain it from [`HttpClient:GetResponse`](HttpClient.md#getresponse).
- The response body is consumed once. The first value-extraction call reads it; subsequent calls on the same response are not supported.
- `HeaderNames` returns the header names only. Use `GetHeader(sName)` to read each value.
- `ContentLength` reflects what the server sent. It may be `-1` for chunked responses where the length is not declared.

## Examples

### Read a JSON response as text

Issues a GET, then reads the body as a string.

```ssl
:PROCEDURE LoadInstrumentSettings;
    :DECLARE oWebServices, oHttpClient, oResponse, sBody;

    oWebServices := WebServices{};
    oHttpClient := oWebServices:CreateHttpClient();

    oResponse := oHttpClient:GetResponse("https://lims-instruments.example/api/settings");
    sBody := oResponse:GetValueAsString();

    UsrMes("Settings: " + sBody);
:ENDPROC;

/* Usage;
DoProc("LoadInstrumentSettings");
```

### Inspect headers before consuming the body

Reads `Content-Type` to decide whether to parse the body as XML or treat it as plain text.

```ssl
:PROCEDURE ReadFlexibleResponse;
    :DECLARE oWebServices, oHttpClient, oResponse, sType, oXml, sText;

    oWebServices := WebServices{};
    oHttpClient := oWebServices:CreateHttpClient();

    oResponse := oHttpClient:GetResponse("https://lims-data.example/api/sample/SAMP-001");
    sType := oResponse:ContentType;

    :IF "xml" $ sType;
        oXml := oResponse:GetValueAsXmlDom();
        UsrMes("XML response received");
    :ELSE;
        sText := oResponse:GetValueAsString();
        UsrMes("Text response: " + sText);
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("ReadFlexibleResponse");
```

### Save a binary response to a file

Downloads a binary report and writes it to a known path.

```ssl
:PROCEDURE DownloadReportPdf;
    :DECLARE oWebServices, oHttpClient, oResponse, sSavedPath;

    oWebServices := WebServices{};
    oHttpClient := oWebServices:CreateHttpClient();

    oResponse := oHttpClient:GetResponse("https://reports.example/batch/B-1042.pdf");
    sSavedPath := oResponse:SaveValueToFile("C:\Lims\Inbox\B-1042.pdf");

    UsrMes("Saved to: " + sSavedPath);
:ENDPROC;

/* Usage;
DoProc("DownloadReportPdf");
```

## Related

- [`HttpClient`](HttpClient.md)
- [`HttpRequest`](HttpRequest.md)
- [`HttpException`](HttpException.md)
- [`netobject`](../types/netobject.md)
- [`WebServices`](../classes/WebServices.md)
