---
title: "Sqrt"
summary: "Calculates the square root of a number."
id: ssl.function.sqrt
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Sqrt

Calculates the square root of a number.

`Sqrt` returns the square root of `nNumber`. For zero and positive values,
it returns the expected non-negative result. Passing a negative number returns the special numeric value `NaN`. Passing [`NIL`](../literals/nil.md) raises an error for `nNumber`.

## When to use

- When you need the side length implied by an area or squared value.
- When calculating geometric results such as distances or hypotenuse lengths.
- When implementing numeric formulas such as standard deviation or RMS values.

## Syntax

```ssl
Sqrt(nNumber)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nNumber` | [number](../types/number.md) | yes | — | Numeric value whose square root will be returned. |

## Returns

**[number](../types/number.md)** — The square root of `nNumber`, or `NaN` when `nNumber` is negative.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `nNumber` is [`NIL`](../literals/nil.md). | `Argument nNumber cannot be null.` |

## Best practices

!!! success "Do"
    - Check whether the input can be negative when downstream logic cannot tolerate `NaN`.
    - Use `Sqrt` directly when the operation is known in advance.
    - Validate or normalize incoming values before calling when the source data may be incomplete.

!!! failure "Don't"
    - Assume a negative input returns `0` or raises a domain exception. It returns `NaN`.
    - Pass a value that might be [`NIL`](../literals/nil.md) without checking first. The call
      fails instead of returning a fallback result.
    - Use [`MatFunc`](MatFunc.md) just to wrap a fixed square-root call.

## Examples

### Calculate a hypotenuse

Use `Sqrt` in a direct formula where the squared value is known to be non-negative.

```ssl
:PROCEDURE ShowHypotenuse;
    :DECLARE nSideA, nSideB, nHypotenuse;

    nSideA := 3;
    nSideB := 4;
    nHypotenuse := Sqrt((nSideA * nSideA) + (nSideB * nSideB));

    UsrMes("Hypotenuse: " + LimsString(nHypotenuse));
:ENDPROC;

/* Usage;
DoProc("ShowHypotenuse");
```

[`UsrMes`](UsrMes.md) displays:

```
Hypotenuse: 5
```

### Guard against negative input

Validate the input first when a negative value would produce `NaN` that you do not want to propagate.

```ssl
:PROCEDURE SafeSquareRoot;
    :PARAMETERS nValue;
    :DECLARE nRoot;

    :IF nValue < 0;
        UsrMes("Square root requires a non-negative value");
        :RETURN;
    :ENDIF;

    nRoot := Sqrt(nValue);

    UsrMes("Square root: " + LimsString(nRoot));

    :RETURN nRoot;
:ENDPROC;

/* Usage;
DoProc("SafeSquareRoot", {9});
```

`UsrMes` displays:

```text
Square root: 3
```

### Calculate RMS from a series

Combine `Sqrt` with a loop and averaging step in a realistic numeric workflow.

```ssl
:PROCEDURE CalculateRms;
    :PARAMETERS aValues;
    :DECLARE nSumSquares, nMeanSquares, nRms, nValue, nIndex;

    :IF ALen(aValues) = 0;
        :RETURN 0;
    :ENDIF;

    nSumSquares := 0;

    :FOR nIndex := 1 :TO ALen(aValues);
        nValue := aValues[nIndex];
        nSumSquares := nSumSquares + (nValue * nValue);
    :NEXT;

    nMeanSquares := nSumSquares / ALen(aValues);
    nRms := Sqrt(nMeanSquares);

    :RETURN nRms;
:ENDPROC;

/* Usage;
DoProc("CalculateRms", {{1, 2, 3, 4, 5}});
```

## Related

- [`MatFunc`](MatFunc.md)
- [`number`](../types/number.md)
