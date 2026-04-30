---
title: "FormatSqlErrorMessage"
summary: "Returns a human-readable error message from a SQL error value."
id: ssl.function.formatsqlerrormessage
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# FormatSqlErrorMessage

Returns a human-readable error message from a SQL error value.

`FormatSqlErrorMessage` is the SQL-context companion to [`FormatErrorMessage`](FormatErrorMessage.md) and behaves identically. If `vError` is an [`SSLError`](../classes/SSLError.md) object, it returns the error's full description string (`FullDescription`). For any other value, including [`NIL`](../literals/nil.md), empty, or a non-error type, the function returns `"Unknown error."`. The function always returns a valid string.

## When to use

- When displaying SQL error messages to users or administrators after a failed operation.
- When logging SQL errors in a readable format for troubleshooting or review.
- When integrating with other systems that require string error messages rather than error objects.
- When you need to safely handle error values that may not always be structured or may be null.

## Syntax

```ssl
FormatSqlErrorMessage(vError)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vError` | any | yes | — | The error value to format. Pass an SSLError object to extract its full description, or any other value to receive `"Unknown error."`. |

## Returns

**[string](../types/string.md)** — The [`SSLError`](../classes/SSLError.md)'s full description (`FullDescription`) when `vError` is an [`SSLError`](../classes/SSLError.md) object, or `"Unknown error."` for any other input.

## Best practices

!!! success "Do"
    - Always use this function before displaying or logging SQL errors.
    - Handle the possibility of `"Unknown error."` as a return value in your user interface.
    - Use in combination with error retrieval functions like [`GetLastSQLError`](GetLastSQLError.md).

!!! failure "Don't"
    - Extract message properties directly from the error object; use this function to ensure consistent formatting and avoid runtime errors with unexpected value types.
    - Assume all errors will contain detailed or helpful information — non-[`SSLError`](../classes/SSLError.md) values always fall back to `"Unknown error."`.
    - Rely solely on raw SQL error output in user-facing processes.

## Caveats

- The returned message is only as descriptive as the error object provided; incomplete or malformed errors yield less helpful text.

## Examples

### Log a failed SQL operation

Capture and log a formatted error message after a SQL operation fails.

```ssl
:PROCEDURE DisplaySqlErrorExample;
	:DECLARE sSql, sUserMessage;

	sSql := "
	    SELECT *
	    FROM nonexistenttable
	";

	:TRY;
		SQLExecute(sSql);
	:CATCH;
		sUserMessage := FormatSqlErrorMessage(GetLastSQLError());
		ErrorMes(sUserMessage);
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("DisplaySqlErrorExample");
```

`ErrorMes` displays:

```text
The formatted SQL error message returned by GetLastSQLError
```

## Related

- [`ClearLastSSLError`](ClearLastSSLError.md)
- [`GetLastSQLError`](GetLastSQLError.md)
- [`ReturnLastSQLError`](ReturnLastSQLError.md)
- [`SSLError`](../classes/SSLError.md)
- [`string`](../types/string.md)
