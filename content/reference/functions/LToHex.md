---
title: "LToHex"
summary: "Converts a string or integer to hexadecimal text."
id: ssl.function.ltohex
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LToHex

Converts a string or integer to hexadecimal text.

`LToHex` accepts a non-empty string or a whole-number numeric value. String input is converted character by character using uppercase hexadecimal formatting. Numeric input returns an 8-character uppercase hexadecimal string. Negative integers from `-2147483647` through `-1` are converted to their unsigned 32-bit hexadecimal form. Positive integers above `4294967295`, integers below `-2147483647`, non-integer numerics, and other non-empty types raise an error.

If `vSource` is empty according to [`Empty`](Empty.md), `LToHex` returns `vSource` unchanged instead of converting it.

## When to use

- When you need hexadecimal text for a string value.
- When you need an 8-character hexadecimal form of an integer for external systems.
- When you are round-tripping text with [`LFromHex`](LFromHex.md).

## Syntax

```ssl
LToHex(vSource)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vSource` | any | yes | — | Value to convert. Non-empty values must be a string or a whole-number numeric value in the supported range. Empty values are returned unchanged. |

## Returns

**[string](../types/string.md)** — Hexadecimal encoding of `vSource`. For string input, returns the character bytes encoded as uppercase hex pairs. For numeric input, returns an 8-character zero-padded uppercase hex string. Returns the original `vSource` value unchanged (preserving its input type) when `vSource` is empty.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `vSource` is a non-empty unsupported type, a non-integer numeric value, or outside the supported numeric range. | `Argument: vSource must be a string or an integer.` |

## Best practices

!!! success "Do"
    - Pass strings when you need a text-to-hex conversion.
    - Pass only whole-number numeric values when you need the 8-character integer form.
    - Use [`LFromHex`](LFromHex.md) to verify round-trip string conversions.

!!! failure "Don't"
    - Assume every numeric value is accepted. Decimal values and out-of-range integers raise an error.
    - Assume empty values are converted. `LToHex` returns them unchanged.
    - Use `LToHex` when you need hexadecimal-to-decimal conversion. Use [`LHex2Dec`](LHex2Dec.md) for that direction.

## Caveats

- Numeric 0 is considered empty by [`Empty`](Empty.md) and is returned unchanged rather than converted to `"00000000"`.
- String conversion is byte-oriented, so the output is best treated as encoded data rather than display text.
- For string input, byte values below `16` are space-padded by the formatter rather than zero-padded.

## Examples

### Convert a string to its hexadecimal encoding

Each ASCII character in `"ABC-12345"` is encoded as two uppercase hex digits and the results are concatenated into a single string. All characters in this input have byte values above 15, so no space-padding occurs.

```ssl
:PROCEDURE EncodeSampleId;
	:DECLARE sSampleId, sHexValue;

	sSampleId := "ABC-12345";
	sHexValue := LToHex(sSampleId);

	UsrMes("Hex value: " + sHexValue);
:ENDPROC;

/* Usage;
DoProc("EncodeSampleId");
```

[`UsrMes`](UsrMes.md) displays:

```
Hex value: 4142432D3132333435
```

### Convert positive and negative integers to 8-character hex

Positive 255 produces a zero-padded 8-character string. Negative `-9847` is mapped to its unsigned 32-bit equivalent before conversion, producing a different 8-character result.

```ssl
:PROCEDURE ShowLegacyIdsAsHex;
	:DECLARE nCurrentId, nLegacyId, sCurrentHex, sLegacyHex;

	nCurrentId := 255;
	nLegacyId := -9847;

	sCurrentHex := LToHex(nCurrentId);
	sLegacyHex := LToHex(nLegacyId);

	UsrMes("Current ID hex: " + sCurrentHex);
	UsrMes("Legacy ID hex: " + sLegacyHex);

	:RETURN sLegacyHex;
:ENDPROC;

/* Usage;
DoProc("ShowLegacyIdsAsHex");
```

`UsrMes` displays:

```text
Current ID hex: 000000FF
Legacy ID hex: FFFFD989
```

### Handle empty values and invalid input safely

Call `LToHex` with an empty string, a whole number, and a non-integer to observe all three outcomes: empty values return unchanged, valid integers convert successfully, and non-integers raise an error caught by [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md).

```ssl
:PROCEDURE ValidateHexInput;
	:DECLARE sEmptyText, sEmptyResult, nWholeValue, sWholeHex;
	:DECLARE nDecimalValue, oErr;

	sEmptyText := "";
	nWholeValue := 1024;
	nDecimalValue := 12.5;

	sEmptyResult := LToHex(sEmptyText);
	sWholeHex := LToHex(nWholeValue);

	UsrMes("Whole-number hex: " + sWholeHex);

	:IF Empty(sEmptyResult);
		UsrMes("Empty input was returned unchanged");
	:ENDIF;

	:TRY;
		LToHex(nDecimalValue);
	:CATCH;
		oErr := GetLastSSLError();
		UsrMes("Conversion failed: " + oErr:Description);
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ValidateHexInput");
```

`UsrMes` displays:

```text
Whole-number hex: 00000400
Empty input was returned unchanged
Conversion failed: Argument: vSource must be a string or an integer.
```

## Related

- [`IsHex`](IsHex.md)
- [`LFromHex`](LFromHex.md)
- [`LHex2Dec`](LHex2Dec.md)
- [`string`](../types/string.md)
