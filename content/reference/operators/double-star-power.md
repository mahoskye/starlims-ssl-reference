---
title: "double-star-power"
summary: "Raises one number to the exponent of another number."
id: ssl.operator.double-star-power
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# double-star-power

## What it does

Raises one number to the exponent of another number.

The double-star operator (`**`) performs numeric exponentiation. It raises the left operand to the power of the right operand and returns a number. SSL treats `**` and [`^`](power.md) as the same power operator, so both spellings have the same behavior and precedence. Exponentiation is right-associative, so `2 ** 3 ** 2` is evaluated as `2 ** (3 ** 2)`. Power is implemented for number-to-number operations only. Using a non-numeric operand raises a runtime error.

## When to use it

- When you need exponentiation such as squaring, cubing, or repeated growth calculations.
- When a formula uses reciprocal, negative, or fractional exponents.

## Syntax

```ssl
nResult := nBase ** nExponent;
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [number](../types/number.md) | [number](../types/number.md) | [number](../types/number.md) | Raises the left operand to the power of the right operand. |
| [number](../types/number.md) | non-number | error | Raises a runtime error because the exponent must be numeric. |
| non-number | any | error | Raises a runtime error because power is only defined for numeric bases. |

## Precedence

- **Precedence:** Power
- **Associativity:** right

## Notes for daily SSL work

!!! success "Do"
    - Use `**` only when both operands are numeric values.
    - Use parentheses to make exponent chains and fractional exponents easier to read.

!!! failure "Don't"
    - Assume chained exponentiation runs left to right. `**` is right-associative.
    - Pass strings, arrays, objects, or other non-numeric values to `**`. SSL raises a runtime error instead of coercing them.

## Errors and edge cases

- Fractional exponents are allowed, so `x ** 0.5` can be used for square-root style calculations.

## Examples

### Computing the square of a number

Raises `nBase` to the power of 2. With `nBase = 7`, the result is 49.

```ssl
:PROCEDURE CalculateSquare;
	:DECLARE nBase, nSquared, sResult;

	nBase := 7;
	nSquared := nBase ** 2;

	sResult := "The square of " + LimsString(nBase) + " is " + LimsString(nSquared);
	UsrMes(sResult);

	:RETURN nSquared;
:ENDPROC;

/* Usage;
DoProc("CalculateSquare");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
The square of 7 is 49
```

### Chaining exponentiation with right-associative grouping

Shows how the default right-associative grouping of `2 ** 3 ** 2` gives 512 (= 2 ^ 9), while explicit left grouping `(2 ** 3) ** 2` gives 64 (= 8 ^ 2).

```ssl
:PROCEDURE ChainExponentDemo;
	:DECLARE nBase, nExp1, nExp2, nRightAssoc, nGroupedLeft, sResult;

	nBase := 2;
	nExp1 := 3;
	nExp2 := 2;

	/* Default grouping is 2 ** (3 ** 2);
	nRightAssoc := nBase ** nExp1 ** nExp2;

	/* Parentheses force (2 ** 3) ** 2;
	nGroupedLeft := (nBase ** nExp1) ** nExp2;

	sResult := "Default grouping: " + LimsString(nRightAssoc);
	UsrMes(sResult);

	sResult := "Grouped left with parentheses: " + LimsString(nGroupedLeft);
	UsrMes(sResult);

	:RETURN nRightAssoc;
:ENDPROC;

/* Usage;
DoProc("ChainExponentDemo");
```

`UsrMes` displays:

```text
Default grouping: 512
Grouped left with parentheses: 64
```

### Fractional and negative exponents

Uses a negative exponent (`-1`) for the reciprocal and a fractional exponent (`0.5`) for a square root. With `nBase = 4`, the square root is 2 and the reciprocal is 0.25.

```ssl
:PROCEDURE PowerAdvancedDemo;
	:DECLARE nBase, nReciprocal, nSquareRoot, sOutput;

	nBase := 4;

	nReciprocal := nBase ** -1;
	sOutput := "4 ** -1 = " + LimsString(nReciprocal);
	UsrMes(sOutput);

	nSquareRoot := nBase ** 0.5;
	sOutput := "4 ** 0.5 = " + LimsString(nSquareRoot);
	UsrMes(sOutput);

	:RETURN nSquareRoot;
:ENDPROC;

/* Usage;
DoProc("PowerAdvancedDemo");
```

`UsrMes` displays:

```text
4 ** -1 = 0.25
4 ** 0.5 = 2
```

## Related elements

- [`power`](power.md)
- [`power-assign`](power-assign.md)
