---
title: "BuildArray"
summary: "Splits text into a one-dimensional array using a literal delimiter."
id: ssl.function.buildarray
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# BuildArray

Splits text into a one-dimensional array using a literal delimiter.

`BuildArray` splits `sText` into string elements using a literal delimiter. If `sText` is [`NIL`](../literals/nil.md) or contains only whitespace after trimming, the function returns an empty array.

If optional parameters are omitted, these defaults apply: `bCrlfOk` = [`.F.`](../literals/false.md), `sDelimiter` = `","`, `bUnique` = [`.F.`](../literals/false.md), and `bTrimSpaces` = [`.T.`](../literals/true.md). When `bCrlfOk` is [`.F.`](../literals/false.md), the function removes CR/LF pairs from the source text before splitting. When `bTrimSpaces` is [`.T.`](../literals/true.md), it trims each returned element with [`AllTrim`](AllTrim.md). The `bUnique` parameter is accepted but has no effect, so duplicate values are preserved.

## When to use

- When you need to split a single delimited string into values you can loop over.
- When you need to normalize user input or imported text before comparisons or lookups.
- When you need to parse text that uses a custom or multi-character literal separator.

## Syntax

```ssl
BuildArray(sText, [bCrlfOk], [sDelimiter], [bUnique], [bTrimSpaces])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `sText` | [string](../types/string.md) | yes | — | Source text to split. [`NIL`](../literals/nil.md) or whitespace-only input returns `{}`. |
| `bCrlfOk` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | When [`.F.`](../literals/false.md), removes CR/LF pairs from the source text before splitting. |
| `sDelimiter` | [string](../types/string.md) | no | `","` | Literal delimiter used to split the source text. |
| `bUnique` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Accepted for compatibility, but currently has no effect. |
| `bTrimSpaces` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | When [`.T.`](../literals/true.md), trims leading and trailing spaces from each returned element. |

## Returns

**[array](../types/array.md)** — A one-dimensional array of strings.

## Best practices

!!! success "Do"
    - Pass `sDelimiter` explicitly when the source format is known.
    - Leave `bTrimSpaces` enabled when the values will be compared, searched, or displayed.
    - Handle the empty-array result when `sText` may be [`NIL`](../literals/nil.md) or whitespace-only.
    - Use [`BuildArray2`](BuildArray2.md) instead when the input contains both row and column delimiters.

!!! failure "Don't"
    - Expect `bUnique` to remove duplicates. It is accepted but has no effect.
    - Assume `bCrlfOk := .F.` removes every newline variant. It removes CR/LF pairs before splitting.
    - Use `BuildArray` for CSV-style quoted parsing or tabular text. It performs literal delimiter splitting only.
    - Assume empty elements are discarded. Adjacent delimiters are preserved as empty strings in the result.

## Caveats

- When `sDelimiter` does not appear in `sText`, the result contains one element with the original text after any configured CR/LF removal and trimming.
- Adjacent delimiters produce empty-string elements in the result — they are not discarded.

## Examples

### Split a comma-separated list

Splits a comma-delimited status string into individual values and joins them back with brackets to confirm each element.

```ssl
:PROCEDURE ParseStatusList;
	:DECLARE sStatusList, aStatuses, nIndex, sMessage;

	sStatusList := "Logged,Complete,Pending";
	aStatuses := BuildArray(sStatusList);

	sMessage := "Statuses:";

	:FOR nIndex := 1 :TO ALen(aStatuses);
		sMessage := sMessage + " [" + aStatuses[nIndex] + "]";
	:NEXT;

	UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("ParseStatusList");
```

[`UsrMes`](UsrMes.md) displays:

```text
Statuses: [Logged] [Complete] [Pending]
```

### Trim values from a custom-delimited filter

Splits a pipe-delimited string with surrounding spaces, using `bTrimSpaces` to clean each element so the result contains compact identifiers.

```ssl
:PROCEDURE ParseSampleFilter;
	:DECLARE sFilter, aSampleIds, nIndex, sMessage;

	sFilter := "  S-1001  | S-1002 |  S-1003  ";
	aSampleIds := BuildArray(sFilter, .F., "|", .F., .T.);

	sMessage := "Parsed sample IDs:";

	:FOR nIndex := 1 :TO ALen(aSampleIds);
		sMessage := sMessage + Chr(13) + Chr(10)
					+ "- " + aSampleIds[nIndex];
	:NEXT;

	UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("ParseSampleFilter");
```

[`UsrMes`](UsrMes.md) displays:

```text
Parsed sample IDs:
- S-1001
- S-1002
- S-1003
```

### Preserve embedded line breaks with a multi-character delimiter

Passes `bCrlfOk := .T.` so that CR/LF characters inside each section are kept intact, and uses a multi-character `"||NEXT||"` string as the delimiter to split the template into two sections.

```ssl
:PROCEDURE ParseTemplateSections;
	:DECLARE sTemplate, aSections, sPreview;

	sTemplate := "Summary line 1" + Chr(13) + Chr(10)
				 + "Summary line 2"
				 + "||NEXT||"
				 + "Action line 1" + Chr(13) + Chr(10)
				 + "Action line 2";

	aSections := BuildArray(sTemplate, .T., "||NEXT||", .F., .T.);

	sPreview := "Section count: " + LimsString(ALen(aSections))
				+ Chr(13) + Chr(10) + Chr(13) + Chr(10)
				+ "Section 1:" + Chr(13) + Chr(10) + aSections[1]
				+ Chr(13) + Chr(10) + Chr(13) + Chr(10)
				+ "Section 2:" + Chr(13) + Chr(10) + aSections[2];

	UsrMes(sPreview);
:ENDPROC;

/* Usage;
DoProc("ParseTemplateSections");
```

[`UsrMes`](UsrMes.md) displays:

```text
Section count: 2

Section 1:
Summary line 1
Summary line 2

Section 2:
Action line 1
Action line 2
```

## Related

- [`BuildArray2`](BuildArray2.md)
- [`BuildString`](BuildString.md)
- [`BuildString2`](BuildString2.md)
- [`BuildStringForIn`](BuildStringForIn.md)
- [`PrepareArrayForIn`](PrepareArrayForIn.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
