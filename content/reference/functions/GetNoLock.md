---
title: "GetNoLock"
summary: "Returns the database-specific no-lock clause for a connection."
id: ssl.function.getnolock
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetNoLock

Returns the database-specific no-lock clause for a connection.

`GetNoLock` looks up the target database connection and returns the string you can insert after a table name when building SQL dynamically. For Oracle connections, it returns a single space because Oracle does not use this hint. For any non-Oracle connection, it returns ` WITH (NOLOCK) `.

If `sConnectionName` is omitted or empty, the function uses the current default connection. If the specified connection name, or the default connection, cannot be resolved, the function raises an error.

## When to use

- When building SQL dynamically and the statement must adapt to the current database platform.
- When you need to add a no-lock hint after a table name for non-Oracle connections.
- When shared SQL-building code runs against both Oracle and non-Oracle connections.

## Syntax

```ssl
GetNoLock([sConnectionName])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sConnectionName` | [string](../types/string.md) | no | current default connection | Connection name used to resolve the target database. When omitted or empty, the function uses the default connection. |

## Returns

**[string](../types/string.md)** — ` WITH (NOLOCK) ` for non-Oracle connections; a single space (` `) for Oracle connections.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| The specified connection name, or the default connection, cannot be resolved. | `The provider name: <sConnectionName> not found.` |

## Best practices

!!! success "Do"
    - Append the returned value immediately after the table name it applies to.
    - Use this helper instead of hardcoding `WITH (NOLOCK)` when the same code may run against different database platforms.
    - Restrict usage to queries where dirty reads are acceptable.

!!! failure "Don't"
    - Wrap the result in another `WITH (...)` clause. The returned string is already the full clause for non-Oracle connections.
    - Append it at the end of the statement or after `WHERE` or `GROUP BY`. It belongs after the table name.
    - Use it for queries that require fully consistent committed data.

## Caveats

- The function does not modify the SQL statement for you. You must place the returned text in a valid position in the SQL string.
- On non-Oracle connections, using `WITH (NOLOCK)` can expose uncommitted or inconsistent data.

## Examples

### Add the platform-specific clause after a table name

Gets the no-lock hint for a named connection and embeds it immediately after the table name in a dynamically built SQL string.

```ssl
:PROCEDURE LoadLoggedSamples;
    :DECLARE sSQL, sNoLock, aSamples;

    sNoLock := GetNoLock("LIMS");

    sSQL := "
        SELECT sample_id, status
        FROM sample
        " + sNoLock + "
        WHERE status = 'Logged'
        ORDER BY sample_id
    ";

    aSamples := SQLExecute(sSQL);

    :RETURN aSamples;
:ENDPROC;

/* Example call;
DoProc("LoadLoggedSamples");
```

### Use the default connection in a query builder

Omits `sConnectionName` so the function resolves against the current default connection, then uses the returned clause in a query builder that returns the assembled SQL string.

```ssl
:PROCEDURE BuildOpenTaskQuery;
    :DECLARE sNoLock, sSQL;

    sNoLock := GetNoLock();

    sSQL := "
        SELECT ordno, testcode, status
        FROM ordtask
        " + sNoLock + "
        WHERE status = 'Pending'
        ORDER BY ordno, testcode
    ";

    :RETURN sSQL;
:ENDPROC;

/* Example call;
DoProc("BuildOpenTaskQuery");
```

### Apply the clause across multiple joined tables

Retrieves the hint once and reuses the same value after each table name in a multi-join query, keeping the SQL consistent across all tables.

```ssl
:PROCEDURE LoadPendingResults;
    :DECLARE sConnection, sNoLock, sSQL, aRows;

    sConnection := "LIMS";
    sNoLock := GetNoLock(sConnection);

    sSQL := "
        SELECT o.ordno, t.testcode, r.result
        FROM orders o
        " + sNoLock + "
        INNER JOIN ordtask t
        " + sNoLock + "
          ON t.ordno = o.ordno
        INNER JOIN ordresult r
        " + sNoLock + "
          ON r.ordno = t.ordno
          AND r.testcode = t.testcode
        WHERE o.status = 'Pending'
        ORDER BY o.ordno, t.testcode
    ";

    aRows := SQLExecute(sSQL);

    :RETURN aRows;
:ENDPROC;

/* Example call;
DoProc("LoadPendingResults");
```

## Related

- [`AddColDelimiters`](AddColDelimiters.md)
- [`AddNameDelimiters`](AddNameDelimiters.md)
- [`GetRdbmsDelimiter`](GetRdbmsDelimiter.md)
- [`string`](../types/string.md)
