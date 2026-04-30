---
title: "NoOfDays"
summary: "Returns the number of days in the month for a date value."
id: ssl.function.noofdays
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# NoOfDays

Returns the number of days in the month for a date value.

`NoOfDays()` returns the number of days in the month represented by `dDate`. For valid dates, the result is `28`, `29`, `30`, or `31` depending on the month and year. If `dDate` is an empty date, the function returns `0`. Passing [`NIL`](../literals/nil.md) or a value that is not a date raises an error.

## When to use

- When validating that a day number fits within the selected month.
- When calculating month-end dates without hard-coding `28`, `29`, `30`, or `31`.
- When handling leap-year differences for February.
- When building scheduling or UI logic that depends on the actual month length.

## Syntax

```ssl
NoOfDays(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | Date value whose month length should be returned |

## Returns

**[number](../types/number.md)** — The number of days in `dDate`'s month, or `0` when `dDate` is empty

| Input state | Return value |
|-------------|--------------|
| Empty date | `0` |
| February in a non-leap year | `28` |
| February in a leap year | `29` |
| 30-day month | `30` |
| 31-day month | `31` |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `Argument: dDate cannot be null.` |
| `dDate` is not a date value. | `Argument: dDate must be of date type` |

## Best practices

!!! success "Do"
    - Use `NoOfDays()` instead of hard-coding month lengths.
    - Treat a `0` result as an empty-date case and handle it before using the value in downstream logic.
    - Use the function when leap-year-safe month length matters, especially around February.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) or non-date values. `NoOfDays()` validates the argument and raises on invalid input.
    - Assume every month has `30` or `31` days, or that February is always `28`.
    - Treat a `0` result as a real month length. It indicates an empty date.

## Examples

### Validate a day number against the selected month

`CToD("02/15/2024")` is a February date in a leap year, so `NoOfDays()` returns `29`. Day `31` exceeds that limit, so `bValid` is [`.F.`](../literals/false.md) and the message reports the excess.

```ssl
:PROCEDURE ValidateDayOfMonth;
    :DECLARE dSelectedDate, nEnteredDay, nMaxDays, bValid, sMessage;

    dSelectedDate := CToD("02/15/2024");
    nEnteredDay := 31;
    nMaxDays := NoOfDays(dSelectedDate);
    bValid := nEnteredDay <= nMaxDays;

    :IF bValid;
        sMessage := "Day " + LimsString(nEnteredDay)
            + " is valid for " + CMonth(dSelectedDate) + ".";
    :ELSE;
        sMessage := "Day " + LimsString(nEnteredDay)
            + " exceeds the " + LimsString(nMaxDays)
            + " days in " + CMonth(dSelectedDate) + ".";
    :ENDIF;

    UsrMes(sMessage);

    :RETURN bValid;
:ENDPROC;

/* Usage;
DoProc("ValidateDayOfMonth");
```

[`UsrMes`](UsrMes.md) displays:

```text
Day 31 exceeds the 29 days in February.
```

### Calculate the last day of a month

Get the last valid day of `dInputDate`'s month using [`DateFromNumbers`](DateFromNumbers.md). An empty input returns an empty date immediately; otherwise, the result is the final day of the month.

```ssl
:PROCEDURE GetMonthEndDate;
    :PARAMETERS dInputDate;
    :DECLARE nLastDay, dMonthEnd;

    nLastDay := NoOfDays(dInputDate);

    :IF nLastDay == 0;
        :RETURN CToD("");
    :ENDIF;

    dMonthEnd := DateFromNumbers(
        Year(dInputDate),
        Month(dInputDate),
        nLastDay
    );

    UsrMes("Month end is " + DToC(dMonthEnd));

    :RETURN dMonthEnd;
:ENDPROC;

/* Usage;
DoProc("GetMonthEndDate", {CToD("03/15/2024")});
```

[`UsrMes`](UsrMes.md) displays:

```text
Month end is 03/31/2024
```

### Compare month lengths across multiple reporting periods

Iterate over four period dates and print each month's length. February periods receive an additional note because their length varies with the year.

```ssl
:PROCEDURE ReviewReportingPeriods;
    :DECLARE aPeriods, nIndex, dPeriodDate, nDaysInMonth, sMessage;

    aPeriods := {
        CToD("01/15/2024"),
        CToD("02/15/2024"),
        CToD("02/15/2025"),
        CToD("04/15/2025")
    };

    :FOR nIndex := 1 :TO ALen(aPeriods);
        dPeriodDate := aPeriods[nIndex];
        nDaysInMonth := NoOfDays(dPeriodDate);

        sMessage := CMonth(dPeriodDate) + " " + LimsString(Year(dPeriodDate))
            + " has " + LimsString(nDaysInMonth) + " days.";

        :IF Month(dPeriodDate) == 2;
            sMessage := sMessage
                + " Check leap-year rules for February-sensitive schedules.";
        :ENDIF;

        UsrMes(sMessage);
    :NEXT;

    :RETURN ALen(aPeriods);
:ENDPROC;

/* Usage;
DoProc("ReviewReportingPeriods");
```

[`UsrMes`](UsrMes.md) displays:

```text
January 2024 has 31 days.
February 2024 has 29 days. Check leap-year rules for February-sensitive schedules.
February 2025 has 28 days. Check leap-year rules for February-sensitive schedules.
April 2025 has 30 days.
```

## Related

- [`DOW`](DOW.md)
- [`DOY`](DOY.md)
- [`Day`](Day.md)
- [`JDay`](JDay.md)
- [`Month`](Month.md)
- [`Year`](Year.md)
- [`number`](../types/number.md)
- [`date`](../types/date.md)
