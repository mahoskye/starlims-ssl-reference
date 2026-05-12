---
title: "SSLNameValueContainer"
summary: "A name/value bag — read or list values from a request's headers, query string, cookies, forms, server variables, or client certificate fields."
id: ssl.returns.sslnamevaluecontainer
element_type: returns
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SSLNameValueContainer

A name/value bag — read or list values from a request's headers, query string, cookies, forms, server variables, or client certificate fields.

An `SSLNameValueContainer` is the object returned by six properties on [`SSLRequest`](SSLRequest.md): `QueryString`, `Cookies`, `Forms`, `Headers`, `ServerVariables`, and `ClientCertificate`. Each instance wraps a single name/value collection from the incoming HTTP request. You read individual values by name, list every key, or replace a value.

Two reading idioms are equivalent for known names:

```ssl
sValue := oContainer:Get("SomeName");   /* explicit method call ;
sValue := oContainer:SomeName;          /* expando-style member access ;
```

The expando form is more concise and is the recommended idiom for fixed, known keys (e.g., reading a specific query parameter or header). Use `Get` when the key is dynamic — the value is in a variable, looped over from `AllKeys`, etc.

## When to use

- When you need to read a query-string parameter, header, cookie, or form field from an incoming request.
- When you need to list all keys present in one of those collections.
- When you need to programmatically iterate over every entry.

## How obtained

| Producer | Call form |
|---|---|
| [`SSLRequest`](SSLRequest.md) | `Request:QueryString`, `Request:Cookies`, `Request:Forms`, `Request:Headers`, `Request:ServerVariables`, `Request:ClientCertificate` |

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `AllKeys` | [array](../types/array.md) | read-only | Every key in the collection, as an array of strings. Returns an empty array when the collection has no entries. |

## Methods

### `Get`

Returns the value associated with the given name. Returns an empty string when the name is not present.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sName` | [string](../types/string.md) | yes | Key to look up. |

**Returns:** [string](../types/string.md) — The value, or `""` when the name is not in the collection.

### `Set`

Stores a value under the given name. Use this for collections you can write to (for example, a response header collection if your endpoint exposes one). For request-side collections, treat values as read — `Set` does not change the underlying request.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sName` | [string](../types/string.md) | yes | Key to write. |
| `sValue` | [string](../types/string.md) | yes | New value. |

## Best practices

!!! success "Do"
    - Use the expando form (`oContainer:SomeName`) for fixed, known keys — it reads more naturally.
    - Use `Get(sName)` when the key is in a variable.
    - Use `AllKeys` to list every entry, then `Get` each value, when you need to iterate.

!!! failure "Don't"
    - Try to construct an `SSLNameValueContainer` directly — it is only obtainable from one of the six [`SSLRequest`](SSLRequest.md) properties listed above.
    - Use the expando form to *write* a value (e.g., `oContainer:SomeName := "x"`). Expando-style writes to a name already in the collection raise an error; use `Set(sName, sValue)` instead.
    - Assume `Get` raises when a name is missing. It returns an empty string instead.

## Caveats

- `SSLNameValueContainer` is not directly constructable. Obtain it from one of the [`SSLRequest`](SSLRequest.md) collection properties.
- Values from the request side (`QueryString`, `Cookies`, `Forms`, `Headers`, `ServerVariables`, `ClientCertificate`) reflect the incoming request. Calling `Set` on them does not modify the request and has no effect downstream.
- The expando form (`oContainer:Name`) reads work for any name present in the collection. Writes to a name in the collection raise an error — use `Set` for writes.
- Lookups are case-insensitive: `oQueryString:UserName` and `oQueryString:USERNAME` resolve to the same value.

## Examples

### Read one query-string value

Reads a single named query parameter from the incoming request.

```ssl
:PROCEDURE GreetByName;
    :DECLARE oQueryString, sName;

    oQueryString := Request:QueryString;
    sName := oQueryString:Name;

    Response:Write("Hello, " + sName);
:ENDPROC;

/* Usage: GET /MyEndpoint?Name=Alice ;
```

### Iterate every header

Lists every header on the incoming request, then writes each name/value pair to the response body.

```ssl
:PROCEDURE DumpHeaders;
    :DECLARE oHeaders, aKeys, sKey, sValue, i;

    oHeaders := Request:Headers;
    aKeys := oHeaders:AllKeys;

    :FOR i := 1 :TO Len(aKeys);
        sKey := aKeys[i];
        sValue := oHeaders:Get(sKey);
        Response:Write(sKey + ": " + sValue + Chr(10));
    :NEXT;
:ENDPROC;

/* Usage: any HTTP request that hits this endpoint ;
```

### Read a cookie with a dynamic key

Looks up a cookie whose name comes from another piece of state, so the expando form is not appropriate.

```ssl
:PROCEDURE ReadDynamicCookie;
    :DECLARE oCookies, sCookieName, sValue;

    sCookieName := "session_" + Request:UserName;
    oCookies := Request:Cookies;
    sValue := oCookies:Get(sCookieName);

    :IF Empty(sValue);
        Response:Write("No cookie set for this user");
    :ELSE;
        Response:Write("Found cookie: " + sValue);
    :ENDIF;
:ENDPROC;
```

## Related

- [`SSLRequest`](SSLRequest.md)
- [`Request`](../special-forms/request.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
