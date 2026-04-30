---
title: "CToD"
summary: "Converts a string in the current SSL date format to a date value."
id: ssl.function.ctod
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CToD

Converts a string in the current SSL date format to a date value.

`CToD` parses `sDateString` using the current SSL date format setting. When the text can be parsed with that setting, the function returns the corresponding date value. When parsing fails, it returns an empty date instead of raising a parse error. Passing [`NIL`](../literals/nil.md) is the documented exception case.

## When to use

- When you need to parse text that follows the current SSL date format setting.
- When you want to validate date text by calling `CToD` and checking whether the result is empty.
- When you are round-tripping values produced by [`DToC`](DToC.md).

## Syntax

```ssl
CToD(sDateString)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sDateString` | [string](../types/string.md) | yes | — | Text to parse using the current configured date format. |

## Returns

**[date](../types/date.md)** — The parsed date value, or an empty date when `sDateString` cannot be parsed with the current date format setting.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDateString` is [`NIL`](../literals/nil.md). | `Argument: date cannot be null.` |

## Best practices

!!! success "Do"
    - Check `Empty(vDate)` after calling `CToD` when the input might be invalid.
    - Validate or default missing input before calling the function.
    - Use `CToD` for values that should follow the same date format used by [`DToC`](DToC.md).

!!! failure "Don't"
    - Assume every non-empty string will parse successfully. Invalid text returns an empty date.
    - Use `CToD` when you need to supply an explicit format. Use [`DateFromString`](DateFromString.md) or [`StringToDate`](StringToDate.md) for that.
    - Rely on `CToD` to distinguish among different date formats. It uses only the current configured date format.

## Caveats

- `CToD` uses the current date format setting, so the same text can parse differently after [`DateFormat`](DateFormat.md) changes that setting.

## Examples

### Parse a date string and check whether it succeeded

Parses a date string using the current date format and checks whether the result is valid or empty, displaying the formatted date on success.

```ssl
:PROCEDURE ParseSingleDate;
	:DECLARE sDateText, dParsedDate, sMessage;

	sDateText := "03/15/2024";
	dParsedDate := CToD(sDateText);

	:IF Empty(dParsedDate);
		sMessage := "The date text is invalid";
	:ELSE;
		sMessage := "Parsed date: " + DToC(dParsedDate);
	:ENDIF;

	UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("ParseSingleDate");
```

[`UsrMes`](UsrMes.md) displays (assuming MM/DD/YYYY date format):

```text
Parsed date: 03/15/2024
```

### Validate a batch of imported date strings

Parses a batch of date strings, accumulates the valid ones in an array, and displays a count of valid and invalid entries.

```ssl
:PROCEDURE ValidateImportedDates;
	:DECLARE aDateText, aValidDates, dParsedDate, sDateText, sSummary;
	:DECLARE nValidCount, nInvalidCount, nIndex;

	aDateText := {"03/15/2024", "03/18/2024", "not-a-date", "04/01/2024"};
	aValidDates := {};
	nValidCount := 0;
	nInvalidCount := 0;

	:FOR nIndex := 1 :TO ALen(aDateText);
		sDateText := aDateText[nIndex];
		dParsedDate := CToD(sDateText);

		:IF Empty(dParsedDate);
			nInvalidCount += 1;
		:ELSE;
			AAdd(aValidDates, dParsedDate);
			nValidCount += 1;
		:ENDIF;
	:NEXT;

	sSummary := "Valid: " + LimsString(nValidCount)
				+ ", Invalid: " + LimsString(nInvalidCount);

	UsrMes(sSummary);
:ENDPROC;

/* Usage;
DoProc("ValidateImportedDates");
```

[`UsrMes`](UsrMes.md) displays:

```text
Valid: 3, Invalid: 1
```

### Distinguish missing input from an invalid date string

Resolves a cutoff date from a text parameter, returning early with separate messages for empty input and unparseable text, and displaying the formatted date when the input is valid.

```ssl
:PROCEDURE ResolveCutoffDate;
	:PARAMETERS sCutoffText;
	:DEFAULT sCutoffText, "";
	:DECLARE dCutoffDate, sStatus;

	:IF Empty(sCutoffText);
		UsrMes("No cutoff date was provided");
		:RETURN .F.;
	:ENDIF;

	dCutoffDate := CToD(sCutoffText);

	:IF Empty(dCutoffDate);
		UsrMes("Cutoff date must match the current date format");
		:RETURN .F.;
	:ENDIF;

	sStatus := "Using cutoff date: " + DToC(dCutoffDate);

	UsrMes(sStatus);
	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ResolveCutoffDate", {"03/15/2024"});
```

`UsrMes` displays on success:

```text
Using cutoff date: 03/15/2024
```

## Related

- [`DToC`](DToC.md)
- [`DToS`](DToS.md)
- [`DateFormat`](DateFormat.md)
- [`DateFromNumbers`](DateFromNumbers.md)
- [`DateFromString`](DateFromString.md)
- [`DateToString`](DateToString.md)
- [`LimsGetDateFormat`](LimsGetDateFormat.md)
- [`StringToDate`](StringToDate.md)
- [`date`](../types/date.md)
- [`string`](../types/string.md)
