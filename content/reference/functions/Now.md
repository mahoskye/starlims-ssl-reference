---
title: "Now"
summary: "Returns the current system date and time as an SSL date value."
id: ssl.function.now
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Now

Returns the current system date and time as an SSL date value.

`Now()` returns the current local date and time when the function is called. The result is an SSL date value, so you can store it, compare it with other date values, pass it to date/time functions, or format it for display. Use [`Today`](Today.md) when you need the current date without a time component.

## When to use

- When you need to record the exact current date and time for logging or audit purposes.
- When calculating time intervals from the present moment, such as for expiration checks or elapsed time monitoring.
- When you want to display the current date and time in an interface or message.
- When you require consistent system-timed values for workflows, rather than user-input or fixed times.

## Syntax

```ssl
Now()
```

## Parameters

This function takes no parameters.

## Returns

**[date](../types/date.md)** — The current local date and time as an SSL date value

## Best practices

!!! success "Do"
    - Use `Now()` when you need both the current date and the current time.
    - Capture the value once and reuse it when multiple operations should share the same timestamp.
    - Combine the result with functions such as [`Hour`](Hour.md), [`Minute`](Minute.md), or [`Second`](Second.md) when you need specific time parts.

!!! failure "Don't"
    - Use `Now()` when you only need today's date. Use [`Today`](Today.md) for date-only logic.
    - Call `Now()` repeatedly inside one logical operation if all values should match. Each call can return a later timestamp.
    - Convert the value to text too early if you still need to compare or calculate with it as a date value.

## Caveats

- Each call reads the current system clock, so repeated calls can return different values.
- The result includes a time component. Comparisons against date-only values such as [`Today`](Today.md) may behave differently than expected.
- Use [`Time()`](Time.md) or [`LimsTime()`](LimsTime.md) when you need a formatted time string instead of a date value.

## Examples

### Capture the current timestamp for a log entry

Call `Now()` once and store the result, then format it with [`DateToString`](DateToString.md) so the message shows both the date and the time. The exact timestamp depends on when the procedure runs.

```ssl
:PROCEDURE LogTimestamp;
	:DECLARE dTimestamp, sLogMessage;

	dTimestamp := Now();
	sLogMessage := "Event recorded at " + DateToString(dTimestamp);

	UsrMes(sLogMessage);

	:RETURN dTimestamp;
:ENDPROC;

/* Usage;
DoProc("LogTimestamp");
```

[`UsrMes`](UsrMes.md) logs:

```text
Event recorded at <timestamp>
```

`<timestamp>` is the moment the procedure runs, in the `MM/dd/yyyy HH:mm:ss` pattern that [`DateToString`](DateToString.md) uses by default. Converting the value with [`LimsString`](LimsString.md) instead logs only the date part.

### Measure elapsed time between two timestamps

Capture the start time, do work, then capture the end time and pass both to [`DateDiff`](DateDiff.md). The elapsed count is typically `0` in this example because both `Now()` calls happen immediately after each other.

```ssl
:PROCEDURE MeasureElapsedTime;
	:DECLARE dStart, dEnd, nElapsedSeconds, sMessage;

	dStart := Now();

	UsrMes("Starting work at " + DateToString(dStart));
	/* Logs the current start timestamp;

	dEnd := Now();
	nElapsedSeconds := DateDiff(dStart, dEnd, "second");

	sMessage := "Elapsed seconds: " + LimsString(nElapsedSeconds);
	UsrMes(sMessage);
	/* Logs the elapsed seconds;

	:RETURN nElapsedSeconds;
:ENDPROC;

/* Usage;
DoProc("MeasureElapsedTime");
```

### Use one captured timestamp across a SQL update and follow-up message

Capture `Now()` once so both the SQL update and the confirmation message use the same timestamp. The message reflects whether the update succeeded: a failed update raises, and [`:CATCH`](../keywords/CATCH.md) records the reason.

```ssl
:PROCEDURE StampReleasedSamples;
	:DECLARE dReleasedAt, sSQL, bSuccess, sMessage, sStatus, oErr;

	dReleasedAt := Now();
	sStatus := "Released";
	bSuccess := .F.;
	sSQL := "
	    UPDATE sample SET
	        released_at = ?,
	        status = ?
	    WHERE sample_id = ?
	";

	:TRY;
		RunSQL(sSQL,, {dReleasedAt, sStatus, "S-1001"});
		bSuccess := .T.;
		sMessage := "Sample released at " + DateToString(dReleasedAt);
	:CATCH;
		oErr := GetLastSSLError();
		sMessage := "Sample release update failed: " + oErr:Description;
	:ENDTRY;

	UsrMes(sMessage);

	:RETURN bSuccess;
:ENDPROC;

/* Usage;
DoProc("StampReleasedSamples");
```

`UsrMes` logs either:

```text
Sample released at <timestamp>
```

or:

```text
Sample release update failed: <database error>
```

## Related

- [`Hour`](Hour.md)
- [`LimsTime`](LimsTime.md)
- [`Minute`](Minute.md)
- [`Second`](Second.md)
- [`Seconds`](Seconds.md)
- [`Time`](Time.md)
- [`Today`](Today.md)
- [`date`](../types/date.md)
