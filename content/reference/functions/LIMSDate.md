---
title: "LIMSDate"
summary: "Returns a date value as a formatted string."
id: ssl.function.limsdate
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LIMSDate

Returns a date value as a formatted string.

`LIMSDate` accepts either an SSL date value or a string. When you pass a string, the function parses it using the current application date format, the same behavior used by [`CToD`](CToD.md). If you omit the format or pass an empty format, the function returns the date in `dd-MMM-yy` format.

Null-date inputs are handled specially. With no format, the function returns `0--`. With a supplied format that contains `MMM`, it returns `0--0`. With other supplied formats, it returns a blank placeholder shaped like the format string. Non-date, non-string inputs raise an error.

## When to use

- When you need a formatted date string for display, export, or reporting.
- When your input may already be an SSL date or may arrive as a date string.
- When you need the function's built-in null-date placeholder behavior.
- When you want string inputs parsed using the current STARLIMS date format.

## Syntax

```ssl
LIMSDate(vDate, [sFormat])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vDate` | [date](../types/date.md) or [string](../types/string.md) | yes | — | Date value to format. String inputs are parsed using the current application date format. |
| `sFormat` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Output format. If omitted or empty, `LIMSDate` uses `dd-MMM-yy`. If the supplied format contains `MMM`, the function uses `dd-MMM-yyyy`. |

## Returns

**[string](../types/string.md)** — The formatted date string, or a null-date placeholder such as `0--`, `0--0`, or a blank pattern-shaped string.

If `vDate` is a string that cannot be parsed, `LIMSDate` treats it as a null date and returns the same placeholder output it would use for an empty date.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `vDate` is [`NIL`](../literals/nil.md). | `Argument vDate cannot be null.` |
| `vDate` is neither a string nor a date. | `Argument vDate must be a date or string value.` |

## Best practices

!!! success "Do"
    - Pass an SSL date when you already have one and only use string input when parsing is intentional.
    - Specify the output format explicitly when downstream code depends on a fixed date shape.
    - Handle null-date placeholder output when your source data may contain empty or invalid dates.

!!! failure "Don't"
    - Pass arrays, objects, or other non-date values. Those inputs raise an error.
    - Assume an omitted format uses the current global date format. `LIMSDate` defaults to `dd-MMM-yy` instead.
    - Assume a format containing `MMM` preserves your exact token pattern. `LIMSDate` normalizes those cases to `dd-MMM-yyyy`.

## Caveats

- String input is parsed with the current application date format, not an explicitly supplied parse format.

## Examples

### Format a date string using an explicit pattern

Call `LIMSDate` with a date string and an explicit format to see both the input and the formatted result. The input `"03/15/2024"` formats to `"2024-03-15"` under the `"yyyy-MM-dd"` pattern.

```ssl
:PROCEDURE FormatUserDate;
	:DECLARE sUserInput, sFormattedDisplay;

	sUserInput := "03/15/2024";
	sFormattedDisplay := LIMSDate(sUserInput, "yyyy-MM-dd");

	UsrMes("Entered: " + sUserInput + " | Displayed: " + sFormattedDisplay);

	:RETURN sFormattedDisplay;
:ENDPROC;

/* Usage;
DoProc("FormatUserDate");
```

[`UsrMes`](UsrMes.md) displays:

```
Entered: 03/15/2024 | Displayed: 2024-03-15
```

### Handle blank and invalid date strings without exceptions

Process a batch of legacy date strings where some entries are blank or unparseable. `LIMSDate` treats both as null dates and returns a blank placeholder shaped like the format. Neither raises an exception.

```ssl
:PROCEDURE FormatLegacyDates;
	:DECLARE aLegacyRecords, nIndex, sSampleId, sSourceDate;
	:DECLARE sFormattedDate, sReportLine;

	aLegacyRecords := {
		{"SAM001", "03/15/1998"},
		{"SAM002", ""},
		{"SAM003", "not-a-date"},
		{"SAM004", "12/31/2001"},
		{"SAM005", "07/04/1999"}
	};

	:FOR nIndex := 1 :TO ALen(aLegacyRecords);
		sSampleId := aLegacyRecords[nIndex, 1];
		sSourceDate := aLegacyRecords[nIndex, 2];
		sFormattedDate := LIMSDate(sSourceDate, "yyyy/MM/dd");

		sReportLine := "Sample: " + sSampleId + " | Imported: " + sFormattedDate;
		UsrMes(sReportLine);
	:NEXT;

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("FormatLegacyDates");
```

`UsrMes` displays one line per record, for example:

```text
Sample: SAM001 | Imported: 1998/03/15
Sample: SAM002 | Imported:
Sample: SAM003 | Imported:
Sample: SAM004 | Imported: 2001/12/31
Sample: SAM005 | Imported: 1999/07/04
```

### Apply MMM format normalization across multiple dates

Show that a format containing `MMM` is normalized to `dd-MMM-yyyy` regardless of what was passed. The supplied format `"dd-MMM-yy"` is replaced, so all three dates render with a four-digit year.

```ssl
:PROCEDURE FormatReportDates;
	:DECLARE dReportDate, dSampleDate, dDueDate;
	:DECLARE sDisplayFormat, sReportDate, sSampleDate, sDueDate;
	:DECLARE aReportRows, nIndex;

	dReportDate := CToD("04/11/2026");
	dSampleDate := CToD("04/08/2026");
	dDueDate := CToD("04/15/2026");
	sDisplayFormat := "dd-MMM-yy";

	sReportDate := LIMSDate(dReportDate, sDisplayFormat);
	sSampleDate := LIMSDate(dSampleDate, sDisplayFormat);
	sDueDate := LIMSDate(dDueDate, sDisplayFormat);

	aReportRows := {
		"Report Generated: " + sReportDate,
		"Earliest Sample: " + sSampleDate,
		"Due Date: " + sDueDate
	};

	:FOR nIndex := 1 :TO ALen(aReportRows);
		UsrMes(aReportRows[nIndex]);
	:NEXT;

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("FormatReportDates");
```

`UsrMes` displays:

```text
Report Generated: 11-Apr-2026
Earliest Sample: 08-Apr-2026
Due Date: 15-Apr-2026
```

## Related

- [`CToD`](CToD.md)
- [`DateFormat`](DateFormat.md)
- [`LimsGetDateFormat`](LimsGetDateFormat.md)
- [`string`](../types/string.md)
- [`date`](../types/date.md)
