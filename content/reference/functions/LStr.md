---
title: "LStr"
summary: "Converts a value to its trimmed string representation, returning \"NIL\" when the input is NIL."
id: ssl.function.lstr
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LStr

Converts a value to its trimmed string representation, returning `"NIL"` when the input is [`NIL`](../literals/nil.md).

`LStr` calls [`LimsString`](LimsString.md) internally and trims the result. When the input is a number, global group and decimal separators are applied. For other input types, the default string conversion is used. Unlike [`LTransform`](LTransform.md) or [`StrZero`](StrZero.md), `LStr` does not pad or shape the output — use those functions when fixed field widths or decimal precision are required.

## When to use

- When displaying or exporting numbers that might be missing, and a non-empty explicit placeholder is required instead of a blank.
- When converting numeric results to strings for downstream systems or templated reports.
- When preparing data with mixed types where all entries must be strings and [`NIL`](../literals/nil.md) values must be made explicit.

## Syntax

```ssl
LStr(vNumber)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vNumber` | any | yes | — | The value to convert to a string |

## Returns

**[string](../types/string.md)** — The trimmed string form of `vNumber`, with locale-specific group and decimal separators applied when `vNumber` is a number. Returns the literal string `"NIL"` when `vNumber` is [`NIL`](../literals/nil.md).

## Best practices

!!! success "Do"
    - Use `LStr` when [`NIL`](../literals/nil.md) values must appear as the explicit placeholder `"NIL"` in UI output, logs, or exports.
    - Pair `LStr` with [`LTransform`](LTransform.md) or [`StrZero`](StrZero.md) when field-width padding or decimal precision is required after conversion.
    - Apply `LStr` when serializing mixed data sources that must never produce empty strings for missing values.

!!! failure "Don't"
    - Assume the output will be empty or [`NIL`](../literals/nil.md); `LStr` always returns a non-empty string.
    - Use `LStr` when strict output formatting or padding is required — use [`LTransform`](LTransform.md) or [`StrZero`](StrZero.md) instead.
    - Use the result directly in numeric operations; the output is always a string and must be reconverted if a number is needed.

## Caveats

- [`NIL`](../literals/nil.md) input returns the four-character string `"NIL"`, not an empty string — add a guard when a blank placeholder is expected instead.
- Leading and trailing whitespace in the converted result is trimmed; strings with intentional leading or trailing spaces will lose them.
- Passing complex types such as objects returns their default string representation, which may not match expectations.

## Examples

### Convert a NIL value to the placeholder string

Passing [`NIL`](../literals/nil.md) directly to `LStr` returns the four-character placeholder `"NIL"`, while a numeric value returns a trimmed decimal string. Both calls demonstrate the two distinct outputs of `LStr`.

```ssl
:PROCEDURE DemonstrateLStr;
	:DECLARE nValue;

	UsrMes("Missing: " + LStr(NIL));

	nValue := 3.14;
	UsrMes("Number:  " + LStr(nValue));
:ENDPROC;

/* Usage;
DoProc("DemonstrateLStr");
```

[`UsrMes`](UsrMes.md) displays:

```text
Missing: NIL
Number:  3.14
```

### Log a batch of measurements with NIL entries labeled explicitly

Loop over an array of measurements and convert each entry with `LStr` so that [`NIL`](../literals/nil.md) entries appear as `"NIL"` in the output rather than causing a concatenation error or producing silent blanks.

```ssl
:PROCEDURE LogMeasurements;
	:DECLARE aMeasurements, nIndex, vValue, sLog;

	aMeasurements := {420.5, NIL, 18.3};
	sLog := "";

	:FOR nIndex := 1 :TO ALen(aMeasurements);
		vValue := aMeasurements[nIndex];
		:IF nIndex > 1;
			sLog := sLog + Chr(10);
		:ENDIF;
		sLog := sLog + "Sample " + LimsString(nIndex) + ": " + LStr(vValue);
	:NEXT;

	UsrMes(sLog);
:ENDPROC;

/* Usage;
DoProc("LogMeasurements");
```

[`UsrMes`](UsrMes.md) displays:

```
Sample 1: 420.5
Sample 2: NIL
Sample 3: 18.3
```

### Build a formatted report using LStr and StrZero together

Use `LStr` to convert numeric results to strings and [`StrZero`](StrZero.md) to zero-pad integer sample IDs. The contrast shows where each function fits: [`StrZero`](StrZero.md) for fixed-width integers, `LStr` for plain numeric conversion.

```ssl
:PROCEDURE GenerateSampleReport;
	:DECLARE aSamples, sReport, nIndex;
	:DECLARE nSampleID, nResult, nSpecMin, nSpecMax, bPass, sStatus;

	aSamples := {
		{1001, 45.7, 40.0, 50.0},
		{1002, 38.2, 40.0, 50.0},
		{1003, 51.2, 40.0, 50.0}
	};

	sReport := "ID      Result  Status" + Chr(10);

	:FOR nIndex := 1 :TO ALen(aSamples);
		nSampleID := aSamples[nIndex, 1];
		nResult := aSamples[nIndex, 2];
		nSpecMin := aSamples[nIndex, 3];
		nSpecMax := aSamples[nIndex, 4];

		bPass := nResult >= nSpecMin .AND. nResult <= nSpecMax;
		:IF bPass;
			sStatus := "PASS";
		:ELSE;
			sStatus := "FAIL";
		:ENDIF;

		sReport := sReport + StrZero(nSampleID, 6) + "  " + LStr(nResult) + "    " + sStatus
			+ Chr(10);
	:NEXT;

	UsrMes(sReport);
:ENDPROC;

/* Usage;
DoProc("GenerateSampleReport");
```

[`UsrMes`](UsrMes.md) displays:

```
ID      Result  Status
001001  45.7    PASS
001002  38.2    FAIL
001003  51.2    FAIL
```

## Related

- [`LTransform`](LTransform.md)
- [`LimsString`](LimsString.md)
- [`Str`](Str.md)
- [`StrZero`](StrZero.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
