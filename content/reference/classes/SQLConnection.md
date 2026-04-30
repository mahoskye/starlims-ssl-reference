---
title: "SQLConnection"
summary: "Represents a configured database connection returned by GetConnectionByName."
id: ssl.class.sqlconnection
element_type: class
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SQLConnection

Represents a configured database connection returned by [`GetConnectionByName`](../functions/GetConnectionByName.md).

`SQLConnection` exposes connection metadata such as the data source, database name, user name, platform, connection string, and UTC setting. SSL code normally receives this object from [`GetConnectionByName`](../functions/GetConnectionByName.md) and reads its members with colon-property syntax such as `oConn:DataSource`.

## When to use

- When you need to inspect which configured database connection a script is using.
- When a function accepts either a connection name or a connection object.
- When diagnostic or routing logic needs the connection platform, database name, or data source.

## Constructors

`SQLConnection` does not expose a documented SSL constructor. Use [`GetConnectionByName`](../functions/GetConnectionByName.md) to retrieve one for a configured connection.

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `DataSource` | [string](../types/string.md) | read-only | Server, DSN, or data source name from the connection string. |
| `DatabaseName` | [string](../types/string.md) | read-only | Database name for SQL Server connections. Oracle connections return `"Not Set"`. |
| `UserId` | [string](../types/string.md) | read-only | User name from the connection string. |
| `Password` | [string](../types/string.md) | read-only | Password from the connection string. |
| `Platforma` | [string](../types/string.md) | read-only | Database platform name, such as `"Microsoft SQL Server"`. |
| `ConnectionString` | [string](../types/string.md) | read-only | Full connection string for the connection. |
| `UseUTC` | [boolean](../types/boolean.md) | read-only | Whether the connection uses UTC timestamps. |

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Use [`GetConnectionByName`](../functions/GetConnectionByName.md) when you need a `SQLConnection` object.
    - Read `DataSource`, `DatabaseName`, or `Platforma` for diagnostics instead of parsing the connection string yourself.
    - Treat `UseUTC` as connection metadata when formatting or comparing timestamp values.

!!! failure "Don't"
    - Display, log, or return `Password` or `ConnectionString` in user-facing messages.
    - Assume `DatabaseName` is populated for every platform. Oracle connections return `"Not Set"`.

## Caveats

- `Password` and `ConnectionString` can expose sensitive credentials. Avoid writing them to logs, UI messages, audit tables, or error details.
- `DatabaseName` is only extracted for SQL Server connections. Other platforms may report `"Not Set"`.
- Property names are available through standard SSL colon-property access, for example `oConn:Platforma`.

## Examples

### Inspect a configured connection

Retrieves a configured connection and displays non-sensitive metadata.

```ssl
:PROCEDURE ShowConnectionInfo;
    :DECLARE oConn, sMessage;

    oConn := GetConnectionByName("LIMS");

    sMessage := "Database: " + oConn:DatabaseName;
    sMessage := sMessage + ", platform: " + oConn:Platforma;
    sMessage := sMessage + ", data source: " + oConn:DataSource;

    UsrMes(sMessage);

    :RETURN oConn;
:ENDPROC;

/* Usage;
DoProc("ShowConnectionInfo");
```

### Check UTC behavior for a connection

Uses the `UseUTC` property to branch timestamp-handling logic.

```ssl
:PROCEDURE DescribeConnectionTimeMode;
    :DECLARE oConn, sMode;

    oConn := GetConnectionByName("LIMS");

    :IF oConn:UseUTC;
        sMode := "Connection uses UTC timestamps";
    :ELSE;
        sMode := "Connection uses local timestamps";
    :ENDIF;

    UsrMes(sMode);

    :RETURN sMode;
:ENDPROC;

/* Usage;
DoProc("DescribeConnectionTimeMode");
```

## Related

- [`GetConnectionByName`](../functions/GetConnectionByName.md)
- [`LimsSqlConnect`](../functions/LimsSqlConnect.md)
- [`IsInTransaction`](../functions/IsInTransaction.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
- [`object`](../types/object.md)
