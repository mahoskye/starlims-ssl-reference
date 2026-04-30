---
title: "SSLError"
summary: "Represents an SSL error and exposes its message, location, code, formatted diagnostic text, and nested SSL error details."
id: ssl.class.sslerror
element_type: class
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SSLError

Represents an SSL error and exposes its message, location, code, formatted diagnostic text, and nested SSL error details.

`SSLError` is the standard error object used by SSL error handling. You usually get one from [`GetLastSSLError`](../functions/GetLastSSLError.md) inside a [`:CATCH`](../keywords/CATCH.md) block rather than constructing it directly. The object gives you the main error text through `Description`, the reported location through `Operation`, the numeric code through `Code`, and expanded diagnostic text through `FullDescription` and `FullDescriptionEx`.

## When to use

- When you need to inspect the error captured by [`GetLastSSLError()`](../functions/GetLastSSLError.md).
- When you need user-facing error text from `:Description` or `:Message`.
- When you need diagnostic output that includes stack details or nested errors.

## Constructors

### `SSLError{oException}`

Wraps an exception object as an `SSLError`. In normal SSL code, use [`GetLastSSLError()`](../functions/GetLastSSLError.md) instead of constructing `SSLError` yourself.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `oException` | [object](../types/object.md) | yes | Exception object to wrap. |

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `RuntimeException` | [object](../types/object.md) | read-only | Low-level exception object. Prefer `Description`, `Operation`, `Code`, or `FullDescription` for typical error handling. |
| `Description` | [string](../types/string.md) | read-only | Primary error message text. |
| `Operation` | [string](../types/string.md) | read-only | Reported error location or operation name. This can be empty. |
| `GenCode` | [number](../types/number.md) | read-only | Numeric error code. |
| `Code` | [number](../types/number.md) | read-only | Alias of `GenCode`. |
| `FullDescription` | [string](../types/string.md) | read-only | Multi-line diagnostic text with abbreviated stack details and nested causes. |
| `FullDescriptionEx` | [string](../types/string.md) | read-only | Multi-line diagnostic text with full stack details and nested causes. |
| `NETException` | [object](../types/object.md) | read-only | Low-level exception object for advanced troubleshooting or interop scenarios. |
| `InnerException` | `SSLError` | read-only | Nested SSL error when the inner cause is also an SSL runtime error. Otherwise this is empty. |
| `Message` | [string](../types/string.md) | read-only | Alias of `Description`. |

## Methods

`SSLError` does not expose documented public methods. Use its properties to inspect the error.

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Read `oErr:Description` for user-facing error text after [`GetLastSSLError()`](../functions/GetLastSSLError.md).
    - Use `oErr:Code` and `oErr:Operation` when you need structured diagnostics.
    - Use `oErr:FullDescriptionEx` for support logs when you need the complete stack trace.

!!! failure "Don't"
    - Assume `oErr:InnerException` is always available or that it contains every nested cause. Only nested SSL runtime errors surface there.
    - Show `FullDescription` or `FullDescriptionEx` directly to end users unless they need technical diagnostics.
    - Rely on `Operation` or `Code` being populated when you build an `SSLError` from an arbitrary exception object.

## Caveats

- `InnerException` only returns nested SSL runtime errors, not every possible nested cause.
- `Operation` can be blank and `Code` can be `0` when the source error did not provide them.
- `FullDescription` and `FullDescriptionEx` are formatted diagnostic strings, not structured field-by-field data.
- `FullDescriptionEx` includes the full stack trace when one is available; `FullDescription` uses a shorter stack view.
- For compiler errors, SQL errors, and script-not-found errors, the formatted diagnostic text uses specialized headings instead of a generic `Error:` line.
- When constructing `SSLError` from an arbitrary exception, `Operation` defaults to blank and `Code` to `0` unless the wrapped exception already carried that information.

## Examples

### Inspecting the last SSL error

Uses [`GetLastSSLError()`](../functions/GetLastSSLError.md) inside [`:CATCH`](../keywords/CATCH.md) to read the message, operation, and code from the captured error object, then displays them as a single formatted string.

```ssl
:PROCEDURE ShowErrorSummary;
    :DECLARE oErr, sMsg;

    :TRY;
        RaiseError("Sample approval failed", "ApproveSample", 1201);
    :CATCH;
        oErr := GetLastSSLError();

        :IF Empty(oErr);
            UsrMes("No error was captured");

            :RETURN;
        :ENDIF;

        sMsg := "Error: " + oErr:Description;
        sMsg := sMsg + Chr(13) + Chr(10)
            + "Operation: " + oErr:Operation;
        sMsg := sMsg + Chr(13) + Chr(10)
            + "Code: " + LimsString(oErr:Code);

        /* Displays the captured error summary;
        UsrMes(sMsg);
    :ENDTRY;
:ENDPROC;

DoProc("ShowErrorSummary");
```

### Working with nested errors

Uses a nested [`:TRY`](../keywords/TRY.md) to raise a first error, then raises a second error that wraps it via [`GetLastSSLError()`](../functions/GetLastSSLError.md). The outer [`:CATCH`](../keywords/CATCH.md) reads `FullDescription` for the top-level diagnostic text and appends the inner cause description when `InnerException` is populated.

```ssl
:PROCEDURE ShowNestedError;
    :DECLARE oErr, sReport;

    :TRY;
        :TRY;
            RaiseError("Result row is locked", "LoadResult", 2201);
        :CATCH;
            RaiseError(
                "Could not complete sample release",
                "ReleaseSample",
                2202,
                GetLastSSLError()
            );
        :ENDTRY;
    :CATCH;
        oErr := GetLastSSLError();
        sReport := oErr:FullDescription;

        :IF .NOT. Empty(oErr:InnerException);
            sReport := sReport + Chr(13) + Chr(10)
                + "Root cause: " + oErr:InnerException:Description;
        :ENDIF;

        /* Displays the formatted error report;
        UsrMes(sReport);
    :ENDTRY;
:ENDPROC;

DoProc("ShowNestedError");
```

## Related

- [`GetLastSSLError`](../functions/GetLastSSLError.md)
- [`ClearLastSSLError`](../functions/ClearLastSSLError.md)
- [`RaiseError`](../functions/RaiseError.md)
- [`SSLSQLError`](SSLSQLError.md)
