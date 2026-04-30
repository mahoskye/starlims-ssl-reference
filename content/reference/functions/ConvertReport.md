---
title: "ConvertReport"
summary: "Converts a report file identified by a file path and returns .T. when the conversion completes."
id: ssl.function.convertreport
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ConvertReport

Converts a report file identified by a file path and returns [`.T.`](../literals/true.md) when the conversion completes.

`ConvertReport` converts the report file identified by `sFile`. On success it returns [`.T.`](../literals/true.md). It does not return [`.F.`](../literals/false.md) for failure cases. Instead, it raises an error if `sFile` is [`NIL`](../literals/nil.md) or if the conversion fails. Use `:TRY/:CATCH` when your workflow must continue after a failed conversion attempt.

## When to use

- When you need to convert a report file as part of an automated workflow.
- When you want a simple success signal of [`.T.`](../literals/true.md) and are prepared to catch raised errors.
- When batch logic should continue after individual conversion failures by using `:TRY/:CATCH`.

## Syntax

```ssl
ConvertReport(sFile)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sFile` | [string](../types/string.md) | yes | — | Source file path for the report to convert |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the conversion completes successfully. Failure raises an error instead of returning [`.F.`](../literals/false.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sFile` is [`NIL`](../literals/nil.md). | `Source string cannot be null.` |
| The conversion fails. | `Error Converting Report(s): <underlying error message>` |

## Best practices

!!! success "Do"
    - Treat a successful return as confirmation that the conversion completed.
    - Wrap calls in `:TRY/:CATCH` when a failed conversion should not stop the surrounding workflow.
    - Log or surface the caught error description when conversion is part of a batch process.

!!! failure "Don't"
    - Write logic that expects `ConvertReport` to return [`.F.`](../literals/false.md) on failure.
      Failure paths raise errors instead.
    - Pass a [`NIL`](../literals/nil.md) path. That raises an immediate error.
    - Ignore exceptions in batch or migration code where one bad file should be reported and the rest should continue.

## Caveats

- `ConvertReport` never returns [`.F.`](../literals/false.md). Code that branches on a false return value is misleading because failures are reported as raised errors.

## Examples

### Convert a single report and continue on success

Calls `ConvertReport` directly in an [`:IF`](../keywords/IF.md) condition and displays a confirmation message when the call returns [`.T.`](../literals/true.md).

```ssl
:PROCEDURE ConvertReportExample;
	:DECLARE sReportPath;

	sReportPath := "C:\Reports\AnalysisReport001.rpt";

	:IF ConvertReport(sReportPath);
		UsrMes("Report conversion succeeded for " + sReportPath);
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("ConvertReportExample");
```

### Handle conversion failure with :TRY/:CATCH

Wraps the call in `:TRY/:CATCH` so a failed conversion is reported via the error description rather than silently ignored or assumed to return [`.F.`](../literals/false.md).

```ssl
:PROCEDURE HandleMissingReport;
	:DECLARE sFile, oErr, sErrMsg;

	sFile := "NonExistentReport.rpt";

	:TRY;
		ConvertReport(sFile);
		UsrMes("Report conversion succeeded for " + sFile);
	:CATCH;
		oErr := GetLastSSLError();
		sErrMsg := "ConvertReport failed for " + sFile + ": "
					+ oErr:Description;
		UsrMes(sErrMsg);
		/* Displays on failure: conversion failure summary;
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("HandleMissingReport");
```

### Batch convert reports and aggregate failures

Converts four report files, keeps processing after failures, counts both outcomes, and displays one summary at the end.

```ssl
:PROCEDURE BatchConvertReports;
	:DECLARE aFiles, sSourceFolder, oErr, sLogMessage;
	:DECLARE nSuccessCount, nFailCount, nIndex, sFilePath, sResultSummary;

	sSourceFolder := "C:\\Reports\\Pending\\";
	aFiles := {
		"Analysis_Q1.rpt",
		"Analysis_Q2.rpt",
		"Analysis_Q3.rpt",
		"Invalid_File.rpt"
	};

	nSuccessCount := 0;
	nFailCount := 0;

	:FOR nIndex := 1 :TO ALen(aFiles);
		sFilePath := sSourceFolder + aFiles[nIndex];

		:TRY;
			ConvertReport(sFilePath);
			nSuccessCount += 1;
			UsrMes("Converted: " + sFilePath);
			/* Displays one line for each successful conversion;
		:CATCH;
			nFailCount += 1;
			oErr := GetLastSSLError();
			sLogMessage := "Failed to convert " + sFilePath + ": "
							+ oErr:Description;
			UsrMes(sLogMessage);
			/* Displays one line for each failed conversion;
		:ENDTRY;
	:NEXT;

	sResultSummary := "Batch complete: "
						+ LimsString(nSuccessCount) + " succeeded, "
						+ LimsString(nFailCount) + " failed";
	InfoMes(sResultSummary);
	/* Displays batch totals;

	:RETURN nSuccessCount;
:ENDPROC;

/* Usage;
DoProc("BatchConvertReports");
```

## Related

- [`GetLastSSLError`](GetLastSSLError.md)
- [`ErrorMes`](ErrorMes.md)
- [`UsrMes`](UsrMes.md)
- [`InfoMes`](InfoMes.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
