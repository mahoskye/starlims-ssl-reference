---
title: "GetDBMSName"
summary: "Returns the DBMS platform name for a configured database connection."
id: ssl.function.getdbmsname
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetDBMSName

Returns the DBMS platform name for a configured database connection.

Returns `"SQL"` for SQL Server connections and `"ORACLE"` for Oracle connections, for the connection identified by `sConnectionName`. If `sConnectionName` is omitted or [`NIL`](../literals/nil.md), the function uses the default connection. If the name does not match any configured connection, or if the internal database collection is unavailable, the function raises an error.

## When to use

- When you need to branch on database platform to generate compatible SQL.
- When validating that a connection is backed by an expected DBMS before running platform-specific logic.
- When auditing all configured connections to confirm their platforms.

## Syntax

```ssl
GetDBMSName(sConnectionName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sConnectionName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Connection name to look up. If omitted or [`NIL`](../literals/nil.md), the default connection is used. |

## Returns

**[string](../types/string.md)** — The DBMS platform identifier for the specified connection: `"SQL"` for SQL Server connections and `"ORACLE"` for Oracle connections.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sConnectionName` names an unknown connection. | `The provider name: {sConnectionName} not found.` |
| The internal database collection is unavailable. | `The internal database collection is null` |

## Best practices

!!! success "Do"
    - Pass `sConnectionName` explicitly in scripts that run against multiple environments.
    - Use the returned value to branch SQL logic rather than hard-coding platform assumptions.
    - Pair with [`GetDBMSProviderName`](GetDBMSProviderName.md) when you also need the provider string.

!!! failure "Don't"
    - Assume the default connection is always the intended target in scripted workflows.
    - Expect this function to return provider connection details or schema information; it returns only the platform name.

## Caveats

- In multi-database environments, always pass `sConnectionName` explicitly — the default connection may not be the intended target.
- The returned platform string depends on system configuration and may vary between environments.

## Examples

### Get the platform name for a connection

Calls `GetDBMSName` with an explicit connection name and displays the result in a message.

```ssl
:PROCEDURE ShowDatabaseType;
	:DECLARE sDBMSName;

	sDBMSName := GetDBMSName("LIMSDB");

	UsrMes("DBMS: " + sDBMSName);
:ENDPROC;

/* Usage;
DoProc("ShowDatabaseType");
```

[`UsrMes`](UsrMes.md) displays:

```text
DBMS: SQL
```

### Branch SQL logic by database platform

Reads the DBMS name for a given connection and selects the appropriate SQL syntax for row limiting and current-date expressions.

```ssl
:PROCEDURE BuildQueryByDBMS;
	:PARAMETERS sConnectionName;
	:DECLARE sDBMSName, sLimitClause, sDateFunction, sQuery;

	sDBMSName := GetDBMSName(sConnectionName);

	:BEGINCASE;
	:CASE sDBMSName == "SQL";
		sLimitClause := "TOP 10";
		sDateFunction := "GETDATE()";
		:EXITCASE;
	:CASE sDBMSName == "ORACLE";
		sLimitClause := "ROWNUM <= 10";
		sDateFunction := "SYSDATE";
		:EXITCASE;
	:OTHERWISE;
		sLimitClause := "1 = 1";
		sDateFunction := "CURRENT_DATE";
		:EXITCASE;
	:ENDCASE;

	sQuery := "SELECT sample_id FROM samples WHERE " + sLimitClause
			  + " AND created_date > " + sDateFunction;

	:RETURN sQuery;
:ENDPROC;

/* Usage;
DoProc("BuildQueryByDBMS", {"REPORTING"});
```

### Audit all configured connections for their platform

Iterates every connection returned by [`GetConnectionStrings`](GetConnectionStrings.md), calls `GetDBMSName` for each, and reports the platform or an error message when a connection cannot be resolved.

```ssl
:PROCEDURE AuditDatabasePlatforms;
	:DECLARE aConnections, nIndex, sConnName, sDBMSName, oErr;

	aConnections := GetConnectionStrings();

	:FOR nIndex := 1 :TO ALen(aConnections);
		sConnName := aConnections[nIndex, 1];

		:TRY;
			sDBMSName := GetDBMSName(sConnName);
			UsrMes(sConnName + ": " + sDBMSName);
			/* Displays the connection name and DBMS platform;
		:CATCH;
			oErr := GetLastSSLError();
			UsrMes(sConnName + ": ERROR - " + oErr:Description);
			/* Displays an error for an unresolved connection;
		:ENDTRY;
	:NEXT;
:ENDPROC;

/* Usage;
DoProc("AuditDatabasePlatforms");
```

## Related

- [`GetDBMSProviderName`](GetDBMSProviderName.md)
- [`GetConnectionByName`](GetConnectionByName.md)
- [`GetConnectionStrings`](GetConnectionStrings.md)
- [`GetTables`](GetTables.md)
- [`string`](../types/string.md)
