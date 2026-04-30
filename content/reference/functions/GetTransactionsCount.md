---
title: "GetTransactionsCount"
summary: "Returns the number of open database transactions for a specified or default connection."
id: ssl.function.gettransactionscount
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetTransactionsCount

Returns the number of open database transactions for a specified or default connection.

Use `GetTransactionsCount` to inspect the current transaction depth for a database connection. When `sConnection` is omitted or passed as an empty string, the function checks the default connection. When `sConnection` is provided, it must be a string naming the target connection.

## When to use

- When deciding whether commit or rollback logic should run.
- When diagnosing unexpected nested transactions.
- When checking a named connection without changing transaction state.

## Syntax

```ssl
GetTransactionsCount()
GetTransactionsCount(sConnection)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sConnection` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | The name of the database connection to inspect. If omitted or empty, the default connection is used. |

## Returns

**[number](../types/number.md)** — The number of open transactions for the specified connection, or for the default connection when `sConnection` is omitted or empty.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sConnection` is provided but is not a string. | `Argument 'sConnection' must be a string.` |
| `sConnection` names a connection that does not exist. | `The provider name: <sConnection> not found.` |

## Best practices

!!! success "Do"
    - Use the default connection when you only need the current script context.
    - Check the count before calling [`EndLimsTransaction`](EndLimsTransaction.md) in defensive transaction-handling code.
    - Pass an explicit connection name when your script works with more than one database connection.

!!! failure "Don't"
    - Pass numbers, arrays, or objects as `sConnection`.
    - Assume a named connection exists without validating the connection name used by your environment.
    - Use this function as a replacement for [`BeginLimsTransaction`](BeginLimsTransaction.md), [`EndLimsTransaction`](EndLimsTransaction.md), or [`IsInTransaction`](IsInTransaction.md).

## Caveats

- The function only reports the current transaction count; it does not start, commit, or roll back transactions.
- An invalid connection name raises an error instead of returning `0`.

## Examples

### Check the default connection transaction depth

Calls `GetTransactionsCount` without arguments to inspect the default connection's open transaction depth and branches on whether any transactions are currently active.

```ssl
:PROCEDURE CheckDefaultTransactionCount;
    :DECLARE nTranCount;

    nTranCount := GetTransactionsCount();

    :IF nTranCount > 0;
        UsrMes(
            "There are " + LimsString(nTranCount) + " open transaction(s) "
            + "on the default connection."
        );
        /* Displays when transactions are open;
    :ELSE;
        UsrMes("There are no open transactions on the default connection.");
        /* Displays when no transactions are open;
    :ENDIF;

    :RETURN nTranCount;
:ENDPROC;

/* Usage;
DoProc("CheckDefaultTransactionCount");
```

### Check a named connection

Passes an explicit connection name and displays the current open transaction count for that connection.

```ssl
:PROCEDURE CheckNamedConnection;
    :DECLARE sConnection, nTranCount;

    sConnection := "LIMS";
    nTranCount := GetTransactionsCount(sConnection);

    UsrMes(
        "Connection " + sConnection + " has "
        + LimsString(nTranCount) + " open transaction(s)."
    );

    :RETURN nTranCount;
:ENDPROC;

/* Usage;
DoProc("CheckNamedConnection");
```

[`UsrMes`](UsrMes.md) displays:

```
Connection LIMS has 0 open transaction(s).
```

### End only the transaction your code started

Records the transaction depth before the update, opens a new transaction only when none are active, then checks the count at both commit and rollback time before calling [`EndLimsTransaction`](EndLimsTransaction.md) to avoid closing a transaction that was opened by the caller.

```ssl
:PROCEDURE UpdateSampleStatusSafely;
    :PARAMETERS sSampleID;
    :DECLARE sConnection, nStartCount, nEndCount, bStartedHere, oErr;

    sConnection := "LIMS";
    bStartedHere := .F.;
    nStartCount := GetTransactionsCount(sConnection);

    :IF nStartCount == 0;
        BeginLimsTransaction(sConnection, "READ COMMITTED");
        bStartedHere := .T.;
    :ENDIF;

    :TRY;
        RunSQL("
            UPDATE sample SET
                status = ?
            WHERE sample_id = ?
            ",,{"COMPLETE", sSampleID});

        nEndCount := GetTransactionsCount(sConnection);

        :IF bStartedHere .AND. nEndCount > 0;
            EndLimsTransaction(sConnection, .T.);
        :ENDIF;
    :CATCH;
        oErr := GetLastSSLError();
        nEndCount := GetTransactionsCount(sConnection);

        :IF bStartedHere .AND. nEndCount > 0;
            EndLimsTransaction(sConnection, .F.);
        :ENDIF;

        ErrorMes("Update failed: " + oErr:Description);
        /* Displays on failure: Update failed;
        :RETURN .F.;
    :ENDTRY;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("UpdateSampleStatusSafely", {"S-1001"});
```

## Related

- [`BeginLimsTransaction`](BeginLimsTransaction.md)
- [`EndLimsTransaction`](EndLimsTransaction.md)
- [`IsInTransaction`](IsInTransaction.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
