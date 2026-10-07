---
title: "ERROR"
summary: "Starts a legacy error handler at the end of a procedure that handles failures in the statements before it."
id: ssl.keyword.error
element_type: keyword
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# ERROR

Starts a legacy error handler at the end of a procedure that handles failures in the statements before it.

`:ERROR;` starts the last section of a procedure, which runs to [`:ENDPROC`](ENDPROC.md). The statements before `:ERROR` are the protected region. The statements after it are the handler body, which runs only when a protected statement fails. The handler body must contain at least one statement.

Without [`:RESUME`](RESUME.md), the first failure runs the handler and the procedure ends. With [`:RESUME`](RESUME.md) at the end of the handler, every failing statement runs the handler and execution continues with the next statement.

Use `:ERROR` primarily when maintaining older SSL code that already relies on the `:ERROR` / [`:RESUME`](RESUME.md) pattern. For new code, prefer structured [`:TRY`](TRY.md) / [`:CATCH`](CATCH.md) / [`:FINALLY`](FINALLY.md) blocks.

## Behavior

**Placement.** `:ERROR` protects the statements that come before it in the same procedure. The statements after it are handler code, not protected code: they run only when an earlier statement fails. A handler placed first therefore protects nothing, and the code after it never runs on the success path. When no error occurs, execution never enters the handler body, and a procedure that reaches `:ERROR` without a [`:RETURN`](RETURN.md) returns an empty string.

**Without [`:RESUME`](RESUME.md).** The first failing statement skips the rest of the protected region and runs the handler. The procedure then ends and returns whatever the handler returns, or `""` if the handler has no [`:RETURN`](RETURN.md). A [`:TRY`](TRY.md) block in the protected region keeps its own [`:CATCH`](CATCH.md): errors raised inside the `:TRY` body go to that `:CATCH`, not to the legacy handler.

**With [`:RESUME`](RESUME.md).** Every failing statement in the protected region runs the handler, and execution then continues with the statement after the one that failed. This includes statements inside a [`:TRY`](TRY.md) body: in observed runtime behavior the legacy handler takes the error, [`:CATCH`](CATCH.md) does not run, and the rest of the `:TRY` body keeps running.

Use [`GetLastSSLError()`](../functions/GetLastSSLError.md) inside the handler to retrieve the current error object and read properties such as `:Description`.

## When to use

- When maintaining legacy procedures that already use `:ERROR` / [`:RESUME`](RESUME.md).
- When one shared handler at the end of a procedure should cover every statement before it.
- When recoverable failures should be logged or corrected before optionally continuing with [`:RESUME`](RESUME.md).

## Syntax

```ssl
:PROCEDURE ProcName;
    protected_statements;
:ERROR;
    handler_statements;
:ENDPROC;
```

`:ERROR;` is followed by one or more handler statements, which run to [`:ENDPROC`](ENDPROC.md). Add `:RESUME;` as the last handler statement when the procedure should continue after each failure.

## Keyword group

**Group:** Error Handling
**Role:** handler

## Best practices

!!! success "Do"
    - Use `:ERROR` only for legacy handler flows that genuinely need `:ERROR` / [`:RESUME`](RESUME.md).
    - Put `:ERROR` after the statements it is meant to protect, as the last section of the procedure.
    - End the protected region with a [`:RETURN`](RETURN.md) so the success path returns its own value, and give the handler its own [`:RETURN`](RETURN.md) when callers need a failure value.
    - Use [`GetLastSSLError()`](../functions/GetLastSSLError.md) and `oErr:Description` inside the handler when you need a readable error message.
    - Prefer [`:TRY`](TRY.md) / [`:CATCH`](CATCH.md) / [`:FINALLY`](FINALLY.md) for new code.

!!! failure "Don't"
    - Put `:ERROR` before the statements you want to protect. Those statements become handler code and run only when an error occurs.
    - Describe `:ERROR` as part of [`:TRY`](TRY.md) / [`:CATCH`](CATCH.md) / [`:FINALLY`](FINALLY.md). It is a separate legacy mechanism.
    - Use `:ERROR` for new structured exception-handling examples when [`:TRY`](TRY.md) / [`:CATCH`](CATCH.md) would be clearer.
    - Add [`:RESUME`](RESUME.md) to a procedure that also contains [`:TRY`](TRY.md) / [`:CATCH`](CATCH.md). In resume mode the legacy handler takes errors from the `:TRY` body and `:CATCH` never runs.

## Caveats

- `:ERROR` is legacy handling for the statements before it in the current procedure. It is not a clause inside [`:TRY`](TRY.md).
- The handler runs to [`:ENDPROC`](ENDPROC.md). Statements placed after `:ERROR` never run on the success path.
- Without [`:RESUME`](RESUME.md), a [`:TRY`](TRY.md) block in the protected region keeps its own [`:CATCH`](CATCH.md).
- With [`:RESUME`](RESUME.md), the legacy handler takes errors raised inside a [`:TRY`](TRY.md) body before [`:CATCH`](CATCH.md) can run, and execution continues inside the `:TRY` body at the next statement. Do not combine resume mode with [`:TRY`](TRY.md)/[`:CATCH`](CATCH.md) in the same procedure. See [Error Handling](../../guides/error-handling.md#do-not-mix-errorresume-with-trycatch).
- If no error occurs, the handler body is skipped.

## Examples

### Logging a failure and stopping the procedure

The protected region checks a result and approves it. When the check raises an error, the rest of the protected region is skipped, the handler logs the reason, and the procedure returns [`.F.`](../literals/false.md) from the handler.

```ssl
:PROCEDURE ApproveResult;
    :PARAMETERS sSampleID, nResult;
    :DECLARE oErr;

    UsrMes("Checking " + sSampleID);

    :IF nResult < 0;
        RaiseError("Result cannot be negative");
    :ENDIF;

    /* Skipped when the check fails;
    UsrMes("Approved " + sSampleID);

    :RETURN .T.;
:ERROR;
    /* Runs only when a statement above fails;
    oErr := GetLastSSLError();
    UsrMes("Approval failed for " + sSampleID + ": " + oErr:Description);

    :RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("ApproveResult", {"S-1002", -4});
```

[`UsrMes`](../functions/UsrMes.md) logs:

```text
Checking S-1002
Approval failed for S-1002: Result cannot be negative
```

With a result of `12.5` instead, the handler is skipped, `UsrMes` logs `Checking S-1002` and `Approved S-1002`, and the procedure returns [`.T.`](../literals/true.md).

### A handler placed first protects nothing

This shape looks like it guards the lines below `:ERROR`, but those lines are handler code. No error occurs before `:ERROR`, so the handler never runs: nothing is logged and the procedure returns an empty string, not `"finished"`.

```ssl
:PROCEDURE HandlerFirst;
    :DECLARE sStatus;

    sStatus := "start";
:ERROR;
    /* Handler code, not a protected region;
    UsrMes("This line runs only after an earlier failure");
    sStatus := "finished";

    :RETURN sStatus;
:ENDPROC;

/* Usage;
:RETURN DoProc("HandlerFirst");
```

### Continuing after a failed read with :RESUME

Uses [`:RESUME`](RESUME.md) so each failed [`ReadText`](../functions/ReadText.md) call keeps its default value and the procedure goes on to the next line. When `settings/footer.txt` does not exist, the handler runs once, `sFooter` keeps its default, and execution continues with the summary line, which reports one missing file.

```ssl
:PROCEDURE LoadDisplaySettings;
    :DECLARE sTitle, sFooter, nMissing, oErr;

    sTitle := "Sample Register";
    sFooter := "";
    nMissing := 0;

    /* A failed read runs the handler, then the next line runs;
    sTitle := ReadText("settings/title.txt");
    sFooter := ReadText("settings/footer.txt");

    UsrMes("Settings loaded, missing files: " + LimsString(nMissing));

    :RETURN {sTitle, sFooter};
:ERROR;
    oErr := GetLastSSLError();
    nMissing += 1;
    UsrMes("Keeping a default value: " + oErr:Description);
:RESUME;
:ENDPROC;

/* Usage;
DoProc("LoadDisplaySettings");
```

## Related

- [`RESUME`](RESUME.md)
- [`TRY`](TRY.md)
- [`CATCH`](CATCH.md)
- [`FINALLY`](FINALLY.md)
- [`ENDTRY`](ENDTRY.md)
