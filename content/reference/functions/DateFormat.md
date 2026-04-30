---
title: "DateFormat"
summary: "Sets the current SSL date format string."
id: ssl.function.dateformat
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DateFormat

Sets the current SSL date format string.

`DateFormat` stores the format used by current-format date operations such as [`DToC`](DToC.md) and [`CToD`](CToD.md). Before storing the value, it normalizes token casing by replacing `Y` with `y`, `m` with `M`, and `D` with `d`. [`LimsGetDateFormat`](LimsGetDateFormat.md) returns the stored normalized value. `DateFormat` always returns an empty string.

## When to use

- When you need [`DToC`](DToC.md) output to follow a specific date pattern.
- When you need [`CToD`](CToD.md) to parse text using a different current format.
- When you need to switch formats temporarily, then restore the previous value.

## Syntax

```ssl
DateFormat(sNewFormat)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sNewFormat` | [string](../types/string.md) | yes | — | Date format string to store as the current format. Common token casing is normalized before storage. |

## Returns

**[string](../types/string.md)** — Always returns an empty string.

## Best practices

!!! success "Do"
    - Save the current format with [`LimsGetDateFormat`](LimsGetDateFormat.md) before making a temporary change.
    - Restore the previous format after export, display, or parsing work that needs a different pattern.
    - Verify the effective format with [`LimsGetDateFormat`](LimsGetDateFormat.md) when the exact stored pattern matters.

!!! failure "Don't"
    - Assume `DateFormat` returns the previous format. It always returns an empty string.
    - Rely on it to validate that a format string is usable for later parsing or formatting.
    - Change the current format in shared workflow code without restoring it afterward.

## Caveats

- The stored format may differ from what you passed: `"YYYY-mm-DD"` normalizes to `"yyyy-MM-dd"`.

## Examples

### Set a day-first format and confirm the stored value

Sets a day-first date format and then reads back the stored value with [`LimsGetDateFormat`](LimsGetDateFormat.md) to confirm normalization, followed by today's date formatted in that pattern.

```ssl
:PROCEDURE ShowDayFirstFormat;
	:DECLARE sCurrentFormat, sTodayText;

	DateFormat("DD/MM/YYYY");

	sCurrentFormat := LimsGetDateFormat();
	sTodayText := DToC(Today());

	/* Displays current stored format and today's date in day-first format;
	UsrMes("Current format: " + sCurrentFormat);
	UsrMes("Today: " + sTodayText);
:ENDPROC;

/* Usage;
DoProc("ShowDayFirstFormat");
```

### Temporarily switch to an ISO-style format and restore afterward

Saves the current format, switches to an ISO-style pattern inside a [`:TRY`](../keywords/TRY.md) block, formats today's date, then restores the original format in the [`:FINALLY`](../keywords/FINALLY.md) block.

```ssl
:PROCEDURE BuildExportDate;
	:DECLARE sOriginalFormat, sExportDate;

	sOriginalFormat := LimsGetDateFormat();

	:TRY;
		DateFormat("YYYY-MM-DD");

		sExportDate := DToC(Today());

		/* Displays export date in ISO-style format;
		UsrMes("Export date: " + sExportDate);
	:FINALLY;
		DateFormat(sOriginalFormat);
	:ENDTRY;

	:RETURN sExportDate;
:ENDPROC;

/* Usage;
DoProc("BuildExportDate");
```

### Select a format by output target and verify the stored normalization

Selects a format string based on the target system (EU, ISO, or default), applies it, then reads back the stored normalized value and formats today's date. The ISO case shows how `"YYYY-mm-DD"` normalizes to `"yyyy-MM-dd"`.

```ssl
:PROCEDURE FormatDateForTarget;
	:PARAMETERS sTarget;
	:DECLARE sOriginalFormat, sRequestedFormat, sStoredFormat, sDateText;

	sOriginalFormat := LimsGetDateFormat();

	:BEGINCASE;
	:CASE Upper(sTarget) == "EU";
		sRequestedFormat := "DD/MM/YYYY";
		:EXITCASE;
	:CASE Upper(sTarget) == "ISO";
		sRequestedFormat := "YYYY-mm-DD";
		:EXITCASE;
	:OTHERWISE;
		sRequestedFormat := "MM/DD/YYYY";
		:EXITCASE;
	:ENDCASE;

	:TRY;
		DateFormat(sRequestedFormat);

		sStoredFormat := LimsGetDateFormat();
		sDateText := DToC(Today());

		/* ISO target shows requested, normalized stored, and formatted values;
		UsrMes("Requested format: " + sRequestedFormat);
		UsrMes("Stored format: " + sStoredFormat);
		UsrMes("Formatted date: " + sDateText);
	:FINALLY;
		DateFormat(sOriginalFormat);
	:ENDTRY;

	:RETURN sDateText;
:ENDPROC;

/* Usage;
DoProc("FormatDateForTarget", {"ISO"});
```

## Related

- [`CToD`](CToD.md)
- [`DToC`](DToC.md)
- [`LimsGetDateFormat`](LimsGetDateFormat.md)
- [`StringToDate`](StringToDate.md)
- [`string`](../types/string.md)
- [`date`](../types/date.md)
