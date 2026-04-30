---
title: "Year"
summary: "Extracts the numeric year from a date value."
id: ssl.function.year
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Year

Extracts the numeric year from a [`date`](../types/date.md) value.

`Year()` returns the year component of a [`date`](../types/date.md) as a [`number`](../types/number.md). For a valid date, the result is the calendar year such as `2026`. If the input is an empty date, the function returns `0`. Passing [`NIL`](../literals/nil.md) or a value that is not a date raises an error.

## When to use

- When you need to group dates by year for reporting, charting, or summaries.
- When validating that a date falls within a certain year range, such as for age checks or fiscal reports.
- When extracting the year to compare with user input or other numeric values.

## Syntax

```ssl
Year(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | The date value from which to extract the year number. |

## Returns

**[number](../types/number.md)** — The calendar year for a valid date, or `0` when `dDate` is an empty date.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `Argument: dDate cannot be null.` |
| `dDate` is not a date value. | `Argument: dDate must be of date type.` |

## Best practices

!!! success "Do"
    - Use `Year()` when you need the numeric year for grouping, comparison, or reporting.
    - Treat a return value of `0` as an empty date case.
    - Pair `Year()` with [`Month`](Month.md) or [`Day`](Day.md) when you need full calendar context.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) or non-date values. `Year()` raises an error instead of converting them.
    - Treat `0` as a real year from your data. It only indicates an empty date.
    - Use the result as though it were still a date value. `Year()` returns a number, not a date.

## Examples

### Check a birth year against a minimum age requirement

Compute the age as a year difference and check whether it meets a minimum. The output below uses `CToD("01/01/2000")` and `18` as sample inputs.

```ssl
:PROCEDURE ValidateMinimumAge;
	:PARAMETERS dBirthDate, nMinAge;
	:DECLARE nBirthYear, nCurrentYear, nAge, bIsEligible;

	nCurrentYear := Year(Today());
	nBirthYear := Year(dBirthDate);
	nAge := nCurrentYear - nBirthYear;

	:IF nAge >= nMinAge;
		bIsEligible := .T.;
		UsrMes(
			"User is eligible. Age "
			+ LimsString(nAge)
			+ " meets minimum requirement of "
			+ LimsString(nMinAge)
			+ "."
		); /* Displays when eligible: eligibility message;
	:ELSE;
		bIsEligible := .F.;
		UsrMes(
			"User is not eligible. Age "
			+ LimsString(nAge)
			+ " does not meet minimum requirement of "
			+ LimsString(nMinAge)
			+ "."
		); /* Displays when ineligible: eligibility message;
	:ENDIF;

	:RETURN bIsEligible;
:ENDPROC;

/* Usage;
DoProc("ValidateMinimumAge", {CToD("01/01/2000"), 18});
```

### Count events grouped by calendar year

Extract the year from each date and accumulate counts per year in a [`SSLStringDictionary`](../classes/SSLStringDictionary.md). The sample data contains 3 events in 2023, 3 in 2024, and 2 in 2025.

```ssl
:PROCEDURE CountEventsByYear;
	:DECLARE aEventDates, oYearCounts, nIndex, dEventDate, nYear, sReport;
	:DECLARE nEvents2023, nEvents2024, nEvents2025;

	aEventDates := {
		CToD("03/15/2023"),
		CToD("07/22/2023"),
		CToD("11/05/2023"),
		CToD("02/28/2024"),
		CToD("09/10/2024"),
		CToD("12/01/2024"),
		CToD("04/17/2025"),
		CToD("08/30/2025")
	};

	oYearCounts := SSLStringDictionary{};

	:FOR nIndex := 1 :TO ALen(aEventDates);
		dEventDate := aEventDates[nIndex];
		nYear := Year(dEventDate);

		/* Initialize the year key on first occurrence;
		:IF oYearCounts:Contains(LimsString(nYear));
			oYearCounts:AddValue(
				LimsString(nYear),
				oYearCounts:GetValue(LimsString(nYear), 0) + 1
			);
		:ELSE;
			oYearCounts:AddValue(LimsString(nYear), 1);
		:ENDIF;
	:NEXT;

	nEvents2023 := oYearCounts:GetValue("2023", 0);
	nEvents2024 := oYearCounts:GetValue("2024", 0);
	nEvents2025 := oYearCounts:GetValue("2025", 0);

	sReport := "Event Summary by Year:" + Chr(13) + Chr(10);
	sReport := sReport + "2023: " + LimsString(nEvents2023)
		+ " events" + Chr(13) + Chr(10);
	sReport := sReport + "2024: " + LimsString(nEvents2024)
		+ " events" + Chr(13) + Chr(10);
	sReport := sReport + "2025: " + LimsString(nEvents2025) + " events";

	UsrMes(sReport);
:ENDPROC;

/* Usage;
DoProc("CountEventsByYear");
```

[`UsrMes`](UsrMes.md) displays:

```text
Event Summary by Year:
2023: 3 events
2024: 3 events
2025: 2 events
```

### Filter records matching a specific year and month

Combine `Year()` and [`Month`](Month.md) to select only rows that match both the target year and month. With the defaults (`2024`, `3`), two rows from March 2024 are returned.

```ssl
:PROCEDURE FilterRecordsByYearMonth;
	:PARAMETERS nTargetYear, nTargetMonth;
	:DEFAULT nTargetYear, 2024;
	:DEFAULT nTargetMonth, 3;
	:DECLARE aRecords, aFiltered, nIndex, dRecordDate, nRecordYear, nRecordMonth;

	/* Sample rows: [1] id, [2] date, [3] status;
	aRecords := {
		{"RUN-001", CToD("01/15/2024"), "Active"},
		{"RUN-002", CToD("03/10/2024"), "Active"},
		{"RUN-003", CToD("03/25/2024"), "Pending"},
		{"RUN-004", CToD("04/05/2024"), "Active"},
		{"RUN-005", CToD("03/28/2023"), "Closed"}
	};

	aFiltered := {};

	:FOR nIndex := 1 :TO ALen(aRecords);
		dRecordDate := aRecords[nIndex, 2];
		nRecordYear := Year(dRecordDate);
		nRecordMonth := Month(dRecordDate);

		/* Match both year and month;
		:IF nRecordYear == nTargetYear .AND. nRecordMonth == nTargetMonth;
			AAdd(aFiltered, aRecords[nIndex]);
		:ENDIF;
	:NEXT;

	UsrMes(
		"Found "
		+ LimsString(ALen(aFiltered))
		+ " record(s) for "
		+ LimsString(nTargetMonth)
		+ "/"
		+ LimsString(nTargetYear)
	);

	:RETURN aFiltered;
:ENDPROC;

/* Usage;
DoProc("FilterRecordsByYearMonth");
```

[`UsrMes`](UsrMes.md) displays:

```text
Found 2 record(s) for 3/2024
```

## Related

- [`DOW`](DOW.md)
- [`DOY`](DOY.md)
- [`Day`](Day.md)
- [`JDay`](JDay.md)
- [`Month`](Month.md)
- [`NoOfDays`](NoOfDays.md)
- [`date`](../types/date.md)
- [`number`](../types/number.md)
