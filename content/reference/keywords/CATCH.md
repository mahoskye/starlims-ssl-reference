---
title: "CATCH"
summary: "Handles errors raised in the immediately preceding :TRY block."
id: ssl.keyword.catch
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
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
- Keywords are case-sensitive and must be written in uppercase.

## Examples

### Catch a runtime error and show the error text

Use `:CATCH` to intercept a failed query and display the error description. Either the query succeeds and [`UsrMes`](../functions/UsrMes.md) shows the row count, or `:CATCH` runs and reports the failure message.

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
		/* Displays loaded row count;

	:CATCH;
		oErr := GetLastSSLError();
		sErrMsg := "Sample query failed: " + oErr:Description;
		UsrMes(sErrMsg);
		/* Displays query failure message;

	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ConnectToSamples");
```

### Branch on error type and use FINALLY for shared cleanup

Use a [`:BEGINCASE`](BEGINCASE.md) inside `:CATCH` to route different error codes to different handlers. [`:FINALLY`](FINALLY.md) runs unconditionally to report the final outcome.

```ssl
:PROCEDURE ProcessSampleData;
	:DECLARE sSampleID, sSQL, sLogMessage;
	:DECLARE oErr, aResults, nIndex, nTotal;
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
			RaiseError("No sample found with ID: " + sSampleID);
		:ENDIF;

		:FOR nIndex := 1 :TO ALen(aResults);
			sLogMessage := "Processing row " + LimsString(nIndex);
			UsrMes(sLogMessage);
			/* Displays current row being processed;

			:IF Empty(aResults[nIndex, 1]);
				RaiseError("Empty result value at row " + LimsString(nIndex));
			:ENDIF;

			nTotal += aResults[nIndex, 1];
		:NEXT;

	:CATCH;
		oErr := GetLastSSLError();

		:BEGINCASE;
		:CASE oErr:Code == 207;
			bValidationError := .T.;
			sLogMessage := "Validation failed: " + oErr:Description;
			UsrMes(sLogMessage);
			/* Displays validation failure message;
			:EXITCASE;
		:CASE oErr:Code == 208;
			bDbError := .T.;
			sLogMessage := "Database error in query: " + oErr:Operation;
			ErrorMes(sLogMessage);
			/* Displays database failure message;
			:EXITCASE;
		:OTHERWISE;
			sLogMessage := "Unexpected error (" + LimsString(oErr:Code) + "): "
				+ oErr:Description;
			ErrorMes(sLogMessage);
			/* Displays unexpected failure message;
			:EXITCASE;
		:ENDCASE;

		bSuccess := .F.;

	:FINALLY;
		:IF bSuccess;
			UsrMes("Processing completed successfully. Total: " + LimsString(nTotal));
			/* Displays completion total;
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
