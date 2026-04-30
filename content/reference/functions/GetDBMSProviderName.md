---
title: "GetDBMSProviderName"
summary: "Returns the uppercase DBMS provider identifier for a named database connection."
id: ssl.function.getdbmsprovidername
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetDBMSProviderName

Returns the uppercase DBMS provider identifier for a named database connection.

Returns a string such as `"SQLSERVER"` or `"ORACLE"` for the connection identified by `sConnectionName`. If `sConnectionName` is omitted, empty, or [`NIL`](../literals/nil.md), the function uses the default connection. If the name does not match any configured connection, or if the internal database collection is unavailable, the function raises an error; it never returns [`NIL`](../literals/nil.md) or an empty string for a failed lookup.

## When to use

- When code must branch on the provider identifier to select compatible drivers or features.
- When writing multi-database solutions that need to adapt logic per provider.
- When auditing or diagnosing which provider is configured for each connection.

## Syntax

```ssl
GetDBMSProviderName(sConnectionName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sConnectionName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Connection name to look up. If omitted, empty, or [`NIL`](../literals/nil.md), the default connection is used. |

## Returns

**[string](../types/string.md)** — The DBMS provider identifier in uppercase.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sConnectionName` does not match any configured connection. | `The provider name: {sConnectionName} not found.` |
| The internal database collection is unavailable. | `The internal database collection is null` |

## Best practices

!!! success "Do"
    - Wrap calls in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when `sConnectionName` comes from configuration or user input.
    - Use the returned identifier to branch logic rather than hard-coding provider assumptions.

!!! failure "Don't"
    - Check the return value for empty to detect a missing mapping; a missing mapping raises an error, not an empty return.
    - Use this function to check whether a database is accessible or healthy. Provider mapping existence does not mean the database is operational.

## Caveats

- Logical names are matched exactly; extra spaces or wrong case will fail the lookup and raise an error.

## Examples

### Get the provider identifier for a connection

Calls the function with an explicit connection name and displays the returned uppercase provider identifier.

```ssl
:PROCEDURE ShowProviderName;
    :DECLARE sProviderName;

    sProviderName := GetDBMSProviderName("LIMS");

    UsrMes("Provider: " + sProviderName);
:ENDPROC;

/* Usage;
DoProc("ShowProviderName");
```

[`UsrMes`](UsrMes.md) displays:

```text
Provider: SQLSERVER
```

### Handle an unknown connection name safely

Wraps the call in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) so an unknown connection name returns an empty string instead of propagating the exception to the caller.

```ssl
:PROCEDURE GetProviderSafe;
    :PARAMETERS sConnectionName;
    :DECLARE sProviderName;

    :TRY;
        sProviderName := GetDBMSProviderName(sConnectionName);
        UsrMes("Provider: " + sProviderName);
        :RETURN sProviderName;
    :CATCH;
        :RETURN "";
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("GetProviderSafe", {"LIMS"});
```

### Branch logic by provider identifier

Uses the returned identifier to select a provider-specific integration strategy, falling back to `"GENERIC"` when the connection is not found.

```ssl
:PROCEDURE AdaptIntegrationByProvider;
    :PARAMETERS sConnectionName;
    :DECLARE sProvider, sStrategy;

    :TRY;
        sProvider := GetDBMSProviderName(sConnectionName);
    :CATCH;
        :RETURN "GENERIC";
    :ENDTRY;

    :BEGINCASE;
    :CASE sProvider == "ORACLE";
        sStrategy := "ORACLE_SPECIFIC";
        :EXITCASE;
    :CASE sProvider == "SQLSERVER";
        sStrategy := "MSSQL_SPECIFIC";
        :EXITCASE;
    :CASE sProvider == "POSTGRESQL";
        sStrategy := "POSTGRES_SPECIFIC";
        :EXITCASE;
    :OTHERWISE;
        sStrategy := "GENERIC";
        :EXITCASE;
    :ENDCASE;

    :RETURN sStrategy;
:ENDPROC;

/* Usage;
DoProc("AdaptIntegrationByProvider", {"REPORTING"});
```

## Related

- [`GetDBMSName`](GetDBMSName.md)
- [`GetConnectionByName`](GetConnectionByName.md)
- [`GetConnectionStrings`](GetConnectionStrings.md)
- [`string`](../types/string.md)
