---
title: "HttpException"
summary: "Details on a failed HTTP request — status, message, and the server's response body."
id: ssl.returns.httpexception
element_type: returns
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# HttpException

Details on a failed HTTP request — status, message, and the server's response body.

An `HttpException` is the object you receive from [`HttpClient:GetLastServerException`](HttpClient.md#getlastserverexception) after a failed call. The same exception is also raised by the call that failed, so you can either catch it directly or look it up from the client after the fact.

`StatusCode` and `Status` describe the failure mode in terms of the request lifecycle (DNS, connection, server response). `MessageDetails` gives you the server's error body when one is available — useful for APIs that return a JSON or text error payload alongside a non-success HTTP status.

## When to use

- When you need to read the server's error body after a failed call.
- When you need to branch on the failure mode (timeout, connection failure, server error).
- When you want to log a structured error rather than just a generic message.

## How obtained

| Producer | Call form |
|---|---|
| [`HttpClient`](HttpClient.md) | `oHttpClient:GetLastServerException()` |

`HttpException` is also raised directly by [`HttpClient:GetResponse`](HttpClient.md#getresponse) (and any method that delegates to it) when a request fails. Catch the error in a `:TRY` / `:CATCH` block to access it.

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `StatusCode` | [number](../types/number.md) | read-only | A numeric code identifying the failure mode (e.g., timeout, name resolution failure, protocol error). |
| `Status` | [string](../types/string.md) | read-only | A short text label for the failure mode (e.g., `Timeout`, `ConnectFailure`, `ProtocolError`). |
| `Message` | [string](../types/string.md) | read-only | A short, human-readable description of the failure. |
| `MessageDetails` | [string](../types/string.md) | read-only | The server's response body when one was returned. Falls back to a `"Server is unable to provide more information"` message followed by `Message` when no body is available. |

## Best practices

!!! success "Do"
    - Read `MessageDetails` to get the server's error body when an API returns one — many APIs return JSON or plain-text error payloads alongside non-success statuses.
    - Branch on `Status` (the text label) when behavior should differ for transient failures (timeouts, connect failures) vs. server-reported errors (protocol error).
    - Capture both `Status` and `MessageDetails` in error logs so a reader can tell whether the failure was on the way out or on the way back.

!!! failure "Don't"
    - Try to construct an `HttpException` directly — it is only obtainable via [`HttpClient:GetLastServerException`](HttpClient.md#getlastserverexception) or by catching the error raised by a failed call.
    - Confuse `StatusCode` with the HTTP response status code. `StatusCode` here describes the failure mode of the request itself; for a non-success HTTP status (e.g., 404, 500), the server's response is in `MessageDetails`.
    - Rely on `MessageDetails` always being meaningful — when the server returned no body, it falls back to a generic message.

## Caveats

- `HttpException` is not directly constructable. Obtain it from [`HttpClient:GetLastServerException`](HttpClient.md#getlastserverexception) or catch it as the error raised by a failed [`HttpClient:GetResponse`](HttpClient.md#getresponse).
- The value returned by `GetLastServerException` is cleared by the next successful response on the same client. Read it immediately after a failure.
- `StatusCode` is not the HTTP response code. For HTTP-level failures (404, 500, etc.) the failure mode is reported as a protocol-level status, and the server's body is exposed via `MessageDetails`.

## Examples

### Catch a failed request and report the server's error body

Wraps a call in a `:TRY` block and reads `MessageDetails` from the exception when it fails.

```ssl
:PROCEDURE TryFetchOrLog;
    :DECLARE oWebServices, oHttpClient, sBody, oError;

    oWebServices := WebServices{};
    oHttpClient := oWebServices:CreateHttpClient();

    :TRY;
        sBody := oHttpClient:GetText("https://lims-instruments.example/api/status");
        UsrMes("OK: " + sBody);
    :CATCH;
        oError := oHttpClient:GetLastServerException();
        :IF oError != NIL;
            UsrMes("Failed (" + oError:Status + "): " + oError:MessageDetails);
        :ENDIF;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("TryFetchOrLog");
```

### Branch on the failure mode

Distinguishes a transient timeout from a protocol-level failure to choose between retrying and giving up.

```ssl
:PROCEDURE FetchWithRetryOnTimeout;
    :DECLARE oWebServices, oHttpClient, sBody, oError, bShouldRetry;

    oWebServices := WebServices{};
    oHttpClient := oWebServices:CreateHttpClient();
    bShouldRetry := .F.;

    :TRY;
        sBody := oHttpClient:GetText("https://lims-data.example/api/v2/samples/recent");
        UsrMes("Result: " + sBody);
    :CATCH;
        oError := oHttpClient:GetLastServerException();
        :IF oError != NIL .AND. oError:Status = "Timeout";
            bShouldRetry := .T.;
        :ELSE;
            UsrMes("Permanent failure: " + oError:Message);
        :ENDIF;
    :ENDTRY;

    :IF bShouldRetry;
        UsrMes("Will retry after a backoff");
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("FetchWithRetryOnTimeout");
```

## Related

- [`HttpClient`](HttpClient.md)
- [`HttpRequest`](HttpRequest.md)
- [`HttpResponse`](HttpResponse.md)
- [`WebServices`](../classes/WebServices.md)
