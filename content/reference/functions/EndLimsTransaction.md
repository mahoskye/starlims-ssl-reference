---
title: "EndLimsTransaction"
summary: "Ends a LIMS transaction on the default connection or on a named connection."
id: ssl.function.endlimstransaction
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# EndLimsTransaction

Ends a LIMS transaction on the default connection or on a named connection.

Use `EndLimsTransaction` to close a transaction scope started with [`BeginLimsTransaction`](BeginLimsTransaction.md). If `sConnectionName` is omitted or empty, the function uses the default LIMS connection. If `bCommit` is omitted, it defaults to [`.T.`](../literals/true.md).

Each call decreases the transaction depth for that connection. On the outermost transaction, [`.T.`](../literals/true.md) commits and [`.F.`](../literals/false.md) rolls back. If an inner transaction was rolled back, a later outermost commit raises an error instead of committing.

## When to use

- When you need to explicitly commit completed work.
- When you need to roll back work after a failure or validation problem.
- When you are balancing a [`BeginLimsTransaction`](BeginLimsTransaction.md) call on the default or a named connection.

## Syntax

```ssl
EndLimsTransaction([sConnectionName], [bCommit])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sConnectionName` | [string](../types/string.md) | no | omitted | Connection name of the LIMS database connection to close. If omitted or empty, the default connection is used. |
| `bCommit` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Whether to commit the transaction scope. Pass [`.F.`](../literals/false.md) to roll it back. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the transaction scope ends successfully. Raises an exception on failure rather than returning [`.F.`](../literals/false.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| The named connection does not exist. | `The provider name: {sConnectionName} not found.` |
| No database collection is available. | `The internal database collection is null` |
| The database provider cannot close the transaction. | `Transaction cannot be ended {message}` |

## Best practices

!!! success "Do"
    - Call `EndLimsTransaction` exactly once for every successful [`BeginLimsTransaction`](BeginLimsTransaction.md) call.
    - Keep a `bCommit` flag that only becomes [`.T.`](../literals/true.md) after all transactional work succeeds.
    - Use the same `sConnectionName` that started the transaction when you are working on a named connection.
    - Roll back the outer transaction when an inner transaction on the same connection rolls back.

!!! failure "Don't"
    - Assume the function returns [`.F.`](../literals/false.md) for a missing connection or failed close; those paths raise errors.
    - Mix connection names between [`BeginLimsTransaction`](BeginLimsTransaction.md) and `EndLimsTransaction` calls.
    - Commit in [`:FINALLY`](../keywords/FINALLY.md) before the protected work has finished successfully.
    - Ignore nested rollback state and still try to commit the outermost transaction.

## Caveats

- To pass `bCommit` while using the default connection, skip `sConnectionName` with `EndLimsTransaction(, bCommit)`.

## Examples

### Commit work on the default connection

Opens a transaction on the default connection, runs an update, and commits it. The `bStarted` flag ensures cleanup only runs if the transaction actually opened, and `bCommit` only becomes [`.T.`](../literals/true.md) after the update succeeds.

```ssl
:PROCEDURE UpdateSampleStatus;
    :PARAMETERS sSampleID, sStatus;
    :DECLARE bStarted, bCommit, oErr;

    bStarted := .F.;
    bCommit := .F.;

    :TRY;
        bStarted := BeginLimsTransaction();

        RunSQL("
            UPDATE sample SET
                status = ?
            WHERE sampleid = ?
        ",, {sStatus, sSampleID});

        bCommit := .T.;

    :CATCH;
        oErr := GetLastSSLError();
        /* Displays on failure: update failed;
        ErrorMes("Update failed: " + oErr:Description);

    :FINALLY;
        :IF bStarted;
            EndLimsTransaction(, bCommit);
        :ENDIF;
    :ENDTRY;

    :RETURN bCommit;
:ENDPROC;

/* Usage;
DoProc("UpdateSampleStatus", {"S-001", "Active"});
```

### Roll back a named transaction on validation failure

Opens a transaction on a named connection and validates that no open tasks remain before updating the batch status. If validation fails, [`RaiseError`](RaiseError.md) triggers the [`:CATCH`](../keywords/CATCH.md) block and `bCommit` stays [`.F.`](../literals/false.md), causing the transaction to roll back in [`:FINALLY`](../keywords/FINALLY.md).

```ssl
:PROCEDURE ApplyBatchStatus;
    :PARAMETERS sConnName, sBatchID, sStatus;
    :DECLARE bStarted, bCommit, nOpenTasks, oErr;

    bStarted := .F.;
    bCommit := .F.;

    :TRY;
        bStarted := BeginLimsTransaction(sConnName);

        nOpenTasks := LSearch("
            SELECT COUNT(*)
            FROM batch_task
            WHERE batchid = ?
              AND status = ?
        ", 0,, {sBatchID, "Open"});

        :IF nOpenTasks > 0;
            RaiseError("The batch still has open tasks");
        :ENDIF;

        RunSQL("
            UPDATE batch SET
                status = ?
            WHERE batchid = ?
        ",, {sStatus, sBatchID});

        bCommit := .T.;

    :CATCH;
        oErr := GetLastSSLError();
        /* Displays on failure: batch update failed;
        ErrorMes("Batch update failed: " + oErr:Description);

    :FINALLY;
        :IF bStarted;
            EndLimsTransaction(sConnName, bCommit);
        :ENDIF;
    :ENDTRY;

    :RETURN bCommit;
:ENDPROC;

/* Usage;
DoProc("ApplyBatchStatus", {"MyConn", "BATCH-001", "Closed"});
```

### Handle nested transaction scopes on one connection

Opens an outer transaction for a batch update and an inner transaction for the audit log write. If the inner transaction rolls back, [`RaiseError`](RaiseError.md) propagates the failure to the outer [`:CATCH`](../keywords/CATCH.md), which rolls back the outer transaction too.

```ssl
:PROCEDURE SaveBatchAndAudit;
    :PARAMETERS sConnName, sBatchID;
    :DECLARE bOuterStarted, bOuterCommit, bInnerStarted, bInnerCommit, oErr;

    bOuterStarted := .F.;
    bOuterCommit := .F.;
    bInnerStarted := .F.;
    bInnerCommit := .F.;

    :TRY;
        bOuterStarted := BeginLimsTransaction(sConnName);

        RunSQL("
            UPDATE batch SET
                status = ?
            WHERE batchid = ?
        ",, {"Closed", sBatchID});

        bInnerStarted := BeginLimsTransaction(sConnName);

        :TRY;
            RunSQL("
                INSERT INTO audit_log (
                    event_name, event_ref
                )
                VALUES (
                    ?, ?
                )
            ",, {"BATCH_CLOSEOUT", sBatchID});

            bInnerCommit := .T.;

        :CATCH;
            oErr := GetLastSSLError();
            /* Displays on failure: audit write failed;
            ErrorMes("Audit write failed: " + oErr:Description);

        :FINALLY;
            :IF bInnerStarted;
                EndLimsTransaction(sConnName, bInnerCommit);
            :ENDIF;
        :ENDTRY;

        :IF !bInnerCommit;
            RaiseError("The audit step failed, so the outer transaction must roll back");
        :ENDIF;

        bOuterCommit := .T.;

    :CATCH;
        oErr := GetLastSSLError();
        /* Displays on failure: save batch and audit failed;
        ErrorMes("SaveBatchAndAudit failed: " + oErr:Description);

    :FINALLY;
        :IF bOuterStarted;
            EndLimsTransaction(sConnName, bOuterCommit);
        :ENDIF;
    :ENDTRY;

    :RETURN bOuterCommit;
:ENDPROC;

/* Usage;
DoProc("SaveBatchAndAudit", {"MyConn", "BATCH-001"});
```

## Related

- [`BeginLimsTransaction`](BeginLimsTransaction.md)
- [`GetTransactionsCount`](GetTransactionsCount.md)
- [`IsInTransaction`](IsInTransaction.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
