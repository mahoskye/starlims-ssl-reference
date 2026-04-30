---
title: "Max"
summary: "Returns whichever of two values compares greater when both arguments are the same supported type."
id: ssl.function.max
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Max

Returns whichever of two values compares greater when both arguments are the same supported type.

`Max` accepts two arguments and returns the larger one. It supports three value families: strings, numbers, and dates. When both arguments are strings, it returns the string that compares greater. When both are numbers, it returns the larger numeric value. When both are dates, it returns the later date.

If the two arguments are different types, the function raises an error. If both arguments are the same type but that type is not supported by `Max`, the call also fails.

## When to use

- When you need the larger of two numeric values.
- When you need the later of two dates.
- When you need whichever of two strings compares greater.

## Syntax

```ssl
Max(vValue1, vValue2)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vValue1` | any | yes | — | First value to compare. Must be the same supported type as `vValue2`. |
| `vValue2` | any | yes | — | Second value to compare. Must be the same supported type as `vValue1`. |

## Returns

**[string](../types/string.md), [number](../types/number.md), or [date](../types/date.md)** — The greater of the two input values, in the same type as the inputs.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `vValue1` or `vValue2` is [`NIL`](../literals/nil.md). | `Argument cannot be null.` |
| `vValue1` and `vValue2` are different types. | `Function arguments type must match.` |
| Both arguments are the same type but not a supported type (string, number, or date). | `Max function arguments type must match.` |

## Best practices

!!! success "Do"
    - Pass two values of the same supported type: string, number, or date.
    - Use `Max` directly when you need the greater of two values instead of writing repeated comparison logic.
    - Validate inputs before calling when mixed or unsupported types are possible.

!!! failure "Don't"
    - Mix types such as a string and a number in one call.
    - Assume `Max` supports arrays, objects, booleans, or other non-string, non-number, non-date values.
    - Rewrite simple maximum comparisons by hand unless you need custom comparison rules.

## Examples

### Choose the higher score

Use `Max` to keep the larger of two numeric results.

```ssl
:PROCEDURE SelectTopScore;
	:DECLARE nScoreA, nScoreB, nTopScore;

	nScoreA := 87.5;
	nScoreB := 92.3;
	nTopScore := Max(nScoreA, nScoreB);

	UsrMes("Top score: " + LimsString(nTopScore));
:ENDPROC;

/* Usage;
DoProc("SelectTopScore");
```

[`UsrMes`](UsrMes.md) displays:

```text
Top score: 92.3
```

### Keep the later of two dates

Use `Max` to keep the most recent date before continuing processing.

```ssl
:PROCEDURE GetLatestReviewDate;
	:DECLARE dLabDate, dQaDate, dLatestDate, sMessage;

	dLabDate := CToD("03/15/2026");
	dQaDate := CToD("04/02/2026");
	dLatestDate := Max(dLabDate, dQaDate);

	sMessage := "Latest review date: " + DToC(dLatestDate);
	UsrMes(sMessage);

	:RETURN dLatestDate;
:ENDPROC;

/* Usage;
DoProc("GetLatestReviewDate");
```

[`UsrMes`](UsrMes.md) displays:

```text
Latest review date: 04/02/2026
```

### Compare candidate string keys before lookup

Use `Max` after deriving two candidate keys and keep the greater one for the next step in a workflow.

```ssl
:PROCEDURE SelectPreferredKey;
	:PARAMETERS sPrimaryCode, sFallbackCode;
	:DECLARE sPrimaryKey, sFallbackKey, sChosenKey;

	sPrimaryKey := Upper(AllTrim(sPrimaryCode));
	sFallbackKey := Upper(AllTrim(sFallbackCode));
	sChosenKey := Max(sPrimaryKey, sFallbackKey);

	UsrMes("Chosen key: " + sChosenKey);

	:RETURN sChosenKey;
:ENDPROC;

/* Usage;
DoProc("SelectPreferredKey", {"ALPHA", "BETA"});
```

[`UsrMes`](UsrMes.md) displays:

```text
Chosen key: BETA
```

## Related

- [`Min`](Min.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
- [`date`](../types/date.md)
