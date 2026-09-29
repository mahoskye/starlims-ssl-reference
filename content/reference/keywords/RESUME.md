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

The [`:ERROR`](ERROR.md) handler is the last section of a procedure, and it protects the statements before it. Place `:RESUME;` at the end of that handler, directly before [`:ENDPROC`](ENDPROC.md). With `:RESUME` present, every failing statement in the protected region runs the handler, and execution then continues with the next statement after the one that raised the error. The procedure keeps going until it reaches its own [`:RETURN`](RETURN.md) or the end of the protected region.

Resume mode also applies to statements inside a [`:TRY`](TRY.md) body. In observed runtime behavior, the legacy handler takes an error raised inside the `:TRY` body, [`:CATCH`](CATCH.md) does not run, and execution continues inside the `:TRY` body at the statement after the one that failed. Without `:RESUME`, the `:TRY` keeps its own `:CATCH`.

If a procedure contains `:RESUME` without an [`:ERROR`](ERROR.md) handler, compilation fails. For new code, prefer [`:TRY`](TRY.md) / [`:CATCH`](CATCH.md) / [`:FINALLY`](FINALLY.md), which gives you narrower and clearer control over the protected block.

## When to use

- When you are maintaining legacy code that already relies on [`:ERROR`](ERROR.md) /
  `:RESUME` behavior.
- When the procedure can safely skip a failed statement and continue with later work.
- When you need broad legacy error coverage across every statement before the [`:ERROR`](ERROR.md) handler rather than a smaller [`:TRY`](TRY.md) block.

## Syntax

```ssl
:PROCEDURE ProcName;
    protected_statements;
:ERROR;
    handler_statements;
:RESUME;
:ENDPROC;
```

`:RESUME` takes no parameters. It is the last statement of the [`:ERROR`](ERROR.md) handler.

## Keyword group

**Group:** Error Handling
**Role:** statement

## Best practices

!!! success "Do"
    - Use `:RESUME` only when the failure is expected and later statements can still run safely.
    - Place the [`:ERROR`](ERROR.md) handler after the statements it protects, and end the handler with `:RESUME`.
    - Keep the [`:ERROR`](ERROR.md) handler focused on logging, cleanup, or lightweight recovery before `:RESUME` takes effect.
    - Prefer [`:TRY`](TRY.md) / [`:CATCH`](CATCH.md) / [`:FINALLY`](FINALLY.md) in new code when you only need to protect a specific block.

!!! failure "Don't"
    - Use `:RESUME` for unknown or non-recoverable errors because that can hide real failures and keep the procedure running in a bad state.
    - Use `:RESUME` without an [`:ERROR`](ERROR.md) handler because the procedure will not compile.
    - Place `:RESUME` in [`:CATCH`](CATCH.md) or [`:FINALLY`](FINALLY.md) blocks because it belongs only to the legacy [`:ERROR`](ERROR.md) pattern.
    - Use `:RESUME` in a procedure that also contains [`:TRY`](TRY.md) / [`:CATCH`](CATCH.md). The legacy handler takes the errors meant for `:CATCH`.

## Caveats

- `:RESUME` must appear in a procedure that also contains an [`:ERROR`](ERROR.md) handler.
- `:RESUME` does not retry the failing statement. Execution continues with the next statement after the error. A failed assignment leaves its variable unchanged, so later statements see the old value.
- If later statements keep failing and the handler does not resolve the problem, the procedure can continue producing repeated errors.
- Do not combine `:RESUME` with [`:TRY`](TRY.md)/[`:CATCH`](CATCH.md) in the same procedure. In observed runtime behavior the legacy handler takes errors raised inside a `:TRY` body, [`:CATCH`](CATCH.md) never runs, and execution continues inside the `:TRY` body at the statement after the one that failed. See [Error Handling](../../guides/error-handling.md#do-not-mix-errorresume-with-trycatch).

## Examples

### Every failing statement runs the handler

Records which lines run. Each [`RaiseError`](../functions/RaiseError.md) call runs the handler, and `:RESUME` continues with the statement after it, so both later lines still run and the procedure reaches its own [`:RETURN`](RETURN.md).

```ssl
:PROCEDURE ResumeTrail;
    :DECLARE sTrail;

    sTrail := "start";
    RaiseError("first failure");
    sTrail := sTrail + " > after failure 1";
    RaiseError("second failure");
    sTrail := sTrail + " > after failure 2";

    :RETURN sTrail;
:ERROR;
    sTrail := sTrail + " > handler";
:RESUME;
:ENDPROC;

/* Usage;
:RETURN DoProc("ResumeTrail");
```

Returns:

```text
start > handler > after failure 1 > handler > after failure 2
```

Without `:RESUME`, the same procedure would stop at the first failure and return an empty string, because the handler has no [`:RETURN`](RETURN.md).

### Skip a failed update and continue

Uses `:RESUME` so a failed [`RunSQL`](../functions/RunSQL.md) call does not stop the rest of the procedure. When the update raises an error, the handler logs it, `bUpdated` keeps its initial [`.F.`](../literals/false.md), and execution continues with the summary message.

```ssl
:PROCEDURE UpdateSampleStatus_Legacy;
    :PARAMETERS sSampleID, sStatus;
    :DECLARE bUpdated, oErr;

    bUpdated := .F.;

    bUpdated := RunSQL(
        "UPDATE sample SET status = ? WHERE sample_id = ?",,
        {sStatus, sSampleID}
    );

    UsrMes("Status update for " + sSampleID + " done, updated: " + LimsString(bUpdated));

    :RETURN bUpdated;
:ERROR;
    oErr := GetLastSSLError();
    UsrMes("Update failed for " + sSampleID + ": " + oErr:Description);
:RESUME;
:ENDPROC;

/* Usage;
DoProc("UpdateSampleStatus_Legacy", {"SAMPL-2024-042", "INREVIEW"});
```

When the update fails, the failure message is logged first, then `Status update for SAMPL-2024-042 done, updated: .F.`, and the procedure returns [`.F.`](../literals/false.md).

## Related

- [`ERROR`](ERROR.md)
- [`TRY`](TRY.md)
