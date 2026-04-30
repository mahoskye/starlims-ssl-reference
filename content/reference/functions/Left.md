---
title: "Left"
summary: "Extracts the leftmost characters from a string."
id: ssl.function.left
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Left

Extracts the leftmost characters from a string.

`Left` returns the first characters from `sSource` based on `nLength`. If the requested length is greater than the length of `sSource`, the full string is returned. If the effective length is zero or negative, the function returns [`NIL`](../literals/nil.md). If `sSource` or `nLength` is [`NIL`](../literals/nil.md), the function raises an error.

The `nLength` argument is rounded to a whole number before extraction. Midpoint values round away from zero, so values such as `2.5` behave like `3` and `-0.5` behave like `-1`.

## When to use

- When you need a string prefix without manually calculating indexes.
- When you need to trim imported values to a fixed leading width.
- When you want [`NIL`](../literals/nil.md) for zero or negative requested lengths instead of an empty string.

## Syntax

```ssl
Left(sSource, nLength)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSource` | [string](../types/string.md) | yes | — | Source string to read from. |
| `nLength` | [number](../types/number.md) | yes | — | Number of leading characters to return. The value is rounded to a whole number before use. |

## Returns

**[string](../types/string.md)** — The leftmost `nLength` characters of `sSource`. Returns the full string when `nLength` exceeds the length of `sSource`. Returns [`NIL`](../literals/nil.md) when the effective `nLength` is zero or negative.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSource` is [`NIL`](../literals/nil.md). | `Argument sSource cannot be null.` |
| `nLength` is [`NIL`](../literals/nil.md). | `Argument nLength cannot be null.` |

## Best practices

!!! success "Do"
    - Use `Left` when you need a clear, direct prefix extraction.
    - Check for [`NIL`](../literals/nil.md) when `nLength` may evaluate to zero or less.
    - Normalize or validate the requested length before appending extra text such as ellipses.

!!! failure "Don't"
    - Assume zero or negative lengths return an empty string — `Left` returns [`NIL`](../literals/nil.md) for those cases.
    - Recreate prefix logic with [`SubStr`](SubStr.md) or manual index math when `Left` expresses the intent directly.
    - Ignore rounding behavior when passing decimal lengths — the function rounds before extracting characters.

## Caveats

- An empty `sSource` with a positive `nLength` returns an empty string.
- `nLength` is rounded before evaluation, so decimal values can change whether the result is a string or [`NIL`](../literals/nil.md).
- `Left` does not pad results — if fewer characters are available, it returns only the available characters.

## Examples

### Extract a fixed-length prefix to check against an expected value

Extract the first three characters of a sample ID and compare them to the expected `"LAB"` prefix. The input `"LAB-7829"` matches, so the true branch fires.

```ssl
:DECLARE sSampleId, sPrefix, bMatches;

sSampleId := "LAB-7829";
sPrefix := Left(sSampleId, 3);
bMatches := sPrefix == "LAB";

:IF bMatches;
	UsrMes("Sample ID uses the LAB prefix");
:ELSE;
	UsrMes("Sample ID does not use the LAB prefix");
:ENDIF;
```

### Parse a fixed-width record into status code and sample ID

Extract the 3-character status code from the start of the record using `Left`, then read the remaining 11-character sample ID with [`SubStr`](SubStr.md). The record `"ACTSAM00012345"` produces status `"ACT"` and sample `"SAM00012345"`.

```ssl
:PROCEDURE ParseHeader;
	:DECLARE sRecord, sStatusCode, sSampleId, sSummary;

	sRecord := "ACTSAM00012345";
	sStatusCode := Left(sRecord, 3);
	sSampleId := SubStr(sRecord, 4, 11);

	sSummary := "Status=" + sStatusCode + ", Sample=" + sSampleId;
	UsrMes(sSummary);

	:RETURN sSummary;
:ENDPROC;

/* Call the procedure to run the example;
DoProc("ParseHeader");
```

[`UsrMes`](UsrMes.md) displays:

```
Status=ACT, Sample=SAM00012345
```

### Truncate a caption to a maximum width with an ellipsis

Guard the requested width before appending `"..."` so the call never concatenates a string with a [`NIL`](../literals/nil.md) result from `Left`. For `sCaption = "Hello, World!"` and `nMaxWidth = 10`, the procedure returns `"Hello, ..."` — the first 7 characters plus the ellipsis, within the 10-character budget.

```ssl
:PROCEDURE FormatCaption;
	:PARAMETERS sCaption, nMaxWidth;
	:DECLARE sDisplayCaption, nPrefixWidth;

	:IF nMaxWidth <= 3;
		:RETURN Left(sCaption, nMaxWidth);
	:ENDIF;

	:IF Len(sCaption) <= nMaxWidth;
		:RETURN sCaption;
	:ENDIF;

	nPrefixWidth := nMaxWidth - 3;
	sDisplayCaption := Left(sCaption, nPrefixWidth) + "...";

	:RETURN sDisplayCaption;
:ENDPROC;

/* Call the procedure to run the example;
DoProc("FormatCaption", {"Hello, World!", 10});
```

## Related

- [`Len`](Len.md)
- [`Right`](Right.md)
- [`SubStr`](SubStr.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
