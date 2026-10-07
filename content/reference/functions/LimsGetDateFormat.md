---
title: "LimsGetDateFormat"
summary: "Returns the current session date format string used for date parsing and formatting."
id: ssl.function.limsgetdateformat
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# LimsGetDateFormat

Returns the current session date format string used for date parsing and formatting.

`LimsGetDateFormat()` retrieves the current date format string, such as `"M/d/yyyy"` or `"yyyy-MM-dd"`. It takes no parameters and is safe to call any time. If no format has been set with [`DateFormat`](DateFormat.md), it returns the default session format, `"M/d/yyyy"`.

## When to use

- When you need to dynamically retrieve the system's current date format for parsing or formatting operations.
- When generating or interpreting date strings that must conform to the global StarLIMS date convention.
- When integrating with external systems or databases that require awareness of the application's date format.
- When creating user interfaces that adapt to the configured date display convention.

## Syntax

```ssl
LimsGetDateFormat()
```

## Parameters

This function takes no parameters.

## Returns

**[string](../types/string.md)** — The date format pattern currently in effect for this session (e.g., `"M/d/yyyy"`).

## Best practices

!!! success "Do"
    - Call `LimsGetDateFormat()` at runtime before parsing or formatting dates rather than hard-coding a format string.
    - Use the returned format string when parsing user input or data files.
    - Document the expected date format for integration partners and when writing export/import routines.

!!! failure "Don't"
    - Hard-code the session's display format when you mean "whatever format the user works in"; use an explicit format only when an export or interface needs a fixed shape.
    - Assume a specific date order or delimiter based on regional habits.
    - Ignore the global configuration when presenting or persisting date strings.

## Caveats

- The function returns the format string but does not validate it; a misconfigured format string may cause downstream parsing errors.

## Examples

### Display the expected date format to the user

Call `LimsGetDateFormat` to retrieve the configured format and display it as part of a user prompt. With the default session format, the result is `"M/d/yyyy"`.

```ssl
:PROCEDURE ShowDateFormatPrompt;
	:DECLARE sDateFormat;

	sDateFormat := LimsGetDateFormat();
	UsrMes("Enter date using format: " + sDateFormat);
:ENDPROC;

/* Usage;
DoProc("ShowDateFormatPrompt");
```

[`UsrMes`](UsrMes.md) logs:

```text
Enter date using format: M/d/yyyy
```

### Parse imported date strings using the current global format

Validate and parse a batch of imported date strings against the live global format. Valid dates are converted with [`StringToDate`](StringToDate.md); rows with unparseable dates log an error and store a null date. All three input dates are valid, so [`InfoMes`](InfoMes.md) fires for each row.

```ssl
:PROCEDURE ParseImportedSampleDates;
	:DECLARE sDateFormat, aRawData, aParsedDates, sDateCol;
	:DECLARE nIndex, dParsed, bValid, sLogMsg;

	sDateFormat := LimsGetDateFormat();

	aRawData := {
		{"SMP-001", "Lead", "03/15/2026", "PENDING"},
		{"SMP-002", "Mercury", "03/16/2026", "COMPLETE"},
		{"SMP-003", "Arsenic", "03/17/2026", "PENDING"}
	};

	aParsedDates := {};

	:FOR nIndex := 1 :TO ALen(aRawData);
		sDateCol := aRawData[nIndex, 3];

		bValid := ValidateDate(sDateCol);
		:IF bValid;
			dParsed := StringToDate(sDateCol, sDateFormat);
			AAdd(aParsedDates, dParsed);
			sLogMsg := "Row " + LimsString(nIndex) + ": " + sDateCol + " parsed as " + DToC(
				dParsed);
			InfoMes(sLogMsg);  /* Logs: parsed row details;
		:ELSE;
			AAdd(aParsedDates, CToD(""));
			sLogMsg := "Row " + LimsString(nIndex) + ": Invalid date '" + sDateCol + "' for format "
				+ sDateFormat;
			ErrorMes(sLogMsg);  /* Logs on failure: invalid date;
		:ENDIF;
	:NEXT;

	:RETURN aParsedDates;
:ENDPROC;

/* Usage;
DoProc("ParseImportedSampleDates");
```

## Related

- [`DateFormat`](DateFormat.md)
- [`LIMSDate`](LIMSDate.md)
- [`StringToDate`](StringToDate.md)
- [`ValidateDate`](ValidateDate.md)
- [`string`](../types/string.md)
