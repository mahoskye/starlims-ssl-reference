---
title: "Hour"
summary: "Extracts the hour component from a date value."
id: ssl.function.hour
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Hour

Extracts the hour component from a date value.

`Hour` returns the hour portion of a date as a number from `0` to `23`. If the
input date is empty, the function returns `0`. If the argument is [`NIL`](../literals/nil.md), or if the supplied value is not a date, the function raises an error.

## When to use

- When you need time-of-day logic based on a timestamp's hour value.
- When you need to group or count records by hour.
- When you need the hour without separately parsing a formatted date string.

## Syntax

```ssl
Hour(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | Date value to inspect |

## Returns

**[number](../types/number.md)** — The hour component of `dDate`, from `0` to `23`. Returns `0` when `dDate` is empty.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `Argument: dDate cannot be null.` |
| `dDate` is not a date value. | `Argument: dDate must be of date type` |

## Best practices

!!! success "Do"
    - Pass a real date value before calling `Hour`.
    - Treat a returned `0` carefully when empty dates are possible, because midnight also returns `0`.
    - Combine `Hour` with [`Minute`](Minute.md) or [`Second`](Second.md) when hour-only precision is not enough.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) and expect `0`; [`NIL`](../literals/nil.md) raises an error.
    - Pass strings or other non-date values and expect implicit conversion.
    - Assume `0` always means midnight when your input may be empty.

## Caveats

- Midnight also returns `0`, so the result alone does not distinguish midnight from an empty date.

## Examples

### Choose a greeting based on the current hour

Call `Hour` on the current timestamp and use its value to select a time-of-day greeting. Because the procedure reads the live clock, the greeting and hour shown in the output are representative, and the actual values depend on when the procedure runs.

```ssl
:PROCEDURE ShowLoginGreeting;
	:DECLARE dNow, nHour, sGreeting;

	dNow := Now();
	nHour := Hour(dNow);

	:BEGINCASE;
	:CASE nHour < 12;
		sGreeting := "Good morning";
		:EXITCASE;
	:CASE nHour < 17;
		sGreeting := "Good afternoon";
		:EXITCASE;
	:OTHERWISE;
		sGreeting := "Good evening";
		:EXITCASE;
	:ENDCASE;

	UsrMes(sGreeting + ". Current hour: " + LimsString(nHour));
:ENDPROC;

/* Usage;
DoProc("ShowLoginGreeting");
```

[`UsrMes`](UsrMes.md) displays:

```
Good morning. Current hour: 9
```

### Count events into 24 hourly buckets

Build a 24-element frequency array by extracting the hour from each event's timestamp and incrementing the corresponding slot. This shows how `Hour` converts a full timestamp into an array index for time-based aggregation.

```ssl
:PROCEDURE CountEventsByHour;
	:DECLARE aEvents, aHourCounts, nIndex, nHour, nSlot;

	aEvents := {
		{DateFromNumbers(2026, 4, 18, 8, 15, 0), "Login"},
		{DateFromNumbers(2026, 4, 18, 8, 42, 0), "Login"},
		{DateFromNumbers(2026, 4, 18, 9, 5, 0), "Approve"},
		{DateFromNumbers(2026, 4, 18, 17, 30, 0), "Release"}
	};

	aHourCounts := ArrayNew(24);

	:FOR nIndex := 1 :TO 24;
		aHourCounts[nIndex] := 0;
	:NEXT;

	:FOR nIndex := 1 :TO ALen(aEvents);
		nHour := Hour(aEvents[nIndex, 1]);
		nSlot := nHour + 1;
		aHourCounts[nSlot] := aHourCounts[nSlot] + 1;
	:NEXT;

	:RETURN aHourCounts;
:ENDPROC;

/* Usage;
DoProc("CountEventsByHour");
```

### Route requests based on whether they fall inside business hours

Classify a list of timestamped requests as either ready to process or queued, using `Hour` to test each timestamp against a configurable business-hours window. Requests whose hour falls before `nOpenHour` or at or after `nCloseHour` are assigned the `QUEUE` status.

```ssl
:PROCEDURE ClassifyRequestsByHour;
	:DECLARE aRequests, aStatuses, nIndex, dRequestedAt, nHour;
	:DECLARE nOpenHour, nCloseHour;

	aRequests := {
		{"REQ-1001", DateFromNumbers(2026, 4, 18, 7, 45, 0)},
		{"REQ-1002", DateFromNumbers(2026, 4, 18, 10, 0, 0)},
		{"REQ-1003", DateFromNumbers(2026, 4, 18, 18, 10, 0)}
	};

	aStatuses := {};
	nOpenHour := 9;
	nCloseHour := 17;

	:FOR nIndex := 1 :TO ALen(aRequests);
		dRequestedAt := aRequests[nIndex, 2];
		nHour := Hour(dRequestedAt);

		:IF nHour >= nOpenHour .AND. nHour < nCloseHour;
			AAdd(aStatuses, {aRequests[nIndex, 1], "PROCESS_NOW", nHour});
		:ELSE;
			AAdd(aStatuses, {aRequests[nIndex, 1], "QUEUE", nHour});
		:ENDIF;
	:NEXT;

	:RETURN aStatuses;
:ENDPROC;

/* Usage;
DoProc("ClassifyRequestsByHour");
```

## Related

- [`Minute`](Minute.md)
- [`Now`](Now.md)
- [`Second`](Second.md)
- [`number`](../types/number.md)
- [`date`](../types/date.md)
