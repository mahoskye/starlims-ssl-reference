---
title: "number"
summary: "The number type represents numeric values in SSL. Use it for arithmetic, ordering, exact numeric comparisons, shifts, and integer-only bitwise work."
id: ssl.type.number
element_type: type
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# number

## What it is

The `number` type represents numeric values in SSL. Use it for arithmetic, ordering, exact numeric comparisons, shifts, and integer-only bitwise work.

SSL has a single numeric type for whole numbers and fractional values. Numeric values support arithmetic operators, comparison operators, exponentiation, and shift operators. Integer-only bitwise operations are available through the [`_AND()`](../functions/_AND.md), [`_OR()`](../functions/_OR.md), [`_XOR()`](../functions/_XOR.md), and [`_NOT()`](../functions/_NOT.md) built-ins. Numeric values are scalar values, so they do not support `[]` indexing. For display or string building, convert numbers explicitly with [`LimsString`](../functions/LimsString.md) or `ToString()`.

## Creating values

Number values are created from numeric literals: integers, decimals, negatives, and scientific notation.

```ssl
nCount := 42;
nRatio := 3.14;
nNeg := -5;
nSmall := 1.2e-3;
```

- **Runtime type:** `NUMERIC`
- **Literal syntax:** `42`, `3.14`, `-5`, `1.2e-3`

## Operators

| Operator | Symbol | Returns | Behavior |
|----------|--------|---------|----------|
| [`plus`](../operators/plus.md) | [`+`](../operators/plus.md) | number | Adds two numbers. |
| [`minus`](../operators/minus.md) | [`-`](../operators/minus.md) | number | Subtracts the right operand from the left operand. |
| [`multiply`](../operators/multiply.md) | [`*`](../operators/multiply.md) | number | Multiplies two numbers. |
| [`divide`](../operators/divide.md) | [`/`](../operators/divide.md) | number | Divides the left operand by the right operand. Division by zero raises an error. |
| [`modulo`](../operators/modulo.md) | [`%`](../operators/modulo.md) | number | Returns the remainder after division. |
| [`power`](../operators/power.md) | [`^`](../operators/power.md) or [`**`](../operators/double-star-power.md) | number | Raises the left operand to the power of the right operand. |
| [`shift-left`](../operators/shift-left.md) | [`<<`](../operators/shift-left.md) | number | Shifts bits left. Both operands must be integer-valued numbers. |
| [`shift-right`](../operators/shift-right.md) | [`>>`](../operators/shift-right.md) | number | Shifts bits right. Both operands must be integer-valued numbers. |
| [`equals`](../operators/equals.md) | [`=`](../operators/equals.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) when two numbers are equal. |
| [`strict-equals`](../operators/strict-equals.md) | [`==`](../operators/strict-equals.md) | [boolean](boolean.md) | Behaves the same as [`=`](../operators/equals.md) for numeric values. |
| [`not-equals`](../operators/not-equals.md) | [`!=`](../operators/not-equals.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) when two numbers differ. |
| [`less-than`](../operators/less-than.md) | [`<`](../operators/less-than.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) when the left operand is smaller. |
| [`greater-than`](../operators/greater-than.md) | [`>`](../operators/greater-than.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) when the left operand is larger. |
| [`less-than-or-equal`](../operators/less-than-or-equal.md) | [`<=`](../operators/less-than-or-equal.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) when the left operand is smaller or equal. |
| [`greater-than-or-equal`](../operators/greater-than-or-equal.md) | [`>=`](../operators/greater-than-or-equal.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) when the left operand is larger or equal. |

### Integer bitwise built-ins

| Built-in | Returns | Behavior |
|----------|---------|----------|
| `_AND(nA, nB)` | number | Bitwise AND of two integer-valued numbers. |
| `_OR(nA, nB)` | number | Bitwise OR of two integer-valued numbers. |
| `_XOR(nA, nB)` | number | Bitwise XOR of two integer-valued numbers. |
| `_NOT(nA)` | number | Bitwise complement of an integer-valued number. |

## Members

| Member | Kind | Returns | Description |
|--------|------|---------|-------------|
| `value` | Property | `number` | Gets or sets the stored numeric value. |
| `IsInt` | Property | [`boolean`](boolean.md) | Returns [`.T.`](../literals/true.md) when the value is a whole number within the 32-bit signed integer range (`-2147483648` through `2147483647`). |
| `IsInt64` | Property | [`boolean`](boolean.md) | Returns [`.T.`](../literals/true.md) when the value is a whole number within the 64-bit signed integer range. |
| `IsEmpty()` | Method | [`boolean`](boolean.md) | Returns [`.T.`](../literals/true.md) when the value is `0`, [`.F.`](../literals/false.md) otherwise. |
| `ToString()` | Method | [`string`](string.md) | Formats the number using the default numeric string representation. |
| `ToString(sDecimal, sGroup)` | Method | [`string`](string.md) | Formats the number using caller-supplied decimal and group separators. |
| [`ToJson()`](../functions/ToJson.md) | Method | [`string`](string.md) | Serializes the number with `.` as the decimal separator and `,` as the group separator. |
| `clone()` | Method | `number` | Creates a copy of the current numeric value. |

## Indexing

- **Supported:** false
- **Behavior:** Number values do not support `[]` indexing.

## Notes for daily SSL work

!!! success "Do"
    - Use numeric operators directly for arithmetic and numeric comparisons.
    - Use [`==`](../operators/strict-equals.md) when you want exact equality and want your code to read consistently across types.
    - Check `IsInt` or `IsInt64` before doing shifts or bitwise work on values that may contain fractions.
    - Convert explicitly with [`LimsString`](../functions/LimsString.md) or `ToString()` when building user-facing text.

!!! failure "Don't"
    - Write bitwise logic with [`&`](../operators/and.md), [`|`](../operators/or.md), or [`^`](../operators/power.md) as bitwise operators. In SSL, bitwise work uses [`_AND()`](../functions/_AND.md), [`_OR()`](../functions/_OR.md), [`_XOR()`](../functions/_XOR.md), [`_NOT()`](../functions/_NOT.md), and the shift operators [`<<`](../operators/shift-left.md) and [`>>`](../operators/shift-right.md).
    - Concatenate strings and numbers directly with [`+`](../operators/plus.md). Convert the number first.
    - Use fractional values with shifts or bitwise built-ins. They require integer-valued operands.
    - Treat numbers like arrays or strings. Numeric values are scalar and are not indexable.

## Examples

### Basic arithmetic and comparison

Computes area, perimeter, ratio, and squared width for a 10 x 5 rectangle, then verifies the area equals 50.

```ssl
:PROCEDURE NumberArithmetic;
    :DECLARE nWidth, nHeight, nArea, nPerimeter;
    :DECLARE nRatio, nSquared;

    nWidth := 10;
    nHeight := 5;

    nArea := nWidth * nHeight;
    nPerimeter := (2 * nWidth) + (2 * nHeight);
    nRatio := nWidth / nHeight;
    nSquared := nWidth ^ 2;

    InfoMes("Area: " + LimsString(nArea));
    /* Displays: Area: 50;
    InfoMes("Perimeter: " + LimsString(nPerimeter));
    /* Displays: Perimeter: 30;
    InfoMes("Ratio: " + LimsString(nRatio));
    /* Displays: Ratio: 2;
    InfoMes("Width squared: " + LimsString(nSquared));
    /* Displays: Width squared: 100;

    :IF nArea == 50;
        InfoMes("Area check passed");
    :ENDIF;

    :RETURN nArea;
:ENDPROC;

/* Usage;
DoProc("NumberArithmetic");
```

### Integer-only shifts, masks, and formatting

Validates that the values are integer-valued before using shifts and bitwise built-ins, starting from `nFlags = 6` (binary 0110) and `nMask = 3` (binary 0011).

```ssl
:PROCEDURE NumberBitwiseOps;
    :DECLARE nFlags, nMask, nShifted, nMasked;
    :DECLARE nCombined, nToggled;

    nFlags := 6;
    nMask := 3;

    :IF !nFlags:IsInt .OR. !nMask:IsInt;
        ErrorMes("Bitwise operations require integer values");
        :RETURN .F.;
    :ENDIF;

    nShifted := nFlags << 1;
    /* 6 << 1 = 12;
    nMasked := _AND(nFlags, nMask);
    /* 6 AND 3 = 2;
    nCombined := _OR(nFlags, 8);
    /* 6 OR 8 = 14;
    nToggled := _XOR(nFlags, 2);
    /* 6 XOR 2 = 4;

    InfoMes("Shifted: " + nShifted:ToString(".", ","));
    /* Displays: Shifted: 12;
    InfoMes("Masked: " + nMasked:ToString(".", ","));
    /* Displays: Masked: 2;
    InfoMes("Combined: " + nCombined:ToString(".", ","));
    /* Displays: Combined: 14;
    InfoMes("Toggled: " + nToggled:ToString(".", ","));
    /* Displays: Toggled: 4;

    :RETURN nCombined;
:ENDPROC;

/* Usage;
DoProc("NumberBitwiseOps");
```

### Statistical aggregation with bitwise classification

Computes mean and variance over an array of measurements, then uses bitwise flags to classify the result. For `{10, 20, 30}`: mean = 20, variance ~= 66.67, class bits = 2 (high variance set).

```ssl
:PROCEDURE AnalyzeMeasurements;
    :PARAMETERS aMeasurements;
    :DECLARE nSum, nSumSq, nCount, nMean, nVariance;
    :DECLARE nClassBits, nIndex, sReport;

    nCount := ALen(aMeasurements);
    :IF nCount == 0;
        :RETURN "No data";
    :ENDIF;

    nSum   := 0;
    nSumSq := 0;
    :FOR nIndex := 1 :TO nCount;
        nSum   := nSum   + aMeasurements[nIndex];
        nSumSq := nSumSq + (aMeasurements[nIndex] ^ 2);
    :NEXT;

    nMean     := nSum / nCount;
    nVariance := (nSumSq / nCount) - (nMean ^ 2);

    :IF nMean:IsInt;
        nClassBits := 0;
        :IF nMean > 100;
            nClassBits := _OR(nClassBits, 1);
        :ENDIF;
        :IF nVariance > 25;
            nClassBits := _OR(nClassBits, 2);
        :ENDIF;
    :ELSE;
        nClassBits := -1;
    :ENDIF;

    sReport := "Mean: " + nMean:ToString(".", ",") +
               " | Variance: " + nVariance:ToString(".", ",") +
               " | ClassBits: " + LimsString(nClassBits);

    InfoMes(sReport);
    :RETURN nMean;
:ENDPROC;

/* Usage;
DoProc("AnalyzeMeasurements", {{10, 20, 30}});
```

## Related elements

- [`string`](string.md)
- [`boolean`](boolean.md)
- [`date`](date.md)
