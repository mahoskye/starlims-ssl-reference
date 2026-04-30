---
title: "GetLastSSLError"
summary: "Retrieves the most recent SSL error encountered during the current process."
id: ssl.function.getlastsslerror
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetLastSSLError

Retrieves the most recent SSL error encountered during the current process.

`GetLastSSLError` returns the current stored [`SSLError`](../classes/SSLError.md) object. If no error has been recorded, it returns [`NIL`](../literals/nil.md). Calling the function does not clear the stored error.

Use it after a failed operation, typically inside [`:CATCH`](../keywords/CATCH.md), when you need to inspect properties such as `:Description`, `:Operation`, `:Code`, `:FullDescription`, or `:InnerException`.

## When to use

- When implementing robust error handling that inspects the details of the last SSL failure before taking action.
- When logging or displaying user-friendly error information after operations that might fail.
- When developing automated diagnostics or error reporting features that need the full context of recent SSL errors.
- When you need to determine if an error occurred since the last reset and respond accordingly.

## Syntax

```ssl
GetLastSSLError()
```

## Parameters

This function takes no parameters.

## Returns

**[SSLError](../classes/SSLError.md)** — The current stored error object. Returns [`NIL`](../literals/nil.md) when no error has been recorded.

## Best practices

!!! success "Do"
    - Call `GetLastSSLError` inside [`:CATCH`](../keywords/CATCH.md) blocks when you need details about the failure.
    - Check `Empty(oErr)` before reading error properties when the call might happen outside a guaranteed failure path.
    - Clear handled errors with [`ClearLastSSLError`](ClearLastSSLError.md) so later checks do not reuse stale state.

!!! failure "Don't"
    - Assume the function creates a default error object when no error exists. It returns [`NIL`](../literals/nil.md).
    - Keep reusing the same stored error after you have finished handling it.
    - Show raw diagnostic detail to end users unless that level of detail is appropriate for the situation.

## Caveats

- A previously handled error remains available until you call [`ClearLastSSLError`](ClearLastSSLError.md).

## Examples

### Display an error message after a save fails

Show a message to a user if saving a record fails, using details from the last error.

```ssl
:PROCEDURE SaveSampleRecord;
	:DECLARE sSampleID, sStatus, bSuccess, oErr, sErrMsg;
	:DECLARE sSQL;

	sSampleID := "SAMPLE-2024-001";
	sStatus := "A";
	sSQL := "
	    UPDATE sample SET
	        status = ?
	    WHERE sampleid = ?
	";

	:TRY;
		bSuccess := RunSQL(sSQL,, {sStatus, sSampleID});
		:IF bSuccess;
			UsrMes("Record saved successfully");
		:ENDIF;
	:CATCH;
		oErr := GetLastSSLError();

		:IF ! Empty(oErr);
			sErrMsg := "Save failed: " + oErr:Description;
			ErrorMes(sErrMsg);
		:ENDIF;
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("SaveSampleRecord");
```

### Log comprehensive error details for debugging

Capture and log comprehensive error details after any SSL exception to support debugging.

```ssl
:PROCEDURE LogFailureDetails;
	:DECLARE sInput, oErr, sLogMessage;

	sInput := "bad-value";

	:TRY;
		RaiseError(
			"Validation failed for input " + sInput,
			"LogFailureDetails",
			1001,
			NIL
		);
	:CATCH;
		oErr := GetLastSSLError();

		:IF ! Empty(oErr);
			sLogMessage := "Message: " + oErr:Description + Chr(10);
			sLogMessage := sLogMessage + "Operation: " + oErr:Operation + Chr(10);
			sLogMessage := sLogMessage + "Code: " + LimsString(oErr:Code) + Chr(10);
			sLogMessage := sLogMessage + oErr:FullDescription;
			ErrorMes(sLogMessage); /* Displays error details for debugging;
		:ENDIF;

		ClearLastSSLError();
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("LogFailureDetails");
```

### Inspect a chain of inner exceptions

Inspect nested error information to diagnose compound or wrapped failures.

```ssl
:PROCEDURE InspectErrorChain;
	:DECLARE oErr, oInner, sChain, nDepth;

	:TRY;
		:TRY;
			RaiseError(
				"Connection timeout after 30 seconds",
				"Database.ADODB",
				20001,
				NIL
			);
		:CATCH;
			oErr := GetLastSSLError();
		:ENDTRY;

		RaiseError(
			"Data retrieval failed",
			"DataLayer.GetSamples",
			10001,
			oErr
		);
	:CATCH;
		oErr := GetLastSSLError();

		:IF ! Empty(oErr);
			nDepth := 0;
			sChain := "Top error: " + oErr:Description + Chr(10);
			sChain := sChain + "Operation: " + oErr:Operation + Chr(10);

			oInner := oErr:InnerException;
			:WHILE ! Empty(oInner);
				nDepth := nDepth + 1;
				sChain := sChain + "Level " + LimsString(nDepth);
				sChain := sChain + ": [" + LimsString(oInner:Code) + "] ";
				sChain := sChain + oInner:Description + Chr(10);

				oInner := oInner:InnerException;
			:ENDWHILE;

			ErrorMes(sChain); /* Displays nested error details;
		:ENDIF;
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("InspectErrorChain");
```

## Related

- [`ClearLastSSLError`](ClearLastSSLError.md)
- [`FormatErrorMessage`](FormatErrorMessage.md)
- [`RaiseError`](RaiseError.md)
- [`SSLError`](../classes/SSLError.md)
