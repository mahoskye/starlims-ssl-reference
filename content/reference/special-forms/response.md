---
title: "Response"
summary: "An ambient identifier in endpoint scripts that holds the outgoing HTTP response."
id: ssl.special_form.response
element_type: special_form
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Response

## What it does

Provides a reference to the outgoing HTTP response inside an SSL endpoint script. `Response` is an ambient identifier — the runtime makes it available by name inside any script invoked as an endpoint. You don't construct it; you just reference it.

The value is an [`SSLResponse`](../returns/SSLResponse.md) — set its properties (`ContentType`, `StatusCode`) and call its methods (`Write`, `Redirect`, `AddHeader`, `AddCookie`, `End`) to shape the response. When the script is invoked as a web service, the value is the [`SSLWsResponse`](../returns/SSLWsResponse.md) subclass, which adds a `Value` property used to return a structured result instead of writing a body.

## Syntax

`Response` has no declaration syntax — it is an ambient identifier the runtime makes available by name. Reference it directly:

```ssl
Response:PropertyName := value;
Response:MethodName(args)
```

## Availability

`Response` is available **only inside endpoint scripts**. Outside that context — for example, in a script invoked through `DoProc` from an interactive desktop session — referencing `Response` raises an undeclared-variable error.

If your code may run in either context, guard with a `:TRY` / `:CATCH` block:

```ssl
:TRY;
    Response:Write("only sent to HTTP callers");
:CATCH;
    /* not running as an endpoint — write to a log or skip ;
:ENDTRY;
```

## What it holds

| Context | Type |
|---|---|
| Plain HTTP endpoint | [`SSLResponse`](../returns/SSLResponse.md) |
| Web-service endpoint | [`SSLWsResponse`](../returns/SSLWsResponse.md) (subclass — adds `Value`) |

The web-service subclass inherits everything from `SSLResponse`, so calls like `Response:StatusCode := 400` work in both contexts.

## When to use

- When an endpoint script needs to send a body, set a status, or redirect.
- When a web-service script needs to return a structured result via `Response:Value`.
- When you need to attach a header or cookie to the outgoing response.

## Caveats

- `Response` is mutable: assigning properties and calling methods affects what the client receives. Be deliberate about ordering — set `ContentType` and `StatusCode` before the first `Write` so headers go out correctly.
- Outside an endpoint context, `Response` raises an undeclared-variable error on access. Guard with `:TRY` / `:CATCH` if your script may run in either context.
- Whether `Response` is an `SSLResponse` or `SSLWsResponse` depends on how the script was invoked. Code that needs to work in both contexts should rely only on the inherited surface — avoid `Value` unless you know the call path is a web service.
- After calling `End()`, further `Write` calls have no effect on the wire. After `Redirect()`, `:RETURN` from the script — subsequent code may run but its output is unlikely to reach the client.

## Examples

### Send a JSON response with an explicit status

```ssl
:PROCEDURE SendStatus;
    Response:ContentType := "application/json";
    Response:StatusCode := 200;
    Response:Write("{""status"":""ok""}");
:ENDPROC;
```

### Return a structured value from a web-service endpoint

```ssl
:PROCEDURE WebServiceLookup;
    :DECLARE sId, oResult;

    sId := Request:Parameters[1];

    oResult := CreateUdObject();
    oResult:Id := sId;
    oResult:Found := .T.;

    Response:Value := oResult;
:ENDPROC;
```

### Redirect after a side effect

```ssl
:PROCEDURE SaveAndRedirect;
    :DECLARE sOrderId;

    sOrderId := Request:Forms:OrderId;

    /* ... persist the order ... ;

    Response:Redirect("/Orders/" + sOrderId);
    :RETURN;
:ENDPROC;
```

## Related

- [`SSLResponse`](../returns/SSLResponse.md) — the type when invoked as a plain HTTP endpoint
- [`SSLWsResponse`](../returns/SSLWsResponse.md) — the type when invoked as a web service
- [`Request`](request.md) — the request-side ambient
