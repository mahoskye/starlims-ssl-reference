---
title: "StringToDate"
summary: "Converts a formatted date string into a date value using a specified pattern."
id: ssl.function.stringtodate
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# StringToDate

Converts a formatted date string into a date value using a specified pattern.

`StringToDate()` converts a string to an SSL date using the format you supply.

When the text matches the expected format, the function returns a date value. When parsing fails, it does not raise a format error; it returns an empty date instead. The function only raises when `sDateString` or `sDateFormat` is [`NIL`](../literals/nil.md).

Parsing uses invariant-culture rules rather than the current user locale. That makes `StringToDate()` a good choice when you need stable parsing for imported or application-defined date formats.

## When to use

- When you receive a date from a file, API, or user input and need to convert it to a date type for further processing.
- When validating that a date string matches a required order and separator pattern before storing or using it.
- When integrating with systems that require or produce dates in specific string formats, and you need parsing that does not depend on the current locale.
- When refactoring legacy string-based date manipulations to use proper date types for improved reliability and clarity.

## Syntax

```ssl
StringToDate(sDateString, sDateFormat)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sDateString` | [string](../types/string.md) | yes | — | Date string containing the date representation to parse. |
| `sDateFormat` | [string](../types/string.md) | yes | — | Date format pattern used for parsing the date string. |

## Returns

**[date](../types/date.md)** — Parsed date when conversion succeeds. Returns an empty date when the input does not match the supplied format.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDateString` is [`NIL`](../literals/nil.md). | `Argument: sDateString cannot be null.` |
| `sDateFormat` is [`NIL`](../literals/nil.md). | `Argument: sDateFormat cannot be null.` |

## Best practices

!!! success "Do"
    - Check [`Empty`](Empty.md)`(dParsedDate)` after calling `StringToDate()` so failed parses do not silently flow into later logic.
    - Keep the expected format in one place, such as a local variable or configuration value, when multiple rows use the same pattern.
    - Prefer unambiguous formats such as `yyyy-MM-dd` or `yyyyMMdd` when you control the input format.

!!! failure "Don't"
    - Assume a failed parse will throw. Format mismatches return an empty date, so [`:CATCH`](../keywords/CATCH.md) will not handle ordinary bad input.
    - Pass [`NIL`](../literals/nil.md) for either argument. Those cases raise immediately instead of returning an empty date.
    - Rely on locale-dependent expectations when a stable external format is available. `StringToDate()` uses invariant-culture parsing.

## Caveats

- Parsing uses invariant culture, so month-name formats such as `dd-MMM-yyyy` depend on invariant-culture month text.
- The format is normalized before parsing, so common patterns such as `MM/dd/yyyy` and `dd-MM-yyyy` accept one- or two-digit month/day input.

## Examples

### Validate a user-entered date string

Parse a user-supplied date string against a fixed pattern and use an empty-date check to detect mismatches. The function never raises on a bad format, so the guard must be explicit.

```ssl
:PROCEDURE ValidateSampleDate;
	:DECLARE sUserInput, sFormat, dParsedDate;

	sUserInput := "03/15/2024";
	sFormat := "MM/dd/yyyy";

	dParsedDate := StringToDate(sUserInput, sFormat);

	:IF Empty(dParsedDate);
		UsrMes("Enter the date as MM/DD/YYYY.");
		:RETURN .F.;
	:ENDIF;

	UsrMes("Accepted date: " + DToC(dParsedDate));
	:RETURN .T.;
:ENDPROC;

DoProc("ValidateSampleDate");
```

### Parse and separate valid and invalid rows from an import feed

Loop over rows from a CSV-style import, attempt to parse each date string, and collect accepted and rejected entries into separate arrays. The row with `"20240230"` (February 30) fails because that date does not exist.

```ssl
:PROCEDURE ImportSampleDatesFromCSV;
	:DECLARE aRows, aAccepted, aRejected;
	:DECLARE nIndex, sSampleId, sDateString, dParsedDate;

	aRows := {
		{"SMP-001", "20240315"},
		{"SMP-002", "20240230"},
		{"SMP-003", "20240401"}
	};

	aAccepted := {};
	aRejected := {};

	:FOR nIndex := 1 :TO ALen(aRows);
		sSampleId := aRows[nIndex, 1];
		sDateString := aRows[nIndex, 2];
		dParsedDate := StringToDate(sDateString, "yyyyMMdd");

		:IF Empty(dParsedDate);
			AAdd(aRejected, {sSampleId, sDateString});
		:ELSE;
			AAdd(aAccepted, {sSampleId, dParsedDate});
		:ENDIF;
	:NEXT;

	UsrMes("Accepted rows: " + LimsString(ALen(aAccepted)));
	UsrMes("Rejected rows: " + LimsString(ALen(aRejected)));

	:RETURN aAccepted;
:ENDPROC;

DoProc("ImportSampleDatesFromCSV");
```

### Normalize dates arriving in different formats from multiple sources

Dispatch to the correct format string based on each row's source system, then parse and collect a status alongside each normalized date. The `"legacy"` row with `"15-Mars-2024"` fails because `"Mars"` is not an invariant-culture month abbreviation; the `"custom"` source has no registered format and is marked unsupported without attempting to parse.

```ssl
:PROCEDURE NormalizeIncomingDates;
	:DECLARE aEvents, aNormalized;
	:DECLARE nIndex, sSource, sDateText, sFormat, dEventDate;

	aEvents := {
		{"portal", "2024-03-15"},
		{"instrument", "20240315"},
		{"legacy", "15-Mar-2024"},
		{"legacy", "15-Mars-2024"},
		{"custom", "2024/03/15"}
	};

	aNormalized := {};

	:FOR nIndex := 1 :TO ALen(aEvents);
		sSource := aEvents[nIndex, 1];
		sDateText := aEvents[nIndex, 2];
		sFormat := "";

		:BEGINCASE;
		:CASE sSource == "portal";
			sFormat := "yyyy-MM-dd";
			:EXITCASE;
		:CASE sSource == "instrument";
			sFormat := "yyyyMMdd";
			:EXITCASE;
		:CASE sSource == "legacy";
			sFormat := "dd-MMM-yyyy";
			:EXITCASE;
		:OTHERWISE;
			AAdd(aNormalized, {sSource, sDateText, "UNSUPPORTED SOURCE"});
			:EXITCASE;
		:ENDCASE;

		:IF Empty(sFormat);
			:LOOP;
		:ENDIF;

		dEventDate := StringToDate(sDateText, sFormat);

		:IF Empty(dEventDate);
			AAdd(aNormalized, {sSource, sDateText, "INVALID"});
		:ELSE;
			AAdd(aNormalized, {sSource, DToS(dEventDate), "OK"});
		:ENDIF;
	:NEXT;

	:RETURN aNormalized;
:ENDPROC;

DoProc("NormalizeIncomingDates");
```

## Related

- [`CToD`](CToD.md)
- [`DToC`](DToC.md)
- [`DToS`](DToS.md)
- [`DateFromNumbers`](DateFromNumbers.md)
- [`DateFromString`](DateFromString.md)
- [`DateToString`](DateToString.md)
- [`date`](../types/date.md)
- [`string`](../types/string.md)
