---
title: "StdRound"
summary: "Returns a string produced by applying a named rounding standard to a numeric value."
id: ssl.function.stdround
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# StdRound

Returns a string produced by applying a named rounding standard to a numeric value.

`StdRound(sStandard, nDigits, nNumber)` requires all three arguments and returns text, not a numeric value. The function has explicit handling only for `FDA`, `EPA`, and `ISO`, then replaces `.` with the current system decimal separator before returning. Negative inputs keep a leading minus sign in the final string, and `ISO` results are left-padded with spaces to a total width of 15 characters when needed.

The meaning of `nDigits` depends on the selected standard. The FDA and ISO branches use it as a decimal-digit count in the returned string. The EPA branch uses it in its own rounding path and preserves that many significant digits in the formatted result.

## When to use

- When a workflow already depends on the named `FDA`, `EPA`, or `ISO` rounding behavior.
- When you need a formatted string result instead of a numeric result.
- When fixed-width or locale-sensitive output matters, especially for `ISO` output or custom decimal separators.

## Syntax

```ssl
StdRound(sStandard, nDigits, nNumber)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sStandard` | [string](../types/string.md) | yes | — | Rounding standard name. Supported names are `FDA`, `EPA`, and `ISO`. |
| `nDigits` | [number](../types/number.md) | yes | — | Whole-number digit count passed to the selected rounding routine. FDA and ISO use it as decimal digits; EPA uses it in its own significant-digit-style rounding path. |
| `nNumber` | [number](../types/number.md) | yes | — | Numeric value to round and format. |

## Returns

**[string](../types/string.md)** — The formatted string returned by the selected rounding routine.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sStandard` is [`NIL`](../literals/nil.md). | `Argument sStandard cannot be null.` |
| `nDigits` is [`NIL`](../literals/nil.md). | `Argument nDigits cannot be null.` |
| `nNumber` is [`NIL`](../literals/nil.md). | `Argument nNumber cannot be null.` |

## Best practices

!!! success "Do"
    - Pass one of the supported standard names: `FDA`, `EPA`, or `ISO`.
    - Pass `nDigits` as a whole-number value.
    - Treat the result as a string, especially before concatenating, exporting, or storing it.
    - Trim `ISO` output when you need a display value without the fixed-width left padding.
    - Use [`Round`](Round.md) instead when you need an ordinary numeric rounding result.

!!! failure "Don't"
    - Assume `StdRound` returns a number. It returns formatted text.
    - Pass [`NIL`](../literals/nil.md) for any argument. The function raises an error instead
      of supplying defaults.
    - Rely on undocumented standard names or alternate casing. The function only branches on exact `FDA`, `EPA`, and `ISO` values.
    - Assume `nDigits` means the same thing for every standard. The EPA path does not behave like a simple decimal-place formatter.

## Caveats

- For `ISO`, the returned string is truncated to 15 characters when it becomes longer than that.
- `nDigits` is parsed as an integer by the implementation, so fractional values are not a supported input shape.
- Unsupported `sStandard` values are not rejected. They skip the named rounding branches and still return a formatted string.

## Examples

### Format one reported value with the FDA standard

Round one value for display and treat the result as text.

```ssl
:PROCEDURE FormatReportedValue;
	:DECLARE sStandard, sRounded;
	:DECLARE nDigits, nValue;

	sStandard := "FDA";
	nDigits := 2;
	nValue := 12.3456;

	sRounded := StdRound(sStandard, nDigits, nValue);

	UsrMes("Reported value: " + sRounded);

	:RETURN sRounded;
:ENDPROC;

/* Usage;
DoProc("FormatReportedValue");
```

[`UsrMes`](UsrMes.md) displays:

```text
Reported value: <rounded value>
```

### Compare FDA, EPA, and ISO results

Run the same input through each supported standard so a review script can show the different formatted outputs.

```ssl
:PROCEDURE ReviewStandardOutputs;
	:DECLARE aRequests, aRow;
	:DECLARE sStandard, sRounded, sLine;
	:DECLARE nDigits, nValue, nIndex;

	aRequests := {
		{"FDA", 2, 12.3456},
		{"EPA", 3, 12.3456},
		{"ISO", 2, 12.3456}
	};

	:FOR nIndex := 1 :TO ALen(aRequests);
		aRow := aRequests[nIndex];
		sStandard := aRow[1];
		nDigits := aRow[2];
		nValue := aRow[3];

		sRounded := StdRound(sStandard, nDigits, nValue);
		sLine := sStandard + ": " + sRounded;

		UsrMes(sLine);  /* Displays one line for the current standard;
	:NEXT;
:ENDPROC;

/* Usage;
DoProc("ReviewStandardOutputs");
```

### Normalize ISO output for export while preserving the raw value

Keep the original fixed-width `ISO` string for export logic, but derive a trimmed display value for logs or UI text.

```ssl
:PROCEDURE BuildIsoExportValue;
	:PARAMETERS nDigits, nValue;
	:DECLARE sRounded, sDisplay, oErr;

	:TRY;
		sRounded := StdRound("ISO", nDigits, nValue);
		sDisplay := AllTrim(sRounded);

		UsrMes("ISO display value: " + sDisplay);

		:RETURN "VALUE=" + sDisplay + "|RAW=" + sRounded;

	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("BuildIsoExportValue failed: " + oErr:Description);
		/* Displays on failure: BuildIsoExportValue failed;

		:RETURN "";
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("BuildIsoExportValue", {2, 12.3456});
```

## Related

- [`Round`](Round.md)
- [`SigFig`](SigFig.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
