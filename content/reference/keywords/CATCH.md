---
title: "CATCH"
summary: "Handles errors raised in the immediately preceding :TRY block."
id: ssl.keyword.catch
element_type: keyword
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# CATCH

Handles errors raised in the immediately preceding [`:TRY`](TRY.md) block.

The `:CATCH` keyword starts the error-handling branch of a [`:TRY`](TRY.md) block. When any statement in the preceding [`:TRY`](TRY.md) body raises an error, control transfers to `:CATCH`, where you can inspect [`GetLastSSLError`](../functions/GetLastSSLError.md), log the failure, show a message, or prepare a fallback result.

`:CATCH` must appear after the [`:TRY`](TRY.md) statements and before an optional [`:FINALLY`](FINALLY.md). A [`:TRY`](TRY.md) block can have at most one `:CATCH`, and `:CATCH` does not accept an exception variable or error-type filter. After the `:CATCH` block runs, execution continues to [`:FINALLY`](FINALLY.md) when present, otherwise to [`:ENDTRY`](ENDTRY.md).

## When to use

- When you need to recover from any error that occurs within a block of code, performing cleanup, compensation, or user notification before resuming or halting execution.
- When logging or auditing error conditions before ending execution or continuing is essential.
- When you need to prevent program termination from unhandled failures by responding to unexpected errors.

## Syntax

```ssl
:CATCH;
```

## Keyword group

**Group:** Error Handling
**Role:** modifier

## Best practices

!!! success "Do"
    - Keep `:CATCH` focused on the specific work performed in the preceding [`:TRY`](TRY.md) block.
    - Retrieve the current error with [`GetLastSSLError`](../functions/GetLastSSLError.md) and use `oErr:Description` when you need message text.
    - Put cleanup that must run on both success and failure in [`:FINALLY`](FINALLY.md).

!!! failure "Don't"
    - Use one `:CATCH` block to handle unrelated work from distant parts of a procedure — keep it paired closely with its [`:TRY`](TRY.md) so the recovery logic stays predictable.
    - Rely on `:CATCH` alone for required cleanup. If no error occurs, `:CATCH` is skipped, but [`:FINALLY`](FINALLY.md) still runs.

## Caveats

- `:CATCH` cannot appear outside a [`:TRY`](TRY.md) block.
- A `:CATCH` block may be empty, but the preceding [`:TRY`](TRY.md) body must contain at least one statement.
- `:CATCH` handles all errors from that [`:TRY`](TRY.md) block; you cannot declare multiple typed catches.
- If the [`:TRY`](TRY.md) block has no `:CATCH`, the error propagates unless another outer handler intercepts it.
- Do not rely on `:CATCH` running when the procedure also contains a legacy [`:ERROR`](ERROR.md) handler that ends with [`:RESUME`](RESUME.md). In observed runtime behavior the legacy handler takes the error, `:CATCH` is bypassed, and the [`:TRY`](TRY.md) body continues at the statement after the one that failed. Without `:RESUME`, `:CATCH` handles the error as usual. See [Error Handling](../../guides/error-handling.md#do-not-mix-errorresume-with-trycatch).
- Keywords are case-sensitive and must be written in uppercase.

## Examples

### Catch a runtime error and show the error text

Use `:CATCH` to intercept a failed query and log the error description. Either the query succeeds and [`UsrMes`](../functions/UsrMes.md) logs the row count, or `:CATCH` runs and reports the failure message.

```ssl
:PROCEDURE ConnectToSamples;
	:DECLARE sSampleID, sSQL, oErr, sErrMsg, aRows;

	sSampleID := "S-1001";

	sSQL := "
	    SELECT sample_id, status
	    FROM sample
	    WHERE sample_id = ?sSampleID?
	";

/* Handle a failed query and report the error to the user;
	:TRY;
		aRows := SQLExecute(sSQL);
		UsrMes("Loaded " + LimsString(ALen(aRows)) + " row(s).");
		/* Logs loaded row count;

	:CATCH;
		oErr := GetLastSSLError();
		sErrMsg := "Sample query failed: " + oErr:Description;
		UsrMes(sErrMsg);
		/* Logs query failure message;

	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ConnectToSamples");
```

### Branch on error type and use FINALLY for shared cleanup

Use a [`:BEGINCASE`](BEGINCASE.md) inside `:CATCH` to route different errors to different handlers. Validation errors are raised with code `1001` and recognized through `oErr:Code`. A SQL Server error reports `Code` as `0`, so the SQL Server error number (`207` for an invalid column, `208` for an invalid object) is read from `GenCode` on [`GetLastSQLError`](../functions/GetLastSQLError.md)`()`. [`:FINALLY`](FINALLY.md) runs unconditionally to report the final outcome.

```ssl
:PROCEDURE ProcessSampleData;
	:DECLARE sSampleID, sSQL, sLogMessage;
	:DECLARE oErr, oSqlErr, nSqlCode, aResults, nIndex, nTotal;
	:DECLARE bSuccess, bValidationError, bDbError;

	sSampleID := "LAB-2024-0042";
	nTotal := 0;
	bSuccess := .T.;
	bValidationError := .F.;
	bDbError := .F.;

	sSQL := "
	    SELECT result_value
	    FROM sample_result
	    WHERE sample_id = ?sSampleID?
	    ORDER BY result_no
	";

	:TRY;
		aResults := SQLExecute(sSQL);

		:IF ALen(aResults) == 0;
			RaiseError("No sample found with ID: " + sSampleID, "ProcessSampleData", 1001);
		:ENDIF;

		:FOR nIndex := 1 :TO ALen(aResults);
			sLogMessage := "Processing row " + LimsString(nIndex);
			UsrMes(sLogMessage);
			/* Logs current row being processed;

			:IF Empty(aResults[nIndex, 1]);
				RaiseError("Empty result value at row " + LimsString(nIndex), "ProcessSampleData",
					1001);
			:ENDIF;

			nTotal += aResults[nIndex, 1];
		:NEXT;

	:CATCH;
		oErr := GetLastSSLError();
		nSqlCode := 0;

		/* SQL Server error numbers are in GenCode on the SQL error object, not in oErr:Code;
		oSqlErr := GetLastSQLError();
		:IF !Empty(oSqlErr);
			nSqlCode := oSqlErr:GenCode;
		:ENDIF;

		:BEGINCASE;
		:CASE oErr:Code == 1001;
			bValidationError := .T.;
			sLogMessage := "Validation failed: " + oErr:Description;
			UsrMes(sLogMessage);
			/* Logs validation failure message;
			:EXITCASE;
		:CASE nSqlCode == 207 .OR. nSqlCode == 208;
			bDbError := .T.;
			sLogMessage := "Database error " + LimsString(nSqlCode) + " in query: "
				+ oErr:Description;
			ErrorMes(sLogMessage);
			/* Logs database failure message;
			:EXITCASE;
		:OTHERWISE;
			sLogMessage := "Unexpected error: " + oErr:Description;
			ErrorMes(sLogMessage);
			/* Logs unexpected failure message;
			:EXITCASE;
		:ENDCASE;

		bSuccess := .F.;

	:FINALLY;
		:IF bSuccess;
			UsrMes("Processing completed successfully. Total: " + LimsString(nTotal));
			/* Logs completion total;
		:ELSE;
			:IF bValidationError;
				UsrMes("Please review data and resubmit.");
			:ENDIF;
			:IF bDbError;
				UsrMes("Database error occurred. Contact system administrator.");
			:ENDIF;
		:ENDIF;

	:ENDTRY;

	:RETURN bSuccess;
:ENDPROC;

/* Usage;
DoProc("ProcessSampleData");
```

## Related

- [`TRY`](TRY.md)
- [`FINALLY`](FINALLY.md)
- [`ENDTRY`](ENDTRY.md)
- [`ERROR`](ERROR.md)
- [`RESUME`](RESUME.md)
