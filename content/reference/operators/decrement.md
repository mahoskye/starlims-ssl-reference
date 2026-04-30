---
title: "decrement"
summary: "Decreases a number variable by one, trims trailing spaces in strings, or subtracts days from a date depending on operand type."
id: ssl.operator.decrement
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# decrement

## What it does

Decreases a number variable by one, trims trailing spaces in strings, or subtracts days from a date depending on operand type.

The `--` operator decreases the value of variables in place, supporting numbers, strings, and dates with type-specific behavior.

For number variables, prefix (`--x`) subtracts one then returns the new value, while postfix (`x--`) returns the original value before decrementing. On strings, `--` trims trailing spaces from the value. With dates, `--` subtracts one day from the date.

The operator must be applied directly to a variable. Applying it to a constant, expression result, or a value of an unsupported type raises an error.

`--` differs from [`++`](increment.md), which increases values, and from [`subtract-assign`](subtract-assign.md) ([`-=`](subtract-assign.md)), which supports multi-step or non-unit decrements.

## When to use it

- When you need to decrease a number variable by exactly one.
- When you need to subtract one day from a date variable.
- When the variable's updated value or the original value after decrement is needed in a calculation (choose prefix/postfix accordingly).

## Syntax

Prefix form — decrements before returning:

```ssl
--variable
```

Postfix form — returns the original value, then decrements:

```ssl
variable--
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [number](../types/number.md) | n/a | [number](../types/number.md) | Subtracts 1 from the number value |
| [string](../types/string.md) | n/a | [string](../types/string.md) | Trims trailing spaces from the string |
| [date](../types/date.md) | n/a | [date](../types/date.md) | Subtracts one day from the date |

## Precedence

- **Precedence:** Unary
- **Associativity:** none

## Notes for daily SSL work

!!! success "Do"
    - Use prefix form (`--variable`) when the decremented value is needed immediately in further computations.
    - Decrement dates when you need to step backward by one day.
    - Apply `--` only to supported value types (numbers, strings, dates).

!!! failure "Don't"
    - Assume postfix (`variable--`) also returns the updated value. The postfix form returns the original before decrementing.
    - Use `--` on arrays, objects, booleans, or expression results. Unsupported usage raises errors.
    - Use `--` when a non-unit decrement is needed. Use [`subtract-assign`](subtract-assign.md) ([`-=`](subtract-assign.md)) instead.

## Examples

### Counting down with decrement

Decrements `nCount` by one on each iteration using postfix `--`. The loop runs five times and displays each value before decrement takes effect.

```ssl
:PROCEDURE Countdown;
	:DECLARE nCount, sMessage;

	nCount := 5;

	:WHILE nCount > 0;
		sMessage := "Count: " + LimsString(nCount);
		UsrMes(sMessage);
		nCount--;
	:ENDWHILE;

	sMessage := "Done. Final count: " + LimsString(nCount);
	UsrMes(sMessage);

	:RETURN nCount;
:ENDPROC;

/* Usage;
DoProc("Countdown");
```

[`UsrMes`](../functions/UsrMes.md) displays (one line per iteration, then final):

```
Count: 5
Count: 4
Count: 3
Count: 2
Count: 1
Done. Final count: 0
```

### Prefix vs postfix return values

Shows the difference between prefix and postfix `--`. Prefix decrement returns the updated value; postfix decrement returns the original and then decrements. Both source variables start at `5`, but the captured return values differ.

```ssl
:PROCEDURE DemoDecrementAssignment;
	:DECLARE nPrefix, nPostfix, nPrefixResult, nPostfixResult, sResult;

	nPrefix := 5;
	nPostfix := 5;

	/* Prefix: decrements first, then returns the new value;
	nPrefixResult := --nPrefix;

	/* Postfix: returns the original value, then decrements the variable;
	nPostfixResult := nPostfix--;

	sResult := "Prefix result: " + LimsString(nPrefixResult) + ", Postfix result: " + LimsString(
		nPostfixResult);
	UsrMes(sResult);

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("DemoDecrementAssignment");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Prefix result: 4, Postfix result: 5
```

## Related elements

- [`increment`](increment.md)
- [`subtract-assign`](subtract-assign.md)
