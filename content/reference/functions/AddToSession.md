---
title: "AddToSession"
summary: "Store a non-object, non-array value in the current session under a string key."
id: ssl.function.addtosession
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# AddToSession

Store a non-object, non-array value in the current session under a string key.

`AddToSession` stores `vValue` under `sKey` in the current session and always returns [`NIL`](../literals/nil.md). The key is required. Strings, numbers, booleans, dates, and other non-object values can be stored directly.

If `sKey` is [`NIL`](../literals/nil.md), the function raises an error. If `vValue` is an object or array, it raises an error instead of storing the value. If the `Session` public variable is unavailable in the current execution context, the function silently does nothing and still returns [`NIL`](../literals/nil.md).

## When to use

- When you need to keep simple per-user state across requests.
- When a workflow spans multiple steps and later steps need an earlier value.
- When you want session-scoped storage instead of writing to a database table.

## Syntax

```ssl
AddToSession(sKey, vValue)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sKey` | [string](../types/string.md) | yes | — | Session key used to store the value. |
| `vValue` | any | yes | — | Value to store. Objects and arrays are rejected. |

## Returns

**NIL** — Always returns [`NIL`](../literals/nil.md), including when the session context is not available.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sKey` is [`NIL`](../literals/nil.md). | `Argument: key cannot be null.` |
| `vValue` is an object. | `Objects are not supported in session - use Serialize/Deserialize methods.` |
| `vValue` is an array. | `Arrays are not supported in session - use ToXml/FromXml methods.` |

## Best practices

!!! success "Do"
    - Use descriptive session keys so unrelated features do not collide.
    - Convert objects to a string form before storing them in session.
    - Convert arrays to XML before storing them in session.

!!! failure "Don't"
    - Store objects or arrays directly. AddToSession rejects both.
    - Assume a successful call means the value was definitely stored. If
      the session context is unavailable, the function returns [`NIL`](../literals/nil.md) silently.
    - Leave stale session values around longer than the workflow needs.

## Examples

### Store a simple session value

Stores a username string under a named key so that later steps in the same session can retrieve it with [`GetFromSession`](GetFromSession.md).

```ssl
:PROCEDURE SaveLoginName;
	:DECLARE sUserName;

	sUserName := "jsmith";
	AddToSession("LoginUserName", sUserName);

	UsrMes("User name saved to session.");
:ENDPROC;

/* Usage;
DoProc("SaveLoginName");
```

[`UsrMes`](UsrMes.md) displays:

```text
User name saved to session.
```

### Store a serialized object as XML

Converts a user-defined object to an XML string with [`ToXml`](ToXml.md) before passing it to `AddToSession`, working around the restriction on storing objects directly.

```ssl
:PROCEDURE SaveAnalysisContext;
	:DECLARE oContext, sPayload;

	oContext := CreateUdObject({
		{"SampleID", "LAB-2024-0847"},
		{"TestCode", "WETCHEM"}
	});

	sPayload := ToXml(oContext, "AnalysisContext");
	AddToSession("CurrentAnalysisContext", sPayload);

	UsrMes("Serialized analysis context stored as XML.");
:ENDPROC;

/* Usage;
DoProc("SaveAnalysisContext");
```

[`UsrMes`](UsrMes.md) displays:

```text
Serialized analysis context stored as XML.
```

## Related

- [`ClearSession`](ClearSession.md)
- [`GetFromSession`](GetFromSession.md)
- [`ToXml`](ToXml.md)
- [`FromXml`](FromXml.md)
- [`string`](../types/string.md)
