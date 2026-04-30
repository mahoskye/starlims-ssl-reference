---
title: "IgnoreSqlErrors"
summary: "Enables or disables SQL error suppression and returns the previous setting."
id: ssl.function.ignoresqlerrors
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# IgnoreSqlErrors

Enables or disables SQL error suppression and returns the previous setting.

`IgnoreSqlErrors(bEnable)` sets the current SQL error suppression flag to the boolean value you pass and returns the previous value. This makes it suitable for temporary changes around a specific block of database work, where you want best-effort SQL execution and then a clean restore of the earlier behavior.

## When to use

- When you are running best-effort cleanup where some SQL statements may fail and the rest of the work should continue.
- When you need to suppress SQL errors only for a short, controlled section of code and then restore the prior setting.
- When you are coordinating SQL error suppression with [`ShowSqlErrors`](ShowSqlErrors.md) for quieter maintenance or cleanup flows.

## Syntax

```ssl
IgnoreSqlErrors(bEnable)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `bEnable` | [boolean](../types/boolean.md) | yes | — | [`.T.`](../literals/true.md) enables SQL error suppression. [`.F.`](../literals/false.md) restores normal SQL error throwing. |

## Returns

**[boolean](../types/boolean.md)** — The previous SQL error suppression setting.

## Best practices

!!! success "Do"
    - Save the returned value and restore it after the temporary SQL work is complete.
    - Limit suppression to a small, clearly defined block of database operations.
    - Add a brief comment explaining why the SQL work is intentionally best-effort.

!!! failure "Don't"
    - Leave SQL error suppression enabled longer than necessary because later SQL failures can be hidden.
    - Use this as a default error-handling strategy because it can mask real database problems.
    - Change this flag without considering [`ShowSqlErrors`](ShowSqlErrors.md) when you need predictable SQL error visibility.

## Caveats

- The setting remains in effect for later SQL operations until you change it again.
- If you forget to restore the previous value, unrelated SQL work later in the same execution flow may continue with suppression still enabled.
- SQL error suppression is not a substitute for validation, transaction control, or explicit post-operation checks.
- This setting works together with [`ShowSqlErrors`](ShowSqlErrors.md); some SQL errors classified as fatal may still be raised when SQL error display is enabled.

## Examples

### Suppress errors for a batch of best-effort deletes

Shows the save-and-restore pattern: capture the previous value before enabling suppression, run best-effort deletes where any individual failure is intentionally ignored, then restore the original setting so later SQL operations are unaffected.

```ssl
:PROCEDURE CleanupOptionalAuditRows;
    :DECLARE bPrevIgnore, sSql, aSampleIds, nIndex;

    bPrevIgnore := IgnoreSqlErrors(.T.);

    sSql := "
        DELETE FROM sample_audit
        WHERE sample_id = ?
    ";
    aSampleIds := {"S-1001", "S-1002", "S-9999"};

    :FOR nIndex := 1 :TO ALen(aSampleIds);
        RunSQL(sSql,, {aSampleIds[nIndex]});
    :NEXT;

    IgnoreSqlErrors(bPrevIgnore);
:ENDPROC;

/* Usage;
DoProc("CleanupOptionalAuditRows");
```

### Restore the previous setting with [`:FINALLY`](../keywords/FINALLY.md)

Uses [`:FINALLY`](../keywords/FINALLY.md) to guarantee restoration even if the archive SQL throws. Capturing the return value before the [`:TRY`](../keywords/TRY.md) block and restoring it in [`:FINALLY`](../keywords/FINALLY.md) prevents the suppression flag from being stranded if an error escapes the block.

```ssl
:PROCEDURE ArchiveCompletedTasks;
    :DECLARE bPrevIgnore, sInsertSql, sDeleteSql, dCutoff;

    dCutoff := Today() - 30;
    bPrevIgnore := IgnoreSqlErrors(.T.);

    :TRY;
        sInsertSql := "
            INSERT INTO ordtask_archive
	            (ordno, testcode, status, logdate)
            SELECT ordno, testcode, status, logdate
            FROM ordtask
            WHERE status = ?
              AND logdate < ?
            ";
        RunSQL(sInsertSql,, {"Complete", dCutoff});

        sDeleteSql := "
            DELETE FROM ordtask
            WHERE status = ?
              AND logdate < ?
            ";
        RunSQL(sDeleteSql,, {"Complete", dCutoff});
    :FINALLY;
        IgnoreSqlErrors(bPrevIgnore);
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ArchiveCompletedTasks");
```

### Coordinate SQL suppression and error display together

Combines `IgnoreSqlErrors` with [`ShowSqlErrors`](ShowSqlErrors.md) to make a maintenance window fully quiet. Both settings are saved before the block and restored in [`:FINALLY`](../keywords/FINALLY.md) in reverse order, display restored first and then suppression, to match the reverse of how they were set.

```ssl
:PROCEDURE RunQuietMaintenance;
    :DECLARE bPrevIgnore, bPrevShow, sDeleteSql, sUpdateSql, dCutoff;

    dCutoff := Today() - 7;
    bPrevIgnore := IgnoreSqlErrors(.T.);
    bPrevShow := ShowSqlErrors(.F.);

    :TRY;
        sDeleteSql := "
            DELETE FROM temp_results
            WHERE logdate < ?
            ";
        RunSQL(sDeleteSql,, {dCutoff});

        sUpdateSql := "
            UPDATE batch_queue SET
                status = ?
            WHERE status = ?
              AND startdate < ?
            ";
        RunSQL(sUpdateSql,, {"Expired", "Pending", dCutoff});
    :FINALLY;
        ShowSqlErrors(bPrevShow);
        IgnoreSqlErrors(bPrevIgnore);
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("RunQuietMaintenance");
```

## Related

- [`SetSqlTimeout`](SetSqlTimeout.md)
- [`ShowSqlErrors`](ShowSqlErrors.md)
- [`boolean`](../types/boolean.md)
