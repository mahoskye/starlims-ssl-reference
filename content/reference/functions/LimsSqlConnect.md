---
title: "LimsSqlConnect"
summary: "Registers a configured database connection by connection name."
id: ssl.function.limssqlconnect
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LimsSqlConnect

Registers a configured database connection by connection name.

`LimsSqlConnect` looks up a configured connection name and adds it to the active
connection set so later database calls can target it by name. It returns [`.T.`](../literals/true.md)
when the registration succeeds and [`.F.`](../literals/false.md) when the name cannot be registered.

If the runtime supplies a null connection name, SSL substitutes the current default connection name before attempting the lookup. That fallback is only a name substitution; the call still returns [`.F.`](../literals/false.md) if the resolved name is not configured or cannot be registered.

This function does not change the default connection by itself. Use [`SetDefaultConnection`](SetDefaultConnection.md) separately when you want later database calls to use a different default connection.

Use [`GetConnectionByName`](GetConnectionByName.md) when you need a [`SQLConnection`](../classes/SQLConnection.md) object with readable connection metadata such as `DataSource`, `DatabaseName`, or `UseUTC`.

## When to use

- When you want to make a configured connection available by connection name.
- When a script needs to work with more than one configured database connection.
- When you plan to pass `sConnectionName` to functions such as [`SQLExecute`](SQLExecute.md) or [`RunSQL`](RunSQL.md) instead of relying on the current default connection.

## Syntax

```ssl
LimsSqlConnect(sConnectionName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sConnectionName` | [string](../types/string.md) | yes | — | Connection name of the configured connection to register. If the runtime supplies a null value, SSL substitutes the current default connection name before lookup. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) if the connection name was registered successfully; otherwise [`.F.`](../literals/false.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| The connection registration step throws an internal error. | `AddConnection throws an exception <message>` |

## Best practices

!!! success "Do"
    - Validate that the connection name exists in configuration before calling the function.
    - Check the boolean return value before running SQL against that connection name.
    - Disconnect with [`LimsSqlDisconnect`](LimsSqlDisconnect.md) when the named connection is no longer needed.

!!! failure "Don't"
    - Assume `LimsSqlConnect` changes the default connection. It only registers the named connection.
    - Treat [`.F.`](../literals/false.md) as an exception-only case. Unknown names and unavailable tenant-specific names can fail by returning [`.F.`](../literals/false.md).
    - Re-register the same connection name without a reason. A later registration replaces the existing named entry.

## Caveats

- If `sConnectionName` does not match a configured connection name, the function returns [`.F.`](../literals/false.md).
- If the name is tenant-specific and the current tenant context is missing or does not match the tenant encoded in the name, the function returns [`.F.`](../literals/false.md).
- If the runtime has not initialized the active connection collection, the function returns [`.F.`](../literals/false.md).
- Re-registering an existing connection name replaces the currently registered entry for that name.

## Examples

### Register a connection and confirm it is available

Call `LimsSqlConnect` with a configured connection name and branch on the boolean result to confirm availability before issuing queries.

```ssl
:PROCEDURE ConnectToSampleDb;
    :DECLARE sConnectionName, bConnected, sMessage;

    sConnectionName := "SampleDB";
    bConnected := LimsSqlConnect(sConnectionName);

    :IF bConnected;
        sMessage := sConnectionName + " is ready for database calls";
    :ELSE;
        sMessage := "Could not register connection " + sConnectionName;
    :ENDIF;

    UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("ConnectToSampleDb");
```

### Register two connections and target each one explicitly

Register two named connections and pass each connection name to subsequent [`SQLExecute`](SQLExecute.md) and [`RunSQL`](RunSQL.md) calls to target distinct databases in a single procedure.

```ssl
:PROCEDURE SyncBatchAcrossSystems;
    :DECLARE sLabName, sInvName, sBatchId, sSql;
    :DECLARE bLabReady, bInvReady, aPending, nPending;

    sLabName := "LabSystem";
    sInvName := "InventoryDB";
    sBatchId := "BATCH-1001";

    bLabReady := LimsSqlConnect(sLabName);
    bInvReady := LimsSqlConnect(sInvName);

    :IF !bLabReady .OR. !bInvReady;
        ErrorMes("Required named connections are not available");
        :RETURN .F.;
    :ENDIF;

    sSql := "
        SELECT sample_id, sample_name
        FROM samples
        WHERE status = 'PENDING'
    ";
    aPending := SQLExecute(sSql, sLabName);
    nPending := ALen(aPending);

    :IF nPending > 0;
        sSql := "
            UPDATE sync_audit SET
                batch_id = ?,
                sample_count = ?
            WHERE system_name = ?
        ";
        RunSQL(sSql, sInvName, {sBatchId, nPending, "LAB"});
    :ENDIF;

    LimsSqlDisconnect(sLabName);
    LimsSqlDisconnect(sInvName);

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("SyncBatchAcrossSystems");
```

### Distinguish [`.F.`](../literals/false.md) returns from thrown errors

Wrap `LimsSqlConnect` in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) to separate the normal [`.F.`](../literals/false.md) return (unknown connection name) from an internal error that propagates as an exception.

```ssl
:PROCEDURE TestConnectionRegistration;
    :DECLARE sConnectionName, bConnected, oErr;

    sConnectionName := "MissingConnection";

    :TRY;
        bConnected := LimsSqlConnect(sConnectionName);

        :IF !bConnected;
            UsrMes("Connection name is not available: " + sConnectionName);
            /* Displays when the connection name is unavailable;
            :RETURN .F.;
        :ENDIF;

        :IF IsDBConnected(sConnectionName);
            UsrMes("Connection registered successfully: " + sConnectionName);
            /* Displays when registration succeeds;
        :ENDIF;

    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("Connection registration failed: " + oErr:Description);
        /* Displays on failure: connection registration failed;
        :RETURN .F.;
    :ENDTRY;

    LimsSqlDisconnect(sConnectionName);

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("TestConnectionRegistration");
```

## Related

- [`CreateORMSession`](CreateORMSession.md)
- [`GetConnectionByName`](GetConnectionByName.md)
- [`GetConnectionStrings`](GetConnectionStrings.md)
- [`GetDefaultConnection`](GetDefaultConnection.md)
- [`IsDBConnected`](IsDBConnected.md)
- [`LimsSqlDisconnect`](LimsSqlDisconnect.md)
- [`SetDefaultConnection`](SetDefaultConnection.md)
- [`SQLConnection`](../classes/SQLConnection.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
