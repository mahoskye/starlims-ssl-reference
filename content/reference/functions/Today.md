---
title: "Today"
summary: "Returns the current date as a date object."
id: ssl.function.today
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Today

Returns the current date as a date object.

`Today()` returns the current system date as an SSL date value with no time
component. Use it when your logic should depend on the current day only.

Unlike [`Now()`](Now.md), `Today()` is date-only. You can compare its result with other date values, store it in variables, pass it to date functions, or format it with helpers such as [`DToC`](DToC.md).

## When to use

- When you need the current date for validation, filtering, or comparisons
  without a time component.
- When you want one date value to reuse across an operation, such as stamping rows or setting defaults.
- When calculating due dates, expirations, or age checks based on the current
  day.
- When you need a date value that can be passed directly to other SSL date functions.

## Syntax

```ssl
Today()
```

## Parameters

This function takes no parameters.

## Returns

**[date](../types/date.md)** — The current system date as an SSL date value.

## Best practices

!!! success "Do"
    - Use `Today()` when you need the current day without a time component.
    - Capture the value once and reuse it when several related steps should use the same date.
    - Compare date values directly and format them only for display.

!!! failure "Don't"
    - Use [`Now()`](Now.md) when you need date-only logic. Its time component can change comparison results.
    - Convert `Today()` to text too early if the value still needs to be compared or stored as a date.
    - Call `Today()` repeatedly in one logical operation if all steps should use the same captured date.

## Caveats

- `Today()` returns a date value, not formatted text.

## Examples

### Compare a due date with today

Check whether a record is due today. The due date is set to a specific past date, so the else branch runs and reports that the record is not due today.

```ssl
:PROCEDURE CheckDueToday;
	:DECLARE dDueDate, dToday, sMessage;

	dToday := Today();
	dDueDate := CToD("04/11/2026");

	:IF dDueDate == dToday;
		sMessage := "The record is due today: " + DToC(dToday);
	:ELSE;
		sMessage := "The record is not due today";
	:ENDIF;

	UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("CheckDueToday");
```

[`UsrMes`](UsrMes.md) displays:

```text
The record is not due today
```

### Use `Today()` in a date-filtered query

Capture the current date once and reuse it as a named [`SQLExecute`](SQLExecute.md) parameter so the query and the result message both reference the same value.

```ssl
:PROCEDURE GetTodaySamples;
	:DECLARE dToday, sSQL, aSamples, nCount, sMessage;

	dToday := Today();

	sSQL :=

		"
	    SELECT sample_id, receivedate, status
	    FROM sample
	    WHERE receivedate = ?dToday?
	    ORDER BY sample_id
	";

	aSamples := SQLExecute(sSQL);
	nCount := ALen(aSamples);

	:IF nCount > 0;
		sMessage := "Found " + LimsString(nCount) + " sample(s) for " + DToC(dToday);
	:ELSE;
		sMessage := "No samples found for " + DToC(dToday);
	:ENDIF;

	UsrMes(sMessage);

	:RETURN aSamples;
:ENDPROC;

/* Usage;
DoProc("GetTodaySamples");
```

`UsrMes` displays one of:

```text
Found <n> sample(s) for <date>
No samples found for <date>
```

### Reuse one captured date across update logic

Use one `Today()` value for both an update and a follow-up message so every
step uses the same date.

```ssl
:PROCEDURE StampReviewDate;
	:DECLARE dReviewDate, sSQL, bUpdated, sSampleID, sMessage;

	dReviewDate := Today();
	sSampleID := "S-1001";

	sSQL :=

		"
	    UPDATE sample SET
	        review_date = ?,
	        status = ?
	    WHERE sample_id = ?
	";

	bUpdated := RunSQL(sSQL,, {dReviewDate, "Reviewed", sSampleID});

	:IF bUpdated;
		sMessage := "Sample " + sSampleID + " reviewed on " + DToC(dReviewDate);
	:ELSE;
		sMessage := "Review update failed for sample " + sSampleID;
	:ENDIF;

	UsrMes(sMessage);

	:RETURN bUpdated;
:ENDPROC;

/* Usage;
DoProc("StampReviewDate");
```

`UsrMes` displays one of:

```text
Sample S-1001 reviewed on <date>
Review update failed for sample S-1001
```

## Related

- [`LimsTime`](LimsTime.md)
- [`Now`](Now.md)
- [`Seconds`](Seconds.md)
- [`Time`](Time.md)
- [`date`](../types/date.md)
