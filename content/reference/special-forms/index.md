---
title: "Special Forms"
summary: "8 language constructs grouped by role - class infrastructure, endpoint runtime ambients, and other script-level forms."
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Special Forms

**8 language constructs**, grouped by where they apply.

## Class infrastructure

Forms that only have meaning inside a [`:CLASS`](../keywords/CLASS.md) method body. See [`:CLASS`](../keywords/CLASS.md) and [`:INHERIT`](../keywords/INHERIT.md) for how classes are declared.

| Special Form | Description |
|--------------|-------------|
| [`Me:`](me.md) | Reference to the current instance inside a class method. Required to qualify class-level fields and to call sibling methods. |
| [`Base:`](base.md) | Explicit access to fields or methods defined on the immediate parent class. |
| [`Constructor`](constructor.md) | Reserved declaration name (`:PROCEDURE Constructor;`) that runs one-time initialization when an instance is created. |

## Endpoint ambients

Identifiers that are pre-bound by the runtime inside endpoint and web-service scripts.

| Special Form | Description |
|--------------|-------------|
| [`Request`](request.md) | The incoming HTTP request inside an endpoint script — an [`SSLRequest`](../returns/SSLRequest.md) (or [`SSLWsRequest`](../returns/SSLWsRequest.md) in a web-service context). |
| [`Response`](response.md) | The outgoing HTTP response inside an endpoint script — an [`SSLResponse`](../returns/SSLResponse.md) (or [`SSLWsResponse`](../returns/SSLWsResponse.md) in a web-service context). |

## Other

Script-level forms that are not tied to classes or endpoints.

| Special Form | Description |
|--------------|-------------|
| [Access Modifiers](access-modifiers.md) | `/*@private;` and `/*@protected;` annotations for controlling visibility of script-level [`:PROCEDURE`](../keywords/PROCEDURE.md) declarations. Ignored inside [`:CLASS`](../keywords/CLASS.md) bodies. |
| [Code Block](code-block.md) | Defines an anonymous code block with bound parameters and a single expression body that can be stored, passed, and invoked dynamically. |
| [Code Organization](code-organization.md) | Comment regions (`/* region` / `/* endregion`) for grouping related procedures or code sections in long files. |
