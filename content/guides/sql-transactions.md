# SQL and Transaction Management

SSL provides explicit transaction control for database operations. Understanding the transaction model — especially nested transaction behavior and rollback semantics — is essential for writing reliable data modification code.

## Transaction basics

### Starting and ending transactions

Place [`BeginLimsTransaction`](../reference/functions/BeginLimsTransaction.md) inside the [`:TRY`](../reference/keywords/TRY.md) block so that a connection failure is caught cleanly. Store its return value in a `bStarted` flag and check that flag in [`:FINALLY`](../reference/keywords/FINALLY.md), so the code calls [`EndLimsTransaction`](../reference/functions/EndLimsTransaction.md) only for a transaction it began.

```ssl
:DECLARE bStarted, bCommit, oError;
bStarted := .F.;
bCommit := .F.;

:TRY;
    bStarted := BeginLimsTransaction();

    RunSQL("INSERT INTO samples (sample_id, status) VALUES ('S-001', 'A')");
    RunSQL("UPDATE batch SET sample_count = sample_count + 1");

    bCommit := .T.;
:CATCH;
    oError := GetLastSSLError();
    ErrorMes("DB ERROR", "Transaction failed: " + oError:Description);
:FINALLY;
    :IF bStarted;
        EndLimsTransaction(, bCommit);
    :ENDIF;
:ENDTRY;
```

!!! tip "Why BeginLimsTransaction belongs inside :TRY"
    If [`BeginLimsTransaction`](../reference/functions/BeginLimsTransaction.md) raises an error, for example on a connection failure, the [`:CATCH`](../reference/keywords/CATCH.md) handles it and `bStarted` stays [`.F.`](../reference/literals/false.md), so the [`:FINALLY`](../reference/keywords/FINALLY.md) does not try to end anything.

!!! warning "End only a transaction you began"
    [`EndLimsTransaction`](../reference/functions/EndLimsTransaction.md) does not raise an error when there is nothing for it to end: with no transaction open, it returns [`.T.`](../reference/literals/true.md) silently. The real danger is ending a transaction your routine did not begin. When a caller has a transaction open, a helper that never began one but calls `EndLimsTransaction()` in its [`:FINALLY`](../reference/keywords/FINALLY.md) ends the **caller's** transaction and, with `bCommit` omitted, commits it. The caller's later rollback then has nothing to roll back. An [`IsInTransaction`](../reference/functions/IsInTransaction.md) check in the helper does not prevent this, because it returns [`.T.`](../reference/literals/true.md) for the caller's transaction too. Track ownership with a `bStarted` flag set from [`BeginLimsTransaction`](../reference/functions/BeginLimsTransaction.md), and pass `bCommit` explicitly.

| Function | Purpose |
|----------|---------|
| [`BeginLimsTransaction`](../reference/functions/BeginLimsTransaction.md) | Opens a transaction (optional: connection name, isolation level) |
| [`EndLimsTransaction`](../reference/functions/EndLimsTransaction.md) | Commits ([`.T.`](../reference/literals/true.md)) or rolls back ([`.F.`](../reference/literals/false.md)) the transaction |
| [`IsInTransaction`](../reference/functions/IsInTransaction.md) | Returns [`.T.`](../reference/literals/true.md) if a transaction is currently active |
| [`GetTransactionsCount`](../reference/functions/GetTransactionsCount.md) | Returns the current nesting depth |

### EndLimsTransaction parameters

```ssl
EndLimsTransaction(sConnectionName, bCommit);
```

- **sConnectionName** — database connection name; omit for the default connection
- **bCommit** — [`.T.`](../reference/literals/true.md) to commit, [`.F.`](../reference/literals/false.md) to rollback

Omitting the first argument uses the default connection:

```ssl
EndLimsTransaction(, .T.);    /* commit on default connection;
EndLimsTransaction(, .F.);    /* rollback on default connection;
```

## Nested transactions

SSL supports nested [`BeginLimsTransaction`](../reference/functions/BeginLimsTransaction.md) calls. Transactions are **reference-counted**: only the **outermost** Begin/End pair actually starts and commits or rolls back the database transaction. Inner calls increment and decrement a counter. Each level needs its own End, so the example tracks both levels: after a failure between the inner Begin and End, two levels are still open.

```ssl
:DECLARE bOuter, bInner, bCommit, oError;
bOuter := .F.;
bInner := .F.;
bCommit := .F.;

:TRY;
    bOuter := BeginLimsTransaction();    /* count = 1, DB transaction starts;

    bInner := BeginLimsTransaction();    /* count = 2, no new DB transaction;
    RunSQL(sInnerSQL);
    EndLimsTransaction(, .T.);           /* count = 1, nothing committed yet;
    bInner := .F.;

    RunSQL(sOuterSQL);
    bCommit := .T.;
:CATCH;
    oError := GetLastSSLError();
    ErrorMes("ERROR", oError:Description);
:FINALLY;
    :IF bInner;
        EndLimsTransaction(, .F.);       /* inner level still open after a failure;
    :ENDIF;

    :IF bOuter;
        EndLimsTransaction(, bCommit);   /* count = 0, commits or rolls back;
    :ENDIF;
:ENDTRY;
```

### Inner rollback poisons the outer transaction

This is the most critical behavior to understand: **if any inner transaction is rolled back, the outer transaction cannot commit**.

```ssl
:DECLARE bOuter, bInner, oError;
bOuter := .F.;
bInner := .F.;

:TRY;
    bOuter := BeginLimsTransaction();

    bInner := BeginLimsTransaction();
    RunSQL(sInsertSQL);
    EndLimsTransaction(, .F.);           /* inner rollback, sets the poison flag;
    bInner := .F.;

    RunSQL(sUpdateSQL);

    bOuter := .F.;
    EndLimsTransaction(, .T.);           /* raises the cannot-commit error and rolls back;
:CATCH;
    oError := GetLastSSLError();
    ErrorMes("ERROR", oError:Description);
:FINALLY;
    :IF bInner;
        EndLimsTransaction(, .F.);
    :ENDIF;

    :IF bOuter;
        EndLimsTransaction(, .F.);
    :ENDIF;
:ENDTRY;
```

The outermost `EndLimsTransaction(, .T.)` finishes the outer level whether it commits or raises, so `bOuter` is cleared just before it and `:FINALLY` does not end the level a second time.

When an inner `EndLimsTransaction(, .F.)` is called:

1. The nesting counter decrements but the DB transaction stays open
2. An internal rollback flag is set
3. When the outermost `EndLimsTransaction(, .T.)` runs, it sees the flag
4. It **rolls back** instead of committing
5. It **throws an exception** — "Cannot commit the outermost transaction because one of the inner transactions was rollbacked!"

!!! danger "Always handle the poisoned-transaction exception"
    If you call `EndLimsTransaction(, .T.)` on an outer transaction where an inner transaction was rolled back, the commit silently becomes a rollback AND throws. Always use [`:TRY`](../reference/keywords/TRY.md) / [`:CATCH`](../reference/keywords/CATCH.md) / [`:FINALLY`](../reference/keywords/FINALLY.md) around your transaction boundaries.

### Per-step error handling inside one transaction

Instead of nesting [`BeginLimsTransaction`](../reference/functions/BeginLimsTransaction.md), catch each step's error and let the single outer transaction decide whether to commit.

```ssl
:PROCEDURE ProcessBatchWithSteps;
    :PARAMETERS aBatchItems;
    :DECLARE nIndex, bStarted, bAllSucceeded, oError;

    bStarted := .F.;
    bAllSucceeded := .T.;

    :TRY;
        bStarted := BeginLimsTransaction();

        :FOR nIndex := 1 :TO ALen(aBatchItems);
            :TRY;
                RunSQL("INSERT INTO results VALUES (?)",, {aBatchItems[nIndex]});
            :CATCH;
                /* Log but don't rollback inner — let outer decide;
                oError := GetLastSSLError();
                ErrorMes("WARN", "Step " + LimsString(nIndex) + " failed: " + oError:Description);
                bAllSucceeded := .F.;
            :ENDTRY;
        :NEXT;
    :CATCH;
        oError := GetLastSSLError();
        ErrorMes("ERROR", "Batch processing failed: " + oError:Description);
        bAllSucceeded := .F.;
    :FINALLY;
        :IF bStarted;
            EndLimsTransaction(, bAllSucceeded);
        :ENDIF;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ProcessBatchWithSteps", {{"R-001", "R-002"}});
```

## Isolation levels

In most cases, calling [`BeginLimsTransaction`](../reference/functions/BeginLimsTransaction.md) with no arguments is the right choice — the server's default isolation level applies (on SQL Server this is normally Read Committed unless the database or connection is configured otherwise).

For advanced scenarios where you need explicit control, [`BeginLimsTransaction`](../reference/functions/BeginLimsTransaction.md) accepts an optional second parameter to override the isolation level:

```ssl
BeginLimsTransaction(, "Repeatable Read");
BeginLimsTransaction(, "Serializable");
BeginLimsTransaction(, "Snapshot");
```

Supported values (case-insensitive):

**`Read Uncommitted`** — Lowest isolation. Your transaction can see uncommitted changes from other transactions (dirty reads). Fast but risky — use only for rough estimates or monitoring queries where accuracy isn't critical.

**`Read Committed`** — Normally the SQL Server default. Your transaction only sees data that other transactions have committed. However, if you read the same row twice, another transaction could change it between reads (non-repeatable read). Suitable for most LIMS operations.

**`Repeatable Read`** — Once your transaction reads a row, that row is locked and cannot be changed by others until you commit or roll back. Prevents non-repeatable reads but other transactions can still insert new rows that match your query (phantom reads).

**`Serializable`** — Strictest level. Transactions execute as if they were run one at a time. Prevents all anomalies but significantly reduces concurrency. Use only when data integrity requirements demand it — can cause blocking and deadlocks under load.

**`Snapshot`** — Each transaction sees a consistent snapshot of the database as of the transaction start. Other transactions can modify data concurrently without blocking. Requires SQL Server snapshot isolation to be enabled at the database level.

| Level | Dirty Reads | Non-repeatable Reads | Phantom Reads | Concurrency |
|-------|-------------|---------------------|---------------|-------------|
| Read Uncommitted | Yes | Yes | Yes | Highest |
| Read Committed | No | Yes | Yes | High |
| Repeatable Read | No | No | Yes | Medium |
| Serializable | No | No | No | Lowest |
| Snapshot | No | No | No | High (no blocking) |

!!! note
    An unrecognized isolation level string silently falls back to Read Uncommitted. Always use one of the exact strings above.

## SQL error handling

### RunSQL behavior on failure

What happens when a [`RunSQL`](../reference/functions/RunSQL.md) statement fails depends on two global flags. Both start at [`.T.`](../reference/literals/true.md), so by default a failing statement raises:

| [`IgnoreSqlErrors`](../reference/functions/IgnoreSqlErrors.md) | [`ShowSqlErrors`](../reference/functions/ShowSqlErrors.md) | Behavior |
|-------------------|-----------------|----------|
| [`.T.`](../reference/literals/true.md) (default) | [`.T.`](../reference/literals/true.md) (default) | The failure raises. Handle it with [`:TRY`](../reference/keywords/TRY.md) / [`:CATCH`](../reference/keywords/CATCH.md). |
| [`.T.`](../reference/literals/true.md) | [`.F.`](../reference/literals/false.md) | `RunSQL` returns [`.F.`](../reference/literals/false.md). The error is available from [`GetLastSQLError`](../reference/functions/GetLastSQLError.md). Nothing is stored for [`GetLastSSLError`](../reference/functions/GetLastSSLError.md). |
| [`.F.`](../reference/literals/false.md) | either | The failure raises, whatever `ShowSqlErrors` is set to. |

`ShowSqlErrors` is the flag that decides: setting only `IgnoreSqlErrors(.T.)` changes nothing, because it is already on. To get a [`.F.`](../reference/literals/false.md) return instead of an error, turn `ShowSqlErrors` off. Set `IgnoreSqlErrors(.T.)` as well, in case a caller turned it off. Save both previous values and restore them when the block ends:

```ssl
:DECLARE nIndex, bOk, bPrevIgnore, bPrevShow, oSqlErr;

/* Make failing statements return .F. for a batch operation;
bPrevIgnore := IgnoreSqlErrors(.T.);
bPrevShow := ShowSqlErrors(.F.);

:TRY;
    :FOR nIndex := 1 :TO ALen(aStatements);
        bOk := RunSQL(aStatements[nIndex]);

        :IF !bOk;
            oSqlErr := GetLastSQLError();
            ErrorMes("SQL", "Statement " + LimsString(nIndex) + " failed: " + oSqlErr:Description);
        :ENDIF;
    :NEXT;
:FINALLY;
    /* Restore the values saved above;
    ShowSqlErrors(bPrevShow);
    IgnoreSqlErrors(bPrevIgnore);
:ENDTRY;
```

!!! warning "Always restore error flags in :FINALLY"
    [`IgnoreSqlErrors`](../reference/functions/IgnoreSqlErrors.md) and [`ShowSqlErrors`](../reference/functions/ShowSqlErrors.md) are global state. If you change them, save the previous values and restore them in a [`:FINALLY`](../reference/keywords/FINALLY.md) block. Restoring hard-coded values instead can switch off a setting a caller relied on, and leaving `ShowSqlErrors` off masks failures in subsequent code.

### SQLExecute and bRollbackExistingTransaction

[`SQLExecute`](../reference/functions/SQLExecute.md) has a `bRollbackExistingTransaction` parameter for non-`SELECT` statements. Don't rely on it to close your transaction: in Designer, after a failed `UPDATE` inside a transaction, [`IsInTransaction`](../reference/functions/IsInTransaction.md) is still [`.T.`](../reference/literals/true.md) whether the argument is [`.T.`](../reference/literals/true.md) or [`.F.`](../reference/literals/false.md). End the transaction in [`:FINALLY`](../reference/keywords/FINALLY.md), exactly as for any other failure:

```ssl
:DECLARE bStarted, bCommit, bUpdated, oError;
bStarted := .F.;
bCommit := .F.;

:TRY;
    bStarted := BeginLimsTransaction();

    bUpdated := SQLExecute(sSQL,, .T.);
    bCommit := .T.;
:CATCH;
    oError := GetLastSSLError();
    ErrorMes("SQL ERROR", oError:Description);
:FINALLY;
    :IF bStarted;
        EndLimsTransaction(, bCommit);   /* the failed call left the transaction open;
    :ENDIF;
:ENDTRY;
```

## Complete transaction pattern

This pattern covers the common case — a procedure that modifies data with proper error handling, transaction management, and error reporting:

```ssl
:PROCEDURE UpdateSampleStatus;
    :PARAMETERS sSampleId, sNewStatus;
    :DECLARE bStarted, bCommit, oError;

    bStarted := .F.;
    bCommit := .F.;

    :TRY;
        bStarted := BeginLimsTransaction();

        RunSQL("
            UPDATE samples SET status = ? WHERE sample_id = ?
        ",, {sNewStatus, sSampleId});

        RunSQL("
            INSERT INTO audit_log (sample_id, action, timestamp)
            VALUES (?, 'STATUS_CHANGE', ?)
        ",, {sSampleId, DToS(Now())});

        bCommit := .T.;
    :CATCH;
        oError := GetLastSSLError();
        ErrorMes("DB ERROR", "Failed to update " + sSampleId + ": " + oError:Description);
    :FINALLY;
        :IF bStarted;
            EndLimsTransaction(, bCommit);
        :ENDIF;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("UpdateSampleStatus", {"S-001", "Released"});
```

Key points:

- [`BeginLimsTransaction`](../reference/functions/BeginLimsTransaction.md) inside [`:TRY`](../reference/keywords/TRY.md) so connection failures are caught
- `bCommit` starts as [`.F.`](../reference/literals/false.md) — defaults to rollback if anything goes wrong
- Set `bCommit := .T.` only after all operations succeed
- `bStarted` guard in [`:FINALLY`](../reference/keywords/FINALLY.md) ends only the transaction this procedure began, never a caller's
- [`EndLimsTransaction`](../reference/functions/EndLimsTransaction.md) in [`:FINALLY`](../reference/keywords/FINALLY.md) ensures the transaction always closes
- [`:CATCH`](../reference/keywords/CATCH.md) logs the error with [`ErrorMes`](../reference/functions/ErrorMes.md) so it's never silenced
- Omit the first argument to use the default connection
