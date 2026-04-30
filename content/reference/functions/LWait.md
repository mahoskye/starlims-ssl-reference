---
title: "LWait"
summary: "Blocks further script execution for a specified number of seconds and returns an empty string."
id: ssl.function.lwait
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LWait

Blocks further script execution for a specified number of seconds and returns an empty string.

`LWait` pauses the calling thread for the given duration and then returns. A [`NIL`](../literals/nil.md) argument or missing parameter is treated as `0` and produces no delay. Fractional seconds are truncated to a whole number before the wait begins. Negative values raise an error; clamp inputs to zero or above before calling.

`LWait` is a simple blocking timer intended for rate limiting, step sequencing, or synchronizing with external processes. The current thread is held for the full duration; other events do not process until the wait completes.

## When to use

- When forcing a delay before proceeding, for instance to synchronize with external systems or files.
- When implementing simple timing, throttling, or rate limits in scripts that should pause between actions.
- When introducing a fixed wait inside automated workflows, such as waiting for resource initialization or output availability.

## Syntax

```ssl
LWait([nSeconds])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nSeconds` | [number](../types/number.md) | no | [`NIL`](../literals/nil.md) | Number of seconds to wait. Fractional values are truncated. [`NIL`](../literals/nil.md) or an omitted argument defaults to `0`. |

## Returns

**[string](../types/string.md)** — Always returns `""` after the delay completes.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `nSeconds` is negative. | `(Argument out of range)` |

## Best practices

!!! success "Do"
    - Use for explicit pauses between actions in automated, non-user-interactive code.
    - Clamp `nSeconds` to zero or above before calling when the value may be negative.
    - Capture the result only if needed; the return value is always `""`.

!!! failure "Don't"
    - Use `LWait` in code paths that require UI responsiveness or asynchronous activities.
      It blocks execution and may produce an unresponsive application if misapplied.
    - Add `LWait` to temporarily work around race conditions or timing bugs in production scripts. Relying on fixed delays leads to fragile and unreliable automation.
    - Pass non-numeric types as `nSeconds`. Unrecognized types default to zero, causing the wait to be silently skipped.

## Caveats

- Passing a negative number raises an error; clamp inputs to zero or above before calling. [`NIL`](../literals/nil.md) and omitted arguments are treated as zero and do not raise.
- Fractional seconds are truncated to whole seconds; `LWait(0.9)` is the same as `LWait(0)` and introduces no delay.
- Calling `LWait` in user-interactive or UI-sensitive code may freeze the interface during the wait.

## Examples

### Introduce a delay before file access

Wait three seconds after triggering a process before checking whether the output file exists, giving the file system time to finish writing.

```ssl
:PROCEDURE WaitForFileAccess;
	:DECLARE sFilePath, nWaitSeconds, bFileExists;

	sFilePath := "C:\Temp\AnalysisReport.txt";
	nWaitSeconds := 3;

	UsrMes("Report generation started");

	LWait(nWaitSeconds);

	bFileExists := FileSupport(sFilePath, "EXISTS");

	:IF bFileExists;
		UsrMes("File is ready for processing");
	:ELSE;
		UsrMes("File not found after waiting");
	:ENDIF;

	:RETURN bFileExists;
:ENDPROC;

/* Usage;
DoProc("WaitForFileAccess");
```

### Throttle API calls in a scheduled batch

Add a pause between endpoint calls to avoid exceeding rate limits. The delay is skipped after the last endpoint so the procedure does not wait unnecessarily.

```ssl
:PROCEDURE ThrottleApiCalls;
	:DECLARE aEndpoints, sEndpoint, nRateLimit, nDelaySeconds, nIndex, nCount;
	:DECLARE sStatus, sLogMsg;

	aEndpoints := {
		"Analysis.SubmitBatch",
		"Analysis.GetResults",
		"Inventory.CheckStock",
		"Users.SyncDirectory"
	};
	nRateLimit := 5;
	nDelaySeconds := 2;

	nCount := ALen(aEndpoints);
	sLogMsg := "Processing " + LimsString(nCount) + " endpoints with rate limit of "
		+ LimsString(nRateLimit) + " calls per minute";
	UsrMes(sLogMsg);

	:FOR nIndex := 1 :TO nCount;
		sEndpoint := aEndpoints[nIndex];
		sLogMsg := "Calling endpoint " + LimsString(nIndex) + " of " + LimsString(nCount)
			+ ": " + sEndpoint;
		UsrMes(sLogMsg);  /* Displays endpoint progress;

		:TRY;
			ExecFunction(sEndpoint);
			sStatus := "Success";
		:CATCH;
			sStatus := "Failed";
		:ENDTRY;

		sLogMsg := "Endpoint " + sEndpoint + " returned: " + sStatus;
		UsrMes(sLogMsg);  /* Displays the current endpoint result;

		:IF nIndex < nCount;
			sLogMsg := "Waiting " + LimsString(nDelaySeconds) + " seconds before next request";
			UsrMes(sLogMsg);
			LWait(nDelaySeconds);
		:ENDIF;
	:NEXT;

	sLogMsg := "All " + LimsString(nCount) + " API calls completed";
	UsrMes(sLogMsg);
:ENDPROC;

/* Usage;
DoProc("ThrottleApiCalls");
```

## Related

- [`RunApp`](RunApp.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
