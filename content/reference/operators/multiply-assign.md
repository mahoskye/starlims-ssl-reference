---
title: "multiply-assign"
summary: "Multiplies a numeric value by another numeric value and stores the product back in the left operand."
id: ssl.operator.multiply-assign
element_type: operator
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# multiply-assign

## What it does

Multiplies a numeric value by another numeric value and stores the product back in the left operand.

The `*=` operator is the compound-assignment form of [`multiply`](multiply.md). It reads the current left-side value, multiplies it by the right-side value, and writes the product back to the same target.

`*=` follows the same runtime type rules as [`*`](multiply.md): numeric multiplication is the only supported combination. SSL does not perform implicit type coercion for this operator. If the left operand is not numeric, the operation fails because [`*`](multiply.md) is not implemented for that type. If the left operand is numeric but the right operand is not, it fails with an invalid-operand runtime error.

## When to use it

- When scaling a numeric variable in place.
- When updating running totals, factors, or measurements without repeating the target on both sides of [`:=`](assignment.md).
- When replacing `nValue := nValue * nFactor;` with a shorter equivalent form.

## Syntax

```ssl
target *= value;
```

`target` must be an assignable left-hand side: a variable, property, or array element.

## Type behavior

| Left | Right | Result | Behavior |
| --- | --- | --- | --- |
| [number](../types/number.md) | [number](../types/number.md) | [number](../types/number.md) | Multiplies the left value by the right value and stores the product back in the left operand. |

## Precedence

- **Precedence:** Assignment
- **Associativity:** right

## Notes for daily SSL work

!!! success "Do"
    - Use `*=` when updating the same numeric target in place.
    - Validate uncertain inputs before applying `*=` if either side might not be numeric.
    - Use `*=` inside loops when repeatedly scaling a value or array element.

!!! failure "Don't"
    - `*=` only accepts number operands; using it with strings, dates, arrays, objects, or booleans raises a runtime error.
    - Implicit type conversion from text, [`NIL`](../literals/nil.md), or mixed-type values is not performed.
    - The left side must be an assignable target. Expressions such as `(nValue + 1) *= 2;` are invalid.

## Errors and edge cases

- The left side must be assignable. An expression on the left side causes a compile-time error.

## Examples

### Doubling a counter in a loop

Repeatedly doubles `nCounter` by multiplying it in place. The value before each doubling is appended to `sOutput`.

```ssl
:PROCEDURE DoubleLoopCounter;
    :DECLARE nCounter, nIndex, sOutput;

    nCounter := 1;
    sOutput := "Counter values: ";

    :FOR nIndex := 1 :TO 6;
        sOutput := sOutput + LimsString(nCounter) + " ";
        nCounter *= 2;
    :NEXT;

    UsrMes(sOutput);

    :RETURN nCounter;
:ENDPROC;

/* Usage;
DoProc("DoubleLoopCounter");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Counter values: 1 2 4 8 16 32 
```

### Scaling each reading in an array

Applies a calibration factor to each element of `aReadings` in place, then accumulates the scaled values into `nSum`.

```ssl
:PROCEDURE ScaleMeasurements;
    :DECLARE aReadings, nCalibration, nSum, nCount, nIndex;

    aReadings := {1.23, 2.34, 3.45, 4.56};
    nCalibration := 1.05;
    nCount := ALen(aReadings);
    nSum := 0;

    :FOR nIndex := 1 :TO nCount;
        aReadings[nIndex] *= nCalibration;
        nSum += aReadings[nIndex];
    :NEXT;

    UsrMes("Scaled sum: " + LimsString(nSum));

    :RETURN nSum;
:ENDPROC;

/* Usage;
DoProc("ScaleMeasurements");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Scaled sum: 12.159
```

## Related elements

- [`multiply`](multiply.md)
- [`assignment`](assignment.md)
