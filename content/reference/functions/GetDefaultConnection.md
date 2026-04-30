---
title: "GetDefaultConnection"
summary: "Returns the current default database connection name."
id: ssl.function.getdefaultconnection
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetDefaultConnection

Returns the current default database connection name.

`GetDefaultConnection` returns the current default database connection value held by the runtime. Use it when you need to inspect which connection name later database operations will use by default. The function takes no parameters and simply returns the current value as a string. It does not change the active connection, list configured connections, or verify that the returned connection is valid or currently connected.

## When to use

- When you need to see which connection name is currently set as the default.
- When you want to log or display the active default connection before running database work.
- When you need to compare the current default connection before and after calling [`SetDefaultConnection`](SetDefaultConnection.md).
- When a script can operate against multiple connections and needs to inspect the current default first.

## Syntax

```ssl
GetDefaultConnection()
```

## Parameters

This function takes no parameters.

## Returns

**[string](../types/string.md)** — The current default database connection name.

## Best practices

!!! success "Do"
    - Read the current default connection before changing it with [`SetDefaultConnection`](SetDefaultConnection.md).
    - Treat the return value as a connection name to inspect or pass to related database functions.
    - Verify connectivity separately when your script depends on the connection being available.

!!! failure "Don't"
    - Assume the returned name is automatically valid or currently connected. This function only reports the current default value.
    - Use this function when you need to change the active connection. Use [`SetDefaultConnection`](SetDefaultConnection.md) for that.
    - Confuse this with connection enumeration. Use [`GetConnectionStrings`](GetConnectionStrings.md) when you need the list of configured connections.

## Caveats

- If another part of the same runtime context changes the default connection, later calls return the updated value.

## Examples

### Save and restore the default connection

Captures the current default connection name, temporarily switches to a different connection, confirms the switch, then restores the original.

```ssl
:PROCEDURE UseTemporaryConnection;
    :DECLARE sOriginalConnection, sTempConnection, sCurrentConnection;

    sOriginalConnection := GetDefaultConnection();
    sTempConnection := "Reporting";

    SetDefaultConnection(sTempConnection);
    sCurrentConnection := GetDefaultConnection();

    :IF sCurrentConnection == sTempConnection;
        UsrMes("Using connection: " + sCurrentConnection);
    :ENDIF;

    SetDefaultConnection(sOriginalConnection);
:ENDPROC;

/* Usage;
DoProc("UseTemporaryConnection");
```

`UsrMes` displays:

```text
Using connection: Reporting
```

## Related

- [`GetConnectionByName`](GetConnectionByName.md)
- [`GetConnectionStrings`](GetConnectionStrings.md)
- [`IsDBConnected`](IsDBConnected.md)
- [`LimsSqlConnect`](LimsSqlConnect.md)
- [`LimsSqlDisconnect`](LimsSqlDisconnect.md)
- [`SetDefaultConnection`](SetDefaultConnection.md)
- [`string`](../types/string.md)
