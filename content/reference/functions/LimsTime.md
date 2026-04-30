---
title: "LimsTime"
summary: "Returns the current time as a formatted string."
id: ssl.function.limstime
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LimsTime

Returns the current time as a formatted string.

`LimsTime()` returns the current time as a string using the current configured time format. It takes no parameters. Each call evaluates the current time at the moment of the call, so repeated calls can return different values.

`LimsTime()` is functionally equivalent to [`Time()`](Time.md). Use it when you need a display-ready time string. If you need a date-time value instead of a formatted string, use [`Now()`](Now.md).

## When to use

- When displaying the current time in a message, form, or status line.
- When adding a time-only stamp to user-facing output or simple logs.
- When you need the current time as text rather than as a date-time value.
- When matching other code that already uses `LimsTime()` as the time-string helper.

## Syntax

```ssl
LimsTime()
```

## Parameters

This function takes no parameters.

## Returns

**[string](../types/string.md)** — The current time formatted with the active time format.

## Best practices

!!! success "Do"
    - Use `LimsTime()` when you need a display-ready time string.
    - Capture the value once and reuse it when several messages should show the same time within one operation.
    - Pair it with [`Today()`](Today.md) or [`Now()`](Now.md) when your logic also needs date context.

!!! failure "Don't"
    - Use `LimsTime()` when you need a date-time value for comparisons or calculations.
    - Assume the returned string always uses one fixed format.
    - Call `LimsTime()` repeatedly if a single action should keep one consistent displayed time.

## Caveats

- If the configured time format changes, the returned string changes with it.

## Examples

### Capture time once for consistent output across related messages

Capture `LimsTime()` once at the start of a step and reuse the value in both the user message and the audit log, so both show the same time even if execution takes a moment.

```ssl
:PROCEDURE LogReviewStep;
	:DECLARE sTime, sSampleID, sUserMsg, sAuditMsg;

	sSampleID := "S-100123";
	sTime := LimsTime();

	sUserMsg := "Review started for " + sSampleID + " at " + sTime;
	sAuditMsg := "AUDIT " + sSampleID + " START " + sTime;

	UsrMes(sUserMsg);  /* Displays review start time;
	InfoMes(sAuditMsg);  /* Displays matching audit time;

	:RETURN sTime;
:ENDPROC;

/* Usage;
DoProc("LogReviewStep");
```

### Combine [`Today()`](Today.md) and `LimsTime()` for a display timestamp

Pair [`Today()`](Today.md) and `LimsTime()` to build a full timestamp label for a printed document.

```ssl
:PROCEDURE ShowPrintedLabelTimestamp;
	:DECLARE dPrinted, sPrintedTime, sStamp;

	dPrinted := Today();
	sPrintedTime := LimsTime();

	:IF Empty(dPrinted);
		:RETURN "";
	:ENDIF;

	sStamp := "Printed on " + DToC(dPrinted) + " at " + sPrintedTime;
	UsrMes(sStamp);  /* Displays printed date and time stamp;

	:RETURN sStamp;
:ENDPROC;

/* Usage;
DoProc("ShowPrintedLabelTimestamp");
```

## Related

- [`Now`](Now.md)
- [`Seconds`](Seconds.md)
- [`Time`](Time.md)
- [`Today`](Today.md)
- [`string`](../types/string.md)
