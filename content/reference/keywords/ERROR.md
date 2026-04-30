---
title: "ERROR"
summary: "Defines a legacy error handler for the statements that follow it in the current procedure or method."
id: ssl.keyword.error
element_type: keyword
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ERROR

Defines a legacy error handler for the statements that follow it in the current procedure or method.

`:ERROR` starts the legacy scope-based error-handling pattern. Its body must contain at least one statement, and it handles runtime errors raised by subsequent statements in the same scope. When used together with [`:RESUME`](RESUME.md), execution can continue after a handled failure. Without [`:RESUME`](RESUME.md), the handler still runs, but execution does not resume statement-by-statement.

Use `:ERROR` primarily when maintaining older SSL code that already relies on the `:ERROR` / [`:RESUME`](RESUME.md) pattern. For new code, prefer structured [`:TRY`](TRY.md) / [`:CATCH`](CATCH.md) / [`:FINALLY`](FINALLY.md) blocks.

## Behavior

`:ERROR` applies to the subsequent statements in the current scope, not to a [`:TRY`](TRY.md) block.

If a handled statement fails, the `:ERROR` body runs. Use [`GetLastSSLError()`](../functions/GetLastSSLError.md) inside the handler to retrieve the current error object and read properties such as `:Description`.

If the procedure includes [`:RESUME`](RESUME.md), the runtime switches to resume-mode handling so execution can continue after a failing statement. If there is no [`:RESUME`](RESUME.md), the handler still catches the error, but the procedure does not continue in that statement-by-statement recovery mode.

## When to use

- When maintaining legacy procedures that already use `:ERROR` / [`:RESUME`](RESUME.md).
- When you need one shared handler for the remaining statements in the current scope.
- When recoverable failures should be logged or corrected before optionally continuing with [`:RESUME`](RESUME.md).

## Syntax

```ssl
:ERROR;
```

`:ERROR` is followed by one or more handler statements. In practice it is usually paired with `:RESUME;` later in the same handler block when the procedure should continue after an error.

## Keyword group

**Group:** Error Handling
**Role:** handler

## Best practices

!!! success "Do"
    - Use `:ERROR` only for legacy handler flows that genuinely need `:ERROR` / [`:RESUME`](RESUME.md).
    - Put the `:ERROR` block before the statements it is meant to protect.
    - Use [`GetLastSSLError()`](../functions/GetLastSSLError.md) and `oErr:Description` inside the handler when you need a readable error message.
    - Prefer [`:TRY`](TRY.md) / [`:CATCH`](CATCH.md) / [`:FINALLY`](FINALLY.md) for new code.

!!! failure "Don't"
    - Describe `:ERROR` as part of [`:TRY`](TRY.md) / [`:CATCH`](CATCH.md) / [`:FINALLY`](FINALLY.md). It is a separate legacy mechanism.
    - Use `:ERROR` for new structured exception-handling examples when [`:TRY`](TRY.md) / [`:CATCH`](CATCH.md) would be clearer.
    - Assume [`:RESUME`](RESUME.md) is optional when the procedure is meant to continue after failures. Without it, the handler does not provide resume-mode recovery.

## Caveats

- `:ERROR` is legacy scope-based handling for the current procedure or method. It is not a clause inside [`:TRY`](TRY.md).
- [`:RESUME`](RESUME.md) changes the flow to resume-mode handling for subsequent statements. Use it only when continuing is safe.
- If no handled error occurs, the `:ERROR` body is skipped.

## Examples

### Logging a failure and stopping the procedure

Uses one shared legacy handler to catch any failure in the remaining procedure body. If [`ReadText`](../functions/ReadText.md) fails, the handler logs the error via [`ErrorMes`](../functions/ErrorMes.md). If it succeeds, the file content is reported via [`UsrMes`](../functions/UsrMes.md).

```ssl
:PROCEDURE LoadConfiguration;
    :DECLARE sFilePath, sContent, oErr;

    sFilePath := "config/settings.txt";

    /* Handle any later failure in this procedure;
    :ERROR;
        oErr := GetLastSSLError();
        ErrorMes("Configuration load failed: " + oErr:Description);
        /* Displays on failure: configuration load failed;

    /* If ReadText fails, control jumps to the handler;
    sContent := ReadText(sFilePath);

    /* Only runs when the file was read successfully;
    UsrMes("File loaded successfully: " + sContent);
    /* Displays on success: loaded file contents;

    :RETURN sContent;
:ENDPROC;

/* Usage;
DoProc("LoadConfiguration");
```

### Resuming after per-record failures

Uses [`:RESUME`](RESUME.md) so a batch loop can continue after logging a recoverable error for a single record. With the input `{"S-001", "BAD", "S-003"}`, the `"BAD"` record triggers the error handler and increments the failure count; the other records are processed normally.

```ssl
:PROCEDURE ImportResults;
    :PARAMETERS aSampleIDs;
    :DECLARE nIndex, sSampleID, oErr, nImported, nFailed;

    nImported := 0;
    nFailed := 0;

    /* Log the failure and continue with the next statement;
    :ERROR;
        oErr := GetLastSSLError();
        nFailed := nFailed + 1;
        UsrMes("Skipping sample " + sSampleID + ": " + oErr:Description);
        /* Displays on failure: skipping the current sample;
    :RESUME;

    :FOR nIndex := 1 :TO ALen(aSampleIDs);
        sSampleID := aSampleIDs[nIndex];

        /* Simulate a failing record in the batch;
        :IF sSampleID == "BAD";
            RaiseError("Sample is not valid for import");
        :ENDIF;

        nImported := nImported + 1;
    :NEXT;

    UsrMes(
        "Imported " + LimsString(nImported)
        + " samples. Failed: " + LimsString(nFailed)
    );
    /* Displays a summary of imported and failed records;

    :RETURN nImported;
:ENDPROC;

/* Usage;
DoProc("ImportResults", {{"S-001", "BAD", "S-003"}});
```

## Related

- [`RESUME`](RESUME.md)
- [`TRY`](TRY.md)
- [`CATCH`](CATCH.md)
- [`FINALLY`](FINALLY.md)
- [`ENDTRY`](ENDTRY.md)
