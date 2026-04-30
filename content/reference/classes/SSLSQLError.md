---
title: "SSLSQLError"
summary: "Represents the SQL-specific error object returned after a database failure."
id: ssl.class.sslsqlerror
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SSLSQLError

Represents the SQL-specific error object returned after a database failure.

`SSLSQLError` is the SQL-focused subclass of [`SSLError`](SSLError.md). In SSL code, you normally receive it from [`GetLastSQLError`](../functions/GetLastSQLError.md) or [`ReturnLastSQLError`](../functions/ReturnLastSQLError.md) after a failed database operation.

It adds SQL-specific details such as the captured SQL statement, provider error state text, and combined stack trace while still exposing the inherited diagnostic members from [`SSLError`](SSLError.md).

## When to use

- When you need SQL-specific details after a failed database call.
- When you need the SQL state or SQL text in addition to the usual error description.
- When you need to log database diagnostics without parsing a formatted message.

## Constructors

`SSLSQLError` is normally returned by [`GetLastSQLError()`](../functions/GetLastSQLError.md) or [`ReturnLastSQLError()`](../functions/ReturnLastSQLError.md).

No separate SSL-facing constructor contract is surfaced for normal script use.

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `ErrorMessage` | [string](../types/string.md) | read-only | Combined message text from the captured database exception chain, or `No Exception.` when no message text was captured. |
| `SQLState` | [string](../types/string.md) | read-only | Provider error state or code text captured for the SQL error. |
| `ErrorStackTrace` | [string](../types/string.md) | read-only | Combined stack trace text from the captured exception chain, or `Empty stack trace.` when no stack trace text was captured. |
| `Description` | [string](../types/string.md) | read-only | Alias of `ErrorMessage`. |
| `Operation` | [string](../types/string.md) | read-only | Always returns `SQL operation.` |
| `GenCode` | [number](../types/number.md) | read-only | Numeric code derived from `SQLState`. If `SQLState` is a 9-character provider code, SSL tries its 5-character suffix. Returns `0` when no numeric code can be extracted. |
| `Sql` | [string](../types/string.md) | read-only | SQL statement associated with the captured database error, when available. |

## Methods

`SSLSQLError` does not add documented public methods. Use its properties and the inherited [`SSLError`](SSLError.md) properties for inspection.

## Inheritance

**Base class:** [`SSLError`](SSLError.md)

## Best practices

!!! success "Do"
    - Use `oErr:Description` or `oErr:ErrorMessage` for the primary SQL error text.
    - Check `oErr:SQLState`, `oErr:GenCode`, and `oErr:Sql` together when you need structured diagnostics.
    - Use inherited members such as `oErr:Code`, `oErr:FullDescription`, or `oErr:FullDescriptionEx` when support logging needs more context.

!!! failure "Don't"
    - Assume `oErr:SQLState` uses the same text format for every provider.
    - Treat `oErr:GenCode` as an independently stored database field. SSL derives it from `SQLState`.
    - Show raw SQL text or stack traces directly to end users unless that level of technical detail is intentional.

## Caveats

- `Description` and `ErrorMessage` are the same value, and inherited `Code` returns the same numeric value as `GenCode`.
- `ErrorMessage` and `ErrorStackTrace` can include text from nested causes in the same exception chain.
- Inherited [`SSLError`](SSLError.md) properties such as `FullDescription`, `FullDescriptionEx`, `NETException`, and `InnerException` are still available.

## Examples

### Inspect a failed SQL query

Use [`GetLastSQLError()`](../functions/GetLastSQLError.md) inside [`:CATCH`](../keywords/CATCH.md) to read the SQL-specific details from a failed query.

```ssl
:PROCEDURE ShowLastSqlError;
	:DECLARE sOrdNo, oErr, sMsg;

	sOrdNo := "ORD-100045";

	:TRY;
		SQLExecute("
		    SELECT missing_column
		    FROM ordtask
		    WHERE ordno = ?sOrdNo?
		");

	:CATCH;
		oErr := GetLastSQLError();

		:IF Empty(oErr);
			UsrMes("No SQL error was captured");

			:RETURN;
		:ENDIF;

		sMsg := "Error: " + oErr:Description;
		sMsg += Chr(13) + Chr(10) + "SQLState: " + oErr:SQLState;
		sMsg += Chr(13) + Chr(10) + "GenCode: " + LimsString(oErr:GenCode);
		sMsg += Chr(13) + Chr(10) + "SQL: " + oErr:Sql;

		UsrMes(sMsg); /* Displays SQL error details on failure;
	:ENDTRY;
:ENDPROC;

DoProc("ShowLastSqlError");
```

### Build a support-friendly SQL error report

Use [`ReturnLastSQLError()`](../functions/ReturnLastSQLError.md) when you want to capture structured SQL diagnostics for logging or support workflows.

```ssl
:PROCEDURE BuildSqlErrorReport;
	:DECLARE oErr, oReport;

	:TRY;
		RunSQL("
		    UPDATE ordtask SET
		        missing_column = ?
		    WHERE ordno = ?
		",
			, {"Released", "ORD-100045"});

	:CATCH;
		oErr := ReturnLastSQLError();

		:IF Empty(oErr);
			:RETURN NIL;
		:ENDIF;

		oReport := CreateUdObject();
		oReport:summary := oErr:Description;
		oReport:sqlState := oErr:SQLState;
		oReport:genCode := oErr:GenCode;
		oReport:sqlText := oErr:Sql;
		oReport:details := oErr:FullDescription;

		:RETURN oReport;
	:ENDTRY;

	:RETURN NIL;
:ENDPROC;

DoProc("BuildSqlErrorReport");
```

## Related

- [`GetLastSQLError`](../functions/GetLastSQLError.md)
- [`ReturnLastSQLError`](../functions/ReturnLastSQLError.md)
- [`ClearLastSSLError`](../functions/ClearLastSSLError.md)
- [`SSLError`](SSLError.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
- [`object`](../types/object.md)
