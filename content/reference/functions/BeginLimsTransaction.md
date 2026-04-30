---
title: "BeginLimsTransaction"
summary: "Starts a LIMS database transaction on the default connection or on a named connection."
id: ssl.function.beginlimstransaction
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# BeginLimsTransaction

Starts a LIMS database transaction on the default connection or on a named connection.

Use `BeginLimsTransaction` when a group of database operations must succeed or fail as one unit. If `sConnectionName` is omitted or empty, the function uses the default LIMS connection. If `sIsoLevel` is omitted, empty, or passed as a non-string value, the server default isolation setting is used.

When `sIsoLevel` is supplied as a non-empty string, these values are recognized case-insensitively: `Read Uncommitted`, `Read Committed`, `Repeatable Read`, `Serializable`, and `Snapshot`. Any other non-empty string falls back to `Read Uncommitted`.

Calling `BeginLimsTransaction` again on the same connection increases the transaction depth for that connection. Each successful call must be paired with [`EndLimsTransaction`](EndLimsTransaction.md).

## When to use

- When multiple updates must be committed together or rolled back together.
- When you need to control which LIMS connection owns the transaction.
- When a workflow needs a specific transaction isolation level.

## Syntax

```ssl
BeginLimsTransaction([sConnectionName], [sIsoLevel])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sConnectionName` | [string](../types/string.md) | no | default connection | Connection name of the LIMS database connection to use. If omitted or empty, the default connection is used. Passing a non-string value raises an error. |
| `sIsoLevel` | [string](../types/string.md) | no | server default isolation level | Transaction isolation level. Recognized values are `Read Uncommitted`, `Read Committed`, `Repeatable Read`, `Serializable`, and `Snapshot`. Matching is case-insensitive. If omitted, empty, or passed as a non-string value, the server default isolation setting is used. Any other non-empty string falls back to `Read Uncommitted`. |

## Returns

**[boolean](../types/boolean.md)** — Returns [`.T.`](../literals/true.md) when the transaction scope starts successfully. Raises an error if the transaction cannot be started.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sConnectionName` is provided as a non-string value. | `Argument 'sConnectionName' must be a string` |
| The named connection does not exist. | `The provider name: {sConnectionName} not found.` |
| No database collection is available. | `The internal database collection is null` |
| The database provider fails to begin the transaction. | `The transaction cannot be started {message}` |

## Best practices

!!! success "Do"
    - Call [`EndLimsTransaction`](EndLimsTransaction.md) exactly once for every transaction you start.
    - Set a `bStarted` flag after a successful begin so [`:FINALLY`](../keywords/FINALLY.md) only closes transactions that were actually opened.
    - Start the transaction inside a [`:TRY`](../keywords/TRY.md) block and call [`EndLimsTransaction`](EndLimsTransaction.md) in [`:FINALLY`](../keywords/FINALLY.md), especially when the same connection may be entered more than once.
    - Pass a supported isolation-level string when you need behavior other than the server default.
    - Use a named connection only when you know that connection exists in the current environment.

!!! failure "Don't"
    - Leave a transaction open and rely on later code to clean it up.
    - Pass a misspelled isolation level and assume it will behave like the documented level you intended.
    - Pass a non-string `sConnectionName`; that raises an error instead of selecting a connection.
    - Assume a failed begin will quietly return [`.F.`](../literals/false.md); handle it as an exception path.

## Caveats

- Repeated calls on the same connection increase that connection's transaction depth, so each successful begin must be matched with exactly one [`EndLimsTransaction`](EndLimsTransaction.md) call.

## Examples

### Use the default connection

Wraps a single SQL update in the standard TRY/FINALLY transaction pattern, using a `bStarted` flag to ensure [`EndLimsTransaction`](EndLimsTransaction.md) is only called if the transaction was actually opened.

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
        ErrorMes("Update failed: " + oErr:Description);
        /* Displays on failure: update failed;

    :FINALLY;
        :IF bStarted;
            EndLimsTransaction(, bCommit);
        :ENDIF;
    :ENDTRY;

    :RETURN bCommit;
:ENDPROC;

/* Usage;
DoProc("UpdateSampleStatus", {"SAMP-001", "APPROVED"});
```

### Use a named connection for related updates

Passes `sConnName` to target a specific connection, then updates an order and all its task codes inside a single transaction so they commit or roll back together.

```ssl
:PROCEDURE SaveOrderAndTasks;
    :PARAMETERS sConnName, sOrdNo, sNewStatus, aTaskCodes;
    :DECLARE bStarted, bCommit, nIndex, oErr;

    bStarted := .F.;
    bCommit := .F.;

    :TRY;
        bStarted := BeginLimsTransaction(sConnName);

        RunSQL("
            UPDATE orders SET
                status = ?
            WHERE ordno = ?
        ",, {sNewStatus, sOrdNo});

        :FOR nIndex := 1 :TO ALen(aTaskCodes);
            RunSQL("
                UPDATE ordtask SET
                    status = ?
                WHERE ordno = ?
                  AND testcode = ?
            ",, {sNewStatus, sOrdNo, aTaskCodes[nIndex]});
        :NEXT;

        bCommit := .T.;

    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("Transaction failed: " + oErr:Description);
        /* Displays on failure: transaction failed;

    :FINALLY;
        :IF bStarted;
            EndLimsTransaction(sConnName, bCommit);
        :ENDIF;
    :ENDTRY;

    :RETURN bCommit;
:ENDPROC;

/* Usage;
DoProc("SaveOrderAndTasks", {
    "LABDB",
    "ORD-001",
    "APPROVED",
    {"TASK-01", "TASK-02"}
});
```

### Request a specific isolation level

Passes `"Serializable"` as the isolation level to prevent other transactions from modifying the batch during the check-and-update sequence.

```ssl
:PROCEDURE PostCloseoutAudit;
    :PARAMETERS sConnName, sBatchID;
    :DECLARE bStarted, bCommit, nOpenTasks, oErr;

    bStarted := .F.;
    bCommit := .F.;

    :TRY;
        bStarted := BeginLimsTransaction(sConnName, "Serializable");

        nOpenTasks := LSearch("
            SELECT COUNT(*)
            FROM batch_task
            WHERE batchid = ?
              AND status != ?
        ", 0,, {sBatchID, "Closed"});

        :IF nOpenTasks > 0;
            RaiseError("The batch still has open tasks");
        :ENDIF;

        RunSQL("
            INSERT INTO audit_log (
                event_name, event_ref
            )
            VALUES (
                ?, ?
            )
        ",, {"BATCH_CLOSEOUT", sBatchID});

        RunSQL("
            UPDATE batch SET
                status = ?
            WHERE batchid = ?
        ",, {"Closed", sBatchID});

        bCommit := .T.;

    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("Closeout audit failed: " + oErr:Description);
        /* Displays on failure: closeout audit failed;

    :FINALLY;
        :IF bStarted;
            EndLimsTransaction(sConnName, bCommit);
        :ENDIF;
    :ENDTRY;

    :RETURN bCommit;
:ENDPROC;

/* Usage;
DoProc("PostCloseoutAudit", {"LABDB", "BATCH-001"});
```

## Related

- [`CreateORMSession`](CreateORMSession.md)
- [`EndLimsTransaction`](EndLimsTransaction.md)
- [`GetTransactionsCount`](GetTransactionsCount.md)
- [`IsInTransaction`](IsInTransaction.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
