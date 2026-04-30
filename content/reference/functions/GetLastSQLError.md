---
title: "GetLastSQLError"
summary: "Returns the most recently stored SQL error as an SSLSQLError object, or NIL when no SQL error is currently recorded."
id: ssl.function.getlastsqlerror
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetLastSQLError

Returns the most recently stored SQL error as an [`SSLSQLError`](../classes/SSLSQLError.md) object, or [`NIL`](../literals/nil.md) when no SQL error is currently recorded.

`GetLastSQLError` is the SSL-facing alias of [`ReturnLastSQLError`](ReturnLastSQLError.md). It gives you the current database error object after a failing SQL operation so you can inspect members such as `Description`, `SQLState`, `GenCode`, `Sql`, and `ErrorStackTrace`.

The function does not take parameters and does not create a new error object. It returns the SQL error currently stored by the database library, if one is available.

## When to use

- When you need SQL-specific diagnostics immediately after a database call fails.
- When you want structured error details instead of only a formatted message.
- When support or logging code needs the SQL text, SQL state, or numeric error code from the last failure.

## Syntax

```ssl
GetLastSQLError()
```

## Parameters

This function takes no parameters.

## Returns

**[SSLSQLError](../classes/SSLSQLError.md)** — The current SQL error object when a database operation has stored an error. Returns [`NIL`](../literals/nil.md) when no SQL error is currently recorded.

## Best practices

!!! success "Do"
    - Call `GetLastSQLError()` immediately after the failing database operation or inside the matching [`:CATCH`](../keywords/CATCH.md) block.
    - Check for [`NIL`](../literals/nil.md) before reading properties from the returned object.
    - Use [`FormatSqlErrorMessage`](FormatSqlErrorMessage.md) when you need a display-ready message, and inspect `SQLState`, `GenCode`, or `Sql` when you need structured diagnostics.

!!! failure "Don't"
    - Assume a value is always returned. A later database call may leave you with [`NIL`](../literals/nil.md) or a different SQL error state.
    - Assume this function returns general non-database exceptions. It is specifically for the database library's stored SQL error.
    - Show raw SQL text or stack traces to end users unless that level of technical detail is intentional.

## Caveats

- This function reports the SQL error currently stored by the database library, not a snapshot taken at call time.
- Later database operations can clear or replace the stored SQL error before you read it.

## Examples

### Read the SQL error inside [`:CATCH`](../keywords/CATCH.md)

Runs a [`RunSQL`](RunSQL.md) call that references a non-existent column, catches the failure in [`:CATCH`](../keywords/CATCH.md), reads the error object, and displays the description with [`ErrorMes`](ErrorMes.md).

```ssl
:PROCEDURE ShowLastSqlError;
	:DECLARE bSuccess, oSqlErr, sMessage;

	bSuccess := .F.;

	:TRY;
		bSuccess := RunSQL("
		    UPDATE ordtask SET
		        missing_column = ?
		    WHERE ordno = ?
		",, {"Released", "ORD-100045"});
	:CATCH;
		oSqlErr := GetLastSQLError();

		:IF !Empty(oSqlErr);
			sMessage := "Database update failed: " + oSqlErr:Description;
			ErrorMes(sMessage);
		:ENDIF;
	:ENDTRY;

	:RETURN bSuccess;
:ENDPROC;

/* Usage;
DoProc("ShowLastSqlError");
```

### Return structured diagnostics for support code

Extracts individual [`SSLSQLError`](../classes/SSLSQLError.md) properties after a failed [`SQLExecute`](SQLExecute.md) call and packs them into a diagnostic object, returning [`NIL`](../literals/nil.md) when no error object is available.

```ssl
:PROCEDURE BuildSqlDiagnostic;
	:DECLARE sOrdNo, oSqlErr, oDiag;

	sOrdNo := "ORD-100045";

	:TRY;
		SQLExecute("
		    SELECT missing_column
		    FROM ordtask
		    WHERE ordno = ?sOrdNo?
		");
	:CATCH;
		oSqlErr := GetLastSQLError();

		:IF Empty(oSqlErr);
			:RETURN NIL;
		:ENDIF;

		oDiag := CreateUdObject();
		oDiag:description := oSqlErr:Description;
		oDiag:sqlState := oSqlErr:SQLState;
		oDiag:genCode := oSqlErr:GenCode;
		oDiag:sqlText := oSqlErr:Sql;

		:RETURN oDiag;
	:ENDTRY;

	:RETURN NIL;
:ENDPROC;

/* Usage;
DoProc("BuildSqlDiagnostic");
```

### Combine a formatted message with raw SQL diagnostics

Uses [`FormatSqlErrorMessage`](FormatSqlErrorMessage.md) for a user-facing string alongside raw properties (`SQLState`, `GenCode`, `Sql`, `ErrorStackTrace`) packed into a support ticket object.

```ssl
:PROCEDURE CaptureSqlFailureForSupport;
	:DECLARE sOrdNo, oSqlErr, oTicket, sFormatted;

	sOrdNo := "ORD-100045";

	:TRY;
		SQLExecute("
		    SELECT missing_column
		    FROM ordtask
		    WHERE ordno = ?sOrdNo?
		");
	:CATCH;
		oSqlErr := GetLastSQLError();

		:IF Empty(oSqlErr);
			:RETURN NIL;
		:ENDIF;

		sFormatted := FormatSqlErrorMessage(oSqlErr);

		oTicket := CreateUdObject();
		oTicket:userMessage := sFormatted;
		oTicket:sqlState := oSqlErr:SQLState;
		oTicket:genCode := oSqlErr:GenCode;
		oTicket:sqlText := oSqlErr:Sql;
		oTicket:stackTrace := oSqlErr:ErrorStackTrace;

		:RETURN oTicket;
	:ENDTRY;

	:RETURN NIL;
:ENDPROC;

/* Usage;
DoProc("CaptureSqlFailureForSupport");
```

## Related

- [`ReturnLastSQLError`](ReturnLastSQLError.md)
- [`FormatSqlErrorMessage`](FormatSqlErrorMessage.md)
- [`ClearLastSSLError`](ClearLastSSLError.md)
- [`SSLSQLError`](../classes/SSLSQLError.md)
