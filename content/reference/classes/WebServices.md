---
title: "WebServices"
summary: "Creates client objects for outbound HTTP and SOAP integrations."
id: ssl.class.webservices
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# WebServices

Creates client objects for outbound HTTP and SOAP integrations.

`WebServices` is a factory class. Create it with `WebServices{}` and then call the method that matches the type of service you need to call.

## When to use

- When a script needs a new HTTP client object.
- When a script needs a new SOAP client object.
- When you want to choose the client type at runtime.

## Constructors

### `WebServices{}`

Creates a `WebServices` factory object.

## Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `CreateHttpClient()` | [object](../types/object.md) | Returns a new HTTP client object. |
| `CreateSoapClient()` | [object](../types/object.md) | Returns a new SOAP client object. |

### `CreateHttpClient`

Returns a new HTTP client object.

**Returns:** [object](../types/object.md) — A new HTTP client object.

### `CreateSoapClient`

Returns a new SOAP client object.

**Returns:** [object](../types/object.md) — A new SOAP client object.

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Use `CreateHttpClient()` for HTTP-based integrations.
    - Use `CreateSoapClient()` for SOAP-based integrations.
    - Treat each factory call as returning a new client object.

!!! failure "Don't"
    - Call `CreateSoapClient()` when you need an HTTP client.
    - Call `CreateHttpClient()` when you need a SOAP client.
    - Assume this page documents the full API of the returned client objects.

## Caveats

- This page documents the `WebServices` factory class only. The returned HTTP and SOAP client objects have their own APIs that are not described here.

## Examples

### Create an HTTP client object

Creates a `WebServices` factory instance and calls `CreateHttpClient()` to obtain a new HTTP client object that the caller can use for outbound HTTP requests.

```ssl
:PROCEDURE BuildHttpClient;
    :DECLARE oWebServices, oHttpClient;

    oWebServices := WebServices{};
    oHttpClient := oWebServices:CreateHttpClient();

    :RETURN oHttpClient;
:ENDPROC;

/* Run the procedure;
DoProc("BuildHttpClient");
```

### Choose a client type at runtime

Creates the factory and selects between `CreateSoapClient()` and `CreateHttpClient()` based on a boolean flag, showing how to branch on the integration type at runtime.

```ssl
:PROCEDURE CreateIntegrationClient;
    :PARAMETERS bUseSoap;
    :DECLARE oWebServices, oClient;

    oWebServices := WebServices{};

    :IF bUseSoap;
        oClient := oWebServices:CreateSoapClient();
    :ELSE;
        oClient := oWebServices:CreateHttpClient();
    :ENDIF;

    :RETURN oClient;
:ENDPROC;

/* Run the procedure;
DoProc("CreateIntegrationClient", {.T.});
```

## Related

- [`object`](../types/object.md)
