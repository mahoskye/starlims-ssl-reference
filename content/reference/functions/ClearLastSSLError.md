---
title: "ClearLastSSLError"
summary: "Clears the current SSL error state."
id: ssl.function.clearlastsslerror
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ClearLastSSLError

Clears the current SSL error state.

`ClearLastSSLError` removes the currently stored SSL error and returns [`.T.`](../literals/true.md).
It does not tell you whether an error was present before the call. If you need the previous error details, read [`GetLastSSLError`](GetLastSSLError.md) first.

## When to use

- When you have already handled the current SSL error and want later checks to start clean.
- When a retry loop should ignore an error that belonged to the previous attempt.
- When you want [`GetLastSSLError`](GetLastSSLError.md) to reflect only failures that happen after a reset point.

## Syntax

```ssl
ClearLastSSLError();
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

Reads the current SSL error, displays its description, then clears the state so later error checks start fresh.

```ssl
:PROCEDURE HandleAndClearSslError;
    :DECLARE oErr;

    oErr := GetLastSSLError();

    :IF Empty(oErr);
        :RETURN .F.;
    :ENDIF;

    UsrMes("Handled SSL error: " + oErr:Description);
    /* Displays the handled error description;
    ClearLastSSLError();

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("HandleAndClearSslError");
```

### Reset before a retry

Logs the error from a failed SQL update, clears the error state, then retries the same operation once so the second attempt is not tainted by the first failure.

```ssl
:PROCEDURE RetryStatusUpdate;
    :PARAMETERS sSampleID, sStatus;
    :DECLARE bUpdated, oErr;

    bUpdated := RunSQL("
        UPDATE sample SET
	        status = ?
	    WHERE sampleid = ?
    ",, {sStatus, sSampleID});

    :IF bUpdated;
        :RETURN .T.;
    :ENDIF;

    oErr := GetLastSSLError();
    UsrMes("First update failed: " + oErr:Description);
    /* Displays the first failure description;

    ClearLastSSLError();

    bUpdated := RunSQL("
        UPDATE sample SET
	        status = ?
	    WHERE sampleid = ?
    ",, {sStatus, sSampleID});

    :RETURN bUpdated;
:ENDPROC;

/* Usage;
DoProc("RetryStatusUpdate", {"SAMP-001", "APPROVED"});
```

### Batch work with per-item error resets

Clears the error state at the start of each loop iteration so a failure on one sample cannot contaminate the error check for the next sample.

```ssl
:PROCEDURE ProcessQueuedSamples;
    :DECLARE aSampleIDs, aFailed, sSampleID, oErr, nIndex;

    aSampleIDs := {"SAM-001", "SAM-002", "SAM-003"};
    aFailed := {};

    :FOR nIndex := 1 :TO ALen(aSampleIDs);
        sSampleID := aSampleIDs[nIndex];
        ClearLastSSLError();

        :IF RunSQL("
            UPDATE sample SET
				status = ?
			WHERE sampleid = ?
        ",, {"COMPLETE", sSampleID});
            :LOOP;
        :ENDIF;

        oErr := GetLastSSLError();
        AAdd(aFailed, {sSampleID, oErr:Description});
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
