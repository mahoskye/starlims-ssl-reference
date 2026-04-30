---
title: "DOW"
summary: "Returns the numeric day of week for a date."
id: ssl.function.dow
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DOW

Returns the numeric day of week for a date.

`DOW()` returns a number from `1` through `7` for valid dates, where `1`
represents Sunday and `7` represents Saturday. If the supplied date is empty, the function returns `0`. Passing [`NIL`](../literals/nil.md) or a value that is not a date raises an error.

## When to use

- When business logic depends on a weekday number rather than a formatted date.
- When you need to detect weekends or specific weekdays in workflow logic.
- When you need a stable weekday code for reporting, grouping, or comparisons.

## Syntax

```ssl
DOW(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | The date value to evaluate |

## Returns

**[number](../types/number.md)** — the weekday number for the supplied date, or `0` when the date is empty

| Input state | Return value |
|-------------|--------------|
| Empty date | `0` |
| Sunday | `1` |
| Monday | `2` |
| Tuesday | `3` |
| Wednesday | `4` |
| Thursday | `5` |
| Friday | `6` |
| Saturday | `7` |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `dDate argument cannot be null` |
| `dDate` is not a date value. | `dDate must be of date type` |

## Best practices

!!! success "Do"
    - Treat `0` as an empty-date result and handle it before weekday-specific logic.
    - Document or centralize the mapping `1 = Sunday` through `7 = Saturday` when downstream code depends on it.
    - Use `DOW()` when you need a weekday number, not a localized weekday name.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) or non-date values. `DOW` validates the argument and raises on invalid input.
    - Treat `0` as a weekday. It indicates an empty date, not Sunday.
    - Assume Monday-based or zero-based numbering. `DOW` starts at Sunday = `1`.

## Examples

### Get the weekday number for a date

Converts a hardcoded date string to a date value and displays the weekday number returned by `DOW`.

```ssl
:PROCEDURE ShowWeekdayNumber;
	:DECLARE dRunDate, nDayOfWeek, sMessage;

	dRunDate := CToD("03/23/2024");
	nDayOfWeek := DOW(dRunDate);

	sMessage := "Weekday number for " + DToC(dRunDate) + " is "
				+ LimsString(nDayOfWeek);

	UsrMes(sMessage);

	:RETURN nDayOfWeek;
:ENDPROC;

/* Usage;
DoProc("ShowWeekdayNumber");
```

[`UsrMes`](UsrMes.md) displays:

```
Weekday number for 03/23/2024 is 7
```

### Guard against an empty date before using the weekday result

Checks whether `DOW` returned `0` (empty date) before branching to a weekday-specific message.

```ssl
:PROCEDURE CheckPlannedDate;
	:DECLARE dPlannedDate, nDayOfWeek, sMessage;

	dPlannedDate := CToD("");
	nDayOfWeek := DOW(dPlannedDate);

	:IF nDayOfWeek == 0;
		sMessage := "Planned date is empty.";
	:ELSE;
		sMessage := "Planned date falls on weekday " + LimsString(nDayOfWeek);
	:ENDIF;

	UsrMes(sMessage);

	:RETURN nDayOfWeek;
:ENDPROC;

/* Usage;
DoProc("CheckPlannedDate");
```

`UsrMes` displays either:

```text
Planned date is empty.
```

or:

```text
Planned date falls on weekday [n]
```

### Route scheduled runs based on weekday rules

Iterates three runs: RUN-001 on a Sunday (04/05/2026, DOW=1), RUN-002 on a Tuesday (04/07/2026, DOW=3), and RUN-003 with no date. Each is routed to a weekend, weekday, or empty-date message based on `DOW`.

```ssl
:PROCEDURE RouteScheduledRuns;
	:DECLARE aRuns, nIndex, oRun, dRunDate, nDayOfWeek, sMessage;

	aRuns := {
		CreateUdObject({{"runId", "RUN-001"}, {"runDate", CToD("04/05/2026")}}),
		CreateUdObject({{"runId", "RUN-002"}, {"runDate", CToD("04/07/2026")}}),
		CreateUdObject({{"runId", "RUN-003"}, {"runDate", CToD("")}})
	};

	:FOR nIndex := 1 :TO ALen(aRuns);
		oRun := aRuns[nIndex];
		dRunDate := oRun:runDate;
		nDayOfWeek := DOW(dRunDate);

		:BEGINCASE;
		:CASE nDayOfWeek == 0;
			sMessage := oRun:runId + " has no scheduled date.";
			/* Displays empty-date message;
			UsrMes(sMessage);
			:EXITCASE;
		:CASE nDayOfWeek == 1 .OR. nDayOfWeek == 7;
			sMessage := oRun:runId + " is scheduled on a weekend ("
						+ LimsString(nDayOfWeek) + ").";
			/* Displays weekend message;
			UsrMes(sMessage);
			:EXITCASE;
		:OTHERWISE;
			sMessage := oRun:runId + " is scheduled on a weekday ("
						+ LimsString(nDayOfWeek) + ").";
			/* Displays weekday message;
			UsrMes(sMessage);
			:EXITCASE;
		:ENDCASE;
	:NEXT;

:ENDPROC;

/* Usage;
DoProc("RouteScheduledRuns");
```

## Related

- [`DOY`](DOY.md)
- [`Day`](Day.md)
- [`JDay`](JDay.md)
- [`Month`](Month.md)
- [`NoOfDays`](NoOfDays.md)
- [`Year`](Year.md)
- [`number`](../types/number.md)
- [`date`](../types/date.md)
