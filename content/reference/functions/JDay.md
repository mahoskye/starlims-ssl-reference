---
title: "JDay"
summary: "Returns the day-of-year number for a date, or for today's date when no argument is supplied."
id: ssl.function.jday
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# JDay

Returns the day-of-year number for a date, or for today's date when no argument is supplied.

`JDay()` returns the ordinal day within the year for a valid date, from `1` through `366`. If you omit the argument, the function uses the current date. If you pass an empty date value such as `CToD("")`, it does not raise an error; instead it returns the sentinel value `34`. Passing a non-date value raises a type error.

## When to use

- When you need a date's position within its year for reporting, sorting, or
  grouping.
- When you want the current day's ordinal position without first calling a
  separate date function.
- When you need `JDay()` specifically because empty dates should return a value
  instead of raising, unlike [`DOY`](DOY.md).

## Syntax

```ssl
JDay([dDate])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | no | [`NIL`](../literals/nil.md) | Date value to evaluate. If omitted or [`NIL`](../literals/nil.md), `JDay()` uses the current date. If an empty date value is supplied, the function returns `34`. |

## Returns

**[number](../types/number.md)** — day-of-year value for the supplied date, or for the current date when no argument is supplied

| Input state | Return value |
|-------------|--------------|
| Valid date | `1` to `366` |
| Omitted argument | current date's day-of-year |
| Empty date | `34` |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is not a date value. | `Argument: dDate must be of date type` |

## Best practices

!!! success "Do"
    - Validate or document how your code handles empty dates before relying on a `JDay()` result.
    - Use `JDay()` when you intentionally want the current date by omitting the argument.
    - Use [`DOY`](DOY.md) instead when empty dates should raise rather than returning a sentinel value.

!!! failure "Don't"
    - Pass strings, numbers, or objects expecting automatic conversion to a date.
    - Treat `34` as a guaranteed real day-of-year result when the input may be empty.
    - Use `JDay()` to calculate the number of days between two dates.

## Caveats

- The empty-date fallback is `34` (February 3rd), which overlaps with a real day-of-year value. Check for empty dates before calling `JDay()` when that distinction matters.
- The normal return range is `1` through `366`; `366` occurs only in leap years.

## Examples

### Get the day-of-year for a specific date

Pass a date value and display its ordinal position within the year. March 15 is the 75th day of 2024, a leap year with 29 days in February.

```ssl
:PROCEDURE ShowSampleJDay;
    :DECLARE dReceivedDate, nDayOfYear, sMessage;

    dReceivedDate := CToD("03/15/2024");
    nDayOfYear := JDay(dReceivedDate);

    sMessage := DToC(dReceivedDate) + " is day "
		        + LimsString(nDayOfYear) + " of the year.";

    UsrMes(sMessage);

    :RETURN nDayOfYear;
:ENDPROC;

/* Usage;
DoProc("ShowSampleJDay");
```

[`UsrMes`](UsrMes.md) displays:

```
03/15/2024 is day 75 of the year.
```

### Get today's day-of-year by omitting the argument

Omit the `dDate` argument to have `JDay` use the current date automatically. The output varies depending on when the procedure runs.

```ssl
:PROCEDURE LogTodayOrdinal;
    :DECLARE nToday, sMessage;

    nToday := JDay();

    sMessage := "Today is day " + LimsString(nToday) + " of the year.";
    UsrMes(sMessage);

    :RETURN nToday;
:ENDPROC;

/* Usage;
DoProc("LogTodayOrdinal");
```

[`UsrMes`](UsrMes.md) displays:

```
Today is day 113 of the year.
```

(day number varies by date)

### Skip empty dates to avoid the sentinel return value

Use [`Empty`](Empty.md) to detect invariant dates before calling `JDay`, so the sentinel value `34` is never mistaken for a real result. With the three-element input, two records produce valid day numbers and one is counted as empty.

```ssl
:PROCEDURE SummarizeScheduleDates;
    :DECLARE aDates, dPlannedDate, nDayOfYear, sMessage;
    :DECLARE nIndex, nValidCount, nEmptyCount;

    aDates := {
        CToD("01/15/2024"),
        CToD("02/29/2024"),
        CToD("")
    };

    nValidCount := 0;
    nEmptyCount := 0;

    :FOR nIndex := 1 :TO ALen(aDates);
        dPlannedDate := aDates[nIndex];

        :IF Empty(dPlannedDate);
            nEmptyCount := nEmptyCount + 1;
            /* Displays empty-date notice;
            UsrMes("Record " + LimsString(nIndex) + " has an empty date.");
            :LOOP;
        :ENDIF;

        nDayOfYear := JDay(dPlannedDate);
        nValidCount := nValidCount + 1;

        sMessage := "Record " + LimsString(nIndex) + ": "
		            + DToC(dPlannedDate) + " -> JDay " + LimsString(nDayOfYear);
        /* Displays record day-of-year;
        UsrMes(sMessage);
    :NEXT;

    sMessage := "Processed " + LimsString(nValidCount)
		        + " dated records and " + LimsString(nEmptyCount)
		        + " empty records.";
    /* Displays summary counts;
    UsrMes(sMessage);

    :RETURN nValidCount;
:ENDPROC;

/* Usage;
DoProc("SummarizeScheduleDates");
```

## Related

- [`DOY`](DOY.md)
- [`DOW`](DOW.md)
- [`Day`](Day.md)
- [`Month`](Month.md)
- [`NoOfDays`](NoOfDays.md)
- [`Year`](Year.md)
- [`number`](../types/number.md)
- [`date`](../types/date.md)
