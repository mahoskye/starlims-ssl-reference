---
title: "FINALLY"
summary: "Starts the cleanup section of a :TRY block and always runs after the protected work completes."
id: ssl.keyword.finally
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

# FINALLY

Starts the cleanup section of a [`:TRY`](TRY.md) block and always runs after the protected work completes.

`:FINALLY` introduces the final section of a structured [`:TRY`](TRY.md) block. The statements in `:FINALLY` run after the [`:TRY`](TRY.md) body finishes, whether the protected work succeeds or raises an error. When a [`:CATCH`](CATCH.md) block is present, it runs before `:FINALLY`; when no [`:CATCH`](CATCH.md) is present, `:FINALLY` can still be used by itself as the cleanup section before [`:ENDTRY;`](ENDTRY.md).

A [`:TRY`](TRY.md) body must contain at least one statement before `:FINALLY`, and the `:FINALLY` block itself must also contain at least one statement. [`:TRY`](TRY.md) cannot end directly with [`:ENDTRY;`](ENDTRY.md) because the structure must include [`:CATCH`](CATCH.md), `:FINALLY`, or both.

## Behavior

`:FINALLY` is part of these valid structured forms:

```ssl
:TRY;
    try_statements;
:FINALLY;
    cleanup_statements;
:ENDTRY;
```

```ssl
:TRY;
    try_statements;
:CATCH;
    catch_statements;
:FINALLY;
    cleanup_statements;
:ENDTRY;
```

Control-flow statements that would bypass the guaranteed cleanup path are invalid inside `:FINALLY`. These forms raise compile-time errors:

- `Cannot have :RETURN inside :FINALLY.`
- `Cannot have :EXITWHILE inside :FINALLY.`
- `Cannot have :EXITFOR inside :FINALLY.`
- `Cannot have :LOOP inside :FINALLY.`

## When to use

- When cleanup must happen regardless of whether the [`:TRY`](TRY.md) body succeeds or fails.
- When resetting state, releasing locks, or restoring temporary settings after protected work.

## Syntax

```ssl
:FINALLY;
```

## Keyword group

**Group:** Error Handling
**Role:** modifier

## Best practices

!!! success "Do"
    - Use `:FINALLY` for cleanup that must happen whether the [`:TRY`](TRY.md) body succeeds or fails.
    - Keep `:FINALLY` focused on cleanup, state restoration, and other mandatory end-of-block work.
    - Put error-specific recovery in [`:CATCH`](CATCH.md) and shared cleanup in `:FINALLY` when you need both.

!!! failure "Don't"
    - Put [`:RETURN`](RETURN.md), [`:EXITWHILE`](EXITWHILE.md), [`:EXITFOR`](EXITFOR.md), or [`:LOOP`](LOOP.md) inside `:FINALLY`. All four forms are invalid there.
    - Move main business logic into `:FINALLY`. That block should stay predictable and cleanup-oriented.
    - Leave a `:FINALLY` body empty. It must contain at least one statement.

## Caveats

- `:FINALLY` is only valid inside a [`:TRY`](TRY.md) structure.
- `:FINALLY` must appear after the [`:TRY`](TRY.md) body and before [`:ENDTRY;`](ENDTRY.md).
- When both blocks are present, [`:CATCH`](CATCH.md) must come before `:FINALLY`.
- Keywords are case-sensitive and must be written in uppercase.

## Examples

### Releasing cleanup state after success or failure

Uses `:FINALLY` to reset a flag that must always be cleared, even when the batch query raises an error. The cleanup runs unconditionally; the [`:CATCH`](CATCH.md) block only runs when an error occurs.

```ssl
:PROCEDURE ProcessBatch;
    :PARAMETERS sBatchID;
    :DECLARE aRows, bCleanupNeeded, oErr, sStatus;

    bCleanupNeeded := .F.;
    sStatus := "Starting";

    :TRY;
        /* Mark temporary state that must always be cleared;
        bCleanupNeeded := .T.;
        sStatus := "Loading batch";

        aRows := SQLExecute("
            SELECT sample_id
            FROM sample
            WHERE batch_id = ?sBatchID?
        ");

        :IF ALen(aRows) == 0;
            RaiseError("No samples found for batch " + sBatchID);
        :ENDIF;

        sStatus := "Loaded " + LimsString(ALen(aRows)) + " sample(s)";

    :CATCH;
        oErr := GetLastSSLError();
        sStatus := "Batch load failed: " + oErr:Description;
        UsrMes(sStatus);  /* Displays batch load failure on error;

    :FINALLY;
        :IF bCleanupNeeded;
            bCleanupNeeded := .F.;
            UsrMes("Cleanup complete");
        :ENDIF;

    :ENDTRY;

    :RETURN sStatus;
:ENDPROC;

/* Usage;
DoProc("ProcessBatch", {"BATCH-001"});
```

## Related

- [`TRY`](TRY.md)
- [`CATCH`](CATCH.md)
- [`ENDTRY`](ENDTRY.md)
