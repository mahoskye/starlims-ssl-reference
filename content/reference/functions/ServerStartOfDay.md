---
title: "ServerStartOfDay"
summary: "Returns a date value set to the start of its day."
id: ssl.function.serverstartofday
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ServerStartOfDay

Returns a date value set to the start of its day.

`ServerStartOfDay(dDate)` validates that the argument is a non-null date value, then returns a date for the same calendar day with the time set to `00:00:00`. If `dDate` is an empty date, the function returns the original value unchanged. Use this function when you need a server-side lower boundary for day-based comparisons, filters, or reporting.

## When to use

- When you need the inclusive lower boundary for a server-side date range.
- When pairing with [`ServerEndOfDay`](ServerEndOfDay.md) to cover one full calendar day.
- When normalizing a date before grouping, filtering, or comparing by day.

## Syntax

```ssl
ServerStartOfDay(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | The date value to convert to the start of its day. |

## Returns

**[date](../types/date.md)** — A date value set to `00:00:00` for the same calendar day as the input. If `dDate` is an empty date, the original value is returned unchanged.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `Argument: dDate cannot be null.` |
| `dDate` is not a date value. | `Argument: dDate must be of date type` |

## Best practices

!!! success "Do"
    - Use this function to create a server-side day start before filtering or grouping records.
    - Pair it with [`ServerEndOfDay`](ServerEndOfDay.md) when you need an inclusive full-day range.
    - Handle empty dates deliberately if your workflow distinguishes between no date and a real boundary.

!!! failure "Don't"
    - Pass strings, numbers, or other non-date values. The function raises an error instead of converting them.
    - Treat an empty date as if it were a computed midnight value. Empty dates are returned unchanged.
    - Use this when the boundary must follow the user's local day. Call [`ClientStartOfDay`](ClientStartOfDay.md) instead.

## Caveats

- Unlike [`ClientStartOfDay`](ClientStartOfDay.md), this function does not apply client timezone offset logic.

## Examples

### Normalize a date to the server day's start

Take any date value and return a version stamped to `00:00:00` on the same calendar day, then display the result.

```ssl
:PROCEDURE GetServerDayStart;
    :PARAMETERS dWorkDate;
    :DECLARE dDayStart, sMessage;

    dDayStart := ServerStartOfDay(dWorkDate);

    sMessage := "Server day start: " + LimsString(dDayStart);
    UsrMes(sMessage);

    :RETURN dDayStart;
:ENDPROC;

/* Usage;
DoProc("GetServerDayStart", {DateFromNumbers(2026, 4, 15)});
```

[`UsrMes`](UsrMes.md) displays:

```text
Server day start: <04/15/2026 00:00:00>
```

### Build a full-day server-side query range

Use `ServerStartOfDay` and [`ServerEndOfDay`](ServerEndOfDay.md) together to build an inclusive date range covering one calendar day, then pass both boundaries as query parameters.

```ssl
:PROCEDURE GetSamplesForDay;
    :PARAMETERS dSampleDate;
    :DECLARE dRangeStart, dRangeEnd, sSQL, sSamplesXml;

    dRangeStart := ServerStartOfDay(dSampleDate);
    dRangeEnd := ServerEndOfDay(dSampleDate);

    sSQL := "
        SELECT sample_id, sample_name, collected_date
        FROM sample
        WHERE collected_date >= ?
          AND collected_date <= ?
        ORDER BY collected_date
    ";

    sSamplesXml := GetDataSet(sSQL, {dRangeStart, dRangeEnd});

    :RETURN sSamplesXml;
:ENDPROC;

/* Usage;
DoProc("GetSamplesForDay", {DateFromNumbers(2026, 4, 15)});
```

### Compare server and client day starts

Compute both the server and client start-of-day boundaries for the same input and show whether they agree.

```ssl
:PROCEDURE CompareDayStarts;
    :PARAMETERS dEventDate;
    :DECLARE dServerStart, dClientStart, sSummary;

    dServerStart := ServerStartOfDay(dEventDate);
    dClientStart := ClientStartOfDay(dEventDate);

    sSummary := "Server start: " + LimsString(dServerStart)
        + ", Client start: " + LimsString(dClientStart);

    :IF dServerStart == dClientStart;
        /* Displays same-boundary summary with both start times;
        UsrMes(sSummary + " (same day boundary)");
    :ELSE;
        /* Displays different-boundary summary with both start times;
        UsrMes(sSummary + " (different day boundary)");
    :ENDIF;

    :RETURN dServerStart;
:ENDPROC;

/* Usage;
DoProc("CompareDayStarts", {DateFromNumbers(2026, 4, 15)});
```

## Related

- [`ClientEndOfDay`](ClientEndOfDay.md)
- [`ClientStartOfDay`](ClientStartOfDay.md)
- [`ServerEndOfDay`](ServerEndOfDay.md)
- [`date`](../types/date.md)
