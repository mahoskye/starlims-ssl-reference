---
title: "DateDiff"
summary: "Returns the whole-number difference between two date values in a requested unit."
id: ssl.function.datediff
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DateDiff

Returns the whole-number difference between two date values in a requested unit.

`DateDiff` compares `dStartDate` and `dEndDate` and returns a numeric result for the requested `sDatepart`. If `sDatepart` is omitted or passed as a non-string value, the function uses `"day"`. The supported units are `"year"`, `"month"`, `"day"`, `"hour"`, `"minute"`, `"second"`, and `"millisecond"`. Both date arguments must be valid date values.

Use `DateDiff` when you need a whole-number result in a specific unit. Use [`DateDiffEx`](DateDiffEx.md) instead when you need the full interval object.

## When to use

- When you need the number of days between two dates.
- When you need elapsed hours, minutes, seconds, or milliseconds between two timestamps.
- When you need a calendar month or calendar year difference rather than a full interval object.
- When your logic depends on a whole-number threshold such as age in days or
  hold time in hours.

## Syntax

```ssl
DateDiff(dStartDate, dEndDate, [sDatepart])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dStartDate` | [date](../types/date.md) | yes | — | The starting date value. |
| `dEndDate` | [date](../types/date.md) | yes | — | The ending date value. |
| `sDatepart` | [string](../types/string.md) | no | `"day"` | Unit to return: `"year"`, `"month"`, `"day"`, `"hour"`, `"minute"`, `"second"`, or `"millisecond"`. If omitted or not a string, `DateDiff` uses `"day"`. |

## Returns

**[number](../types/number.md)** — A whole-number difference between `dStartDate` and `dEndDate` in the requested unit:

| `sDatepart` | Behavior |
|------------|----------|
| `"year"` | Returns `dEndDate` year minus `dStartDate` year. |
| `"month"` | Returns the calendar month difference: `(end year - start year) * 12 + (end month - start month)`. |
| `"day"` | Returns elapsed whole days. Partial days are truncated toward zero. |
| `"hour"` | Returns elapsed whole hours. Partial hours are truncated toward zero. |
| `"minute"` | Returns elapsed whole minutes. Partial minutes are truncated toward zero. |
| `"second"` | Returns elapsed whole seconds. Partial seconds are truncated toward zero. |
| `"millisecond"` | Returns elapsed whole milliseconds. Partial milliseconds are truncated toward zero. |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dStartDate` is [`NIL`](../literals/nil.md). | `Argument: startDate cannot be null.` |
| `dStartDate` is not a date value. | `Argument: startDate must be of date type` |
| `dEndDate` is [`NIL`](../literals/nil.md). | `Argument: endDate cannot be null.` |
| `dEndDate` is not a date value. | `Argument: endDate must be of date type` |
| `sDatepart` is an unsupported string. | `Argument datepart (value=<value>) is invalid. Possible values: day, hour, minute, second, millisecond.` `<value>` is the invalid string supplied. The message contains a line break between the two sentences. |

## Best practices

!!! success "Do"
    - Pass validated date values for `dStartDate` and `dEndDate`.
    - Specify `sDatepart` explicitly when the result is not day-based.
    - Use `"month"` or `"year"` when you need calendar-component differences instead of elapsed time.

!!! failure "Don't"
    - Use `DateDiff` when you need fractional durations. It returns whole numbers only.
    - Estimate months by dividing day counts when calendar month differences matter.
    - Assume the default unit is anything other than `"day"`.

## Caveats

- `"year"` and `"month"` are calendar-based calculations. They do not measure elapsed partial years or partial months.
- `"day"`, `"hour"`, `"minute"`, `"second"`, and `"millisecond"` use elapsed time and truncate partial units toward zero.
- `sDatepart` is normalized to lowercase before validation, so values such as `"DAY"` and `"day"` behave the same.
- The invalid-`sDatepart` error text lists only `day`, `hour`, `minute`, `second`, and `millisecond`, even though `"year"` and `"month"` are also accepted.

## Examples

### Count the whole days since a sample was logged

Computes the elapsed days between a fixed log date and today using the default `day` unit, then displays the result.

```ssl
:PROCEDURE GetSampleAgeDays;
	:DECLARE dLoggedOn, dToday, nAgeDays;

	dLoggedOn := CToD("03/15/2026");
	dToday := Today();

	nAgeDays := DateDiff(dLoggedOn, dToday);

	UsrMes("Sample age in days: " + LimsString(nAgeDays));

	:RETURN nAgeDays;
:ENDPROC;

/* Usage;
DoProc("GetSampleAgeDays");
```

[`UsrMes`](UsrMes.md) displays (output depends on the current date):

```text
Sample age in days: 38
```

### Validate a 48-hour hold time between two timestamps

Computes elapsed hours between two fixed timestamps using the `hour` unit, then checks whether the hold time meets the 48-hour minimum and displays the appropriate status.

```ssl
:PROCEDURE ValidateHoldTime;
	:DECLARE dReceivedAt, dReleasedAt, nHoldHours, sMessage;

	dReceivedAt := DateFromNumbers(2026, 4, 10, 8, 30, 0);
	dReleasedAt := DateFromNumbers(2026, 4, 12, 10, 15, 0);

	nHoldHours := DateDiff(dReceivedAt, dReleasedAt, "hour");

	:IF nHoldHours >= 48;
		sMessage := "Hold time met: " + LimsString(nHoldHours) + " hours";
	:ELSE;
		sMessage := "Hold time not met: " + LimsString(nHoldHours) + " hours";
	:ENDIF;

	UsrMes(sMessage);

	:RETURN nHoldHours;
:ENDPROC;

/* Usage;
DoProc("ValidateHoldTime");
```

[`UsrMes`](UsrMes.md) displays:

```text
Hold time met: 49 hours
```

### Compare calendar months and years between two dates

Computes both the calendar month gap and the calendar year span between two dates, then combines the results into a single summary string.

```ssl
:PROCEDURE SummarizeRenewalGap;
	:DECLARE dStartDate, dRenewalDate, nMonthGap, nYearGap, sSummary;

	dStartDate := DateFromNumbers(2024, 11, 15, 14, 0, 0);
	dRenewalDate := DateFromNumbers(2026, 2, 1, 9, 0, 0);

	nMonthGap := DateDiff(dStartDate, dRenewalDate, "month");
	nYearGap := DateDiff(dStartDate, dRenewalDate, "year");

	sSummary := "Renewal is " + LimsString(nMonthGap) + " calendar months after start";
	sSummary := sSummary + " and spans " + LimsString(nYearGap) + " calendar years";

	UsrMes(sSummary);

	:RETURN nMonthGap;
:ENDPROC;

/* Usage;
DoProc("SummarizeRenewalGap");
```

[`UsrMes`](UsrMes.md) displays:

```text
Renewal is 15 calendar months after start and spans 2 calendar years
```

## Related

- [`DateAdd`](DateAdd.md)
- [`DateDiffEx`](DateDiffEx.md)
- [`date`](../types/date.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
