---
title: "DateToString"
summary: "Converts a date value to a string using a specified or default format."
id: ssl.function.datetostring
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DateToString

Converts a date value to a string using a specified or default format.

`DateToString` requires a date value and accepts an optional format string. If `sFormat` is omitted, the function uses `"MM/dd/yyyy HH:mm:ss"`. If `dDate` is missing or not a date value, the function raises an exception. If `sFormat` is provided, it must be a string.

Use `DateToString` when you need a fixed output pattern. Use [`DToC`](DToC.md) when output should follow the current configured date format, and [`DToS`](DToS.md) when you need the compact `yyyyMMdd` form.

## When to use

- When exported text must use a fixed date pattern.
- When building file names, keys, or messages that include formatted dates.
- When different outputs need different date patterns in the same script.
- When [`DToC`](DToC.md) is too dependent on the current date format setting.

## Syntax

```ssl
DateToString(dDate, [sFormat])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `dDate` | [date](../types/date.md) | yes | — | Date value to format. |
| `sFormat` | [string](../types/string.md) | no | `"MM/dd/yyyy HH:mm:ss"` | Output format to apply. If omitted, the default pattern is used. |

## Returns

**[string](../types/string.md)** — The formatted string representation of `dDate`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `Argument: date cannot be null.` |
| `dDate` is not a date value. | `Argument: date must be of date type` |
| `sFormat` is not a string. | `Argument type must be of type SSLString.` |

## Best practices

!!! success "Do"
    - Use `DateToString` when you need a stable, explicit output pattern.
    - Omit `sFormat` when the built-in default `MM/dd/yyyy HH:mm:ss` already matches the requirement.
    - Keep interchange formats explicit, such as `yyyy-MM-dd` or `yyyyMMdd_HHmmss`, instead of relying on environment settings.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md), strings, or numbers as `dDate`. The function requires a date value.
    - Pass a non-string value as `sFormat`. Only a string or omitted value is accepted.
    - Use `DateToString` where later logic still needs a date value for comparison or arithmetic.

## Caveats

- The format string uses .NET-style tokens (`yyyy`, `MM`, `dd`, `HH`, `mm`, `ss`), not the SSL date format tokens used by [`DToC`](DToC.md) and [`CToD`](CToD.md).

## Examples

### Format a timestamp using the default pattern

Formats the current timestamp using the default `MM/dd/yyyy HH:mm:ss` pattern and displays the result. The output varies with the current time.

```ssl
:PROCEDURE ShowRunTimestamp;
	:DECLARE dRunAt, sRunAt;

	dRunAt := Now();

	sRunAt := DateToString(dRunAt);

	UsrMes("Run completed at " + sRunAt);
:ENDPROC;

/* Usage;
DoProc("ShowRunTimestamp");
```

[`UsrMes`](UsrMes.md) displays (output depends on the current time):

```text
Run completed at 04/23/2026 14:30:00
```

### Format a date with a fixed interchange pattern

Formats a received date using an ISO-style `yyyy-MM-dd` pattern and combines it with a sample ID to build a CSV row for export.

```ssl
:PROCEDURE BuildExportRow;
	:PARAMETERS sSampleID, dReceivedDate;
	:DECLARE sExportDate, sRow;

	sExportDate := DateToString(dReceivedDate, "yyyy-MM-dd");
	sRow := sSampleID + "," + sExportDate;

	:RETURN sRow;
:ENDPROC;

/* Usage;
DoProc("BuildExportRow", {"LAB-001", CToD("04/23/2026")});
```

### Build versioned file names using multiple date patterns

Calls `DateToString` twice with different format patterns, once for the folder date component and once for the timestamp-based filename suffix, to construct a versioned archive path.

```ssl
:PROCEDURE BuildArchivePath;
	:PARAMETERS sBaseName;
	:DECLARE dCreatedAt, sFolderDate, sStamp, sFileName, sPath;

	dCreatedAt := Now();

	sFolderDate := DateToString(dCreatedAt, "yyyyMMdd");
	sStamp := DateToString(dCreatedAt, "yyyyMMdd_HHmmss");

	sFileName := sBaseName + "_" + sStamp + ".txt";
	sPath := "archive/" + sFolderDate + "/" + sFileName;

	:RETURN sPath;
:ENDPROC;

/* Usage;
DoProc("BuildArchivePath", {"LabReport"});
```

## Related

- [`CToD`](CToD.md)
- [`DToC`](DToC.md)
- [`DToS`](DToS.md)
- [`DateFromNumbers`](DateFromNumbers.md)
- [`DateFromString`](DateFromString.md)
- [`StringToDate`](StringToDate.md)
- [`date`](../types/date.md)
- [`string`](../types/string.md)
