---
title: "DetectSqlInjections"
summary: "Enables or disables SQL injection detection for a database connection and returns the previous setting."
id: ssl.function.detectsqlinjections
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DetectSqlInjections

Enables or disables SQL injection detection for a database connection and returns the previous setting.

`DetectSqlInjections` changes the SQL injection detection flag on a specific database connection and returns the flag's earlier value. Pass [`.T.`](../literals/true.md) to enable detection or [`.F.`](../literals/false.md) to disable it. If `sConnectionName` is omitted, empty, or not a string, the function targets the current default connection. If `bEnable` is not a boolean value, the function treats it as enabled.

The change applies immediately to the selected connection. The return value is the prior state, which makes it useful for temporary changes that need to be restored later.

When detection is enabled, later SQL sent through that connection is checked for SQL comments and misplaced semicolons. `CREATE ...` statements are excluded from that semicolon check.

## When to use

- When a script needs to enforce SQL injection detection on a known connection before running database work.
- When you need to temporarily disable detection for a controlled scenario and then restore the prior setting.
- When you want to audit or normalize detection settings across several configured connections.

## Syntax

```ssl
DetectSqlInjections(bEnable, [sConnectionName])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `bEnable` | [boolean](../types/boolean.md) | yes | — | The requested detection state. Pass [`.T.`](../literals/true.md) to enable detection or [`.F.`](../literals/false.md) to disable it. If a non-boolean value is supplied, the function behaves as if [`.T.`](../literals/true.md) was passed. |
| `sConnectionName` | [string](../types/string.md) | no | current default connection | The database connection to update. If omitted, empty, or not a string, the function uses the default connection. |

## Returns

**[boolean](../types/boolean.md)** — The SQL injection detection state that was in effect before this call.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sConnectionName` names an unknown connection. `{sConnectionName}` is replaced with the actual connection name value. | `The provider name: {sConnectionName} not found.` |

## Best practices

!!! success "Do"
    - Pass an explicit [`.T.`](../literals/true.md) or [`.F.`](../literals/false.md) for `bEnable`.
    - Store the returned value when you plan to restore the original setting later.
    - Pass a specific `sConnectionName` when a script should not depend on the current default connection.

!!! failure "Don't"
    - Rely on non-boolean values for `bEnable`. They are treated as enabled, which can hide mistakes.
    - Pass an unvalidated or unintended connection name in security-sensitive code.
    - Assume the return value is the new state. It reports the previous state only.

## Caveats

- A non-string `sConnectionName` does not raise a type error. It causes the function to use the default connection instead.
- A non-boolean `bEnable` does not raise a type error. It enables detection.
- The function changes connection state immediately, so disabling detection should be limited to tightly controlled cases.
- When detection is enabled, later SQL on that connection rejects SQL comments and raises `Invalid SQL statement: remove the comments.` if comments are present.
- When detection is enabled, later non-`CREATE` SQL on that connection rejects misplaced semicolons and raises `Invalid SQL statement: remove any misplaced semicolons ( ; )` when they are found outside quoted strings.

## Examples

### Enable detection for a named connection

Enables SQL injection detection on a named connection and reports whether detection was already active.

```ssl
:PROCEDURE EnableDetection;
    :DECLARE sConnectionName, bPreviousState, sMessage;

    sConnectionName := "LABDATA";
    bPreviousState := DetectSqlInjections(.T., sConnectionName);

    :IF bPreviousState;
        sMessage := "SQL injection detection was already enabled for "
		            + sConnectionName;

    :ELSE;
        sMessage := "SQL injection detection is now enabled for "
		            + sConnectionName;
    :ENDIF;

    UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("EnableDetection");
```

`UsrMes` displays one of:

```text
SQL injection detection was already enabled for LABDATA
SQL injection detection is now enabled for LABDATA
```

### Temporarily disable detection and restore it

Disables SQL injection detection before running a controlled query, then restores the prior setting in a [`:FINALLY`](../keywords/FINALLY.md) block even if the query fails.

```ssl
:PROCEDURE RunControlledQuery;
    :DECLARE sConnectionName, bPreviousState, aRows, sSQL, oErr;

    sConnectionName := "LABDATA";
    bPreviousState := DetectSqlInjections(.F., sConnectionName);

    :TRY;
        sSQL := "
                SELECT sampleid, status
                FROM sample
                WHERE status = 'A'
            ";

        aRows := SQLExecute(sSQL, sConnectionName);

        UsrMes("Rows returned: " + LimsString(ALen(aRows)));
        /* Displays: Rows returned: N;

    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("Controlled query failed: " + oErr:Description);
        /* Displays on failure: Controlled query failed;

    :FINALLY;
        DetectSqlInjections(bPreviousState, sConnectionName);
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("RunControlledQuery");
```

### Normalize detection across multiple connections

Enables SQL injection detection on each connection in a list and tracks which ones were changed from their previous state.

```ssl
:PROCEDURE NormalizeDetectionSettings;
    :DECLARE aConnections, sConnectionName, aChanged, bPreviousState, nIndex;

    aConnections := {"LIMS", "LABDATA", "REPORTING"};
    aChanged := {};

    :FOR nIndex := 1 :TO ALen(aConnections);
        sConnectionName := aConnections[nIndex];
        bPreviousState := DetectSqlInjections(.T., sConnectionName);

        :IF !bPreviousState;
            AAdd(aChanged, sConnectionName);
        :ENDIF;
    :NEXT;

    UsrMes("Connections changed: " + LimsString(ALen(aChanged)));
:ENDPROC;

/* Usage;
DoProc("NormalizeDetectionSettings");
```

[`UsrMes`](UsrMes.md) displays:

```text
Connections changed: 3
```

## Related

- [`GetNoLock`](GetNoLock.md)
- [`SetDefaultConnection`](SetDefaultConnection.md)
- [`SetSqlTimeout`](SetSqlTimeout.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
