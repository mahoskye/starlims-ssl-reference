---
title: "number"
summary: "The number type represents numeric values in SSL. Use it for arithmetic, ordering, exact numeric comparisons, shifts, and integer-only bitwise work."
id: ssl.type.number
element_type: type
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# number

## What it is

The `number` type represents numeric values in SSL. Use it for arithmetic, ordering, exact numeric comparisons, shifts, and integer-only bitwise work.

SSL has a single numeric type for whole numbers and fractional values. Numeric values support arithmetic operators, comparison operators, exponentiation, and shift operators. Integer-only bitwise operations are available through the [`_AND()`](../functions/_AND.md), [`_OR()`](../functions/_OR.md), [`_XOR()`](../functions/_XOR.md), and [`_NOT()`](../functions/_NOT.md) built-ins. Numeric values are scalar values, so they do not support `[]` indexing. For display or string building, convert numbers explicitly with [`LimsString`](../functions/LimsString.md) or `nValue:ToString()`.

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

Numbers have no SSL-defined `:` members. Calls such as `nValue:IsEmpty()`, `nValue:ToJson()` and `nValue:clone()` raise `Run-time error: Invalid method: …`, and properties such as `nValue:value`, `nValue:IsInt` and `nValue:IsInt64` raise `Invalid property: …`. Work with numbers through the operators above and the numeric functions instead:

| Task | Use |
|---|---|
| Convert to text | [`LimsString`](../functions/LimsString.md), or `nValue:ToString()`, a .NET member; see below |
| Format with a pattern | `nValue:ToString(sFormat)`, such as `ToString("N2")`, a .NET member; see below |
| Test for zero | [`Empty`](../functions/Empty.md) |
| Test for a whole number | `nValue == Integer(nValue)`, with [`Integer`](../functions/Integer.md) |
| Round or truncate | [`Round`](../functions/Round.md), [`Integer`](../functions/Integer.md) |
| Serialize to JSON | [`ToJson`](../functions/ToJson.md) |

## Calling .NET numeric methods

Public methods and properties of the value's .NET numeric type can be called on a `number` value with the `:` method-call syntax. For example, `nValue:ToString()` gives `"42"` for `42`, and `nValue:ToString("N2")` gives `"1,234.50"` for `1234.5`. Member names are case-sensitive: `nValue:tostring()` raises `Invalid method: tostring` (see [Member names and case](../../guides/native-members.md#member-names-and-case)).

The .NET type depends on the current value: `nValue:GetType()` reports `System.Int32` for a whole number such as `42` and `System.Double` for `1.5`. As a result, the available member set varies with the value. Members common to both types — for example, `CompareTo(other)`, `Equals(other)`, and `ToString(sFormat)` with a .NET format string — work for any numeric value. Type-specific members only resolve when the value happens to match that type.

Static numeric helpers that live on other .NET types — for example, `System.Math.Sqrt` or `System.Math.Round` — are not reachable this way, because `Math` is not the value's type. Use the SSL function library for those operations.

This passthrough is an interop convenience, not part of the SSL language surface. The members are not declared in SSL and do not appear in editor autocomplete. Prefer SSL-native math functions for portability, and reserve direct .NET calls for behavior the SSL library does not cover. See [Native Members on SSL Values](../../guides/native-members.md) for the members verified on STARLIMS v11 and how to check others.

### Example: formatting a number with grouped digits

Uses the .NET `ToString(sFormat)` member with the `"N0"` standard format string to render a large integer with thousands separators. The separators follow the server's settings.

```ssl
:PROCEDURE FormatRecordCount;
    :DECLARE nRecords, sFormatted;

    nRecords := 1234567;
    sFormatted := nRecords:ToString("N0");

    UsrMes(sFormatted);

    :RETURN sFormatted;
:ENDPROC;

/* Usage;
DoProc("FormatRecordCount");
```

[`UsrMes`](../functions/UsrMes.md) logs:

```text
1,234,567
```

## Indexing

- **Supported:** false
- **Behavior:** Number values do not support `[]` indexing.

## Notes for daily SSL work

!!! success "Do"
    - Use numeric operators directly for arithmetic and numeric comparisons.
    - Use [`==`](../operators/strict-equals.md) when you want exact equality and want your code to read consistently across types.
    - Check that a value is a whole number, such as `nValue == Integer(nValue)`, before doing shifts or bitwise work on values that may contain fractions.
    - Convert explicitly with [`LimsString`](../functions/LimsString.md) or `nValue:ToString()` when building user-facing text.

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
    /* Logs: Area: 50;
    InfoMes("Perimeter: " + LimsString(nPerimeter));
    /* Logs: Perimeter: 30;
    InfoMes("Ratio: " + LimsString(nRatio));
    /* Logs: Ratio: 2;
    InfoMes("Width squared: " + LimsString(nSquared));
    /* Logs: Width squared: 100;

    :IF nArea == 50;
        InfoMes("Area check passed");
    :ENDIF;

    :RETURN nArea;
:ENDPROC;

/* Usage;
DoProc("NumberArithmetic");
```

### Integer-only shifts and masks

Checks with [`Integer`](../functions/Integer.md) that the values are whole numbers before using shifts and bitwise built-ins, starting from `nFlags = 6` (binary 0110) and `nMask = 3` (binary 0011).

```ssl
:PROCEDURE NumberBitwiseOps;
    :DECLARE nFlags, nMask, nShifted, nMasked;
    :DECLARE nCombined, nToggled;

    nFlags := 6;
    nMask := 3;

    :IF nFlags != Integer(nFlags) .OR. nMask != Integer(nMask);
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

    InfoMes("Shifted: " + LimsString(nShifted));
    /* Logs: Shifted: 12;
    InfoMes("Masked: " + LimsString(nMasked));
    /* Logs: Masked: 2;
    InfoMes("Combined: " + LimsString(nCombined));
    /* Logs: Combined: 14;
    InfoMes("Toggled: " + LimsString(nToggled));
    /* Logs: Toggled: 4;

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

    :IF nMean == Integer(nMean);
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

    sReport := "Mean: " + LimsString(nMean) +
               " | Variance: " + LimsString(nVariance) +
               " | ClassBits: " + LimsString(nClassBits);

    InfoMes(sReport);
    :RETURN nMean;
:ENDPROC;

/* Usage;
DoProc("AnalyzeMeasurements", {{10, 20, 30}});
```

## Caveats

- A `:` member call on a number reaches a member of its .NET numeric type (e.g. `nValue:ToString("F2")`). A member that doesn't exist, or doesn't accept the arguments given, raises an error such as `Run-time error: Invalid method: Split`. Check a member before relying on it; see [Native Members](../../guides/native-members.md).

## Related elements

- [`string`](string.md)
- [`boolean`](boolean.md)
- [`date`](date.md)
