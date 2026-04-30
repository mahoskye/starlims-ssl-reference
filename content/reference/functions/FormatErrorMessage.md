---
title: "FormatErrorMessage"
summary: "Returns a formatted string description for an error value."
id: ssl.function.formaterrormessage
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# FormatErrorMessage

Returns a formatted string description for an error value.

If `vError` is an [`SSLError`](../classes/SSLError.md) object, `FormatErrorMessage` returns the error's full description string (`FullDescription`), which is a richer representation than the plain `Description` property available on the object directly. For any other value — including null, empty, or a non-error type — the function returns `"Unknown error."`. The function always returns a valid string.

## When to use

- When you need a clear, user-friendly error message for logs, alerts, or interfaces.
- When handling error values of uncertain or mixed type and want graceful messaging.
- When integrating with code that expects error messages in string format, such as audit trails, notifications, or status reports.
- When you want to avoid displaying low-level object output for failed or unexpected error state values.

## Syntax

```ssl
FormatErrorMessage(vError)
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `vError` | any | yes | — | The error value to format. Pass an SSLError object to extract its full description, or any other value to receive `"Unknown error."`. |

## Returns

**[string](../types/string.md)** — The [`SSLError`](../classes/SSLError.md)'s full description (`FullDescription`) when `vError` is an [`SSLError`](../classes/SSLError.md) object, or `"Unknown error."` for any other input.

## Best practices

!!! success "Do"
    - Always use this function before displaying or logging error values of unknown type.
    - Use this along with error-handling flows that may produce non-error values, especially in catch-all logic.
    - Test with both error and non-error values to validate the user experience of error reporting.

!!! failure "Don't"
    - Assume every input produces a meaningful description — non-SSLError values always fall back to `"Unknown error."`.
    - Cast or convert error objects to string directly; direct conversion may produce technical or unhelpful output.
    - Expect nested or compound error details; only the top-level description is returned.

## Caveats

- Custom error types not based on the standard [`SSLError`](../classes/SSLError.md) structure produce `"Unknown error."`, not their specific fields.

## Examples

### Format a caught error for logging

Turn an SSLError value from a [`:CATCH`](../keywords/CATCH.md) block into a readable log message.

```ssl
:PROCEDURE LogCaughtError;
	:DECLARE oErr, sFormatted;

	:TRY;
		SQLExecute("
		    SELECT *
		    FROM nonexistenttable
		    ");
	:CATCH;
		oErr := GetLastSSLError();
		sFormatted := FormatErrorMessage(oErr);
		ErrorMes("Query failed", sFormatted);
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("LogCaughtError");
```

`ErrorMes` displays a dialog with caption `Query failed` and the formatted SQL error message text.

### Handle a return value of unknown type

Format a result that may be an SSLError object or a plain value — the function returns a usable string either way.

```ssl
:PROCEDURE ReportServiceResult;
	:PARAMETERS vResult;
	:DECLARE sMessage;

	sMessage := FormatErrorMessage(vResult);
	ErrorMes("Service error", sMessage);
:ENDPROC;

/* Usage;
DoProc("ReportServiceResult", {oErr});
```

`ErrorMes` displays a dialog with caption `Service error` and the formatted message string.

## Related

- [`ClearLastSSLError`](ClearLastSSLError.md)
- [`GetLastSSLError`](GetLastSSLError.md)
- [`RaiseError`](RaiseError.md)
- [`SSLError`](../classes/SSLError.md)
- [`string`](../types/string.md)
