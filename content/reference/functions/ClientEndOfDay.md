---
title: "ClientEndOfDay"
summary: "Returns the end of the client's calendar day for a date value."
id: ssl.function.clientendofday
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ClientEndOfDay

Returns the end of the client's calendar day for a date value.

`ClientEndOfDay` returns a date set to `23:59:59.997` for the client-local day that contains the supplied value. If the input carries timezone information, the function adjusts between the user and server timezone offsets before calculating that boundary. If the input is an empty date, the function returns it unchanged. If the input does not carry timezone information, the function follows [`ServerEndOfDay`](ServerEndOfDay.md) behavior.

## When to use

- When filtering or reporting through the end of a day as the user experiences that day.
- When an inclusive upper date boundary must follow client-local time rather than server time.
- When you need the client-side counterpart to [`ServerEndOfDay`](ServerEndOfDay.md).

## Syntax

```ssl
ClientEndOfDay(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | The date value to convert to the end of the client-local day. |

## Returns

**[date](../types/date.md)** — A date value set to `23:59:59.997` for the applicable client-local day. If `dDate` is an empty date, the original value is returned unchanged.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `Argument: dDate cannot be null.` |
| `dDate` is not a date value. | `Argument: dDate must be of date type.` |

## Best practices

!!! success "Do"
    - Use this function for inclusive upper bounds that must follow the client's calendar day.
    - Handle empty dates deliberately if your workflow distinguishes between no date and a real cutoff.
    - Use [`ServerEndOfDay`](ServerEndOfDay.md) instead when server-defined day boundaries are the real requirement.

!!! failure "Don't"
    - Pass strings, numbers, or other non-date values. The function raises an error instead of converting them.
    - Assume client and server day boundaries are interchangeable. They can differ when timezone offsets differ.
    - Treat an empty date as a computed end-of-day value. This function returns empty dates unchanged.

## Caveats

- If the input date does not carry timezone information, the function follows [`ServerEndOfDay`](ServerEndOfDay.md) behavior.
- If no user timezone offset is available, the server offset is used for the client-side calculation.

## Examples

### Build an inclusive upper bound for a user-selected day

Converts a user-selected date to the end of the client-local day and displays the resulting date-time value.

```ssl
:PROCEDURE GetClientDayCutoff;
	:PARAMETERS dSelectedDate;
	:DECLARE dEndOfDay, sMessage;

	dEndOfDay := ClientEndOfDay(dSelectedDate);

	sMessage := "Client end of day: " + LimsString(dEndOfDay);
	UsrMes(sMessage);

	:RETURN dEndOfDay;
:ENDPROC;

/* Usage;
DoProc("GetClientDayCutoff", {CToD("04/23/2026")});
```

`UsrMes` displays:

```text
Client end of day: [date at 23:59:59.997]
```

### Use the end-of-day cutoff as a query upper bound

Passes the client end-of-day value as the upper bound of a SQL query so only transactions on or before the end of the user's calendar day are included.

```ssl
:PROCEDURE GenerateClientDayReport;
	:PARAMETERS dClientDate;
	:DECLARE dEndOfDay, sSQL, sTransactionsXml;

	dEndOfDay := ClientEndOfDay(dClientDate);

	sSQL := "
	    SELECT transaction_id, amount, transaction_date
	    FROM transactions
	    WHERE transaction_date <= ?
	    ORDER BY transaction_date
	";

	sTransactionsXml := GetDataSet(sSQL, {dEndOfDay});

	:RETURN sTransactionsXml;
:ENDPROC;

/* Usage;
DoProc("GenerateClientDayReport", {CToD("04/23/2026")});
```

### Compare client and server end-of-day cutoffs

Computes both the client and server end-of-day for the same input date and reports whether they produce the same cutoff.

```ssl
:PROCEDURE CompareDayCutoffs;
	:PARAMETERS dEventDate;
	:DECLARE dClientEnd, dServerEnd, sSummary;

	dClientEnd := ClientEndOfDay(dEventDate);
	dServerEnd := ServerEndOfDay(dEventDate);

	sSummary := "Client end: " + LimsString(dClientEnd)
				+ ", Server end: " + LimsString(dServerEnd);

	:IF dClientEnd == dServerEnd;
		UsrMes(sSummary + " (same cutoff)");
	:ELSE;
		UsrMes(sSummary + " (different cutoff)");
	:ENDIF;

	:RETURN dClientEnd;
:ENDPROC;

/* Usage;
DoProc("CompareDayCutoffs", {CToD("04/23/2026")});
```

`UsrMes` displays one of:

```text
Client end: [date], Server end: [date] (same cutoff)
```

```text
Client end: [date], Server end: [date] (different cutoff)
```

## Related

- [`ClientStartOfDay`](ClientStartOfDay.md)
- [`ServerEndOfDay`](ServerEndOfDay.md)
- [`ServerStartOfDay`](ServerStartOfDay.md)
- [`date`](../types/date.md)
