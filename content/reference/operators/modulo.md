---
title: "modulo"
summary: "Calculates the remainder after dividing one number by another."
id: ssl.operator.modulo
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# modulo

## What it does

Calculates the remainder after dividing one number by another.

The `%` operator returns the numeric remainder of dividing the left operand by the right operand. SSL only supports modulo for numeric values. The result keeps the sign of the left operand, so negative dividends produce negative remainders.

SSL does not coerce strings, dates, arrays, objects, or [`NIL`](../literals/nil.md) into numbers for `%`. When the left operand is numeric but the right operand is not, SSL raises a runtime operand error. When the left operand does not support `%` at all, SSL raises a runtime operator error. Unlike [`divide`](divide.md), a zero divisor does not raise a divide-by-zero exception; the result is `NaN`.

## When to use it

- When you need the remainder after dividing one numeric value by another.
- When implementing wraparound or bucket logic and you have accounted for negative dividends explicitly.
- When you need remainder behavior without updating the left operand in place.

## Syntax

```ssl
nRemainder := nLeft % nRight;
```

## Type behavior

| Left | Right | Result | Behavior |
| --- | --- | --- | --- |
| [number](../types/number.md) | [number](../types/number.md) | [number](../types/number.md) | Returns the remainder of dividing the left operand by the right operand. |
| [number](../types/number.md) | non-number | error | Raises a runtime operand error for `%`. |
| non-number | any | error | Raises a runtime operator error because `%` is not supported for the left operand type. |

## Precedence

- **Precedence:** Multiplicative
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Guard the divisor before using `%` when `NaN` would be an invalid result.
    - Normalize negative remainders explicitly when using `%` for wraparound logic.
    - Use parentheses for clarity in compound arithmetic expressions.

!!! failure "Don't"
    - `%` does not guarantee a non-negative result. The sign follows the sign of the left operand.
    - `% 0` does not raise a divide-by-zero error; it yields `NaN`. Guard that case explicitly.
    - `%` only accepts numeric operands; using it with strings, booleans, arrays, objects, or [`NIL`](../literals/nil.md) raises a runtime error.

## Errors and edge cases

- Tests such as `x % 2 == 1` are not reliable for negative odd numbers because `-3 % 2` evaluates to `-1`.

## Examples

### Basic remainder calculation

Computes 10 % 3. The remainder is 1 because 10 = 3 x 3 + 1.

```ssl
:PROCEDURE CalculateRemainder;
	:DECLARE nDividend, nDivisor, nRemainder, sMessage;

	nDividend := 10;
	nDivisor := 3;

	nRemainder := nDividend % nDivisor;
	sMessage := "Remainder of " + LimsString(nDividend) + " divided by " + LimsString(
		nDivisor) + " is " + LimsString(nRemainder);
	UsrMes(sMessage);

	:RETURN nRemainder;
:ENDPROC;

/* Usage;
DoProc("CalculateRemainder");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Remainder of 10 divided by 3 is 1
```

### Normalizing a negative offset for wraparound

Wraps offset -1 into a 5-slot window. `((-1 % 5) + 5) % 5` normalizes the negative remainder to 4, giving slot index 5.

```ssl
:PROCEDURE NormalizeWrapOffset;
	:DECLARE nOffset, nWindowSize, nNormalizedOffset, nSlotIndex;

	nOffset := -1;
	nWindowSize := 5;

	nNormalizedOffset := ((nOffset % nWindowSize) + nWindowSize) % nWindowSize;
	nSlotIndex := nNormalizedOffset + 1;

	UsrMes("Wrapped slot index: " + LimsString(nSlotIndex));

	:RETURN nSlotIndex;
:ENDPROC;

/* Usage;
DoProc("NormalizeWrapOffset");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Wrapped slot index: 5
```

### Validating inputs before modulo

Guards against a non-numeric divisor and a zero divisor before applying `%`. With `vDivisor = 4` and `nDividend = 17`, the result is 1.

```ssl
:PROCEDURE SafeModulo;
	:DECLARE nDividend, vDivisor, sDivisorType, vResult, sMessage;

	nDividend := 17;
	vDivisor := 4;
	sDivisorType := LimsTypeEx(vDivisor);

	:IF sDivisorType == "NUMERIC";
		:IF vDivisor == 0;
			vResult := "";
			sMessage := "Modulo by zero returns NaN, so this input is rejected";
		:ELSE;
			vResult := nDividend % vDivisor;
			sMessage := "Remainder: " + LimsString(vResult);
		:ENDIF;
	:ELSE;
		vResult := "";
		sMessage := "Modulo requires a numeric divisor";
	:ENDIF;

	UsrMes(sMessage);

	:RETURN vResult;
:ENDPROC;

/* Usage;
DoProc("SafeModulo");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Remainder: 1
```

## Related elements

- [`modulo-assign`](modulo-assign.md)
- [`divide`](divide.md)
