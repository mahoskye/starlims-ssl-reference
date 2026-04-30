---
title: "ServerEndOfDay"
summary: "Returns a date value set to the end of its day."
id: ssl.function.serverendofday
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ServerEndOfDay

Returns a date value set to the end of its day.

`ServerEndOfDay(dDate)` validates that the argument is a non-null date value, then returns a new date for the same year, month, and day with the time set to `23:59:59.997`. If `dDate` is an empty date, the function returns the original value unchanged. Use this function when you need an inclusive upper boundary for server-side day-based logic.

## When to use

- When you need an inclusive upper boundary for a server-side date range.
- When pairing with [`ServerStartOfDay`](ServerStartOfDay.md) to cover a full calendar day.
- When normalizing a date value before filtering, reporting, or batch logic.

## Syntax

```ssl
ServerEndOfDay(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | The date value to convert to the end of its day. |

## Returns

**[date](../types/date.md)** — A date value set to `23:59:59.997` for the same calendar day as the input. If `dDate` is an empty date, the original value is returned unchanged.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `Argument: dDate cannot be null.` |
| `dDate` is not a date value. | `Argument: dDate must be of date type` |

## Best practices

!!! success "Do"
    - Use this function to create an inclusive end-of-day boundary for server-side logic.
    - Pair it with [`ServerStartOfDay`](ServerStartOfDay.md) when you need a full-day range.
    - Handle empty dates deliberately if your workflow distinguishes between no date and a real cutoff.

!!! failure "Don't"
    - Pass strings, numbers, or other non-date values. The function raises an error instead of converting them.
    - Treat an empty date as if it were a computed end-of-day value. Empty dates are returned unchanged.
    - Use this when the cutoff must follow the user's local day. Call [`ClientEndOfDay`](ClientEndOfDay.md) instead.

## Caveats

- The `23:59:59.997` time includes milliseconds, so it stops just short of the next calendar day — appropriate for inclusive range comparisons at millisecond precision.

## Examples

### Normalize a date to the server day's end

Take any date value and return a version stamped to `23:59:59.997` on the same calendar day, then display the result.

```ssl
:PROCEDURE GetServerCutoff;
    :PARAMETERS dWorkDate;
    :DECLARE dCutoff, sMessage;

    dCutoff := ServerEndOfDay(dWorkDate);

    sMessage := "Server cutoff: " + LimsString(dCutoff);
    UsrMes(sMessage);

    :RETURN dCutoff;
:ENDPROC;

/* Usage;
DoProc("GetServerCutoff", {DateFromNumbers(2026, 4, 15)});
```

[`UsrMes`](UsrMes.md) displays:

```text
Server cutoff: <04/15/2026 23:59:59>
```

### Build a full-day server-side query range

Use [`ServerStartOfDay`](ServerStartOfDay.md) and `ServerEndOfDay` together to build an inclusive date range covering one calendar day, then pass both boundaries as query parameters.

```ssl
:PROCEDURE GetOrdersForDay;
    :PARAMETERS dOrderDate;
    :DECLARE dRangeStart, dRangeEnd, sSQL, sOrdersXml;

    dRangeStart := ServerStartOfDay(dOrderDate);
    dRangeEnd := ServerEndOfDay(dOrderDate);

    sSQL := "
        SELECT ordno, status, logdate
        FROM orders
        WHERE logdate >= ?
          AND logdate <= ?
        ORDER BY logdate
    ";

    sOrdersXml := GetDataSet(sSQL, {dRangeStart, dRangeEnd});

    :RETURN sOrdersXml;
:ENDPROC;

/* Usage;
DoProc("GetOrdersForDay", {DateFromNumbers(2026, 4, 15)});
```

### Compare server and client day cutoffs

Compute both the server and client end-of-day boundaries for the same input and show whether they agree.

```ssl
:PROCEDURE CompareDayCutoffs;
    :PARAMETERS dEventDate;
    :DECLARE dServerEnd, dClientEnd, sSummary;

    dServerEnd := ServerEndOfDay(dEventDate);
    dClientEnd := ClientEndOfDay(dEventDate);

    sSummary := "Server end: " + LimsString(dServerEnd)
        + ", Client end: " + LimsString(dClientEnd);

    :IF dServerEnd == dClientEnd;
        UsrMes(sSummary + " (same cutoff)");
    :ELSE;
        UsrMes(sSummary + " (different cutoff)");
    :ENDIF;

    :RETURN dServerEnd;
:ENDPROC;

/* Usage;
DoProc("CompareDayCutoffs", {DateFromNumbers(2026, 4, 15)});
```

`UsrMes` displays one of:

```text
Server end: [date], Client end: [date] (same cutoff)
```

```text
Server end: [date], Client end: [date] (different cutoff)
```

## Related

- [`ClientEndOfDay`](ClientEndOfDay.md)
- [`ClientStartOfDay`](ClientStartOfDay.md)
- [`ServerStartOfDay`](ServerStartOfDay.md)
- [`date`](../types/date.md)
