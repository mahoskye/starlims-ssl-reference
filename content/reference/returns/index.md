---
title: "Returns"
summary: "Objects you obtain from another element — clients, requests, responses, and other return-shaped values that are not constructed directly."
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Returns

Some SSL objects are not constructed with `Name{}` syntax. You obtain them from another element — typically by calling a method on a class. They have their own properties and methods that are useful in their own right, so they get their own pages here.

Two clusters live here today: the HTTP/SOAP client objects produced by [`WebServices`](../classes/WebServices.md), and the endpoint runtime objects produced by the [`Request`](../special-forms/request.md) and [`Response`](../special-forms/response.md) ambients available inside endpoint scripts. Other return-shaped objects elsewhere in the reference are linked at the bottom for discovery.

## HTTP

| Page | Obtained from | Purpose |
|------|---------------|---------|
| [HttpClient](HttpClient.md) | `WebServices{}:CreateHttpClient()` | Entry point for outbound HTTP requests. Build requests, fetch responses, retrieve text/XML/files. |
| [HttpRequest](HttpRequest.md) | `HttpClient:CreateHttpRequest(url)` | A configurable request: headers, method, content type, body, timeout. |
| [HttpResponse](HttpResponse.md) | `HttpClient:GetResponse(...)` | The response: status, headers, body as text/XML/file. |
| [HttpException](HttpException.md) | `HttpClient:GetLastServerException()` | Details on the most recent failed request — status code, message, server response body. |

## SOAP

| Page | Obtained from | Purpose |
|------|---------------|---------|
| [SoapClient](SoapClient.md) | `WebServices{}:CreateSoapClient()` | Calls SOAP web services. Configures the endpoint, supplies credentials, invokes methods. |
| [SoapResponse](SoapResponse.md) | `SoapClient:CallWebService(method)` | The result of a SOAP call. Read scalar values, navigate object fields and arrays, save binary results. |
| [SoapParameters](SoapParameters.md) | `SoapClient:Parameters` | The parameter list passed to a SOAP method — add scalar, XML-typed, binary, or by-reference parameters. |

## Endpoint runtime

| Page | Obtained from | Purpose |
|------|---------------|---------|
| [SSLRequest](SSLRequest.md) | [`Request`](../special-forms/request.md) ambient | The incoming HTTP request — method, URL, headers, query string, cookies, forms, body, uploaded files. |
| [SSLResponse](SSLResponse.md) | [`Response`](../special-forms/response.md) ambient | The outgoing HTTP response — write content, set status, redirect, attach headers and cookies. |
| [SSLWsRequest](SSLWsRequest.md) | [`Request`](../special-forms/request.md) ambient (web-service context) | Subclass of `SSLRequest` that adds `Parameters` for positional call arguments. |
| [SSLWsResponse](SSLWsResponse.md) | [`Response`](../special-forms/response.md) ambient (web-service context) | Subclass of `SSLResponse` that adds `Value` for structured returns. |
| [SSLNameValueContainer](SSLNameValueContainer.md) | `SSLRequest` collection properties | Name/value bag returned by `Request:QueryString`, `Cookies`, `Forms`, `Headers`, `ServerVariables`, `ClientCertificate`. |

## Related return-shaped pages elsewhere

These objects are also "obtained from" another element rather than constructed, but live in their existing categories:

- [`netobject`](../types/netobject.md) — returned by `MakeNETObject`, `LimsNETConnect`, `LimsNETTypeOf`. Documented as a type because it represents a runtime value class, not a discrete API surface.
- [`SDMSDocUploader`](../classes/SDMSDocUploader.md) — returned by `SDMS:CreateDocUploader()`. Has its own constructable form too, so it is a class.
- [`CDataField`](../classes/CDataField.md), [`CDataRow`](../classes/CDataRow.md), [`CDataColumn`](../classes/CDataColumn.md), [`CDataColumns`](../classes/CDataColumns.md) — produced by navigating from a [`CDataTable`](../classes/CDataTable.md). Documented as classes because the family is tightly cross-referenced.
- [`SSLError`](../classes/SSLError.md) — produced by `GetLastSSLError()` and exposed on properties such as `Email:Exception`. Documented as a class.
