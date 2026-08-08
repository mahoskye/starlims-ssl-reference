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

When `RaiseError` executes inside a [`:TRY`](../keywords/TRY.md) block, the remaining statements in that block are skipped and control transfers to [`:CATCH`](../keywords/CATCH.md), where [`GetLastSSLError`](GetLastSSLError.md) retrieves the raised error. Execution then continues normally after [`:ENDTRY`](../keywords/ENDTRY.md), and the script returns as usual. An uncaught error propagates up the call stack instead; if no caller catches it, the invocation fails and the end user sees a server error. Every `RaiseError` therefore needs a [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) boundary — or a legacy [`:ERROR`](../keywords/ERROR.md) / [`:RESUME`](../keywords/RESUME.md) handler — somewhere up the call stack; raising without one turns a routine failure, such as an invalid sample ID, into a crash. The preferred placement is directly inside the [`:TRY`](../keywords/TRY.md) block whose [`:CATCH`](../keywords/CATCH.md) handles it, so the raise can never escape.

## When to use

- When validation fails and the current operation must stop immediately.
- When you want a caught error to include a specific operation name or numeric code.
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
    - Place `RaiseError` directly inside the [`:TRY`](../keywords/TRY.md) block whose [`:CATCH`](../keywords/CATCH.md) handles it, so the raise can never escape.
    - Catch every raised error at an entry-point boundary with [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md), so failures come back as logged messages and return values instead of server errors.
    - Mark raise-only helper procedures [`/*@private;`](../special-forms/access-modifiers.md) so they cannot be invoked without the entry point that catches them.
    - Raise clear messages that explain what failed and why.
    - Supply `sLocation` and `nErrorCode` when callers or logs need to identify the failing operation precisely.

!!! failure "Don't"
    - Call `RaiseError` inside [`:CATCH`](../keywords/CATCH.md) — the error handler must never become the thing that crashes.
    - Let a raised error escape the outermost procedure — an uncaught error fails the invocation and surfaces as a server error to the end user.
    - Use `RaiseError` for routine status reporting or non-fatal branching, because it stops normal execution.
    - Pass vague messages such as `"failed"` or `"error"`, because they make diagnosis harder after the error is caught.

## Examples

### Raise a validation failure and handle it gracefully

`ValidateSampleID` raises as soon as the input is unusable; `CheckSampleID` — the only public entry point — catches the error and turns it into a plain return value. A raise-only helper like this is a last resort: when you do write one, mark it [`/*@private;`](../special-forms/access-modifiers.md) so external callers cannot invoke it directly and bypass the boundary that catches its errors.

```ssl
/*@private;
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

### Raise inside the :TRY block that handles it

The preferred placement for `RaiseError` is directly inside a [`:TRY`](../keywords/TRY.md) block whose [`:CATCH`](../keywords/CATCH.md) is right there to absorb it. The raise cannot escape, the statements it skips are visible at a glance, and the procedure always returns normally.

```ssl
:PROCEDURE ProcessSample;
	:PARAMETERS sSampleID;
	:DECLARE oErr, sStatus;

	sStatus := "";

	:TRY;
		:IF sSampleID == "MISSING";
			RaiseError("Sample was not found", "ProcessSample", 2001);
		:ENDIF;

		/* Skipped when the raise fires;
		sStatus := "Processed " + sSampleID;
	:CATCH;
		oErr := GetLastSSLError();
		sStatus := "Skipped [" + LimsString(oErr:Code) + "] "
		+ oErr:Description;
		ClearLastSSLError();
	:ENDTRY;

	:RETURN sStatus;
:ENDPROC;

/* Usage;
:RETURN DoProc("ProcessSample", {"MISSING"});
```

Returns:

```text
Skipped [2001] Sample was not found
```

## Related

- [`ClearLastSSLError`](ClearLastSSLError.md)
- [`FormatErrorMessage`](FormatErrorMessage.md)
- [`GetLastSSLError`](GetLastSSLError.md)
- [`SSLError`](../classes/SSLError.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
