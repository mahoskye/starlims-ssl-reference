---
title: "Request"
summary: "An ambient identifier in endpoint scripts that holds the incoming HTTP request."
id: ssl.special_form.request
element_type: special_form
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [11]
---

# Request

## What it does

Provides a reference to the incoming HTTP request inside an SSL endpoint script. `Request` is an ambient identifier — the runtime makes it available by name inside any script invoked as an endpoint (REST handler, custom URL handler, web-service implementation). You don't construct it; you just reference it.

The value is an [`SSLRequest`](../returns/SSLRequest.md) — read its properties to inspect the incoming method, URL, headers, query string, cookies, body, and so on. When the script is invoked specifically as a web service, the value is the [`SSLWsRequest`](../returns/SSLWsRequest.md) subclass, which adds a `Parameters` array on top of everything `SSLRequest` exposes.

## Syntax

`Request` has no declaration syntax — it is an ambient identifier the runtime makes available by name. Reference it directly:

```ssl
Request;
Request:PropertyName;
Request:CollectionName:Key;
Request:MethodName(args)
```

## Availability

`Request` describes an incoming HTTP call **only inside endpoint scripts**. Referencing it elsewhere does not raise an undeclared-variable error: in observed runtime behavior, a script run from Designer can read `Request:UserAgent`, which returns the Designer client's user-agent text. A successful read therefore does not prove that the script is handling an HTTP request.

## What it holds

| Context | Type |
|---|---|
| Plain HTTP endpoint | [`SSLRequest`](../returns/SSLRequest.md) |
| Web-service endpoint | [`SSLWsRequest`](../returns/SSLWsRequest.md) (subclass — adds `Parameters`) |

The web-service subclass inherits everything from `SSLRequest`, so code that reads only the inherited surface (e.g., `Request:HttpMethod`) works in both contexts.

## When to use

- When an endpoint script needs to read the incoming method, URL, headers, query string, cookies, or body.
- When a web-service script needs the call's positional parameters.
- When you need to know the authenticated user's name (`Request:UserName`) inside a request handler.

## Caveats

- `Request` is read-only from the script's perspective. Modifying values on its collection properties (`QueryString`, `Headers`, etc.) does not change anything downstream.
- Outside an endpoint context, `Request` does not raise on access, but its values do not come from an HTTP caller. In a script run from Designer, `Request:UserAgent` returns the Designer client's user-agent text.
- Whether `Request` is an `SSLRequest` or `SSLWsRequest` depends on how the script was invoked. Code that needs to work in both contexts should rely only on the inherited surface — avoid `Parameters` unless you know the call path is a web service.

## Examples

### Read a query parameter and the authenticated user

```ssl
:PROCEDURE GreetCurrentUser;
    :DECLARE sId, sUser;

    sId := Request:QueryString:Id;
    sUser := Request:UserName;

    Response:Write("User " + sUser + " requested item " + sId);
:ENDPROC;
```

### Branch on whether the call is a web service

Reads the inherited `IsHTMLWsRequest` flag to decide which return path to take.

```ssl
:PROCEDURE FlexibleEndpoint;
    :DECLARE sId, oResult;

    sId := Request:QueryString:Id;

    /* ... build oResult ... ;

    :IF Request:IsHTMLWsRequest;
        Response:Value := oResult;
    :ELSE;
        Response:ContentType := "text/html";
        Response:Write("<h1>" + oResult:Title + "</h1>");
    :ENDIF;
:ENDPROC;
```

## Related

- [`SSLRequest`](../returns/SSLRequest.md) — the type when invoked as a plain HTTP endpoint
- [`SSLWsRequest`](../returns/SSLWsRequest.md) — the type when invoked as a web service
- [`Response`](response.md) — the response-side ambient
- [`SSLNameValueContainer`](../returns/SSLNameValueContainer.md) — type returned by `Request:Headers`, `Request:QueryString`, etc.
