---
title: "RoundPoint5"
summary: "Rounds a numeric value to a half-point increment."
id: ssl.function.roundpoint5
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# RoundPoint5

Rounds a numeric value to a half-point increment.

`RoundPoint5` returns a number in `0.5` steps. The implementation first applies FDA rounding to one decimal place, then snaps that rounded value to the nearest multiple of `0.5`. Use it when your business rule is specifically "round to the nearest half" rather than "round to N decimal places."

## When to use

- When reported values must be stored or displayed in `0.5` increments.
- When a workflow uses half-step scores, ratings, or thresholds.
- When [`Round`](Round.md) or [`StdRound`](StdRound.md) would be too general and you want fixed half-point output.

## Syntax

```ssl
RoundPoint5(nNumber)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nNumber` | [number](../types/number.md) | yes | — | Numeric value to round to the nearest `0.5`. |

## Returns

**[number](../types/number.md)** — The input rounded to the nearest half-point value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `nNumber` is [`NIL`](../literals/nil.md). | `Value cannot be null.` |

## Best practices

!!! success "Do"
    - Use `RoundPoint5` when the required output must land on `0.5` boundaries.
    - Validate optional upstream inputs before calling the function if they may be null.
    - Use [`Round`](Round.md) or [`StdRound`](StdRound.md) instead when you need configurable decimal-place rounding.

!!! failure "Don't"
    - Use `RoundPoint5` when you need arbitrary precision such as 1, 2, or 3 decimal places.
    - Pass values that may be [`NIL`](../literals/nil.md) without handling that case first.
    - Assume it is interchangeable with every domain-specific half-step rule; it follows the built-in implementation used by STARLIMS.

## Examples

### Round a single score for display

Round one calculated score before presenting it to the user.

```ssl
:PROCEDURE ShowRoundedScore;
	:DECLARE nRawScore, nRoundedScore, sMessage;

	nRawScore := 3.74;
	nRoundedScore := RoundPoint5(nRawScore);
	sMessage := "Rounded score: " + LimsString(nRoundedScore);

	UsrMes(sMessage);

	:RETURN nRoundedScore;
:ENDPROC;

/* Call the procedure;
DoProc("ShowRoundedScore");
```

[`UsrMes`](UsrMes.md) displays:

```text
Rounded score: 3.5
```

### Normalize several ratings before averaging

Round each reading to a half-point, then calculate the average of the rounded values.

```ssl
:PROCEDURE AverageRoundedRatings;
	:DECLARE aRatings, nSum, nAverage, nRounded, nIndex, sMessage;

	aRatings := {4.2, 3.7, 4.9, 3.5, 4.1};
	nSum := 0;

	:FOR nIndex := 1 :TO ALen(aRatings);
		nRounded := RoundPoint5(aRatings[nIndex]);
		nSum += nRounded;
	:NEXT;

	nAverage := nSum / ALen(aRatings);
	sMessage := "Average rounded rating: " + LimsString(nAverage);

	UsrMes(sMessage);

	:RETURN nAverage;
:ENDPROC;

/* Call the procedure;
DoProc("AverageRoundedRatings");
```

[`UsrMes`](UsrMes.md) displays:

```text
Average rounded rating: 4
```

## Related

- [`Round`](Round.md)
- [`SigFig`](SigFig.md)
- [`StdRound`](StdRound.md)
- [`number`](../types/number.md)
