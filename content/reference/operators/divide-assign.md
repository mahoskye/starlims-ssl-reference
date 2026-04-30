---
title: "divide-assign"
summary: "Divides a numeric value by another numeric value and stores the quotient back in the left operand."
id: ssl.operator.divide-assign
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# divide-assign

## What it does

Divides a numeric value by another numeric value and stores the quotient back in the left operand.

The `/=` operator is the compound-assignment form of [`divide`](divide.md). It evaluates the left operand, divides it by the right operand, and writes the result back to the left side. In practice, `nValue /= nDivisor;` is the concise form of `nValue := nValue / nDivisor;`.

Both operands must be numeric at runtime. If the right operand evaluates to `0`, the operation fails with a runtime division-by-zero error. If either side does not hold a numeric value, the operation also fails at runtime.

## When to use it

- When you want to update a numeric variable in place after dividing it.
- When the compound-assignment form is clearer than repeating the same variable on both sides of [`:=`](assignment.md).

## Syntax

```ssl
target /= divisor;
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [number](../types/number.md) | [number](../types/number.md) | [number](../types/number.md) | Divides the left operand by the right operand and stores the quotient back in the left operand. |

## Precedence

- **Precedence:** Assignment
- **Associativity:** right

## Notes for daily SSL work

!!! success "Do"
    - Check that the divisor is numeric and not `0` before using `/=` when the input is not trusted.
    - Use `/=` when you are updating the same numeric variable in place.

!!! failure "Don't"
    - Assume SSL will coerce strings, arrays, objects, dates, or [`NIL`](../literals/nil.md) into numbers for `/=`.
    - Use `/=` when the divisor may be `0` or may come from mixed-type input without validation.

## Examples

### Dividing a total in place

Computes an average by dividing `nTotal` by the sample count using `/=`. With four samples totaling 120, the result is 30.

```ssl
:PROCEDURE CalculateAverage;
	:DECLARE nTotal, nCount;

	nTotal := 120;
	nCount := 4;

	nTotal /= nCount;

	UsrMes("Average: " + LimsString(nTotal));

	:RETURN nTotal;
:ENDPROC;

/* Usage;
DoProc("CalculateAverage");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Average: 30
```

### Validating the divisor before dividing

Checks that the divisor is numeric and non-zero before applying `/=`. With `vDivisor = 60` the division succeeds; with `vDivisor = "hours"` it is skipped.

```ssl
:PROCEDURE SafeDivideAssign;
	:DECLARE nDuration, vDivisor, sType, sMessage;

	nDuration := 360;
	vDivisor := 60;

	sType := LimsTypeEx(vDivisor);

	:IF sType == "NUMERIC" .AND. vDivisor != 0;
		nDuration /= vDivisor;
		sMessage := "Minutes: " + LimsString(nDuration);
		UsrMes(sMessage);
		/* Displays converted duration in minutes;
	:ELSE;
		sMessage := "Cannot divide: divisor is " + sType;
		UsrMes(sMessage);
		/* Displays failure details for an invalid divisor;
	:ENDIF;

	vDivisor := "hours";
	sType := LimsTypeEx(vDivisor);

	:IF sType == "NUMERIC" .AND. vDivisor != 0;
		nDuration /= vDivisor;
	:ELSE;
		sMessage := "Skipped: divisor is " + sType;
		UsrMes(sMessage);
		/* Displays skip details for a non-numeric divisor;
	:ENDIF;

	:RETURN nDuration;
:ENDPROC;

/* Usage;
DoProc("SafeDivideAssign");
```

## Related elements

- [`divide`](divide.md)
