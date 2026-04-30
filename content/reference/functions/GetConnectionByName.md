---
title: "GetConnectionByName"
summary: "Retrieves a database connection object using a specified connection name."
id: ssl.function.getconnectionbyname
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetConnectionByName

Retrieves a database connection object using a specified connection name.

Returns a [`SQLConnection`](../classes/SQLConnection.md) object for the given `sConnectionName`. If `sConnectionName` is [`NIL`](../literals/nil.md), the function substitutes the system default connection name before lookup. An empty string is not treated as [`NIL`](../literals/nil.md) and is passed through unchanged, so it will fail the lookup. If the resolved name does not match any configured connection, the function raises an error. On success, the function always returns a new connection object.

## When to use

- When you need to interact with a database using a preconfigured connection name.
- When switching between multiple databases in a workflow based on configuration
  or context.
- When enforcing consistent connection reuse across modules without hardcoding
  connection details.

## Syntax

```ssl
GetConnectionByName(sConnectionName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sConnectionName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Connection name of the SQL connection to retrieve. If [`NIL`](../literals/nil.md), the default connection name is used. An empty string is not treated as [`NIL`](../literals/nil.md) and will fail the lookup. |

## Returns

**[SQLConnection](../classes/SQLConnection.md)** — The SQL connection object for the specified connection name.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sConnectionName` does not match any configured connection. | `The provider name: <name> not found.` |

## Best practices

!!! success "Do"
    - Validate that the connection name exists in your configuration before calling.
    - Release the connection object after use.
    - Use this function to centralize database connection logic.

!!! failure "Don't"
    - Pass hardcoded or unvalidated names — a name not present in the system configuration raises an error.
    - Leave connections open after use.
    - Pass an empty string expecting it to fall back to the default connection.
    - Display or log sensitive connection properties such as `oConn:Password` or `oConn:ConnectionString`.

## Examples

### Retrieve a connection by name

Retrieve a named connection and confirm the retrieval succeeded. Pass a configured connection name to get the corresponding SQL connection object.

```ssl
:PROCEDURE GetConnectionExample;
	:DECLARE oConn;

	oConn := GetConnectionByName("LIMS");

	UsrMes("Database: " + oConn:DatabaseName);
:ENDPROC;

/* Usage;
DoProc("GetConnectionExample");
```

[`UsrMes`](UsrMes.md) displays:

```text
Database: LIMSDB
```

## Related

- [`GetConnectionStrings`](GetConnectionStrings.md)
- [`GetDefaultConnection`](GetDefaultConnection.md)
- [`LimsSqlConnect`](LimsSqlConnect.md)
- [`LimsSqlDisconnect`](LimsSqlDisconnect.md)
- [`SQLConnection`](../classes/SQLConnection.md)
- [`string`](../types/string.md)
