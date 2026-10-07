---
title: "IgnoreSqlErrors"
summary: "Enables or disables SQL error suppression and returns the previous setting."
id: ssl.function.ignoresqlerrors
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# IgnoreSqlErrors

Enables or disables SQL error suppression and returns the previous setting.

`IgnoreSqlErrors(bEnable)` sets the current SQL error suppression flag to the boolean value you pass and returns the previous value. This makes it suitable for temporary changes around a specific block of database work, followed by a clean restore of the earlier behavior.

The flag starts at [`.T.`](../literals/true.md), so suppression is on by default. On its own it does not stop a failing [`RunSQL`](RunSQL.md) from raising: [`ShowSqlErrors`](ShowSqlErrors.md) decides that, and it also starts at [`.T.`](../literals/true.md). A failing `RunSQL` returns [`.F.`](../literals/false.md) only while `IgnoreSqlErrors` is [`.T.`](../literals/true.md) and `ShowSqlErrors` is [`.F.`](../literals/false.md). Setting `IgnoreSqlErrors(.F.)` makes failures raise whatever `ShowSqlErrors` is set to.

## When to use

- When a block of SQL work must raise on every failure, even if a caller has turned [`ShowSqlErrors`](ShowSqlErrors.md) off.
- When you turn [`ShowSqlErrors`](ShowSqlErrors.md) off for best-effort cleanup and want suppression on for that block, in case a caller turned it off.
- When you need to change the setting only for a short, controlled section of code and then restore the prior setting.

## Syntax

```ssl
IgnoreSqlErrors(bEnable)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `bEnable` | [boolean](../types/boolean.md) | yes | — | [`.T.`](../literals/true.md) (the starting value) enables SQL error suppression, which takes effect only while [`ShowSqlErrors`](ShowSqlErrors.md) is [`.F.`](../literals/false.md). [`.F.`](../literals/false.md) makes failing statements raise whatever `ShowSqlErrors` is set to. |

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
    - Expect `IgnoreSqlErrors(.T.)` alone to stop a failing [`RunSQL`](RunSQL.md) from raising. It is already on by default. [`ShowSqlErrors`](ShowSqlErrors.md) is the flag that decides.
    - Restore a hard-coded value instead of the saved one. A caller may have set the flag differently.

## Caveats

- The setting remains in effect for later SQL operations until you change it again.
- If you forget to restore the previous value, unrelated SQL work later in the same execution flow runs with a setting it did not expect.
- SQL error suppression is not a substitute for validation, transaction control, or explicit post-operation checks.
- Suppression takes effect only while [`ShowSqlErrors`](ShowSqlErrors.md) is [`.F.`](../literals/false.md). With `ShowSqlErrors` at its starting value of [`.T.`](../literals/true.md), a failing [`RunSQL`](RunSQL.md) raises whatever this flag is set to.

## Examples

### Suppress errors for a batch of best-effort deletes

Shows the save-and-restore pattern: capture both previous values, turn [`ShowSqlErrors`](ShowSqlErrors.md) off so each failing delete returns [`.F.`](../literals/false.md) instead of raising, log any failure from [`GetLastSQLError`](GetLastSQLError.md), then restore the original settings in [`:FINALLY`](../keywords/FINALLY.md) so later SQL operations are unaffected. `IgnoreSqlErrors(.T.)` keeps suppression on even if a caller turned it off.

```ssl
:PROCEDURE CleanupOptionalAuditRows;
    :DECLARE bPrevIgnore, bPrevShow, sSql, aSampleIds, nIndex, oSqlErr;

    sSql := "
        DELETE FROM sample_audit
        WHERE sample_id = ?
    ";
    aSampleIds := {"S-1001", "S-1002", "S-9999"};

    /* Audit rows are optional here, so one failed delete must not stop the rest;
    bPrevIgnore := IgnoreSqlErrors(.T.);
    bPrevShow := ShowSqlErrors(.F.);

    :TRY;
        :FOR nIndex := 1 :TO ALen(aSampleIds);
            :IF !RunSQL(sSql,, {aSampleIds[nIndex]});
                oSqlErr := GetLastSQLError();
                UsrMes("Skipped " + aSampleIds[nIndex] + ": " + oSqlErr:Description);
            :ENDIF;
        :NEXT;
    :FINALLY;
        ShowSqlErrors(bPrevShow);
        IgnoreSqlErrors(bPrevIgnore);
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("CleanupOptionalAuditRows");
```

### Force failures to raise and restore the setting with [`:FINALLY`](../keywords/FINALLY.md)

Sets `IgnoreSqlErrors(.F.)` so a failed archive insert raises even if a caller has turned [`ShowSqlErrors`](ShowSqlErrors.md) off. The delete then never runs after a failed copy. The previous value is captured before the [`:TRY`](../keywords/TRY.md) block and restored in [`:FINALLY`](../keywords/FINALLY.md), and [`:CATCH`](../keywords/CATCH.md) logs the failure.

```ssl
:PROCEDURE ArchiveCompletedTasks;
    :DECLARE bPrevIgnore, sInsertSql, sDeleteSql, dCutoff, oErr;

    dCutoff := Today() - 30;
    bPrevIgnore := IgnoreSqlErrors(.F.);

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
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("Task archive stopped: " + oErr:Description);
    :FINALLY;
        IgnoreSqlErrors(bPrevIgnore);
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ArchiveCompletedTasks");
```

### Coordinate SQL suppression and error display together

Combines `IgnoreSqlErrors` with [`ShowSqlErrors`](ShowSqlErrors.md) to make a maintenance window fully quiet: a failing statement returns [`.F.`](../literals/false.md) and the next one still runs. Both settings are saved before the block and restored in [`:FINALLY`](../keywords/FINALLY.md) in reverse order, display restored first and then suppression, to match the reverse of how they were set.

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
