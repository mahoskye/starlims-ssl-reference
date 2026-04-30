---
title: "DToC"
summary: "Converts a date value to a string using the current SSL date format."
id: ssl.function.dtoc
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DToC

Converts a date value to a string using the current SSL date format.

`DToC` takes one date argument and returns its string representation using the current date format setting. If `dDate` is an empty date, the function returns the placeholder string `"  /  /    "`. Passing [`NIL`](../literals/nil.md) or a non-date value raises an exception. Use `DToC` for user-facing output that should follow the current date format setting. Use [`DToS`](DToS.md) or [`DateToString`](DateToString.md) when you need a fixed output format instead of the active setting.

## When to use

- When you need to display a date in screens, messages, or reports using the current date format setting.
- When you need to concatenate a date into user-facing text.
- When you want conversion behavior that stays aligned with [`DateFormat`](DateFormat.md).
- When you need consistent handling of empty date values in display output.

## Syntax

```ssl
DToC(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `dDate` | [date](../types/date.md) | yes | — | Date value to convert to a string |

## Returns

**[string](../types/string.md)** — Formatted date string using the current date format setting. If `dDate` is empty, returns `"  /  /    "`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `dDate argument cannot be null` |
| `dDate` is not a date value. | `dDate must be of date type` |

## Best practices

!!! success "Do"
    - Use `DToC` for user-facing output that should follow the current date format setting.
    - Treat `"  /  /    "` as an empty-date marker before displaying or storing the result.
    - Use [`DToS`](DToS.md) or [`DateToString`](DateToString.md) instead when you need a fixed format.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md), strings, or numbers directly. `DToC` requires a date value.
    - Assume the result always uses a fixed pattern such as `MM/dd/yyyy`.
    - Use `DToC` for integrations that require a stable interchange format.

## Caveats

- The empty-date placeholder `"  /  /    "` is a literal string of spaces and slashes, not an empty string. Calling [`Empty`](Empty.md) on the result returns [`.F.`](../literals/false.md).

## Examples

### Display a date value in a user message

Converts a date value to a string and displays it in a user message.

```ssl
:PROCEDURE ShowLoggedDate;
	:DECLARE dLoggedDate, sLoggedDate;

	dLoggedDate := CToD("03/15/2024");
	sLoggedDate := DToC(dLoggedDate);

	UsrMes("Logged on " + sLoggedDate);
:ENDPROC;

/* Usage;
DoProc("ShowLoggedDate");
```

[`UsrMes`](UsrMes.md) displays:

```text
Logged on 03/15/2024
```

### Replace the empty-date placeholder with a friendly label

Replaces the `"  /  /    "` placeholder returned for empty dates with a user-friendly `[Not specified]` label.

```ssl
:PROCEDURE GetReleaseDateText;
	:PARAMETERS dReleaseDate;

	:DECLARE sReleaseDate;

	sReleaseDate := DToC(dReleaseDate);

	:IF sReleaseDate == "  /  /    ";
		sReleaseDate := "[Not specified]";
	:ENDIF;

	:RETURN sReleaseDate;
:ENDPROC;

/* Usage;
DoProc("GetReleaseDateText", {CToD("03/15/2024")});
```

### Format multiple date fields for report output

Converts received and released date columns for a batch of samples, replacing any empty released date with `[Pending]` before building the summary lines.

```ssl
:PROCEDURE BuildSampleDateSummary;
	:PARAMETERS aSamples;

	:DECLARE aLines, nIndex, sSampleID, sReceivedDate, sReleasedDate, sLine;

	aLines := {};

	:FOR nIndex := 1 :TO ALen(aSamples);
		sSampleID := aSamples[nIndex, 1];
		sReceivedDate := DToC(aSamples[nIndex, 2]);
		sReleasedDate := DToC(aSamples[nIndex, 3]);

		:IF sReleasedDate == "  /  /    ";
			sReleasedDate := "[Pending]";
		:ENDIF;

		sLine := sSampleID + " | Received: " + sReceivedDate
		+ " | Released: " + sReleasedDate;

		AAdd(aLines, sLine);
	:NEXT;

	:RETURN aLines;
:ENDPROC;

/* Usage;
DoProc("BuildSampleDateSummary", {{{"S-001", CToD("03/15/2024"), CToD("03/16/2024")}}});
```

## Related

- [`CToD`](CToD.md)
- [`DateFormat`](DateFormat.md)
- [`DToS`](DToS.md)
- [`DateFromNumbers`](DateFromNumbers.md)
- [`DateFromString`](DateFromString.md)
- [`DateToString`](DateToString.md)
- [`LimsGetDateFormat`](LimsGetDateFormat.md)
- [`StringToDate`](StringToDate.md)
- [`string`](../types/string.md)
- [`date`](../types/date.md)
