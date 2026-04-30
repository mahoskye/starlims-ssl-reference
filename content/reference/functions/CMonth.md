---
title: "CMonth"
summary: "Returns the full month name for a date value."
id: ssl.function.cmonth
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CMonth

Returns the full month name for a date value.

`CMonth` returns the full month name for a valid date, such as `March`. If the input is an empty date, it returns `""`. Passing [`NIL`](../literals/nil.md) or a non-date value raises an error.

## When to use

- When you need a readable month label for messages, reports, or screen output.
- When you want the month as text instead of the numeric value returned by [`Month`](Month.md).
- When building summaries where a full month name is clearer than `1` through
  `12`.

## Syntax

```ssl
CMonth(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | Date value to convert to a full month name. |

## Returns

**[string](../types/string.md)** — The full month name for `dDate`. Returns `""` when `dDate` is an empty date.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `Argument: dDate cannot be null.` |
| `dDate` is not a date value. | `Argument: dDate must be of date type.` |

## Best practices

!!! success "Do"
    - Check whether a date can be empty before displaying the result.
    - Use `CMonth` for user-facing labels and [`Month`](Month.md) for numeric comparisons or sorting.
    - Pair the month name with [`Year`](Year.md) when summarizing data that can span more than one year.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) or a non-date value. `CMonth` raises an error instead of converting it.
    - Group only by month name when records can come from multiple years. `January 2024` and `January 2025` are different buckets.
    - Assume an empty date returns a fallback month name. It returns an empty string.

## Caveats

- Empty dates return `""`, so blank output may mean the source date was empty.
- If you need numeric comparisons, sorting, or grouping keys, use [`Month`](Month.md) instead.

## Examples

### Display a month name for a date value

Converts a specific date to a month name and displays it in a message. March 15, 2024 produces `"March"`.

```ssl
:PROCEDURE ShowReceiveMonth;
	:DECLARE dReceiveDate, sMonthName;

	dReceiveDate := CToD("03/15/2024");
	sMonthName := CMonth(dReceiveDate);

	UsrMes("Sample received in " + sMonthName);

	:RETURN sMonthName;
:ENDPROC;

/* Usage;
DoProc("ShowReceiveMonth");
```

[`UsrMes`](UsrMes.md) displays:

```text
Sample received in March
```

### Skip empty dates when building a list of month labels

Builds an array of month names from a mixed list that includes an empty date, skipping any entries where the date is empty so blank month labels are not added to the result.

```ssl
:PROCEDURE BuildMonthLabels;
	:DECLARE aDates, aMonthLabels, nIndex, dReviewDate, sMonthName;

	aDates := {CToD("01/10/2024"), CToD("03/22/2024"), CToD("")};
	aMonthLabels := {};

	:FOR nIndex := 1 :TO ALen(aDates);
		dReviewDate := aDates[nIndex];

		:IF Empty(dReviewDate);
			:LOOP;
		:ENDIF;

		sMonthName := CMonth(dReviewDate);
		AAdd(aMonthLabels, sMonthName);
	:NEXT;

	:RETURN aMonthLabels;
:ENDPROC;

/* Usage;
DoProc("BuildMonthLabels");
```

### Group records into month-and-year buckets

Groups dates from multiple calendar years into labeled buckets by combining the month name from `CMonth` with the year from [`Year`](Year.md), so January 2024 and January 2025 become distinct buckets.

```ssl
:PROCEDURE BuildMonthlySummary;
	:DECLARE aDates, aSummary, nIndex, dLogDate, sBucket;
	:DECLARE sMonthName, nMonth, nYear, nPos;

	aDates := {
		CToD("01/15/2024"),
		CToD("01/20/2024"),
		CToD("01/05/2025"),
		CToD("02/01/2025")
	};
	aSummary := {};

	:FOR nIndex := 1 :TO ALen(aDates);
		dLogDate := aDates[nIndex];

		:IF Empty(dLogDate);
			:LOOP;
		:ENDIF;

		sMonthName := CMonth(dLogDate);
		nMonth := Month(dLogDate);
		nYear := Year(dLogDate);
		sBucket := sMonthName + " " + LimsString(nYear);
		nPos := AScan(aSummary, {|aRow| aRow[1] == sBucket});

		:IF nPos == 0;
			AAdd(aSummary, {sBucket, nMonth, nYear, 1});
		:ELSE;
			aSummary[nPos, 4] += 1;
		:ENDIF;
	:NEXT;

	:RETURN aSummary;
:ENDPROC;

/* Usage;
DoProc("BuildMonthlySummary");
```

## Related

- [`Month`](Month.md)
- [`Day`](Day.md)
- [`Year`](Year.md)
- [`DToC`](DToC.md)
- [`date`](../types/date.md)
- [`string`](../types/string.md)
