---
title: "ClientStartOfDay"
summary: "Returns the timestamp for the start of the client's calendar day."
id: ssl.function.clientstartofday
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ClientStartOfDay

Returns the timestamp for the start of the client's calendar day.

`ClientStartOfDay` returns the value that corresponds to the beginning of the client-local day that contains the supplied date. If `dDate` is an empty date, the function returns it unchanged. If the value does not carry timezone information, the function behaves like [`ServerStartOfDay`](ServerStartOfDay.md). Otherwise it uses the difference between the user and server timezone offsets to calculate the client-day boundary.

## When to use

- When date filters or reports must follow the user's calendar day rather than the server's.
- When you need the client-side lower bound of an inclusive date range.
- When the same timestamp may belong to different calendar days for the user and the server.

## Syntax

```ssl
ClientStartOfDay(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `dDate` | [date](../types/date.md) | yes | — | The date value to convert to the start of the client-local day. |

## Returns

**[date](../types/date.md)** — A date value representing the start of the applicable client-local day. If `dDate` is an empty date, the original value is returned unchanged.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `Argument: dDate cannot be null.` |
| `dDate` is not a date value. | `Argument: dDate must be of date type.` |

## Best practices

!!! success "Do"
    - Use this function when the user's local day boundary matters more than the server's day boundary.
    - Pair it with [`ClientEndOfDay`](ClientEndOfDay.md) when building an inclusive client-local date range.
    - Handle empty dates deliberately if your workflow distinguishes between no date and a real cutoff.

!!! failure "Don't"
    - Pass strings, numbers, or other non-date values. The function raises an error instead of converting them.
    - Assume client and server start-of-day values are interchangeable. Different timezone offsets can place the same timestamp on different calendar days.
    - Treat an empty date as a computed day-start value. This function returns empty dates unchanged.

## Caveats

- If the input date does not carry timezone information, the function follows [`ServerStartOfDay`](ServerStartOfDay.md) behavior.
- If no user timezone offset is available, the server timezone offset is used for the client-side calculation.

## Examples

### Normalize a user-selected date to the client-local day start

Converts a user-selected date to the start of the client-local day and displays the resulting boundary timestamp.

```ssl
:PROCEDURE NormalizeClientFilterDate;
	:PARAMETERS dSelectedDate;
	:DECLARE dFilterStart, sMessage;

	dFilterStart := ClientStartOfDay(dSelectedDate);

	sMessage := "Client day starts at: " + LimsString(dFilterStart);
	UsrMes(sMessage);

	:RETURN dFilterStart;
:ENDPROC;

/* Usage;
DoProc("NormalizeClientFilterDate", {CToD("04/23/2026")});
```

`UsrMes` displays:

```text
Client day starts at: [date at 00:00:00.000]
```

### Query records across a full client-local calendar day

Pairs `ClientStartOfDay` with [`ClientEndOfDay`](ClientEndOfDay.md) to build an inclusive date range for the user's full calendar day and passes both bounds to a SQL query.

```ssl
:PROCEDURE GetClientDayResults;
	:PARAMETERS dSelectedDate;
	:DECLARE dDayStart, dDayEnd, sSQL, sResultsXml;

	dDayStart := ClientStartOfDay(dSelectedDate);
	dDayEnd := ClientEndOfDay(dSelectedDate);

	sSQL := "
	    SELECT sample_id, sample_name, received_on
	    FROM sample
	    WHERE received_on >= ?
	      AND received_on <= ?
	    ORDER BY received_on
	";

	sResultsXml := GetDataSet(sSQL, {dDayStart, dDayEnd});

	:RETURN sResultsXml;
:ENDPROC;

/* Usage;
DoProc("GetClientDayResults", {CToD("04/23/2026")});
```

### Compare client and server day-start boundaries

Computes both the client and server start-of-day for the same input date and reports whether they produce the same boundary.

```ssl
:PROCEDURE CompareDayBoundaries;
	:PARAMETERS dEventDate;
	:DECLARE dClientStart, dServerStart, sSummary;

	dClientStart := ClientStartOfDay(dEventDate);
	dServerStart := ServerStartOfDay(dEventDate);

	sSummary := "Client start: " + LimsString(dClientStart)
				+ ", Server start: " + LimsString(dServerStart);

	:IF dClientStart == dServerStart;
		UsrMes(sSummary + " (same day boundary)");
	:ELSE;
		UsrMes(sSummary + " (different day boundary)");
	:ENDIF;

	:RETURN dClientStart;
:ENDPROC;

/* Usage;
DoProc("CompareDayBoundaries", {CToD("04/23/2026")});
```

`UsrMes` displays one of:

```text
Client start: [date], Server start: [date] (same day boundary)
```

```text
Client start: [date], Server start: [date] (different day boundary)
```

## Related

- [`ClientEndOfDay`](ClientEndOfDay.md)
- [`ServerEndOfDay`](ServerEndOfDay.md)
- [`ServerStartOfDay`](ServerStartOfDay.md)
- [`date`](../types/date.md)
