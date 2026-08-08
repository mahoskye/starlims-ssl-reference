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

When `RaiseError` executes inside a [`:TRY`](../keywords/TRY.md) block, the remaining statements in that block are skipped and control transfers to [`:CATCH`](../keywords/CATCH.md), where [`GetLastSSLError`](GetLastSSLError.md) retrieves the raised error. Execution then continues normally after [`:ENDTRY`](../keywords/ENDTRY.md), and the script returns as usual. An uncaught error propagates up the call stack instead; if no caller catches it, the invocation fails and the end user sees a server error. Every `RaiseError` therefore needs a [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) boundary somewhere up the call stack — raising without one turns a routine failure, such as an invalid sample ID, into a crash.

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
| `sMessage` is [`NIL`](../literals/nil.md). | `RaiseError(): error message cannot be null.` |

## Best practices

!!! success "Do"
    - Catch every raised error at an entry-point boundary with [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md), so failures come back as logged messages and return values instead of server errors.
    - Raise clear messages that explain what failed and why.
    - Supply `sLocation` and `nErrorCode` when callers or logs need to identify the failing operation precisely.
    - Re-raise caught errors with `oInnerException` when you need to add context without losing the original failure.

!!! failure "Don't"
    - Let a raised error escape the outermost procedure — an uncaught error fails the invocation and surfaces as a server error to the end user.
    - Re-raise inside [`:CATCH`](../keywords/CATCH.md) unless a caller above is known to catch it; otherwise the error handler itself becomes the crash.
    - Use `RaiseError` for routine status reporting or non-fatal branching, because it stops normal execution.
    - Pass vague messages such as `"failed"` or `"error"`, because they make diagnosis harder after the error is caught.
    - Drop the original error when wrapping a failure, because that removes useful details from the error chain.

## Examples

### Raise a validation failure and handle it gracefully

`ValidateSampleID` raises as soon as the input is unusable; `CheckSampleID` — the procedure callers actually invoke — catches the error and turns it into a plain return value. The raised error never escapes, so a bad sample ID produces a rejection message, not a server error.

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

:PROCEDURE CheckSampleID;
	:PARAMETERS sSampleID;
	:DECLARE oErr, sReason;

	sReason := "";

	:TRY;
		DoProc("ValidateSampleID", {sSampleID});
	:CATCH;
		oErr := GetLastSSLError();
		sReason := oErr:Description;
		ClearLastSSLError();
	:ENDTRY;

	:RETURN {Empty(sReason), sReason};
:ENDPROC;

/* Usage;
:RETURN DoProc("CheckSampleID", {"SAM"});
```

Returns:

```text
{.F., "Sample ID must be at least 5 characters. Length: 3"}
```

### Add context with an inner error, then handle the chain at the boundary

`ProcessSample` catches the low-level failure and re-raises it with higher-level context, preserving the original as the inner exception. That re-raise is safe only because `RunBatch` — the entry point — catches everything, logs the full chain, and returns normally. If `ProcessSample` were invoked directly, nothing would catch the re-raised error and the invocation would fail.

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

[`ErrorMes`](ErrorMes.md) logs:

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
