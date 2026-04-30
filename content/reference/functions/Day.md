---
title: "Day"
summary: "Extracts the day-of-month number from a date value."
id: ssl.function.day
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Day

Extracts the day-of-month number from a date value.

`Day` returns the numeric day component of a date. For a valid date, the result is a number from `1` to `31`. If the input is an empty date, the function returns `0`. Passing [`NIL`](../literals/nil.md) or a value that is not a date raises an error.

## When to use

- When you need the numeric day-of-month for display, validation, or branching logic.
- When you need to test for dates such as the first, fifteenth, or last day used by a workflow rule.
- When combining day-of-month checks with other date logic such as [`Month`](Month.md) or [`Year`](Year.md).

## Syntax

```ssl
Day(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | The date value from which to extract the day-of-month number. |

## Returns

**[number](../types/number.md)** — Returns `1` to `31` for a valid date, or `0` when `dDate` is an empty date.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `Argument: date cannot be null.` |
| `dDate` is not a date value. | `Argument: date must be of date type` |

## Best practices

!!! success "Do"
    - Use `Day` when you need the numeric day component from a date.
    - Treat a return value of `0` as an empty date case.
    - Combine it with [`Month`](Month.md) or [`Year`](Year.md) when the full calendar context matters.

!!! failure "Don't"
    - Pass strings, numbers, or other non-date values. The function requires a date argument and raises an error for other types.
    - Treat `0` as a valid day of the month. It only indicates an empty date.
    - Use the result as though it were still a date value. `Day` returns a number, not a date.

## Caveats

- The function returns a number only; it does not format or zero-pad the result.

## Examples

### Extract the day-of-month from a date value

Extracts the day component from a fixed date and displays the numeric result.

```ssl
:PROCEDURE GetDueDateDay;
    :DECLARE dDueDate, nDay, sMessage;

    dDueDate := CToD("03/15/2026");
    nDay := Day(dDueDate);

    sMessage := "Due date is on day " + LimsString(nDay);
    UsrMes(sMessage);

    :RETURN nDay;
:ENDPROC;

/* Usage;
DoProc("GetDueDateDay");
```

[`UsrMes`](UsrMes.md) displays:

```text
Due date is on day 15
```

### Guard against an empty date before using the day value

Passes an empty date string to [`CToD`](CToD.md) to produce an empty date, then checks whether `Day` returns `0` to distinguish it from a valid calendar day.

```ssl
:PROCEDURE CheckDateDayValue;
    :DECLARE dSampleDate, nDay;

    dSampleDate := CToD("");
    nDay := Day(dSampleDate);

    :IF nDay == 0;
        UsrMes("No calendar day is available because the date is empty");
    :ELSE;
        UsrMes("Recorded day is " + LimsString(nDay));
        /* Displays the recorded day when valid;
    :ENDIF;

    :RETURN nDay;
:ENDPROC;

/* Usage;
DoProc("CheckDateDayValue");
```

### Filter records that fall on a target day of the month

Iterates over an array of run records and collects those whose date falls on a target day-of-month, then displays the count of matches.

```ssl
:PROCEDURE FilterRunsByDayOfMonth;
    :PARAMETERS nTargetDay;
    :DEFAULT nTargetDay, 15;
    :DECLARE aRuns, aMatches, nIndex, dRunDate;

    aRuns := {
        {"RUN-001", CToD("03/15/2026")},
        {"RUN-002", CToD("03/18/2026")},
        {"RUN-003", CToD("04/15/2026")}
    };
    aMatches := {};

    :FOR nIndex := 1 :TO ALen(aRuns);
        dRunDate := aRuns[nIndex, 2];

        :IF Day(dRunDate) == nTargetDay;
            AAdd(aMatches, aRuns[nIndex, 1]);
        :ENDIF;
    :NEXT;

    UsrMes("Found " + LimsString(ALen(aMatches))
           + " runs on day " + LimsString(nTargetDay));
    /* Displays the number of matching runs;

    :RETURN aMatches;
:ENDPROC;

/* Usage;
DoProc("FilterRunsByDayOfMonth", {15});
```

## Related

- [`DOW`](DOW.md)
- [`DOY`](DOY.md)
- [`JDay`](JDay.md)
- [`Month`](Month.md)
- [`NoOfDays`](NoOfDays.md)
- [`Year`](Year.md)
- [`date`](../types/date.md)
- [`number`](../types/number.md)
