# SQL and Transaction Management

SSL provides explicit transaction control for database operations. Understanding the transaction model — especially nested transaction behavior and rollback semantics — is essential for writing reliable data modification code.

## Transaction basics

### Starting and ending transactions

Place [`BeginLimsTransaction`](../reference/functions/BeginLimsTransaction.md) inside the [`:TRY`](../reference/keywords/TRY.md) block so that a connection failure is caught cleanly. Use [`IsInTransaction`](../reference/functions/IsInTransaction.md) in [`:FINALLY`](../reference/keywords/FINALLY.md) to avoid calling [`EndLimsTransaction`](../reference/functions/EndLimsTransaction.md) on a transaction that never started.

```ssl
:DECLARE bCommit, oError;
bCommit := .F.;

:TRY;
    BeginLimsTransaction();

    RunSQL("INSERT INTO samples (sample_id, status) VALUES ('S-001', 'A')");
    RunSQL("UPDATE batch SET sample_count = sample_count + 1");

    bCommit := .T.;
:CATCH;
    oError := GetLastSSLError();
    ErrorMes("DB ERROR", "Transaction failed: " + oError:Description);
:FINALLY;
    :IF IsInTransaction();
        EndLimsTransaction(, bCommit);
    :ENDIF;
:ENDTRY;
```

!!! tip "Why BeginLimsTransaction belongs inside :TRY"
    If [`BeginLimsTransaction`](../reference/functions/BeginLimsTransaction.md) throws (connection failure, DAL error), the [`:CATCH`](../reference/keywords/CATCH.md) handles it gracefully. If it were outside [`:TRY`](../reference/keywords/TRY.md), the [`:FINALLY`](../reference/keywords/FINALLY.md) would try to end a transaction that never started — causing a second error.

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

SSL supports nested [`BeginLimsTransaction`](../reference/functions/BeginLimsTransaction.md) calls. The engine uses a **reference-counting** model — only the **outermost** Begin/End pair actually starts and commits or rolls back the database transaction. Inner calls increment and decrement a counter.

```ssl
:TRY;
    BeginLimsTransaction();          /* count = 1, DB transaction starts;

    BeginLimsTransaction();          /* count = 2, no new DB transaction;
    RunSQL(sInnerSQL);
    EndLimsTransaction(, .T.);       /* count = 1, nothing committed yet;

    RunSQL(sOuterSQL);
:CATCH;
    oError := GetLastSSLError();
    ErrorMes("ERROR", oError:Description);
:FINALLY;
    :IF IsInTransaction();
        EndLimsTransaction(, bCommit);  /* count = 0, commits or rolls back;
    :ENDIF;
:ENDTRY;
```

### Inner rollback poisons the outer transaction

This is the most critical behavior to understand: **if any inner transaction is rolled back, the outer transaction cannot commit**.

```ssl
:TRY;
    BeginLimsTransaction();

    BeginLimsTransaction();
    RunSQL(sInsertSQL);
    EndLimsTransaction(, .F.);       /* inner rollback — sets poison flag;

    RunSQL(sUpdateSQL);

    EndLimsTransaction(, .T.);       /* Throws: cannot-commit exception;
:CATCH;
    oError := GetLastSSLError();
    ErrorMes("ERROR", oError:Description);
:FINALLY;
    :IF IsInTransaction();
        EndLimsTransaction(, .F.);
    :ENDIF;
:ENDTRY;
```

When an inner `EndLimsTransaction(, .F.)` is called:

1. The nesting counter decrements but the DB transaction stays open
2. An internal rollback flag is set
3. When the outermost `EndLimsTransaction(, .T.)` runs, it sees the flag
4. It **rolls back** instead of committing
5. It **throws an exception** — "Cannot commit the outermost transaction because one of the inner transactions was rollbacked!"

!!! danger "Always handle the poisoned-transaction exception"
    If you call `EndLimsTransaction(, .T.)` on an outer transaction where an inner transaction was rolled back, the commit silently becomes a rollback AND throws. Always use [`:TRY`](../reference/keywords/TRY.md) / [`:CATCH`](../reference/keywords/CATCH.md) / [`:FINALLY`](../reference/keywords/FINALLY.md) around your transaction boundaries.

### Safe nested transaction pattern

```ssl
:PROCEDURE ProcessBatchWithSteps;
    :PARAMETERS aBatchItems;
    :DECLARE nIndex, bAllSucceeded, oError;

    bAllSucceeded := .T.;

    :TRY;
        BeginLimsTransaction();

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
        :IF IsInTransaction();
            EndLimsTransaction(, bAllSucceeded);
        :ENDIF;
    :ENDTRY;
:ENDPROC;
```

## Isolation levels

In most cases, calling [`BeginLimsTransaction`](../reference/functions/BeginLimsTransaction.md) with no arguments is the right choice — the server's configured default isolation level applies (typically Read Committed, configurable per tenant by the system administrator).

For advanced scenarios where you need explicit control, [`BeginLimsTransaction`](../reference/functions/BeginLimsTransaction.md) accepts an optional second parameter to override the isolation level:

```ssl
BeginLimsTransaction(, "Repeatable Read");
BeginLimsTransaction(, "Serializable");
BeginLimsTransaction(, "Snapshot");
```

Supported values (case-insensitive):

**`Read Uncommitted`** — Lowest isolation. Your transaction can see uncommitted changes from other transactions (dirty reads). Fast but risky — use only for rough estimates or monitoring queries where accuracy isn't critical.

**`Read Committed`** — The default. Your transaction only sees data that other transactions have committed. However, if you read the same row twice, another transaction could change it between reads (non-repeatable read). Suitable for most LIMS operations.

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

[`RunSQL`](../reference/functions/RunSQL.md) catches database exceptions internally. What happens depends on two global flags:

| [`IgnoreSqlErrors`](../reference/functions/IgnoreSqlErrors.md) | [`ShowSqlErrors`](../reference/functions/ShowSqlErrors.md) | Behavior |
|-------------------|-----------------|----------|
| [`.F.`](../reference/literals/false.md) (default) | — | Exception propagates to caller |
| [`.T.`](../reference/literals/true.md) | [`.T.`](../reference/literals/true.md) | Fatal errors still propagate; non-fatal returns [`.F.`](../reference/literals/false.md) |
| [`.T.`](../reference/literals/true.md) | [`.F.`](../reference/literals/false.md) | All errors return [`.F.`](../reference/literals/false.md) silently |

```ssl
/* Suppress non-fatal SQL errors for a batch operation;
IgnoreSqlErrors(.T.);
ShowSqlErrors(.F.);

:TRY;
    :FOR nIndex := 1 :TO ALen(aStatements);
        bOk := RunSQL(aStatements[nIndex]);

        :IF !bOk;
            ErrorMes("SQL", "Statement " + LimsString(nIndex) + " failed silently");
        :ENDIF;
    :NEXT;
:FINALLY;
    /* Always restore defaults;
    IgnoreSqlErrors(.F.);
    ShowSqlErrors(.T.);
:ENDTRY;
```

!!! warning "Always restore error flags in :FINALLY"
    [`IgnoreSqlErrors`](../reference/functions/IgnoreSqlErrors.md) and [`ShowSqlErrors`](../reference/functions/ShowSqlErrors.md) are global state. If you suppress errors, always restore the defaults in a [`:FINALLY`](../reference/keywords/FINALLY.md) block to avoid masking failures in subsequent code.

### SQLExecute with auto-rollback

[`SQLExecute`](../reference/functions/SQLExecute.md) has a `bRollbackExistingTransaction` parameter. When [`.T.`](../reference/literals/true.md) and the SQL fails, it automatically calls [`EndLimsTransaction`](../reference/functions/EndLimsTransaction.md)(, .F.) on the current connection:

```ssl
:TRY;
    BeginLimsTransaction();

    /* If this fails and rollbackExistingTransaction is .T.,
    /* the transaction is automatically rolled back;
    sResult := SQLExecute(sSQL,, .T.,,, "dataset");
:CATCH;
    oError := GetLastSSLError();
    ErrorMes("SQL ERROR", oError:Description);
:FINALLY;
    :IF IsInTransaction();
        EndLimsTransaction(, .F.);   /* safe — already rolled back if failed;
    :ENDIF;
:ENDTRY;
```

## Complete transaction pattern

This pattern covers the common case — a procedure that modifies data with proper error handling, transaction management, and error reporting:

```ssl
:PROCEDURE UpdateSampleStatus;
    :PARAMETERS sSampleId, sNewStatus;
    :DECLARE bCommit, oError;

    bCommit := .F.;

    :TRY;
        BeginLimsTransaction();

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
        :IF IsInTransaction();
            EndLimsTransaction(, bCommit);
        :ENDIF;
    :ENDTRY;
:ENDPROC;
```

Key points:

- [`BeginLimsTransaction`](../reference/functions/BeginLimsTransaction.md) inside [`:TRY`](../reference/keywords/TRY.md) so connection failures are caught
- `bCommit` starts as [`.F.`](../reference/literals/false.md) — defaults to rollback if anything goes wrong
- Set `bCommit := .T.` only after all operations succeed
- [`IsInTransaction`](../reference/functions/IsInTransaction.md) guard in [`:FINALLY`](../reference/keywords/FINALLY.md) prevents errors when the transaction never started
- [`EndLimsTransaction`](../reference/functions/EndLimsTransaction.md) in [`:FINALLY`](../reference/keywords/FINALLY.md) ensures the transaction always closes
- [`:CATCH`](../reference/keywords/CATCH.md) logs the error with [`ErrorMes`](../reference/functions/ErrorMes.md) so it's never silenced
- Omit the first argument to use the default connection
