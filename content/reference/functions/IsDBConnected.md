---
title: "IsDBConnected"
summary: "Checks whether STARLIMS currently has a database connection available for a given connection name."
id: ssl.function.isdbconnected
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# IsDBConnected

Checks whether STARLIMS currently has a database connection available for a given connection name.

If you pass a connection name, the function checks that named connection. If you omit the argument or pass an empty string, it checks the current default connection instead. The function returns [`.T.`](../literals/true.md) when a matching connection is available and [`.F.`](../literals/false.md) when it is not. It does not run a test query or validate the target database beyond that connection lookup.

## When to use

- When you need to check whether the default database connection is available before running database work.
- When a script can target more than one configured connection and needs to verify a specific one by name.
- When you want a quick connection-availability check without executing SQL.
- When you need to branch between a fallback path and normal database processing.

## Syntax

```ssl
IsDBConnected([sConnectionName])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sConnectionName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Connection name of the database connection to check. If omitted or passed as an empty string, the function checks the current default connection. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) if the named connection exists, or if the default connection exists when no name is supplied; otherwise [`.F.`](../literals/false.md)

## Exceptions

| Trigger | Exception message |
| --- | --- |
| The runtime database collection has not been initialized. | `The internal database collection is null` |

## Best practices

!!! success "Do"
    - Use `IsDBConnected()` before database work when your script needs a fast availability check.
    - Pass an explicit connection name when your script works with more than one connection.

!!! failure "Don't"
    - Treat this as a connectivity probe that validates credentials, network reachability, or a successful round-trip query.
    - Pass an empty string when you mean to verify a specific non-default connection by name.
    - Assume the function always returns [`.F.`](../literals/false.md) on failure; it can raise an error when runtime database state is unavailable.

## Caveats

- If the connection name does not match a known connection, the function returns [`.F.`](../literals/false.md).
- If runtime database state is unavailable, the function raises an error instead of returning [`.F.`](../literals/false.md).
- Passing an empty string checks the default connection, which may not be the named connection you intended to inspect.

## Examples

### Guard a query with a default connection check

Check the default connection before executing a query, and exit early with a message when no connection is available. The success path shows that `IsDBConnected()` without an argument targets the default connection.

```ssl
:PROCEDURE CheckDbBeforeQuery;
    :DECLARE bIsConnected, aResults;

    bIsConnected := IsDBConnected();

    :IF !bIsConnected;
        UsrMes("Default database connection is not available");
        :RETURN .F.;
    :ENDIF;

    aResults := SQLExecute("SELECT COUNT(*) FROM sample");
    UsrMes("Sample count: " + LimsString(aResults[1, 1]));
    /* Logs the sample count when the query succeeds;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("CheckDbBeforeQuery");
```

### Check availability of multiple named connections

Iterate over a list of connection names and report each one's availability. Passing an explicit name to `IsDBConnected` lets you verify named connections independently of the current default.

```ssl
:PROCEDURE CheckMultiDatabaseConnections;
    :DECLARE aConnectionNames, sConnectionName, bIsConnected, sStatusMessage, nIndex;

    aConnectionNames := {"DATABASE", "DICTIONARY"};

    :FOR nIndex := 1 :TO ALen(aConnectionNames);
        sConnectionName := aConnectionNames[nIndex];
        bIsConnected := IsDBConnected(sConnectionName);

        :IF bIsConnected;
            sStatusMessage := sConnectionName + " is available";
        :ELSE;
            sStatusMessage := sConnectionName + " is not available";
        :ENDIF;

        UsrMes(sStatusMessage);
        /* Logs each connection's availability;
    :NEXT;
:ENDPROC;

/* Usage;
DoProc("CheckMultiDatabaseConnections");
```

### Check a caller-supplied connection name

Take the connection name as a parameter and branch on the result. A name that does not match a known connection returns [`.F.`](../literals/false.md) rather than raising, so the procedure can report it and return.

```ssl
:PROCEDURE CheckDatabaseConnectivity;
    :PARAMETERS sConnName;
    :DEFAULT sConnName, "";
    :DECLARE bIsConnected;

    bIsConnected := IsDBConnected(sConnName);

    :IF bIsConnected;
        UsrMes("Requested connection is available");
    :ELSE;
        UsrMes("Requested connection is not available");
    :ENDIF;

    :RETURN bIsConnected;
:ENDPROC;

/* Usage;
DoProc("CheckDatabaseConnectivity", {"DATABASE"});
```

## Related

- [`GetDefaultConnection`](GetDefaultConnection.md)
- [`LimsSqlConnect`](LimsSqlConnect.md)
- [`LimsSqlDisconnect`](LimsSqlDisconnect.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
