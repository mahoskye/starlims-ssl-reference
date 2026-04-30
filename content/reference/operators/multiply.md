---
title: "multiply"
summary: "Multiplies one number by another number and returns the product."
id: ssl.operator.multiply
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# multiply

## What it does

Multiplies one number by another number and returns the product.

The `*` operator performs numeric multiplication in SSL. It is only supported for `number * number` at runtime. SSL does not coerce strings, dates, arrays, objects, booleans, or [`NIL`](../literals/nil.md) into numbers for this operator.

`*` uses multiplicative precedence. It binds more tightly than [`plus`](plus.md) and [`minus`](minus.md), and less tightly than the power operators [`power`](power.md) and [`double-star-power`](double-star-power.md).

## When to use it

- When you need the product of two numeric values.
- When scaling a measurement, quantity, rate, or amount by a numeric factor.
- When you need multiplication inside a larger arithmetic expression and want the normal multiplicative precedence rules to apply.

## Syntax

```ssl
nProduct := nLeft * nRight;
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [number](../types/number.md) | [number](../types/number.md) | [number](../types/number.md) | Returns the product of the two numeric operands. |
| [number](../types/number.md) | non-number | error | Raises a runtime invalid-operand error for `*`. |
| non-number | any | error | Raises a runtime operator error because multiplication is not supported for the left operand type. |

## Precedence

- **Precedence:** Multiplicative
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Ensure both operands are numeric before using `*`.
    - Use parentheses when multiplication appears in a longer expression and readability matters.
    - Convert non-numeric values explicitly before multiplying when the source data may vary.

!!! failure "Don't"
    - `*` only accepts number operands; using it with strings, dates, arrays, objects, booleans, or [`NIL`](../literals/nil.md) raises a runtime error.
    - Assume SSL will coerce text such as `"5"` into a number for `*`.
    - Rely on readers to infer precedence in dense arithmetic. Add parentheses when the grouping is important.

## Examples

### Calculating a rectangle area

Multiplies `nLength` by `nWidth` to get the area. 12.5 × 8.3 = 103.75.

```ssl
:PROCEDURE CalcRectangleArea;
    :DECLARE nLength, nWidth, nArea;

    nLength := 12.5;
    nWidth := 8.3;
    nArea := nLength * nWidth;

    UsrMes("Rectangle area: " + LimsString(nArea));

    :RETURN nArea;
:ENDPROC;

/* Usage;
DoProc("CalcRectangleArea");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Rectangle area: 103.75
```

### Computing a discounted line total

Uses multiplication twice: once for the subtotal and once for the discount. The parentheses on `nSubtotal - nDiscount` are not needed here (subtraction is lower precedence) but make the intent explicit.

```ssl
:PROCEDURE CalcLineTotal;
    :DECLARE nUnitPrice, nQuantity, nDiscountPct, nSubtotal, nDiscount, nTotal;

    nUnitPrice := 14.75;
    nQuantity := 6;
    nDiscountPct := 0.1;

    nSubtotal := nUnitPrice * nQuantity;
    nDiscount := nSubtotal * nDiscountPct;
    nTotal := nSubtotal - nDiscount;

    UsrMes("Line total: " + LimsString(nTotal));

    :RETURN nTotal;
:ENDPROC;

/* Usage;
DoProc("CalcLineTotal");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Line total: 79.65
```

## Related elements

- [`multiply-assign`](multiply-assign.md)
- [`divide`](divide.md)
- [`power`](power.md)
