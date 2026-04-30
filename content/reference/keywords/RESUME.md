---
title: "RESUME"
summary: "Continues execution after a legacy :ERROR handler, starting with the statement after the one that failed."
id: ssl.keyword.resume
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# RESUME

Continues execution after a legacy [`:ERROR`](ERROR.md) handler, starting with the statement after the one that failed.

## Behavior

`:RESUME` is part of the legacy [`:ERROR`](ERROR.md) / `:RESUME` error-handling pattern. Use it only with [`:ERROR`](ERROR.md); it is not used with [`:TRY`](TRY.md), [`:CATCH`](CATCH.md), or [`:FINALLY`](FINALLY.md).

Within an [`:ERROR`](ERROR.md) handler, `:RESUME;` switches the remaining statements in the procedure into resume-mode handling. When one of those later statements fails, the [`:ERROR`](ERROR.md) handler runs and execution continues with the next statement after the one that raised the error.

If a procedure contains `:RESUME` without an [`:ERROR`](ERROR.md) handler, compilation fails. For new code, prefer [`:TRY`](TRY.md) / [`:CATCH`](CATCH.md) / [`:FINALLY`](FINALLY.md), which gives you narrower and clearer control over the protected block.

## When to use

- When you are maintaining legacy code that already relies on [`:ERROR`](ERROR.md) /
  `:RESUME` behavior.
- When the procedure can safely skip a failed statement and continue with later work.
- When you need broad legacy error coverage across the remaining statements in a procedure rather than a smaller [`:TRY`](TRY.md) block.

## Syntax

```ssl
:RESUME;
```

`:RESUME` takes no parameters.

## Keyword group

**Group:** Error Handling
**Role:** statement

## Best practices

!!! success "Do"
    - Use `:RESUME` only when the failure is expected and later statements can still run safely.
    - Keep the [`:ERROR`](ERROR.md) handler focused on logging, cleanup, or lightweight recovery before `:RESUME` takes effect.
    - Prefer [`:TRY`](TRY.md) / [`:CATCH`](CATCH.md) / [`:FINALLY`](FINALLY.md) in new code when you only need to protect a specific block.

!!! failure "Don't"
    - Use `:RESUME` for unknown or non-recoverable errors because that can hide real failures and keep the procedure running in a bad state.
    - Use `:RESUME` without an [`:ERROR`](ERROR.md) handler because the procedure will not compile.
    - Place `:RESUME` in [`:CATCH`](CATCH.md) or [`:FINALLY`](FINALLY.md) blocks because it belongs only to the legacy [`:ERROR`](ERROR.md) pattern.

## Caveats

- `:RESUME` must appear in a procedure that also contains an [`:ERROR`](ERROR.md) handler.
- `:RESUME` does not retry the failing statement. Execution continues with the next statement after the error.
- If later statements keep failing and the handler does not resolve the problem, the procedure can continue producing repeated errors.

## Examples

### Skip a failed update and continue logging

Uses `:RESUME` so a failed [`RunSQL`](../functions/RunSQL.md) call does not stop the rest of the procedure. When the SQL update fails, the error handler logs the failure and execution continues to the confirmation message.

```ssl
:PROCEDURE UpdateSampleStatus_Legacy;
    :DECLARE sSampleID, sStatus, sSQL, oErr;

    sSampleID := "SAMPL-2024-042";
    sStatus := "INREVIEW";
    sSQL := "UPDATE sample SET status = ? WHERE sample_id = ?";

    :ERROR;
        oErr := GetLastSSLError();
        UsrMes("Update failed for " + sSampleID + ": " + oErr:Description);
        /* Displays the failure message when RunSQL errors;
    :RESUME;

    RunSQL(sSQL,, {sStatus, sSampleID});

    InfoMes("Legacy procedure continued after the handled error");
:ENDPROC;

DoProc("UpdateSampleStatus_Legacy");
```

### Continue a batch after record-level failures

Logs each bad record and continues processing the rest of the array. With `{"SMP-001", "INVALID", "SMP-002"}`, the `"INVALID"` entry triggers the error handler once while the loop completes all three iterations via `:RESUME`.

```ssl
:PROCEDURE ValidateSampleRecords;
    :PARAMETERS aSampleIDs;
    :DECLARE nIndex, sSampleID, nValidated, nFailed, oErr, sLogMsg;

    nValidated := 0;
    nFailed := 0;

    :ERROR;
        oErr := GetLastSSLError();
        sLogMsg := "Validation failed for " + sSampleID + ": " + oErr:Description;
        UsrMes(sLogMsg);
        /* Displays the failure message for the rejected record;
        nFailed += 1;
    :RESUME;

    :FOR nIndex := 1 :TO ALen(aSampleIDs);
        sSampleID := aSampleIDs[nIndex];

        :IF sSampleID == "INVALID" .OR. sSampleID == "REJECTED";
            RaiseError("Invalid sample status for " + sSampleID);
        :ENDIF;

        nValidated += 1;
    :NEXT;

    InfoMes(
        "Validation complete. Passed: " + LimsString(nValidated) + ", Failed: " +
        LimsString(nFailed)
    );
    /* Displays the final pass and fail totals;

    :RETURN nValidated;
:ENDPROC;

DoProc("ValidateSampleRecords", {{"SMP-001", "INVALID", "SMP-002"}});
```

## Related

- [`ERROR`](ERROR.md)
- [`TRY`](TRY.md)
