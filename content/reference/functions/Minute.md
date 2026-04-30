---
title: "Minute"
summary: "Extracts the minute component from a date value."
id: ssl.function.minute
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Minute

Extracts the minute component from a date value.

`Minute` returns the minute portion of a date as a number from `0` to `59`.
If the input date is empty, the function returns `0`. If the argument is [`NIL`](../literals/nil.md), or if the supplied value is not a date, the function raises an error.

## When to use

- When you need time-of-day logic based on a timestamp's minute value.
- When you need to group or count records by minute.
- When you need the minute without parsing a formatted date string.

## Syntax

```ssl
Minute(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | Date value to inspect |

## Returns

**[number](../types/number.md)** — The minute component of `dDate`, from `0` to `59`. Returns `0` when `dDate` is empty.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `Argument: dDate cannot be null.` |
| `dDate` is not a date value. | `Argument: dDate must be of date type` |

## Best practices

!!! success "Do"
    - Pass a real date value before calling `Minute`.
    - Treat a returned `0` carefully when empty dates are possible, because `hh:00:ss` also returns `0`.
    - Combine `Minute` with [`Hour`](Hour.md) or [`Second`](Second.md) when minute-only precision is not enough.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) and expect `0`; [`NIL`](../literals/nil.md) raises an error.
    - Pass strings or other non-date values and expect implicit conversion.
    - Assume `0` always means the top of the hour when your input may be empty.

## Caveats

- Times at the top of the hour also return `0`, so the result alone does not distinguish `hh:00` from an empty date.

## Examples

### Show the current minute

Get the current system time with [`Now`](Now.md) and extract the minute component. The output depends on when the procedure runs.

```ssl
:PROCEDURE ShowCurrentMinute;
	:DECLARE dNow, nMinute;

	dNow := Now();
	nMinute := Minute(dNow);

	UsrMes("Current minute: " + LimsString(nMinute));
	:RETURN nMinute;
:ENDPROC;

/*
Usage
;
DoProc("ShowCurrentMinute");
```

[`UsrMes`](UsrMes.md) displays:

```
Current minute: 42
```

The exact value depends on when the procedure runs.

### Count events into 60 minute buckets

Build a 60-slot counter array and increment each slot by the minute component of each event timestamp. Events at the same minute accumulate in the same slot.

```ssl
:PROCEDURE CountEventsByMinute;
	:DECLARE aEvents, aMinuteCounts, nIndex, nMinute, nSlot;

	aEvents := {
		{DateFromNumbers(2026, 4, 18, 8, 15, 0), "Login"},
		{DateFromNumbers(2026, 4, 18, 8, 15, 45), "Approve"},
		{DateFromNumbers(2026, 4, 18, 8, 16, 10), "Release"},
		{DateFromNumbers(2026, 4, 18, 8, 42, 5), "Archive"}
	};

	aMinuteCounts := ArrayNew(60);

	:FOR nIndex := 1 :TO 60;
		aMinuteCounts[nIndex] := 0;
	:NEXT;

	:FOR nIndex := 1 :TO ALen(aEvents);
		nMinute := Minute(aEvents[nIndex, 1]);
		nSlot := nMinute + 1;
		aMinuteCounts[nSlot] := aMinuteCounts[nSlot] + 1;
	:NEXT;

	:RETURN aMinuteCounts;
:ENDPROC;

/*
Usage
;
DoProc("CountEventsByMinute");
```

### Route requests that arrive in the last five minutes of the hour

Classify each request as `ESCALATE` when its timestamp falls at minute 55 or later, and `STANDARD` otherwise. This lets downstream logic apply a different processing path for near-deadline submissions.

```ssl
:PROCEDURE ClassifyRequestsByMinute;
	:DECLARE aRequests, aStatuses, nIndex, dRequestedAt, nMinute;

	aRequests := {
		{"REQ-1001", DateFromNumbers(2026, 4, 18, 8, 12, 0)},
		{"REQ-1002", DateFromNumbers(2026, 4, 18, 8, 55, 0)},
		{"REQ-1003", DateFromNumbers(2026, 4, 18, 8, 59, 30)}
	};

	aStatuses := {};

	:FOR nIndex := 1 :TO ALen(aRequests);
		dRequestedAt := aRequests[nIndex, 2];
		nMinute := Minute(dRequestedAt);

		:IF nMinute >= 55;
			AAdd(aStatuses, {aRequests[nIndex, 1], "ESCALATE", nMinute});
		:ELSE;
			AAdd(aStatuses, {aRequests[nIndex, 1], "STANDARD", nMinute});
		:ENDIF;
	:NEXT;

	:RETURN aStatuses;
:ENDPROC;

/*
Usage
;
DoProc("ClassifyRequestsByMinute");
```

## Related

- [`Hour`](Hour.md)
- [`Now`](Now.md)
- [`Second`](Second.md)
- [`number`](../types/number.md)
- [`date`](../types/date.md)
