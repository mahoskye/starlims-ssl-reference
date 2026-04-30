---
title: "Seconds"
summary: "Returns the current time of day as the number of whole seconds since midnight."
id: ssl.function.seconds
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Seconds

Returns the current time of day as the number of whole seconds since midnight.

`Seconds()` reads the current local system time and returns `hour * 3600 + minute * 60 + second`. The result is a numeric time-of-day value from `0` through `86399`. Use it when you need a simple numeric value for same-day timing, scheduling, or comparisons.

## When to use

- When you need the current time of day as a numeric value instead of a formatted string.
- When measuring elapsed time within the same day.
- When comparing the current time against daily thresholds such as cutoff or batch windows.
- When storing a lightweight time-of-day value that can be recalculated each day.

## Syntax

```ssl
Seconds()
```

## Parameters

This function takes no parameters.

## Returns

**[number](../types/number.md)** — The current number of whole seconds since midnight, from `0` to `86399`.

## Best practices

!!! success "Do"
    - Use `Seconds()` for same-day elapsed-time checks and daily schedule comparisons.
    - Capture the value once and reuse it when multiple checks should use the same timestamp.
    - Add explicit midnight-rollover handling when comparing a later `Seconds()` value to an earlier one.

!!! failure "Don't"
    - Use `Seconds()` by itself for elapsed time that can span more than one day.
    - Treat the result as a date or full timestamp. It only represents the current time of day.
    - Call `Seconds()` repeatedly inside one logical decision if a single consistent value is required.

## Caveats

- The value is based only on the current day, so it wraps back to `0` at midnight.
- Repeated calls can return different values as time advances.

## Examples

### Capture the current second-of-day value

Read the current time of day as a whole-seconds count and display it. The output varies on every call.

```ssl
:PROCEDURE ShowCurrentSeconds;
    :DECLARE nCurrentSeconds, sMessage;

    nCurrentSeconds := Seconds();
    sMessage := "Current time of day: " + LimsString(nCurrentSeconds)
        + " seconds since midnight";

    UsrMes(sMessage);

    :RETURN nCurrentSeconds;
:ENDPROC;

/*
Usage:
DoProc("ShowCurrentSeconds")
;
```

[`UsrMes`](UsrMes.md) displays:

```text
Current time of day: <0–86399> seconds since midnight
```

### Measure same-day elapsed time with midnight rollover

Capture a start and end value, handle the midnight-rollover edge case, and display the elapsed time in seconds.

```ssl
:PROCEDURE MeasureElapsedSeconds;
    :DECLARE nStartSeconds, nEndSeconds, nElapsedSeconds, sMessage;

    nStartSeconds := Seconds();
    nEndSeconds := Seconds();

    :IF nEndSeconds >= nStartSeconds;
        nElapsedSeconds := nEndSeconds - nStartSeconds;
    :ELSE;
        nElapsedSeconds := (86400 - nStartSeconds) + nEndSeconds;
    :ENDIF;

    sMessage := "Elapsed time: " + LimsString(nElapsedSeconds) + " second(s)";
    UsrMes(sMessage);

    :RETURN nElapsedSeconds;
:ENDPROC;

/*
Usage:
DoProc("MeasureElapsedSeconds")
;
```

[`UsrMes`](UsrMes.md) displays:

```text
Elapsed time: <n> second(s)
```

### Check whether the current time falls inside an overnight processing window

Compare the current seconds value against a window that spans midnight to determine whether processing should run at this moment.

```ssl
:PROCEDURE IsInProcessingWindow;
    :DECLARE nCurrentSeconds, nWindowStart, nWindowEnd, bInWindow;

    nWindowStart := (22 * 3600) + (30 * 60);
    nWindowEnd := 1 * 3600;

    nCurrentSeconds := Seconds();
    bInWindow := .F.;

    :IF nWindowStart <= nWindowEnd;
        bInWindow := nCurrentSeconds >= nWindowStart
            .AND. nCurrentSeconds <= nWindowEnd;
    :ELSE;
        bInWindow := nCurrentSeconds >= nWindowStart
            .OR. nCurrentSeconds <= nWindowEnd;
    :ENDIF;

    :RETURN bInWindow;
:ENDPROC;

/*
Usage:
DoProc("IsInProcessingWindow")
;
```

## Related

- [`Now`](Now.md)
- [`Time`](Time.md)
- [`Today`](Today.md)
- [`number`](../types/number.md)
