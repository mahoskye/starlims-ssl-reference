---
title: "ClearLastSSLError"
summary: "Clears the stored SSL error so later error checks start clean."
id: ssl.function.clearlastsslerror
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ClearLastSSLError

Clears the stored SSL error so later error checks start clean.

`ClearLastSSLError` removes the currently stored SSL error and returns [`.T.`](../literals/true.md).
It does not tell you whether an error was present before the call. If you need the previous error details, read [`GetLastSSLError`](GetLastSSLError.md) first.

## When to use

- When you have already handled the current SSL error and want later checks to start clean.
- When a retry loop should ignore an error that belonged to the previous attempt.
- When you want [`GetLastSSLError`](GetLastSSLError.md) to reflect only failures that happen after a reset point.

## Syntax

```ssl
ClearLastSSLError()
```

## Parameters

This function has no parameters.

## Returns

**[boolean](../types/boolean.md)** — Always returns [`.T.`](../literals/true.md).

## Best practices

!!! success "Do"
    - Read or log [`GetLastSSLError`](GetLastSSLError.md) before clearing it when the details matter.
    - Clear the error state at explicit workflow boundaries such as before a retry.
    - Keep the clear close to the code that depends on a fresh error state.

!!! failure "Don't"
    - Clear the error state before you inspect an error you still need.
    - Treat the [`.T.`](../literals/true.md) return value as proof that an earlier operation succeeded.
    - Sprinkle this call through unrelated code paths where it can hide the source of a failure.

## Caveats

- This function clears the stored SSL error state only. It does not fix the underlying problem that raised the error.
- After the call, [`GetLastSSLError`](GetLastSSLError.md) no longer returns the previously stored error details.

## Examples

### Clear the error after logging it

Reads the current SSL error, logs its description, then clears the state so later error checks start fresh.

```ssl
:PROCEDURE HandleAndClearSslError;
    :DECLARE oErr;

    oErr := GetLastSSLError();

    :IF Empty(oErr);
        :RETURN .F.;
    :ENDIF;

    UsrMes("Handled SSL error: " + oErr:Description);
    /* Logs the handled error description;
    ClearLastSSLError();

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("HandleAndClearSslError");
```

### Reset before a retry

Catches the error from a failed SQL update, logs it, clears the error state, then retries the same operation once in its own [`:TRY`](../keywords/TRY.md) so the second attempt starts clean.

```ssl
:PROCEDURE RetryStatusUpdate;
    :PARAMETERS sSampleID, sStatus;
    :DECLARE bUpdated, oErr;

    bUpdated := .F.;

    :TRY;
        bUpdated := RunSQL("
            UPDATE sample SET
                status = ?
            WHERE sampleid = ?
        ",, {sStatus, sSampleID});
    :CATCH;
        oErr := GetLastSSLError();
        UsrMes("First update failed: " + oErr:Description);
        /* Logs the first failure description;
        ClearLastSSLError();
    :ENDTRY;

    :IF bUpdated;
        :RETURN .T.;
    :ENDIF;

    :TRY;
        bUpdated := RunSQL("
            UPDATE sample SET
                status = ?
            WHERE sampleid = ?
        ",, {sStatus, sSampleID});
    :CATCH;
        oErr := GetLastSSLError();
        UsrMes("Retry failed: " + oErr:Description);
        ClearLastSSLError();
    :ENDTRY;

    :RETURN bUpdated;
:ENDPROC;

/* Usage;
DoProc("RetryStatusUpdate", {"SAMP-001", "APPROVED"});
```

### Batch work with per-item error resets

Handles each sample in its own [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) and clears the error state after recording a failure, so one sample's error cannot contaminate the check for the next.

```ssl
:PROCEDURE ProcessQueuedSamples;
    :DECLARE aSampleIDs, aFailed, sSampleID, oErr, nIndex;

    aSampleIDs := {"SAM-001", "SAM-002", "SAM-003"};
    aFailed := {};

    :FOR nIndex := 1 :TO ALen(aSampleIDs);
        sSampleID := aSampleIDs[nIndex];

        :TRY;
            RunSQL("
                UPDATE sample SET
                    status = ?
                WHERE sampleid = ?
            ",, {"COMPLETE", sSampleID});
        :CATCH;
            oErr := GetLastSSLError();
            AAdd(aFailed, {sSampleID, oErr:Description});
            ClearLastSSLError();
        :ENDTRY;
    :NEXT;

    :RETURN aFailed;
:ENDPROC;

/* Usage;
DoProc("ProcessQueuedSamples");
```

## Related

- [`FormatErrorMessage`](FormatErrorMessage.md)
- [`GetLastSSLError`](GetLastSSLError.md)
- [`RaiseError`](RaiseError.md)
- [`boolean`](../types/boolean.md)
