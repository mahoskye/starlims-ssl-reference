---
title: "Right"
summary: "Extracts a specified number of characters from the end of a string."
id: ssl.function.right
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Right

Extracts a specified number of characters from the end of a string.

`Right` returns the trailing characters from `sSource` based on `nLength`. If the requested length is greater than the source length, the full string is returned. If the effective length is zero, the function returns [`NIL`](../literals/nil.md). If `sSource` or `nLength` is [`NIL`](../literals/nil.md), the function raises an error. A negative rounded length also raises an error.

The `nLength` argument is treated as a number and rounded to a whole number before extraction.

## When to use

- When you need a suffix without manually calculating start positions.
- When only the last few characters of an ID, code, or label matter.
- When parsing fixed-width text where the meaningful value is right-aligned.
- When you want a simpler alternative to [`SubStr`](SubStr.md) for trailing extraction.

## Syntax

```ssl
Right(sSource, nLength)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSource` | [string](../types/string.md) | yes | — | Source string to read from. |
| `nLength` | [number](../types/number.md) | yes | — | Number of trailing characters to return. The value is rounded to a whole number before use. |

## Returns

**[string](../types/string.md)** — The trailing `nLength` characters of `sSource`. Returns the full string when `nLength` exceeds the source length, an empty string when `sSource` is empty, or [`NIL`](../literals/nil.md) when the effective length rounds to zero.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSource` is [`NIL`](../literals/nil.md). | `Argument sSource cannot be null.` |
| `nLength` is [`NIL`](../literals/nil.md). | `Argument nLength cannot be null.` |
| The rounded effective length is negative. | `A negative [nLength] value is not allowed.` |

## Best practices

!!! success "Do"
    - Use `Right` when you need a clear, direct suffix extraction.
    - Validate or normalize `nLength` before calling when it may be zero, negative, or decimal.
    - Check for [`NIL`](../literals/nil.md) when the requested length may round to zero.

!!! failure "Don't"
    - Assume zero length returns an empty string. `Right` returns [`NIL`](../literals/nil.md) for an effective `nLength` of zero.
    - Assume an empty source string returns [`NIL`](../literals/nil.md) when a positive length is requested. It returns an empty string.
    - Recreate suffix logic with [`SubStr`](SubStr.md) and manual index math when `Right` already expresses the intent.

## Caveats

- `nLength` is rounded before evaluation, so decimal values can change whether the result is a string, [`NIL`](../literals/nil.md), or an error.

## Examples

### Check a trailing suffix

Use `Right` to compare the final characters of a sample ID with an expected suffix.

```ssl
:DECLARE sSampleId, sSuffix, bArchived;

sSampleId := "QC-2024-ARCH";
sSuffix := Right(sSampleId, 4);
bArchived := sSuffix == "ARCH";

:IF bArchived;
	UsrMes("Sample ID is archived");
:ELSE;
	UsrMes("Sample ID is active");
:ENDIF;
```

### Mask all but the last four characters

Extract the trailing four characters for display while keeping the rest of the value masked.

```ssl
:PROCEDURE FormatMaskedCode;
	:PARAMETERS sUserCode;
	:DECLARE sMaskedCode, sLastFour;

	:IF Len(sUserCode) <= 4;
		:RETURN sUserCode;
	:ENDIF;

	sLastFour := Right(sUserCode, 4);
	sMaskedCode := "****" + sLastFour;

	UsrMes("Project code: " + sMaskedCode);
	:RETURN sMaskedCode;
:ENDPROC;

/* Usage;
DoProc("FormatMaskedCode", {"LIMS-9876"});
```

[`UsrMes`](UsrMes.md) displays:

```text
Project code: ****9876
```

### Parse fields from a fixed-width record

Read multiple right-aligned fields from the end of a fixed-width record by peeling each segment off the right using `Right` and [`Left`](Left.md) in combination.

```ssl
:PROCEDURE ParseRightAlignedRecord;
	:DECLARE sRecord, sStatus, sRegionCode, sSampleNo, sSummary;
	:DECLARE nStatusLen, nRegionLen;

	sRecord := "000145EUOK";
	nStatusLen := 2;
	nRegionLen := 2;

	sStatus := Right(sRecord, nStatusLen);
	sRegionCode := Right(Left(sRecord, Len(sRecord) - nStatusLen), nRegionLen);
	sSampleNo := Left(sRecord, Len(sRecord) - nStatusLen - nRegionLen);

	sSummary := "Sample=" + sSampleNo + ", Region=" + sRegionCode
	+ ", Status=" + sStatus;
	UsrMes(sSummary);

	:RETURN sSummary;
:ENDPROC;

/* Usage;
DoProc("ParseRightAlignedRecord");
```

[`UsrMes`](UsrMes.md) displays:

```text
Sample=000145, Region=EU, Status=OK
```

## Related

- [`Left`](Left.md)
- [`SubStr`](SubStr.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
