---
title: "SubStr"
summary: "Extracts part of a string starting at a position you specify."
id: ssl.function.substr
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SubStr

Extracts part of a string starting at a position you specify.

`SubStr()` returns characters from `sSource` starting at `nStartPos`. Positions are 1-based for positive values, so `1` means the first character. If `nStartPos` is omitted or `0`, extraction starts at the first character. Negative values count backward from the end of the string, so `-1` returns the last character and `-2` starts at the second-to-last character. If `nLength` is omitted, the function returns all remaining characters. If `nStartPos` is beyond the end of the string, the result is `""`. If `nLength` is negative or longer than the remaining characters, `SubStr()` returns only the available characters.

## When to use

- When you need to split or extract specific fields or sections from structured text based on position and length.
- When validating codes or user input by checking or extracting parts of an identifier string.
- When generating abbreviated display values, such as showing only a segment of a longer name or description.
- When you need to remove a known prefix or suffix by specifying the main content's position and length explicitly.

## Syntax

```ssl
SubStr(sSource, [nStartPos], [nLength])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSource` | [string](../types/string.md) | yes | — | Source string to read from. |
| `nStartPos` | [number](../types/number.md) | no | `0` | Start position. Positive values are 1-based, `0` starts at the first character, and negative values count from the end. |
| `nLength` | [number](../types/number.md) | no | all remaining characters | Number of characters to return. |

## Returns

**[string](../types/string.md)** — The extracted substring. Returns `""` when the computed start position is at or beyond the end of the string.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSource` is [`NIL`](../literals/nil.md). | `Argument sSource cannot be null.` |

## Best practices

!!! success "Do"
    - Check that the input string is available before calling `SubStr()`.
    - Use negative `nStartPos` values when you want characters relative to the end of the string.
    - Omit `nLength` when you want everything from the start position to the end.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) as `sSource`. That raises an error instead of returning an empty string.
    - Over-calculate end offsets when a negative `nStartPos` already expresses the intent clearly.
    - Add manual bounds logic just to reach the end of the string when omitting `nLength` already does that.

## Caveats

- A negative `nStartPos` that would go before the start of the string clamps to position 1.

## Examples

### Extract the first three characters

Read a fixed-width prefix from the start of a sample ID.

```ssl
:PROCEDURE GetSampleCategory;
	:DECLARE sSampleID, sCategory, sPrefix;

	sSampleID := "ENV-2024-0042";
	sPrefix := SubStr(sSampleID, 0, 3);

	:IF sPrefix == "ENV";
		sCategory := "Environmental";
	:ELSE;
		:IF sPrefix == "BIO";
			sCategory := "Biological";
		:ELSE;
			:IF sPrefix == "CHE";
				sCategory := "Chemical";
			:ELSE;
				sCategory := "Unknown";
			:ENDIF;
		:ENDIF;
	:ENDIF;

	UsrMes(sSampleID + " maps to category " + sCategory);

	:RETURN sCategory;
:ENDPROC;

/* Usage;
DoProc("GetSampleCategory");
```

`UsrMes` displays:

```text
ENV-2024-0042 maps to category Environmental
```

### Read from the end with a negative position

Extract the last three status characters without first calculating the string length.

```ssl
:PROCEDURE GetStatusSuffix;
	:DECLARE sStatusCode, sSuffix;

	sStatusCode := "REVIEWED";
	sSuffix := SubStr(sStatusCode, -3);

	UsrMes("Suffix: " + sSuffix);
:ENDPROC;

/* Usage;
DoProc("GetStatusSuffix");
```

`UsrMes` displays:

```text
Suffix: WED
```

### Extract text after a delimiter

Locate a delimiter, then return everything after it by omitting `nLength`.

```ssl
:PROCEDURE GetBatchNumber;
	:DECLARE sSampleID, sBatchNumber, nDashPos;

	sSampleID := "QC-2048-17";
	nDashPos := At("-", sSampleID);

	:IF nDashPos > 0;
		sBatchNumber := SubStr(sSampleID, nDashPos + 1);
	:ELSE;
		sBatchNumber := "";
	:ENDIF;

	UsrMes("Batch segment: " + sBatchNumber);

	:RETURN sBatchNumber;
:ENDPROC;

/* Usage;
DoProc("GetBatchNumber");
```

`UsrMes` displays:

```text
Batch segment: 2048-17
```

## Related

- [`Left`](Left.md)
- [`Len`](Len.md)
- [`Right`](Right.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
