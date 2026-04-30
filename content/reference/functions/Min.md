---
title: "Min"
summary: "Returns whichever of two values compares lower when both arguments are the same supported type."
id: ssl.function.min
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Min

Returns whichever of two values compares lower when both arguments are the same supported type.

`Min` accepts two arguments and returns the lesser one. It supports three value families: strings, numbers, and dates. When both arguments are strings, it returns the string that compares lower. When both are numbers, it returns the smaller numeric value. When both are dates, it returns the earlier date.

If the two arguments are different types, the function raises an error. If both arguments are the same type but not a supported type, the function raises an error.

## When to use

- When comparing two dates to determine which comes first in a sequence or schedule.
- When selecting the smaller of two numeric values.
- When choosing whichever of two strings sorts first for a stable key or label.
- When normalizing data by consistently keeping the lesser of two same-type values.

## Syntax

```ssl
Min(vValue1, vValue2)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vValue1` | any | yes | — | First value to compare. Must be the same supported type as `vValue2`. |
| `vValue2` | any | yes | — | Second value to compare. Must be the same supported type as `vValue1`. |

## Returns

**[string](../types/string.md), [number](../types/number.md), or [date](../types/date.md)** — The lesser of the two input values, in the same type as the inputs.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `vValue1` or `vValue2` is [`NIL`](../literals/nil.md). | `Argument cannot be null.` |
| `vValue1` and `vValue2` are different types. | `Function arguments type must match.` |
| Both arguments are the same type but not a supported type (string, number, or date). | `Min function arguments type must match.` |

## Best practices

!!! success "Do"
    - Pass two values of the same supported type: string, number, or date.
    - Use `Min` directly when you need the lesser of two values instead of writing repeated comparison logic.
    - Validate inputs before calling when mixed or unsupported types are possible.

!!! failure "Don't"
    - Mix types such as a string and a number in one call.
    - Assume `Min` supports arrays, objects, booleans, or other non-string, non-number, non-date values.
    - Use `Min` when you actually need to enforce a lower bound. That pattern needs [`Max`](Max.md), not `Min`.

## Examples

### Find the earlier of two dates

Pick the earlier of two scheduled dates for a user event.

```ssl
:PROCEDURE GetEarlierEventDate;
	:DECLARE dEventDate1, dEventDate2, dEarlierDate, sMessage;

	dEventDate1 := CToD("03/15/2026");
	dEventDate2 := CToD("03/10/2026");
	dEarlierDate := Min(dEventDate1, dEventDate2);
	sMessage := "Earlier event date: " + DToC(dEarlierDate);

	UsrMes(sMessage);

	:RETURN dEarlierDate;
:ENDPROC;

/* Usage;
DoProc("GetEarlierEventDate");
```

[`UsrMes`](UsrMes.md) displays:

```text
Earlier event date: 03/10/2026
```

### Keep the smaller of two measurements

Use `Min` to keep the smaller of two measured values before recording a result.

```ssl
:PROCEDURE SelectLowerReading;
	:PARAMETERS nReadingA, nReadingB;
	:DECLARE nLowerValue, sOutput;

	nLowerValue := Min(nReadingA, nReadingB);
	sOutput := "Lower reading: " + LimsString(nLowerValue);

	UsrMes(sOutput);

	:RETURN nLowerValue;
:ENDPROC;

/* Usage;
DoProc("SelectLowerReading", {42.5, 38.7});
```

[`UsrMes`](UsrMes.md) displays:

```text
Lower reading: 38.7
```

### Select the lower-sorting string as a canonical key

Normalize two candidate labels, then keep the lower-sorting one as a stable key.

```ssl
:PROCEDURE GetCanonicalName;
	:PARAMETERS sName1, sName2;
	:DECLARE sLeftName, sRightName, sCanonicalKey;

	sLeftName := Upper(AllTrim(sName1));
	sRightName := Upper(AllTrim(sName2));
	sCanonicalKey := Min(sLeftName, sRightName);

	UsrMes("Canonical key: " + sCanonicalKey);

	:RETURN sCanonicalKey;
:ENDPROC;

/* Usage;
DoProc("GetCanonicalName", {"ALPHA", "BETA"});
```

[`UsrMes`](UsrMes.md) displays:

```text
Canonical key: ALPHA
```

## Related

- [`Max`](Max.md)
- [`Empty`](Empty.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
- [`date`](../types/date.md)
