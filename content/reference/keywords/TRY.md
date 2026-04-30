---
title: "TRY"
summary: "Starts a protected block that can transfer control to :CATCH, :FINALLY, or both when errors occur."
id: ssl.keyword.try
element_type: keyword
category: error-handling
tags:
  - exception-handling
  - cleanup
  - try-catch
  - try-finally
  - control-flow
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# TRY

Starts a protected block that can transfer control to [`:CATCH`](CATCH.md), [`:FINALLY`](FINALLY.md), or both when errors occur.

## Behavior

`:TRY` begins SSL's structured error-handling construct. The statements in the `:TRY` body run in order until the block completes or a statement raises an error.

When an error occurs, control moves to the single [`:CATCH`](CATCH.md) block if one is present. Use [`GetLastSSLError()`](../functions/GetLastSSLError.md) inside [`:CATCH`](CATCH.md) to inspect the current error. After [`:CATCH`](CATCH.md), an optional [`:FINALLY`](FINALLY.md) block runs. If there is no [`:CATCH`](CATCH.md), a [`:FINALLY`](FINALLY.md) block can still be used by itself for cleanup, but the original error continues to propagate after [`:FINALLY`](FINALLY.md) finishes.

The structure must end with [`:ENDTRY;`](ENDTRY.md), and it must include at least one [`:CATCH`](CATCH.md) or [`:FINALLY`](FINALLY.md) section.

## When to use

- When you want to isolate error-prone work so failures do not abort the rest of the procedure unexpectedly.
- When you need a [`:CATCH`](CATCH.md) block to inspect [`GetLastSSLError()`](../functions/GetLastSSLError.md) and set a user message, fallback value, or recovery path.
- When you need a [`:FINALLY`](FINALLY.md) block to release locks, reset state, or perform other cleanup that must run on both success and failure.
- When you want error-handling scope to match one specific operation instead of covering an entire procedure.

## Syntax

```ssl
:TRY;
    try_statements;
:CATCH;
    catch_statements;
:ENDTRY;
```

```ssl
:TRY;
    try_statements;
:FINALLY;
    finally_statements;
:ENDTRY;
```

```ssl
:TRY;
    try_statements;
:CATCH;
    catch_statements;
:FINALLY;
    finally_statements;
:ENDTRY;
```

## Keyword group

**Group:** Error Handling
**Role:** opener

## Best practices

!!! success "Do"
    - Keep the `:TRY` body narrow so the paired [`:CATCH`](CATCH.md) handles one clear unit of work.
    - Use [`GetLastSSLError()`](../functions/GetLastSSLError.md) inside [`:CATCH`](CATCH.md) and prefer `oErr:Description` when you need the message text.
    - Put shared cleanup in [`:FINALLY`](FINALLY.md) when locks, temporary state, or resources must always be released.

!!! failure "Don't"
    - Wrap large unrelated sections of code in one `:TRY` block. That makes failures harder to understand and recover from.
    - Expect multiple typed [`:CATCH`](CATCH.md) blocks. SSL allows only one [`:CATCH`](CATCH.md) per `:TRY`.
    - Put [`:RETURN`](RETURN.md), [`:EXITWHILE`](EXITWHILE.md), [`:EXITFOR`](EXITFOR.md), or [`:LOOP`](LOOP.md) inside [`:FINALLY`](FINALLY.md). Those control-flow statements are invalid there.

## Caveats

- A `:TRY` block must include at least one [`:CATCH`](CATCH.md) or [`:FINALLY`](FINALLY.md) section.
- Only one [`:CATCH`](CATCH.md) block is allowed per `:TRY` block.
- When both are present, [`:CATCH`](CATCH.md) must come before [`:FINALLY`](FINALLY.md).
- The `:TRY` body must contain at least one statement.
- A [`:FINALLY`](FINALLY.md) block must also contain at least one statement when present.
- [`:CATCH`](CATCH.md) does not declare an exception variable; retrieve the current error with [`GetLastSSLError()`](../functions/GetLastSSLError.md).
- Keywords are case-sensitive and must be written in uppercase.

## Examples

### Handling a failed file read

Uses `:TRY` and [`:CATCH`](CATCH.md) to prevent a missing or unreadable file from stopping the procedure. When the file cannot be read, the error handler sets the status message and execution continues normally after [`:ENDTRY;`](ENDTRY.md).

```ssl
:PROCEDURE OpenConfigFile;
    :DECLARE sFilePath, sFileContents, sStatus, oErr;

    sFilePath := "C:\STARLIMS\config\app.cfg";
    sStatus := "";

    :TRY;
        sFileContents := ReadText(sFilePath);
        sStatus := "Configuration file loaded successfully";
        UsrMes(Left(sFileContents, 50));

    :CATCH;
        oErr := GetLastSSLError();
        sStatus := "Could not load config: " + oErr:Description;
        UsrMes(sStatus);

    :ENDTRY;

    :RETURN sStatus;
:ENDPROC;

DoProc("OpenConfigFile");
```

On success, `UsrMes` displays the first 50 characters of the file. On failure, it displays the error text stored in `sStatus`.

### Pairing CATCH and FINALLY for cleanup

Shows how `:TRY`, [`:CATCH`](CATCH.md), and [`:FINALLY`](FINALLY.md) work together when cleanup must run even after a failure. [`RaiseError`](../functions/RaiseError.md) forces the error path; [`:FINALLY`](FINALLY.md) releases the lock regardless of which branch ran.

```ssl
:PROCEDURE ProcessWithLock;
    :DECLARE bLockAcquired, oLock, oErr, sStatus;

    bLockAcquired := .F.;
    sStatus := "Starting";
    oLock := CreateLocal();
    oLock:isLocked := .F.;

    :TRY;
        oLock:isLocked := .T.;
        bLockAcquired := .T.;
        sStatus := "Lock acquired";

        RaiseError("Processing failed due to invalid sample state");

    :CATCH;
        oErr := GetLastSSLError();
        sStatus := "Processing failed: " + oErr:Description;

    :FINALLY;
        :IF bLockAcquired;
            oLock:isLocked := .F.;
            bLockAcquired := .F.;
        :ENDIF;

    :ENDTRY;

    UsrMes(sStatus);

    :RETURN sStatus;
:ENDPROC;

DoProc("ProcessWithLock");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Processing failed: Processing failed due to invalid sample state
```

### Handling multiple failure paths in one CATCH block

Uses one `:TRY` block for a multi-step operation, then branches inside the single [`:CATCH`](CATCH.md) block SSL supports. [`:FINALLY`](FINALLY.md) always displays the outcome regardless of success or failure. With `sBatchID` set to `"B-1001"` and both the load and update succeeding, the final message confirms processing.

```ssl
:PROCEDURE ProcessBatchRecords;
    :PARAMETERS sBatchID;
    :DECLARE aRecords, oErr, sStatusMessage;
    :DECLARE bLoadedRecords, bUpdatedBatch;

    sStatusMessage := "";
    bLoadedRecords := .F.;
    bUpdatedBatch := .F.;

    :TRY;
        aRecords := SQLExecute("
            SELECT record_id, status
            FROM batch_records
            WHERE batch_id = ?sBatchID?
        ");
        bLoadedRecords := .T.;

        :IF ALen(aRecords) == 0;
            RaiseError("No records found for batch " + sBatchID);
        :ENDIF;

        bUpdatedBatch := RunSQL("
            UPDATE batches SET
                processed = ?,
                processed_on = SYSDATE
            WHERE batch_id = ?
        ",, {1, sBatchID});

        :IF !bUpdatedBatch;
            RaiseError("Batch update did not complete");
        :ENDIF;

        sStatusMessage := "Batch " + sBatchID + " processed successfully";

    :CATCH;
        oErr := GetLastSSLError();

        :BEGINCASE;
        :CASE !bLoadedRecords;
            sStatusMessage := "Batch lookup failed: " + oErr:Description;
            :EXITCASE;
        :CASE ALen(aRecords) == 0;
            sStatusMessage := "Nothing to process for batch " + sBatchID;
            :EXITCASE;
        :OTHERWISE;
            sStatusMessage := "Batch update failed: " + oErr:Description;
            :EXITCASE;
        :ENDCASE;

    :FINALLY;
        UsrMes(sStatusMessage);

    :ENDTRY;

    :RETURN sStatusMessage;
:ENDPROC;

DoProc("ProcessBatchRecords", {"B-1001"});
```

## Related

- [`CATCH`](CATCH.md)
- [`FINALLY`](FINALLY.md)
- [`ENDTRY`](ENDTRY.md)
