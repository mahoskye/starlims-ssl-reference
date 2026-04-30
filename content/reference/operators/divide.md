---
title: "divide"
summary: "Divides the left number by the right number and returns the result as a number."
id: ssl.operator.divide
element_type: operator
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# divide

## What it does

Divides the left number by the right number and returns the result as a number.

The `/` operator returns the numeric quotient of the left operand divided by the right operand. SSL only supports division for numeric values. If the right operand is `0`, execution fails with a runtime division-by-zero error. If either operand is not numeric at runtime, the operation also fails with a runtime error.

SSL does not coerce strings, dates, arrays, objects, or [`NIL`](../literals/nil.md) into numbers for division. `/` uses multiplicative precedence and evaluates left to right when it appears with other multiplicative operators in the same expression.

## When to use it

- When you need to calculate a numeric result by dividing one value by another, such as finding averages, rates, or normalized values.
- When both operands are known to be numbers and division by zero is properly guarded.

## Syntax

```ssl
nQuotient := nLeft / nRight;
```

## Type behavior

| Left | Right | Result | Behavior |
| --- | --- | --- | --- |
| [number](../types/number.md) | [number](../types/number.md) | [number](../types/number.md) | Returns the quotient of the left operand divided by the right operand. |
| [number](../types/number.md) | non-number | error | Raises a runtime operand error for `/`. |
| non-number | any | error | Raises a runtime operator error because division is not supported for the left operand type. |

## Precedence

- **Precedence:** Multiplicative
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Always verify that the right operand is not zero before dividing.
    - Ensure both operands are numeric before applying division.
    - Use `/` when you need a quotient rather than a remainder or an in-place update.

!!! failure "Don't"
    - Assume SSL will coerce strings, dates, arrays, objects, or [`NIL`](../literals/nil.md) into numbers for division.
    - Divide when the right operand may be `0`. A zero divisor raises a runtime error and stops the expression.
    - Use `/` when you need the remainder. Use [`modulo`](modulo.md) for that case.

## Examples

### Computing a completion rate

Divides `nCompleted` by `nTotal` to get the proportion. With 18 out of 24, the rate is 0.75.

```ssl
:PROCEDURE ShowCompletionRate;
	:DECLARE nCompleted, nTotal, nRate;

	nCompleted := 18;
	nTotal := 24;

	nRate := nCompleted / nTotal;

	UsrMes("Completion rate: " + LimsString(nRate));

	:RETURN nRate;
:ENDPROC;

/* Usage;
DoProc("ShowCompletionRate");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Completion rate: 0.75
```

### Guarding a divisor before division

Validates the divisor type and checks it is non-zero before dividing. With `nSampleCount = 6`, the check passes and the average is computed.

```ssl
:PROCEDURE SafeAverage;
	:DECLARE nTotalMass, nSampleCount, sType, sMessage, vAverageMass;

	nTotalMass := 42;
	nSampleCount := 6;
	sType := LimsTypeEx(nSampleCount);

	:IF sType == "NUMERIC" .AND. nSampleCount != 0;
		vAverageMass := nTotalMass / nSampleCount;
		sMessage := "Average mass: " + LimsString(vAverageMass);
	:ELSE;
		vAverageMass := "";
		sMessage := "Cannot divide: sample count is " + sType;
	:ENDIF;

	UsrMes(sMessage);

	:RETURN vAverageMass;
:ENDPROC;

/* Usage;
DoProc("SafeAverage");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Average mass: 7
```

## Related elements

- [`divide-assign`](divide-assign.md)
- [`multiply`](multiply.md)
- [`modulo`](modulo.md)
