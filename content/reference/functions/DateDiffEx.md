---
title: "DateDiffEx"
summary: "Returns the elapsed interval between two date values as an object."
id: ssl.function.datediffex
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DateDiffEx

Returns the elapsed interval between two date values as an object.

`DateDiffEx` subtracts `dStartDate` from `dEndDate` and returns an interval object for the full elapsed span. Use it when you need interval members such as `Days`, `Hours`, `Minutes`, [`Seconds`](Seconds.md), or `TotalDays` instead of one whole-number result.

Use [`DateDiff`](DateDiff.md) when you need a numeric difference in one
specific unit.

## When to use

- When you need the elapsed interval between two date values.
- When your logic needs interval members such as days, hours, or minutes.
- When you need to detect whether `dEndDate` is earlier than `dStartDate`.

## Syntax

```ssl
DateDiffEx(dStartDate, dEndDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dStartDate` | [date](../types/date.md) | yes | — | The starting date value. |
| `dEndDate` | [date](../types/date.md) | yes | — | The ending date value. |

## Returns

**[object](../types/object.md)** — An interval object representing `dEndDate - dStartDate`. Read the members you need from the returned object rather than expecting a single number.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dStartDate` is [`NIL`](../literals/nil.md). | `Argument: startDate cannot be null.` |
| `dStartDate` is not a date value. | `Argument: startDate must be of date type` |
| `dEndDate` is [`NIL`](../literals/nil.md). | `Argument: endDate cannot be null.` |
| `dEndDate` is not a date value. | `Argument: endDate must be of date type` |

## Best practices

!!! success "Do"
    - Pass validated date values for both arguments.
    - Read the interval members you need from the returned object.
    - Use `DateDiffEx` when your logic needs a full interval instead of one numeric unit.

!!! failure "Don't"
    - Treat the return value as a plain number.
    - Pass [`NIL`](../literals/nil.md) or non-date values for either argument.
    - Use `DateDiffEx` when [`DateDiff`](DateDiff.md) already provides the single-unit number you need.

## Caveats

- The result can be negative when `dEndDate` is earlier than `dStartDate`.

## Examples

### Read hours and minutes from an approval interval

Computes the interval between a submission time and an approval time, then reads the `Hours` and `Minutes` members from the returned object to build a summary message.

```ssl
:PROCEDURE ShowApprovalInterval;
	:DECLARE dSubmittedAt, dApprovedAt, oInterval, sMessage;

	dSubmittedAt := DateFromNumbers(2026, 4, 18, 8, 30, 0);
	dApprovedAt := DateFromNumbers(2026, 4, 18, 14, 45, 0);

	oInterval := DateDiffEx(dSubmittedAt, dApprovedAt);

	sMessage := "Approval time: " + LimsString(oInterval:Hours)
				+ " hours and " + LimsString(oInterval:Minutes) + " minutes";
	UsrMes(sMessage);

	:RETURN oInterval;
:ENDPROC;

/* Usage;
DoProc("ShowApprovalInterval");
```

[`UsrMes`](UsrMes.md) displays:

```text
Approval time: 6 hours and 15 minutes
```

### Reject an end date that is earlier than the start date

Computes the interval between two dates where the end precedes the start, checks `TotalDays` for a negative value, and returns early with an error message.

```ssl
:PROCEDURE ValidateIntervalOrder;
	:DECLARE dStartDate, dEndDate, oInterval, sMessage;

	dStartDate := DateFromNumbers(2026, 4, 18, 9, 0, 0);
	dEndDate := DateFromNumbers(2026, 4, 17, 17, 0, 0);

	oInterval := DateDiffEx(dStartDate, dEndDate);

	:IF oInterval:TotalDays < 0;
		sMessage := "End date must be on or after the start date";
		UsrMes(sMessage);
		:RETURN .F.;
	:ENDIF;

	UsrMes("Interval is valid");

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ValidateIntervalOrder");
```

### Break a multi-day turnaround into days, hours, and minutes

Computes the elapsed interval between a receipt time and a completion time three days later, then formats the `Days`, `Hours`, and `Minutes` members into a single summary string.

```ssl
:PROCEDURE SummarizeTurnaround;
	:DECLARE dReceivedAt, dCompletedAt, oInterval, sSummary;

	dReceivedAt := DateFromNumbers(2026, 4, 14, 10, 15, 0);
	dCompletedAt := DateFromNumbers(2026, 4, 17, 13, 50, 0);

	oInterval := DateDiffEx(dReceivedAt, dCompletedAt);

	sSummary := "Turnaround time: " + LimsString(oInterval:Days) + " days, "
				+ LimsString(oInterval:Hours) + " hours, "
				+ LimsString(oInterval:Minutes) + " minutes";
	UsrMes(sSummary);

	:RETURN oInterval;
:ENDPROC;

/* Usage;
DoProc("SummarizeTurnaround");
```

[`UsrMes`](UsrMes.md) displays:

```text
Turnaround time: 3 days, 3 hours, 35 minutes
```

## Related

- [`DateAdd`](DateAdd.md)
- [`DateDiff`](DateDiff.md)
- [`date`](../types/date.md)
- [`object`](../types/object.md)
