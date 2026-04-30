---
title: "DateAdd"
summary: "Adds a time interval to a date and returns the resulting date."
id: ssl.function.dateadd
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DateAdd

Adds a time interval to a date and returns the resulting date.

`DateAdd` returns a new date based on the input date, a numeric offset, and an optional interval name. Supported intervals are `year`, `month`, `day`, `hour`, `minute`, `second`, and `millisecond`. If `sDatepart` is omitted, [`NIL`](../literals/nil.md), or not a string, the function uses `day`. For `year` and `month`, the function rounds `nNumber` to an integer before applying the change. Use [`DateDiff`](DateDiff.md) or [`DateDiffEx`](DateDiffEx.md) when you need to measure the difference between two dates instead of shifting one.

## When to use

- When you need to calculate a future or past date by adding a specific number of days, months, or years to an existing date.
- When incrementing a date value by time intervals inside scheduling, expiry, or reminder logic.
- When normalizing or adjusting timestamps during data import, processing, or transformation workflows.

## Syntax

```ssl
DateAdd(dDate, nNumber, [sDatepart])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | The source date value. |
| `nNumber` | [number](../types/number.md) | yes | — | The numeric offset to add. |
| `sDatepart` | [string](../types/string.md) | no | `"day"` | The interval to add: `year`, `month`, `day`, `hour`, `minute`, `second`, or `millisecond`. If omitted, [`NIL`](../literals/nil.md), or not a string, `DateAdd` uses `day`. |

## Returns

**[date](../types/date.md)** — A new date representing `dDate` shifted by `nNumber` units of `sDatepart`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `Argument: date cannot be null.` |
| `dDate` is not a date value. | `Argument: date must be of date type` |
| `nNumber` is [`NIL`](../literals/nil.md). | `Argument: number cannot be null.` |
| `nNumber` is not numeric. | `Argument number must be a number.` |
| `sDatepart` is not a recognized interval name. `<value>` is the invalid string supplied; the message contains a line break between the two sentences. | `Argument datepart (value=<value>) is invalid. Possible values:year, month, day, hour, minute, second, millisecond.` |

## Best practices

!!! success "Do"
    - Pass one of the documented interval names when you need explicit units.
    - Use whole-number values for `year` and `month` additions so the result is predictable.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `dDate` or a non-numeric value for `nNumber`; both raise runtime errors.
    - Pass an unsupported `sDatepart` string such as `"week"`; the function only accepts the documented interval names.

## Caveats

- `sDatepart` is normalized to lowercase before validation, so values such as `"DAY"` and `"day"` behave the same.
- Negative numbers move the date backward instead of forward.

## Examples

### Add days to a start date to calculate a due date

Adds seven days to a fixed start date using the default `day` interval and displays the start and due dates.

```ssl
:PROCEDURE CalculateTaskDueDate;
	:DECLARE dStartDate, dDueDate, nDaysToAdd, sMessage;

	dStartDate := CToD("01/15/2024");
	nDaysToAdd := 7;

	dDueDate := DateAdd(dStartDate, nDaysToAdd);

	sMessage := "Task started on " + DToC(dStartDate)
				+ " and is due on " + DToC(dDueDate);

	UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("CalculateTaskDueDate");
```

[`UsrMes`](UsrMes.md) displays (assuming MM/DD/YYYY date format):

```text
Task started on 01/15/2024 and is due on 01/22/2024
```

### Add a year to a registration date and report renewal status

Adds one year to a fixed registration date using the `year` interval, then compares the resulting expiry date to today and displays the appropriate renewal status message.

```ssl
:PROCEDURE ComputeLicenseRenewal;
	:DECLARE dRegDate, dExpiry, dToday, nDaysUntilExpiry;
	:DECLARE sMessage, sRegDate, sExpiryDate;

	dRegDate := CToD("03/15/2023");
	dToday := Today();

	dExpiry := DateAdd(dRegDate, 1, "year");

	nDaysUntilExpiry := dExpiry - dToday;
	sRegDate := DToC(dRegDate);
	sExpiryDate := DToC(dExpiry);

	:IF nDaysUntilExpiry <= 30 .AND. nDaysUntilExpiry > 0;
		sMessage := "License issued on " + sRegDate
					+ " expires in " + LimsString(Integer(nDaysUntilExpiry))
					+ " days on " + sExpiryDate;
		/* Displays days remaining until expiry;
		UsrMes(sMessage);
	:ELSE;
		:IF nDaysUntilExpiry <= 0;
			sMessage := "License issued on " + sRegDate
						+ " expired on " + sExpiryDate;
			/* Displays the expired license date;
			UsrMes(sMessage);
		:ELSE;
			sMessage := "License issued on " + sRegDate
						+ " remains active until " + sExpiryDate;
			/* Displays the active license expiry date;
			UsrMes(sMessage);
		:ENDIF;
	:ENDIF;

	:RETURN dExpiry;
:ENDPROC;

/* Usage;
DoProc("ComputeLicenseRenewal");
```

## Related

- [`DateDiff`](DateDiff.md)
- [`DateDiffEx`](DateDiffEx.md)
- [`date`](../types/date.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
