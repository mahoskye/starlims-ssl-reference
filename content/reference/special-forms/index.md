---
title: "Special Forms"
summary: "8 language constructs - class infrastructure, scope references, code organization, access control, and endpoint runtime ambients."
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Special Forms

**8 language constructs** — class infrastructure, scope references, code organization, access control, and endpoint runtime ambients.

| Special Form | Description |
|--------------|-------------|
| [access-modifiers](access-modifiers.md) | `/*@private;` and `/*@protected;` annotations for controlling procedure visibility within a class. |
| [base](base.md) | Provides explicit access to properties, fields, or methods defined on the immediate parent class from within an instance method. |
| [code-block](code-block.md) | Defines an anonymous code block with bound parameters and a single expression body that can be stored, passed, and invoked dynamically. |
| [code-organization](code-organization.md) | Comment regions (`/* region` / `/* endregion`) for grouping related procedures or code sections in long files. |
| [constructor](constructor.md) | Runs one-time initialization code when a user-defined class instance is created. |
| [me](me.md) | Provides a reference to the current class instance inside class method bodies, enabling direct access to the object's properties and methods. |
| [request](request.md) | The incoming HTTP request inside an endpoint script — an [`SSLRequest`](../returns/SSLRequest.md) (or [`SSLWsRequest`](../returns/SSLWsRequest.md) in a web-service context). |
| [response](response.md) | The outgoing HTTP response inside an endpoint script — an [`SSLResponse`](../returns/SSLResponse.md) (or [`SSLWsResponse`](../returns/SSLWsResponse.md) in a web-service context). |
