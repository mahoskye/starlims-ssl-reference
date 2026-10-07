---
title: "GetConnectionStrings"
summary: "Retrieves all configured database connections as a two-dimensional array."
id: ssl.function.getconnectionstrings
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# GetConnectionStrings

Retrieves all configured database connections as a two-dimensional [array](../types/array.md).

Returns a 2D [array](../types/array.md) where each row represents one configured database connection. Column 1 is the connection name, column 2 is the provider settings string, and column 3 is the full connection string. The provider settings string is a semicolon-separated list that starts with the platform name and the provider, for example `SQL;NATIVESQL;...;USEUTC`. If no connections are configured, the function returns an empty array. It never raises an exception.

## When to use

- When displaying or auditing all database connections configured in the application.
- When discovering which connections are available at runtime.
- When exporting or migrating connection configuration data.

## Syntax

```ssl
GetConnectionStrings()
```

## Parameters

This function takes no parameters.

## Returns

**[array](../types/array.md)** — Two-dimensional array of connections. Each row contains three strings:
the connection name, the provider settings string, and the full connection string.

## Best practices

!!! success "Do"
    - Check for an empty array before iterating.
    - Treat the returned array as a snapshot. Re-call the function if you need fresh data.
    - Read column 1 for the name, column 2 for the provider settings, and column 3 for the connection string.

!!! failure "Don't"
    - Assume the array always has at least one row. The system may have no connections configured.

## Examples

### List all connection names

Iterate the returned array and print each connection name. The loop runs once per configured connection. If no connections exist, nothing is printed.

```ssl
:PROCEDURE ListConnectionNames;
    :DECLARE aConnections, nIndex;

    aConnections := GetConnectionStrings();

    :FOR nIndex := 1 :TO ALen(aConnections);
        UsrMes(aConnections[nIndex, 1]); /* Logs each connection name;
    :NEXT;
:ENDPROC;

/* Usage;
DoProc("ListConnectionNames");
```

### Find a connection entry by name

Search the connection list for a specific name and display its provider settings when found. Returns [`.T.`](../literals/true.md) if the name was found, [`.F.`](../literals/false.md) otherwise.

```ssl
:PROCEDURE FindConnection;
    :PARAMETERS sTarget;
    :DECLARE aConnections, nIndex;

    aConnections := GetConnectionStrings();

    :FOR nIndex := 1 :TO ALen(aConnections);
        :IF aConnections[nIndex, 1] == sTarget;
            UsrMes("Provider settings: " + aConnections[nIndex, 2]); /* Logs the matching provider settings;
            :RETURN .T.;
        :ENDIF;
    :NEXT;

    :RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("FindConnection", {"DATABASE"});
```

## Related

- [`GetConnectionByName`](GetConnectionByName.md)
- [`GetDefaultConnection`](GetDefaultConnection.md)
- [`LimsSqlConnect`](LimsSqlConnect.md)
- [`LimsSqlDisconnect`](LimsSqlDisconnect.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
