---
title: "GetConnectionStrings"
summary: "Retrieves all configured database connections as a two-dimensional array."
id: ssl.function.getconnectionstrings
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetConnectionStrings

Retrieves all configured database connections as a two-dimensional [array](../types/array.md).

Returns a 2D [array](../types/array.md) where each row represents one configured database connection. Column 1 is the connection name, column 2 is the provider name, and column 3 is the full connection string. If no connections are configured, the function returns an empty array. It never raises an exception.

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
the connection name, the provider name, and the full connection string.

## Best practices

!!! success "Do"
    - Check for an empty array before iterating.
    - Treat the returned array as a snapshot. Re-call the function if you need fresh data.

!!! failure "Don't"
    - Assume the array always has at least one row. The system may have no connections configured.
    - Assume column order. Column 1 is the name, column 2 the provider, and column 3 the connection string. Always access by index in that order.

## Examples

### List all connection names

Iterate the returned array and print each connection name. The loop runs once per configured connection. If no connections exist, nothing is printed.

```ssl
:PROCEDURE ListConnectionNames;
    :DECLARE aConnections, nIndex;

    aConnections := GetConnectionStrings();

    :FOR nIndex := 1 :TO ALen(aConnections);
        UsrMes(aConnections[nIndex, 1]); /* Displays each connection name;
    :NEXT;
:ENDPROC;

/* Usage:
DoProc("ListConnectionNames");
;
```

### Find a connection entry by name

Search the connection list for a specific name and display its provider when found. Returns [`.T.`](../literals/true.md) if the name was found, [`.F.`](../literals/false.md) otherwise.

```ssl
:PROCEDURE FindConnection;
    :PARAMETERS sTarget;
    :DECLARE aConnections, nIndex;

    aConnections := GetConnectionStrings();

    :FOR nIndex := 1 :TO ALen(aConnections);
        :IF aConnections[nIndex, 1] == sTarget;
            UsrMes("Provider: " + aConnections[nIndex, 2]); /* Displays the matching provider;
            :RETURN .T.;
        :ENDIF;
    :NEXT;

    :RETURN .F.;
:ENDPROC;

/* Usage:
DoProc("FindConnection", {"LIMS"});
;
```

## Related

- [`GetConnectionByName`](GetConnectionByName.md)
- [`GetDefaultConnection`](GetDefaultConnection.md)
- [`LimsSqlConnect`](LimsSqlConnect.md)
- [`LimsSqlDisconnect`](LimsSqlDisconnect.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
