---
title: "Second"
summary: "Extracts the seconds component from a date value."
id: ssl.function.second
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Second

Extracts the seconds component from a [date](../types/date.md) value.

`Second` returns the seconds portion of a [date](../types/date.md) as a [number](../types/number.md) from `0` to `59`. If the input date is empty, the function returns `0`. If the argument is [`NIL`](../literals/nil.md), or if the supplied value is not a date, the function raises an error.

## When to use

- When you need second-level time-of-day logic from a timestamp.
- When you need to compare or report the seconds portion without formatting the full date manually.
- When you need to distinguish events that occur within the same minute.

## Syntax

```ssl
Second(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | Date value to inspect |

## Returns

**[number](../types/number.md)** — The seconds component of `dDate`, from `0` to `59`. Returns `0` when `dDate` is empty.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `Argument: dDate cannot be null.` |
| `dDate` is not a date value. | `Argument: dDate must be of date type` |

## Best practices

!!! success "Do"
    - Pass a real date value before calling `Second`.
    - Treat a returned `0` carefully when empty dates are possible, because a valid timestamp at `hh:mm:00` also returns `0`.
    - Combine `Second` with [`Hour`](Hour.md) or [`Minute`](Minute.md) when second-only precision is not enough.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) and expect `0`; [`NIL`](../literals/nil.md) raises an error.
    - Pass strings or other non-date values and expect implicit conversion.
    - Assume `0` always means an exact minute boundary when your input may be empty.

## Caveats

- Times that fall exactly on `hh:mm:00` also return `0`, so the result alone does not distinguish those values from an empty date.

## Examples

### Show the current second

Retrieve the current timestamp and extract its seconds component. The output varies on every call.

```ssl
:PROCEDURE ShowCurrentSecond;
    :DECLARE dNow, nSecond;

    dNow := Now();
    nSecond := Second(dNow);

    UsrMes("Current second: " + LimsString(nSecond));
    :RETURN nSecond;
:ENDPROC;

/* Usage;
DoProc("ShowCurrentSecond");
```

[`UsrMes`](UsrMes.md) displays:

```
Current second: <0–59>
```

### Flag events that land on a minute boundary

Classify a list of timestamped events by checking whether their seconds component is zero, then collect the results for further processing.

```ssl
:PROCEDURE ClassifyEventsBySecond;
    :DECLARE aEvents, aResults, nIndex, dLoggedAt, nSecond;

    aEvents := {
        {"EVT-1001", DateFromNumbers(2026, 4, 18, 8, 15, 0)},
        {"EVT-1002", DateFromNumbers(2026, 4, 18, 8, 15, 42)},
        {"EVT-1003", DateFromNumbers(2026, 4, 18, 8, 16, 0)}
    };

    aResults := {};

    :FOR nIndex := 1 :TO ALen(aEvents);
        dLoggedAt := aEvents[nIndex, 2];
        nSecond := Second(dLoggedAt);

        :IF nSecond == 0;
            AAdd(aResults, {aEvents[nIndex, 1], "BOUNDARY", nSecond});
        :ELSE;
            AAdd(aResults, {aEvents[nIndex, 1], "INTRA_MINUTE", nSecond});
        :ENDIF;
    :NEXT;

    :RETURN aResults;
:ENDPROC;

/* Usage;
DoProc("ClassifyEventsBySecond");
```

### Count events into 60 second buckets

Accumulate a list of timestamped events into per-second occurrence counts using `Second` to map each event to its slot in a 60-element array.

```ssl
:PROCEDURE CountEventsBySecond;
    :DECLARE aEvents, aSecondCounts, nIndex, nSecond, nSlot;

    aEvents := {
        {DateFromNumbers(2026, 4, 18, 8, 15, 0), "Login"},
        {DateFromNumbers(2026, 4, 18, 8, 15, 12), "Approve"},
        {DateFromNumbers(2026, 4, 18, 8, 15, 12), "Review"},
        {DateFromNumbers(2026, 4, 18, 8, 15, 58), "Release"}
    };

    aSecondCounts := ArrayNew(60);

    :FOR nIndex := 1 :TO 60;
        aSecondCounts[nIndex] := 0;
    :NEXT;

    :FOR nIndex := 1 :TO ALen(aEvents);
        nSecond := Second(aEvents[nIndex, 1]);
        nSlot := nSecond + 1;
        aSecondCounts[nSlot] := aSecondCounts[nSlot] + 1;
    :NEXT;

    :RETURN aSecondCounts;
:ENDPROC;

/* Usage;
DoProc("CountEventsBySecond");
```

## Related

- [`Hour`](Hour.md)
- [`Minute`](Minute.md)
- [`Now`](Now.md)
- [`date`](../types/date.md)
- [`number`](../types/number.md)
