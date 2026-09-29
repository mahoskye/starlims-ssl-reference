# Error Handling in SSL

SSL provides two error handling models: the modern **structured** model ([`:TRY`](../reference/keywords/TRY.md) / [`:CATCH`](../reference/keywords/CATCH.md) / [`:FINALLY`](../reference/keywords/FINALLY.md)) and the **legacy** model ([`:ERROR`](../reference/keywords/ERROR.md) / [`:RESUME`](../reference/keywords/RESUME.md)). New code should use structured handling exclusively.

## Structured error handling

### Basic pattern

```ssl
:DECLARE oResult, oError;

:TRY;
    /* Code that might fail;
    oResult := RunSQL(sQuery);
:CATCH;
    /* Error recovery;
    oError := GetLastSSLError();
    UsrMes("Query failed: " + oError:Description);
:FINALLY;
    /* Always runs — cleanup;
    EndLimsTransaction();
:ENDTRY;
```

### Rules

- At least one of [`:CATCH`](../reference/keywords/CATCH.md) or [`:FINALLY`](../reference/keywords/FINALLY.md) must follow [`:TRY`](../reference/keywords/TRY.md)
- Only **one** [`:CATCH`](../reference/keywords/CATCH.md) block is allowed (no multi-catch)
- [`:FINALLY`](../reference/keywords/FINALLY.md) always executes, even after [`:RETURN`](../reference/keywords/RETURN.md) inside [`:TRY`](../reference/keywords/TRY.md) or [`:CATCH`](../reference/keywords/CATCH.md)
- Use [`GetLastSSLError`](../reference/functions/GetLastSSLError.md) inside [`:CATCH`](../reference/keywords/CATCH.md) to retrieve the error object, then access `:Description` or `:FullDescription` for the message text
- Use [`RaiseError`](../reference/functions/RaiseError.md) to throw a custom error — place it directly inside the [`:TRY`](../reference/keywords/TRY.md) block whose [`:CATCH`](../reference/keywords/CATCH.md) handles it, never inside a [`:CATCH`](../reference/keywords/CATCH.md), and never where nothing catches it (an uncaught error surfaces to the end user as a server error)
- [`:RETURN`](../reference/keywords/RETURN.md), [`:EXITFOR`](../reference/keywords/EXITFOR.md), [`:EXITWHILE`](../reference/keywords/EXITWHILE.md), and [`:LOOP`](../reference/keywords/LOOP.md) inside a [`:FINALLY`](../reference/keywords/FINALLY.md) block are **compile-time errors** — keep cleanup code linear and let it fall through

### Common patterns

#### Try-catch with logging

```ssl
:DECLARE oError;

:TRY;
    DocCheckoutDocument(sDocId);
:CATCH;
    oError := GetLastSSLError();
    UsrMes("Checkout", "Failed for " + sDocId + ": " + oError:Description);
:ENDTRY;
```

#### Try-catch with critical error reporting

Use [`ErrorMes`](../reference/functions/ErrorMes.md) instead of [`UsrMes`](../reference/functions/UsrMes.md) when an error **must** be logged regardless of server configuration. [`UsrMes`](../reference/functions/UsrMes.md) can be silenced on production servers, but [`ErrorMes`](../reference/functions/ErrorMes.md) always writes.

```ssl
:DECLARE oError;

:TRY;
    RunSQL(sDeleteSQL);
:CATCH;
    oError := GetLastSSLError();
    ErrorMes("CRITICAL", "Data deletion failed: " + oError:Description);
:ENDTRY;
```

!!! tip "UsrMes vs ErrorMes vs InfoMes"
    - **[UsrMes](../reference/functions/UsrMes.md)(caption, message)** — general-purpose logging; can be disabled on production servers
    - **[ErrorMes](../reference/functions/ErrorMes.md)(caption, message)** — always writes, even when UsrMes is disabled; use for errors that must never be silenced
    - **[InfoMes](../reference/functions/InfoMes.md)(caption, message)** — alias for UsrMes; same suppression behavior

#### Try-finally for resource cleanup

```ssl
:TRY;
    BeginLimsTransaction();
    RunSQL(sInsertSQL);
    RunSQL(sUpdateSQL);
:FINALLY;
    EndLimsTransaction();
:ENDTRY;
```

#### Nested try blocks

```ssl
:DECLARE oConnection;

:TRY;
    :TRY;
        oConnection := LimsNETConnect(sAssembly);
    :CATCH;
        UsrMes("Assembly load failed, trying fallback");
        oConnection := LimsNETConnect(sFallback);
    :ENDTRY;
    /* Continue with oConnection;
:CATCH;
    UsrMes("All connection attempts failed");
:ENDTRY;
```

## Error inspection functions

| Function | Purpose |
|----------|---------|
| [GetLastSSLError](../reference/functions/GetLastSSLError.md) | Returns the most recent error object (use `:Description` for the message text) |
| [GetLastSQLError](../reference/functions/GetLastSQLError.md) | Returns the most recent SQL error message |
| [ClearLastSSLError](../reference/functions/ClearLastSSLError.md) | Clears the stored error state |
| [RaiseError](../reference/functions/RaiseError.md) | Throws a custom error with a specified message |
| [FormatErrorMessage](../reference/functions/FormatErrorMessage.md) | Formats an error object into a full description string |

## Legacy error handling

!!! warning "Legacy pattern — use :TRY/:CATCH for new code"
    The [`:ERROR`](../reference/keywords/ERROR.md) / [`:RESUME`](../reference/keywords/RESUME.md) pattern predates structured exception handling. It is supported for backward compatibility but should not be used in new procedures.

In both forms, `:ERROR;` starts the last section of the procedure, which runs to [`:ENDPROC`](../reference/keywords/ENDPROC.md). The statements **before** `:ERROR` are protected. The statements after it are the handler body, which runs only when a protected statement fails. A handler placed first protects nothing: the code after it runs only as handler code.

In the examples below, `RiskyOperationA`, `RiskyOperationB`, `RiskyOperationC`, and `RiskyOperation` stand for local procedures in the same script that can raise an error.

### Legacy pattern with :RESUME

When [`:RESUME`](../reference/keywords/RESUME.md) ends the [`:ERROR`](../reference/keywords/ERROR.md) handler, **each statement** before `:ERROR` is protected individually. If a statement fails, the handler runs, then [`:RESUME`](../reference/keywords/RESUME.md) continues execution at the **next** statement after the one that failed.

```ssl
:PROCEDURE LegacyResumeExample;
    :DECLARE sResult;

    /* Each statement below is individually protected;
    sResult := DoProc("RiskyOperationA");
    sResult := DoProc("RiskyOperationB");
    sResult := DoProc("RiskyOperationC");

    :RETURN sResult;
:ERROR;
    /* Runs for whichever statement failed;
    ErrorMes("WARN", "A step failed, continuing");
:RESUME;
:ENDPROC;
```

If `RiskyOperationA` fails, the handler runs, [`:RESUME`](../reference/keywords/RESUME.md) continues with the `RiskyOperationB` call, and so on. Every statement gets a chance to run, and the procedure reaches its own [`:RETURN`](../reference/keywords/RETURN.md). A failed call leaves `sResult` unchanged.

### Legacy pattern without :RESUME

Without [`:RESUME`](../reference/keywords/RESUME.md), the statements before `:ERROR` are protected as one region. The first failure skips the rest of them, the handler runs, and the procedure ends. There is no resumption: the procedure returns whatever the handler returns, or an empty string when the handler has no [`:RETURN`](../reference/keywords/RETURN.md).

```ssl
:PROCEDURE LegacyNoResumeExample;
    :DECLARE sResult;

    sResult := DoProc("RiskyOperation");

    :RETURN sResult;
:ERROR;
    /* Runs on any failure, then the procedure ends;
    ErrorMes("ERROR", "Operation failed");
:ENDPROC;
```

### Do not mix :ERROR/:RESUME with :TRY/:CATCH

!!! danger "With :RESUME, a legacy :ERROR handler takes errors from a :TRY block"
    When a procedure's [`:ERROR`](../reference/keywords/ERROR.md) handler ends with [`:RESUME`](../reference/keywords/RESUME.md), an error raised inside a [`:TRY`](../reference/keywords/TRY.md) body goes to the legacy handler, not to [`:CATCH`](../reference/keywords/CATCH.md). Execution then continues **inside** the `:TRY` body at the statement after the one that failed. Do not use `:RESUME` in a procedure that contains `:TRY`/`:CATCH`.

In observed runtime behavior, when a procedure contains a `:TRY`/`:CATCH` block and a trailing `:ERROR` handler:

- **With `:RESUME`:** the legacy handler runs for an error raised inside the `:TRY` body, and the `:CATCH` block does **not** run. `:RESUME` continues at the statement **after** the one that failed, inside the `:TRY` body. The procedure can reach its normal success path and return a success value after a handled failure.
- **Without `:RESUME`:** the `:TRY` keeps its own `:CATCH`. The error goes to `:CATCH`, execution continues after [`:ENDTRY`](../reference/keywords/ENDTRY.md), and the legacy handler is not involved.

This procedure records which lines run:

```ssl
:PROCEDURE MixedHandlingExample;
    :DECLARE sTrail;

    sTrail := "start";

    :TRY;
        RaiseError("Raised inside TRY block.");
        /* :RESUME continues here, inside the TRY body;
        sTrail := sTrail + " > after raise in TRY";
    :CATCH;
        /* Never runs while the handler ends with :RESUME;
        sTrail := sTrail + " > CATCH";
    :ENDTRY;

    sTrail := sTrail + " > after ENDTRY";

    :RETURN "finished: " + sTrail;
:ERROR;
    /* Runs instead of :CATCH;
    sTrail := sTrail + " > legacy handler";
:RESUME;
:ENDPROC;

/* Usage;
:RETURN DoProc("MixedHandlingExample");
```

Returns:

```text
finished: start > legacy handler > after raise in TRY > after ENDTRY
```

Remove the `:RESUME;` line and the same procedure returns `finished: start > CATCH > after ENDTRY`: `:CATCH` handles the error and the rest of the `:TRY` body is skipped.

This matters because, in resume mode, cleanup, retry, or failure-return logic inside `:CATCH` never executes, and code after a failed statement runs in a partially invalid state. In practice:

- Prefer [`:TRY`](../reference/keywords/TRY.md)/[`:CATCH`](../reference/keywords/CATCH.md) for new code.
- Do not add `:RESUME` to a procedure that contains `:TRY`/`:CATCH`.
- Without `:RESUME`, each `:TRY` keeps its own `:CATCH`, but two error models in one procedure are harder to follow. Keep them apart where you can.
- If legacy handling is unavoidable, isolate it in a small wrapper procedure and document the expected control flow.
- Do not rely on `:CATCH` running when the procedure also contains an `:ERROR` handler that ends with `:RESUME`.
- Treat `:RESUME` as hazardous: it can continue execution after a failed statement left variables or resources in a partially initialized state.

### Key differences from structured handling

| Feature | [`:TRY`](../reference/keywords/TRY.md)/[`:CATCH`](../reference/keywords/CATCH.md) | [`:ERROR`](../reference/keywords/ERROR.md)/[`:RESUME`](../reference/keywords/RESUME.md) |
|---------|-------------|----------------|
| Scope | Block-level | Statements before [`:ERROR`](../reference/keywords/ERROR.md) in the same procedure |
| Multiple handlers | One [`:CATCH`](../reference/keywords/CATCH.md) per [`:TRY`](../reference/keywords/TRY.md) | One [`:ERROR`](../reference/keywords/ERROR.md) per procedure |
| Cleanup guarantee | [`:FINALLY`](../reference/keywords/FINALLY.md) always runs | No equivalent |
| Resume point | After [`:ENDTRY`](../reference/keywords/ENDTRY.md) | With [`:RESUME`](../reference/keywords/RESUME.md), the statement after the failing one; without it, the procedure ends after the handler |
| Nesting | Supported | Not supported |
| Recommended | Yes | No (legacy only) |

## Common error patterns

SSL errors surface as runtime exceptions with descriptive messages. Common patterns:

| Error | Cause | Example |
|-------|-------|---------|
| Null argument | [`NIL`](../reference/literals/nil.md) passed to a required parameter | `ALen(NIL)` |
| Type mismatch | Incompatible types in an operation | `.T. = 1` |
| Database error | SQL execution or connection failure | `RunSQL("invalid sql")` |
| Index out of range | Array or string index beyond bounds | `aArr[999]` |
| Property not found | Accessing a nonexistent object property | `oObj:GetProperty("missing")` |
