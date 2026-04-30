---
title: "Time"
summary: "Returns the current time as a formatted string."
id: ssl.function.time
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Time

Returns the current time as a formatted string.

`Time()` returns the current local time when the function is called and formats it with the active application time format. It takes no parameters and always returns text. Each call evaluates the current time again, so repeated calls can return different values.

`Time()` is functionally equivalent to [`LimsTime()`](LimsTime.md). Use [`Now()`](Now.md) when you need a date-time value instead of formatted text.

## When to use

- When displaying the current time in a message, form, or status line.
- When you need a display-ready time string for user-facing output.
- When you want the time portion only, without a date value.
- When existing code or documentation expects `Time()` specifically.

## Syntax

```ssl
Time()
```

## Parameters

This function takes no parameters.

## Returns

**[string](../types/string.md)** — The current time formatted with the active time format.

## Best practices

!!! success "Do"
    - Use `Time()` when you need a display-ready time string.
    - Capture the value once and reuse it when several related messages should show the same displayed time.
    - Use [`Now()`](Now.md) instead when you need a value for date/time calculations or comparisons.

!!! failure "Don't"
    - Assume the returned string always uses one fixed format. If the configured time format changes, the returned string changes with it.
    - Use `Time()` when you need a date-time value for calculations or elapsed-time logic.
    - Call `Time()` repeatedly inside one logical action if all displayed messages should show the same time.

## Caveats

- `Time()` returns formatted text, not an SSL date value.

## Examples

### Capture one time value for consistent display across related messages

Call `Time()` once and store the result so both the user message and the audit entry reflect the same displayed time, even if a moment passes between the two calls.

```ssl
:PROCEDURE LogReviewStart;
    :DECLARE sSampleID, sStartTime, sUserMsg, sAuditMsg;

    sSampleID := "S-100123";
    sStartTime := Time();

    sUserMsg := "Review started for " + sSampleID + " at " + sStartTime;
    sAuditMsg := "AUDIT " + sSampleID + " START " + sStartTime;

    /* Displays current review start message;
    UsrMes(sUserMsg);

    /* Displays current audit start entry;
    InfoMes(sAuditMsg);

    :RETURN sStartTime;
:ENDPROC;

/* Usage;
DoProc("LogReviewStart");
```

### Build a display stamp from separate date and time values

Combine the date from [`Today`](Today.md) with the time from `Time()` to form a human-readable label stamp. Both values reflect the moment the procedure runs.

```ssl
:PROCEDURE ShowLabelPrintedStamp;
    :DECLARE dPrintedDate, sPrintedTime, sStamp;

    dPrintedDate := Today();
    sPrintedTime := Time();

    sStamp := "Label printed on " + DToC(dPrintedDate) + " at " + sPrintedTime;

    UsrMes(sStamp);

    :RETURN sStamp;
:ENDPROC;

/* Usage;
DoProc("ShowLabelPrintedStamp");
```

[`UsrMes`](UsrMes.md) displays:

```text
Label printed on 04/23/2026 at 14:30:00
```

## Related

- [`LimsTime`](LimsTime.md)
- [`Now`](Now.md)
- [`Seconds`](Seconds.md)
- [`Today`](Today.md)
- [`string`](../types/string.md)
