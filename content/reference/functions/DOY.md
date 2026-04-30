---
title: "DOY"
summary: "Calculates the ordinal day number of a date within its year."
id: ssl.function.doy
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DOY

Calculates the ordinal day number of a date within its year.

`DOY()` returns the day-of-year for a valid date, from `1` through `366`. January 1 returns `1`, and December 31 returns `365` or `366` depending on whether the year is a leap year. The function requires a date value. Unlike related date-part functions such as [`Day`](Day.md), [`Month`](Month.md), [`Year`](Year.md), [`DOW`](DOW.md), and [`NoOfDays`](NoOfDays.md), `DOY()` does not return `0` for an empty date. It raises an error instead.

## When to use

- When you need to quickly determine the day number of a sample or transaction within its calendar year for reporting, filtering, or calculations.
- When validating that recurring events or processes are happening on the correct day of the year, regardless of month or weekday.
- When building analytics, charts, or aggregations grouped by day-of-year across multiple years.
- When enforcing schedules or limits, such as handling seasonal operations or timelines based on the specific day of the year.

## Syntax

```ssl
DOY(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | Date value whose ordinal day within the year should be returned |

## Returns

**[number](../types/number.md)** — The day of the year for `dDate`, from `1` to `366`

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md) or an empty date. | `dDate argument cannot be null` |
| `dDate` is not a date value. | `dDate must be of date type` |

## Best practices

!!! success "Do"
    - Validate uncertain inputs before calling `DOY()`, especially when empty dates are possible.
    - Use `DOY()` when you need year-relative positioning such as seasonal cutoffs, annual schedules, or day-of-year grouping.
    - Account for leap years when comparing the same calendar period across different years.

!!! failure "Don't"
    - Pass an empty date and expect a `0` result. `DOY` raises instead of using the fallback returned by several related date-part functions.
    - Use `DOY` when you actually need the month, weekday, or full date value.
    - Assume the result is always between `1` and `365`; leap years can return `366`.

## Examples

### Get the day-of-year for a date

Converts a date string, calls `DOY`, and displays the day-of-year number with the formatted date.

```ssl
:PROCEDURE ShowDayOfYear;
	:DECLARE dSampleDate, nDayOfYear, sMessage;

	dSampleDate := CToD("03/15/2024");

	nDayOfYear := DOY(dSampleDate);

	sMessage := DToC(dSampleDate) + " is day "
				+ LimsString(nDayOfYear) + " of the year.";

	UsrMes(sMessage);

	:RETURN nDayOfYear;
:ENDPROC;

/* Usage;
DoProc("ShowDayOfYear");
```

[`UsrMes`](UsrMes.md) displays:

```text
03/15/2024 is day 75 of the year.
```

### Guard against an empty date before calling DOY

Uses [`Empty`](Empty.md) to detect an empty date before calling `DOY`, avoiding the exception that would otherwise be raised.

```ssl
:PROCEDURE CheckPlannedDate;
	:DECLARE dPlannedDate, nDayOfYear, sMessage;

	dPlannedDate := CToD("");

	:IF Empty(dPlannedDate);
		UsrMes("Planned date is empty. Skip DOY until a real date is available.");
		/* Displays when the planned date is empty;
		:RETURN 0;
	:ENDIF;

	nDayOfYear := DOY(dPlannedDate);

	sMessage := "Planned date " + DToC(dPlannedDate) + " falls on day "
				+ LimsString(nDayOfYear) + " of the year.";

	UsrMes(sMessage);
	/* Displays the planned date and its day-of-year;

	:RETURN nDayOfYear;
:ENDPROC;

/* Usage;
DoProc("CheckPlannedDate");
```

### Compare recurring dates across leap and non-leap years

Iterates five dates spanning both a regular and a leap year, displaying the day-of-year for each and flagging February 29 as a leap-day-only event.

```ssl
:PROCEDURE CompareAnnualSchedule;
	:DECLARE aDates, nIndex, dEventDate, nDayOfYear, sMessage;

	aDates := {
		CToD("02/28/2023"),
		CToD("03/01/2023"),
		CToD("02/28/2024"),
		CToD("02/29/2024"),
		CToD("03/01/2024")
	};

	:FOR nIndex := 1 :TO ALen(aDates);
		dEventDate := aDates[nIndex];
		nDayOfYear := DOY(dEventDate);

		sMessage := DToC(dEventDate) + " maps to DOY "
					+ LimsString(nDayOfYear);

		:IF Month(dEventDate) == 2 .AND. Day(dEventDate) == 29;
			sMessage += " and should be handled as a leap-day-only event.";
		:ENDIF;

		UsrMes(sMessage);
		/* Displays one line per date;
	:NEXT;

	:RETURN ALen(aDates);
:ENDPROC;

/* Usage;
DoProc("CompareAnnualSchedule");
```

## Related

- [`DOW`](DOW.md)
- [`Day`](Day.md)
- [`JDay`](JDay.md)
- [`Month`](Month.md)
- [`NoOfDays`](NoOfDays.md)
- [`Year`](Year.md)
- [`number`](../types/number.md)
- [`date`](../types/date.md)
