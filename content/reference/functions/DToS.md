---
title: "DToS"
summary: "Converts a date value to an 8-character string in yyyyMMdd format."
id: ssl.function.dtos
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DToS

Converts a date value to an 8-character string in `yyyyMMdd` format.

`DToS` takes one date argument and returns a fixed-width string such as `20240509`. If `dDate` is an empty date, the function returns eight spaces instead. Passing [`NIL`](../literals/nil.md) or a non-date value raises an exception. Use `DToS` when you need a stable, lexically sortable date key rather than a display format that depends on current date settings.

## When to use

- When you need a fixed-format date string for sorting, matching, or key generation.
- When writing dates to integrations, files, or exports that expect `yyyyMMdd`.
- When you need date text that does not depend on the current date format setting.

## Syntax

```ssl
DToS(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | Date value to convert to `yyyyMMdd` |

## Returns

**[string](../types/string.md)** — Fixed-width 8-character result. Returns `yyyyMMdd` for a populated date, or eight spaces when `dDate` is empty.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `dDate argument cannot be null` |
| `dDate` is not a date value. | `dDate must be of date type` |

## Best practices

!!! success "Do"
    - Use `DToS` when you need a stable `yyyyMMdd` value for sorting or interchange.
    - Check for empty dates before or after conversion when blank output would be ambiguous.
    - Use [`DToC`](DToC.md) or [`DateToString`](DateToString.md) for user-facing formats.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md), strings, or numbers directly. `DToS` requires a date value.
    - Assume an empty date returns `00000000` or an empty string.
    - Use `DToS` for locale-aware or user-formatted output.

## Caveats

- `DToS` does not parse or coerce strings into dates.
- Because the format is year-month-day, simple string sorting also sorts by date.

## Examples

### Build a fixed-format date key for export or sorting

Converts a date to an 8-character `yyyyMMdd` key and displays it.

```ssl
:PROCEDURE BuildSampleDateKey;
	:DECLARE dLoggedDate, sDateKey;

	dLoggedDate := CToD("03/15/2024");
	sDateKey := DToS(dLoggedDate);

	UsrMes("Sample date key: " + sDateKey);
:ENDPROC;

/* Usage;
DoProc("BuildSampleDateKey");
```

[`UsrMes`](UsrMes.md) displays:

```text
Sample date key: 20240315
```

### Replace the empty-date result before using the key downstream

Replaces the eight-space result returned for an empty date with a `[No release date]` placeholder before returning the key.

```ssl
:PROCEDURE GetReleaseDateKey;
	:PARAMETERS dReleaseDate;
	:DECLARE sDateKey;

	sDateKey := DToS(dReleaseDate);

	:IF Len(sDateKey) == 8 .AND. Empty(AllTrim(sDateKey));
		sDateKey := "[No release date]";
	:ENDIF;

	:RETURN sDateKey;
:ENDPROC;

/* Usage;
DoProc("GetReleaseDateKey", {CToD("03/15/2024")});
```

### Build sortable identifiers for a batch of records

Builds a sortable `SampleID_yyyyMMdd` key for each row in a sample array, substituting `_PENDING` when the logged date is empty.

```ssl
:PROCEDURE BuildBatchKeys;
	:PARAMETERS aSamples;
	:DECLARE aKeys, nIndex, sSampleID, dLoggedDate, sDateKey, sBatchKey;

	aKeys := {};

	:FOR nIndex := 1 :TO ALen(aSamples);
		sSampleID := aSamples[nIndex, 1];
		dLoggedDate := aSamples[nIndex, 2];

		sDateKey := DToS(dLoggedDate);

		:IF Len(sDateKey) == 8 .AND. Empty(AllTrim(sDateKey));
			sBatchKey := sSampleID + "_PENDING";
		:ELSE;
			sBatchKey := sSampleID + "_" + sDateKey;
		:ENDIF;

		AAdd(aKeys, sBatchKey);
	:NEXT;

	:RETURN aKeys;
:ENDPROC;

/* Usage;
DoProc("BuildBatchKeys", {{{"S-001", CToD("03/15/2024")}}});
```

## Related

- [`CToD`](CToD.md)
- [`DToC`](DToC.md)
- [`DateFromNumbers`](DateFromNumbers.md)
- [`DateFromString`](DateFromString.md)
- [`DateToString`](DateToString.md)
- [`StringToDate`](StringToDate.md)
- [`string`](../types/string.md)
- [`date`](../types/date.md)
