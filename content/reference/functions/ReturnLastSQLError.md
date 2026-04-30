---
title: "ReturnLastSQLError"
summary: "Returns the currently stored SQL error as an SSLSQLError object, or NIL when no SQL error is recorded."
id: ssl.function.returnlastsqlerror
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ReturnLastSQLError

Returns the currently stored SQL error as an [`SSLSQLError`](../classes/SSLSQLError.md) object, or [`NIL`](../literals/nil.md) when no SQL error is recorded.

`ReturnLastSQLError()` is a zero-parameter getter for the database library's current SQL error state. It returns the same stored value as [`GetLastSQLError()`](GetLastSQLError.md): when a database operation stores a SQL error, the function returns an [`SSLSQLError`](../classes/SSLSQLError.md); otherwise it returns [`NIL`](../literals/nil.md).

## When to use

- When you need SQL-specific diagnostics immediately after a database call
  fails.
- When you want structured error details instead of only a formatted message.
- When support or logging code needs fields such as `Description`, `SQLState`, `GenCode`, or `Sql` from the last SQL failure.

## Syntax

```ssl
ReturnLastSQLError()
```

## Parameters

This function takes no parameters.

## Returns

**[`SSLSQLError`](../classes/SSLSQLError.md)** — The stored SQL error object. Returns [`NIL`](../literals/nil.md) when no SQL error is currently recorded.

## Best practices

!!! success "Do"
    - Call `ReturnLastSQLError()` immediately after the failing database operation or inside the matching [`:CATCH`](../keywords/CATCH.md) block.
    - Check for [`NIL`](../literals/nil.md) before reading properties from the returned object.
    - Use [`FormatSqlErrorMessage`](FormatSqlErrorMessage.md) when you need a display-ready string, and inspect members such as `Description`, `SQLState`, `GenCode`, or `Sql` when you need structured diagnostics.

!!! failure "Don't"
    - Assume a value is always returned. A later database call may leave you with [`NIL`](../literals/nil.md) or a different SQL error state.
    - Treat this as a general SSL error function. It returns the database library's stored SQL error only.
    - Rely on [`ClearLastSSLError`](ClearLastSSLError.md) to reset this value. That function clears the general SSL error state, not the SQL error exposed here.

## Caveats

- This function returns the SQL error currently stored by the database library, not a snapshot taken earlier.

## Examples

### Read the SQL error inside [`:CATCH`](../keywords/CATCH.md)

Attempt a database write that references a non-existent column, then retrieve and display the SQL error when the operation is caught.

```ssl
:PROCEDURE ShowLastSqlError;
	:DECLARE oSqlErr, sMessage;

	:TRY;
		RunSQL("
		    UPDATE ordtask SET
		        missing_column = ?
		    WHERE ordno = ?
		",
			, {"Released", "ORD-100045"});
	:CATCH;
		oSqlErr := ReturnLastSQLError();

		:IF !Empty(oSqlErr);
			sMessage := "Database update failed: " + oSqlErr:Description;
			ErrorMes(sMessage);
		:ENDIF;
	:ENDTRY;
:ENDPROC;
```

`ErrorMes` displays:

```text
Database update failed: <SQL error description>
```

Call it with `DoProc("ShowLastSqlError");`.

### Return structured SQL diagnostics from a [`:CATCH`](../keywords/CATCH.md) block

Build a plain object from the caught SQL error's fields so a caller can log or display individual diagnostics without string formatting.

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
		oSqlErr := ReturnLastSQLError();

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
```

Call it with `DoProc("BuildSqlDiagnostic");`.

## Related

- [`ClearLastSSLError`](ClearLastSSLError.md)
- [`FormatSqlErrorMessage`](FormatSqlErrorMessage.md)
- [`GetLastSQLError`](GetLastSQLError.md)
- [`SSLSQLError`](../classes/SSLSQLError.md)
