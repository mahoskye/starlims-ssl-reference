---
title: "RaiseError"
summary: "Raises an SSL runtime error using the supplied message and optional location, error code, and inner error."
id: ssl.function.raiseerror
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# RaiseError

Raises an SSL runtime error using the supplied message and optional location, error code, and inner error.

`RaiseError` validates `sMessage` and then throws immediately. The resulting [`SSLError`](../classes/SSLError.md) exposes `sLocation` as `:Operation` and `nErrorCode` as `:Code` when caught. When `oInnerException` is provided, it becomes the inner exception of the raised error.

## When to use

- When validation fails and the current operation must stop immediately.
- When you want a caught error to include a specific operation name or numeric code.
- When you are wrapping a lower-level failure and want to preserve it as an inner error.
- When a caller should handle the failure through [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) rather than by checking a return value.

## Syntax

```ssl
RaiseError(sMessage, [sLocation], [nErrorCode], [oInnerException])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sMessage` | [string](../types/string.md) | yes | — | Message text for the error being raised. |
| `sLocation` | [string](../types/string.md) | no | `""` | Operation or location text to attach to the raised error. |
| `nErrorCode` | [number](../types/number.md) | no | `0` | Numeric code to attach to the raised error. |
| `oInnerException` | [`SSLError`](../classes/SSLError.md) | no | [`NIL`](../literals/nil.md) | Existing SSL error to preserve as the inner error. |

## Returns

**[boolean](../types/boolean.md)** — The surfaced return type is boolean, but `RaiseError` does not return normally because it always raises an error.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sMessage` is [`NIL`](../literals/nil.md). | `Error message cannot be null.` |

## Best practices

!!! success "Do"
    - Raise clear messages that explain what failed and why.
    - Supply `sLocation` and `nErrorCode` when callers or logs need to identify the failing operation precisely.
    - Re-raise caught errors with `oInnerException` when you need to add context without losing the original failure.

!!! failure "Don't"
    - Use `RaiseError` for routine status reporting or non-fatal branching, because it stops normal execution.
    - Pass vague messages such as `"failed"` or `"error"`, because they make diagnosis harder after the error is caught.
    - Drop the original error when wrapping a failure, because that removes useful details from the error chain.

## Examples

### Reject invalid input

Stop processing as soon as a required sample identifier is missing or too short.

```ssl
:PROCEDURE ValidateSampleID;
	:PARAMETERS sSampleID;
	:DECLARE nLength, sMsg;

	nLength := Len(AllTrim(sSampleID));

	:IF nLength == 0;
		RaiseError("Sample ID cannot be blank", "ValidateSampleID", 1001);
	:ENDIF;

	:IF nLength < 5;
		sMsg := "Sample ID must be at least 5 characters. Length: "
		+ LimsString(nLength);
		RaiseError(sMsg, "ValidateSampleID", 1002);
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("ValidateSampleID", {"SAM-001"});
```

### Wrap a lower-level failure as an inner exception

Catch a lower-level error, then raise a new one with higher-level context while preserving the original failure as the inner exception.

```ssl
:PROCEDURE LoadSample;
	:PARAMETERS sSampleID;

	:IF sSampleID == "MISSING";
		RaiseError("Sample was not found", "LoadSample", 2001);
	:ENDIF;
:ENDPROC;

:PROCEDURE ProcessSample;
	:PARAMETERS sSampleID;
	:DECLARE oErr;

	:TRY;
		DoProc("LoadSample", {sSampleID});
	:CATCH;
		oErr := GetLastSSLError();
		RaiseError(
			"ProcessSample failed for " + sSampleID,
			"ProcessSample",
			5001,
			oErr
		);
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ProcessSample", {"SAM-001"});
```

### Inspect chained error details in a central handler

Handle a re-raised error centrally and inspect both the top-level error and its inner error.

```ssl
:PROCEDURE RunBatch;
	:PARAMETERS sSampleID;
	:DECLARE oErr, sLog;

	:TRY;
		DoProc("ProcessSample", {sSampleID});
	:CATCH;
		oErr := GetLastSSLError();

		sLog := "Message: " + oErr:Description + Chr(10);
		sLog := sLog + "Operation: " + oErr:Operation + Chr(10);
		sLog := sLog + "Code: " + LimsString(oErr:Code);

		:IF ! Empty(oErr:InnerException);
			sLog := sLog + Chr(10) + "Inner: "
			+ oErr:InnerException:Description;
		:ENDIF;

		ErrorMes(sLog);
		ClearLastSSLError();
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("RunBatch", {"MISSING"});
```

[`ErrorMes`](ErrorMes.md) displays:

```text
Message: ProcessSample failed for MISSING
Operation: ProcessSample
Code: 5001
Inner: Sample was not found
```

## Related

- [`ClearLastSSLError`](ClearLastSSLError.md)
- [`FormatErrorMessage`](FormatErrorMessage.md)
- [`GetLastSSLError`](GetLastSSLError.md)
- [`SSLError`](../classes/SSLError.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
