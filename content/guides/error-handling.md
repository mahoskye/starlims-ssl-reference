# Error Handling in SSL

SSL provides two error handling models: the modern **structured** model ([`:TRY`](../reference/keywords/TRY.md) / [`:CATCH`](../reference/keywords/CATCH.md) / [`:FINALLY`](../reference/keywords/FINALLY.md)) and the **legacy** model ([`:ERROR`](../reference/keywords/ERROR.md) / [`:RESUME`](../reference/keywords/RESUME.md)). New code should use structured handling exclusively.

## Structured error handling

### Basic pattern

```ssl
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
- Use [`RaiseError`](../reference/functions/RaiseError.md) to throw a custom error
- [`:RETURN`](../reference/keywords/RETURN.md), [`:EXITFOR`](../reference/keywords/EXITFOR.md), [`:EXITWHILE`](../reference/keywords/EXITWHILE.md), and [`:LOOP`](../reference/keywords/LOOP.md) inside a [`:FINALLY`](../reference/keywords/FINALLY.md) block are **compile-time errors** — keep cleanup code linear and let it fall through

### Common patterns

#### Try-catch with logging

```ssl
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

### Legacy pattern with :RESUME

When [`:RESUME`](../reference/keywords/RESUME.md) is present inside the [`:ERROR`](../reference/keywords/ERROR.md) block, the compiler wraps **each statement** individually. If a statement fails, the [`:ERROR`](../reference/keywords/ERROR.md) handler runs, then [`:RESUME`](../reference/keywords/RESUME.md) continues execution at the **next** statement after the one that failed.

```ssl
:PROCEDURE LegacyResumeExample;
    :DECLARE sResult;
    /* Each statement below is individually protected;
    sResult := RiskyOperationA();
    sResult := RiskyOperationB();
    sResult := RiskyOperationC();
    :RETURN sResult;
:ERROR;
    /* Runs for whichever statement failed;
    ErrorMes("WARN", "A step failed, continuing");
:RESUME;
:ENDPROC;
```

If `RiskyOperationA()` fails, the [`:ERROR`](../reference/keywords/ERROR.md) handler runs, [`:RESUME`](../reference/keywords/RESUME.md) continues at `RiskyOperationB()`, and so on. Every statement gets a chance to run.

### Legacy pattern without :RESUME

Without [`:RESUME`](../reference/keywords/RESUME.md), the entire procedure body is wrapped in a single try/catch. After the [`:ERROR`](../reference/keywords/ERROR.md) handler runs, execution falls through to [`:ENDPROC`](../reference/keywords/ENDPROC.md) — there is no resumption.

```ssl
:PROCEDURE LegacyNoResumeExample;
    :DECLARE sResult;
    sResult := RiskyOperation();
    :RETURN sResult;
:ERROR;
    /* Runs on any failure; procedure ends after this block;
    ErrorMes("ERROR", "Operation failed");
:ENDPROC;
```

### Key differences from structured handling

| Feature | [`:TRY`](../reference/keywords/TRY.md)/[`:CATCH`](../reference/keywords/CATCH.md) | [`:ERROR`](../reference/keywords/ERROR.md)/[`:RESUME`](../reference/keywords/RESUME.md) |
|---------|-------------|----------------|
| Scope | Block-level | Procedure-level |
| Multiple handlers | One [`:CATCH`](../reference/keywords/CATCH.md) per [`:TRY`](../reference/keywords/TRY.md) | One [`:ERROR`](../reference/keywords/ERROR.md) per procedure |
| Cleanup guarantee | [`:FINALLY`](../reference/keywords/FINALLY.md) always runs | No equivalent |
| Resume point | After [`:ENDTRY`](../reference/keywords/ENDTRY.md) | After the failing statement |
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
