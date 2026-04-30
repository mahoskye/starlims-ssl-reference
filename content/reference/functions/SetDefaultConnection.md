---
title: "SetDefaultConnection"
summary: "Changes the active default database connection name and returns the previous default connection."
id: ssl.function.setdefaultconnection
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SetDefaultConnection

Changes the active default database connection name and returns the previous default connection.

`SetDefaultConnection()` stores the supplied string as the runtime default connection value and returns the previous default connection name. The function accepts one surfaced parameter, `sDefaultConnection`. It rejects [`NIL`](../literals/nil.md) and any non-string value, but otherwise assigns the provided string without validating that it names a configured or connected database. Use it when later database calls should rely on a different default connection and you want to restore the previous value afterward.

## When to use

- When you need later database calls to use a different default connection name.
- When you want to save the current default, switch temporarily, and restore it after the work completes.
- When a reusable helper should run the same database logic against different configured connections.

## Syntax

```ssl
SetDefaultConnection(sDefaultConnection)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sDefaultConnection` | [string](../types/string.md) | yes | — | Connection name to store as the new default connection |

## Returns

**[string](../types/string.md)** — The previous default connection name.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDefaultConnection` is [`NIL`](../literals/nil.md). | `Argument: sDefaultConnection cannot be null` |
| `sDefaultConnection` is not a string. | `Argument: sDefaultConnection must be a non-null string` |

## Best practices

!!! success "Do"
    - Save the current default with [`GetDefaultConnection`](GetDefaultConnection.md) before switching to another connection.
    - Restore the previous default in cleanup code when the connection change is temporary.
    - Treat the argument as a connection name only. Verify availability separately if your script depends on that connection being usable.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md), numbers, arrays, or objects. The function only accepts non-null strings.
    - Assume this function confirms that the target connection exists or is currently connected. It only stores the supplied string.
    - Change the default connection in shared workflow code without restoring the previous value when later steps depend on the original default.

## Caveats

- An empty string is accepted because it is still a string.
- Later database operations that rely on the default connection may fail if the stored value is not usable.

## Examples

### Switch to a different connection and restore the original

Save the current default, switch to a named connection, confirm the switch, then restore the original value.

```ssl
:PROCEDURE UseReportingConnection;
    :DECLARE sOriginalConnection, sPreviousConnection, sCurrentConnection;

    sOriginalConnection := GetDefaultConnection();

    sPreviousConnection := SetDefaultConnection("Reporting");
    sCurrentConnection := GetDefaultConnection();

    :IF sCurrentConnection == "Reporting";
        UsrMes("Previous default: " + sPreviousConnection);
    :ENDIF;

    SetDefaultConnection(sOriginalConnection);
:ENDPROC;

/* Usage;
DoProc("UseReportingConnection");
```

### Run a query on a temporary default connection using [`:FINALLY`](../keywords/FINALLY.md)

Use [`:FINALLY`](../keywords/FINALLY.md) to guarantee the original connection is restored even when the query raises an exception.

```ssl
:PROCEDURE LoadLoggedOrders;
    :DECLARE sOriginalConnection, sOrdersXml, oErr;

    sOriginalConnection := GetDefaultConnection();

    :TRY;
        SetDefaultConnection("Reporting");

        sOrdersXml := GetDataSet("
            SELECT ordno, status
            FROM orders
            WHERE status = 'Logged'
        ");
        UsrMes("Returned XML length: " + LimsString(Len(sOrdersXml)));
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes(oErr:Description);  /* Displays on failure: database error;
    :FINALLY;
        SetDefaultConnection(sOriginalConnection);
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("LoadLoggedOrders");
```

### Iterate over multiple connections and restore the original

Loop over a list of connection names, run the same count query against each, then restore the original connection in [`:FINALLY`](../keywords/FINALLY.md).

```ssl
:PROCEDURE ReportPendingTasksByConnection;
    :DECLARE aConnections, sOriginalConnection, sConnectionName, oErr;
    :DECLARE nPendingCount, nIndex;

    aConnections := {"LAB_A", "LAB_B", "LAB_C"};
    sOriginalConnection := GetDefaultConnection();

    :TRY;
        :FOR nIndex := 1 :TO ALen(aConnections);
            sConnectionName := aConnections[nIndex];
            SetDefaultConnection(sConnectionName);

            nPendingCount := LSearch("
                SELECT COUNT(*)
                FROM ordtask
                WHERE status = ?
            ",
                0,, {"Pending"});

            UsrMes(sConnectionName + ": " + LimsString(nPendingCount));
        :NEXT;
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes(oErr:Description);  /* Displays on failure: database error;
    :FINALLY;
        SetDefaultConnection(sOriginalConnection);
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ReportPendingTasksByConnection");
```

## Related

- [`GetDefaultConnection`](GetDefaultConnection.md)
- [`GetConnectionStrings`](GetConnectionStrings.md)
- [`LimsSqlConnect`](LimsSqlConnect.md)
- [`string`](../types/string.md)
