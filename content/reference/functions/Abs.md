---
title: "Abs"
summary: "Calculates the absolute value of a number."
id: ssl.function.abs
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Abs

Calculates the absolute value of a number.

`Abs` returns the magnitude of `nValue` without its sign. Negative values become positive, while zero and positive values are returned unchanged. Passing [`NIL`](../literals/nil.md) raises an error.

## When to use

- When you need to ensure a number is non-negative before further calculations, such as in distance or magnitude computations.
- When processing user input or imported data that might contain negative numbers where only positive results are valid.
- When normalizing data for statistical analysis that must not include negative values.
- When displaying values such as balances or counts that should always appear without a sign.

## Syntax

```ssl
Abs(nValue)
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `nValue` | [number](../types/number.md) | yes | — | The numeric value to get the absolute value of. |

## Returns

**[number](../types/number.md)** — The absolute value of `nValue`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `nValue` is [`NIL`](../literals/nil.md). | `<nValue> cannot be null.` |

## Best practices

!!! success "Do"
    - Check whether the input can be [`NIL`](../literals/nil.md) before calling `Abs`.
    - Use `Abs` when the code always needs absolute value and does not need dynamic function selection.
    - Combine `Abs` with range checks when business rules require both non-negative values and upper or lower limits.

!!! failure "Don't"
    - Pass a value that might be [`NIL`](../literals/nil.md) without checking first. The call fails instead of returning a fallback result.
    - Use `Abs` when the sign itself carries meaning, such as debit versus credit or gain versus loss. Converting the value removes that distinction.
    - Treat `Abs` as full validation. It only removes the sign and does not
      enforce business-specific thresholds or rules.

## Examples

### Remove the negative sign from an input value

Demonstrates the basic result for a single negative number: the sign is stripped and the magnitude is returned unchanged.

```ssl
:DECLARE nInput, nAbsValue;

nInput := -125;
nAbsValue := Abs(nInput);

UsrMes("Absolute value is: " + LimsString(nAbsValue));
```

[`UsrMes`](UsrMes.md) displays:

```text
Absolute value is: 125
```

### Sum movement regardless of direction

Shows how `Abs` helps accumulate total movement when positive and negative deltas should contribute equally to a running total.

```ssl
:PROCEDURE SumTotalMovement;
	:DECLARE aSteps, nTotalMovement, nStep, nIndex;

	aSteps := {15, (0 - 4), (0 - 9), 6, (0 - 2)};
	nTotalMovement := 0;

	:FOR nIndex := 1 :TO ALen(aSteps);
		nStep := aSteps[nIndex];
		nTotalMovement := nTotalMovement + Abs(nStep);
	:NEXT;

	UsrMes("Total movement: " + LimsString(nTotalMovement));
:ENDPROC;

/* Usage;
DoProc("SumTotalMovement");
```

[`UsrMes`](UsrMes.md) displays:

```text
Total movement: 36
```

### Compare measured deviation to a tolerance

Uses `Abs` in a quality-check pattern where only the magnitude of the deviation matters, not its direction. The procedure reports whether the measured result falls within the allowed difference.

```ssl
:PROCEDURE CheckResultAgainstTolerance;
	:PARAMETERS nExpected, nActual, nAllowedDiff;
	:DECLARE nDifference;

	nDifference := Abs(nActual - nExpected);

	:IF nDifference <= nAllowedDiff;
		UsrMes("Result is within tolerance");
	:ELSE;
		/* Displays on failure: deviation exceeds the allowed tolerance;
		UsrMes(
			"Deviation "
			+ LimsString(nDifference)
			+ " exceeds allowed tolerance "
			+ LimsString(nAllowedDiff)
		);
	:ENDIF;

	:RETURN nDifference;
:ENDPROC;

/* Usage;
DoProc("CheckResultAgainstTolerance", {100, 97.5, 5});
```

## Related

- [`MatFunc`](MatFunc.md)
- [`number`](../types/number.md)
