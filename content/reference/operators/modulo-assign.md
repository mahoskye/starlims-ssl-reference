---
title: "modulo-assign"
summary: "Updates a numeric variable, property, or array element in place by applying % and storing the remainder back into the left side."
id: ssl.operator.modulo-assign
element_type: operator
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# modulo-assign

## What it does

Updates a numeric variable, property, or array element in place by applying [`%`](modulo.md) and storing the remainder back into the left side.

The `%=` operator is a compound assignment operator. It performs the same numeric remainder operation as [`modulo`](modulo.md), then writes the updated value back to the left operand. `x %= y` reads `x`, computes `x % y`, stores the result in `x`, and the expression evaluates to the updated left-side value.

Only number `%=` number is supported. A non-numeric left side raises a runtime error because [`%`](modulo.md) is not implemented for that type. A non-numeric right operand raises a runtime error as an invalid operand. A zero divisor does not raise but produces `NaN`, which is then assigned back into the left side.

## When to use it

- When reducing a numeric value in place without repeating the left operand.
- When keeping remainder-based state updates concise inside loops.
- When implementing wraparound logic where a remainder update is the intended state change.

## Syntax

```ssl
target %= divisor;
```

`target` must be an assignable left-hand side: a variable, property, or array element.

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [number](../types/number.md) | [number](../types/number.md) | [number](../types/number.md) | Computes `left % right`, stores the remainder back into the left operand, and returns the updated value. |

## Precedence

- **Precedence:** Assignment
- **Associativity:** right

## Notes for daily SSL work

!!! success "Do"
    - Use `%=` when you want the variable itself to become its remainder.
    - Guard or validate the divisor before using `%=` when `NaN` is not acceptable.
    - Normalize negative results explicitly when using `%=` for wraparound logic.

!!! failure "Don't"
    - `%=` only accepts number operands; using it with strings, booleans, arrays, or objects raises a runtime error.
    - `%=` does not guarantee a positive result. Negative left operands produce negative remainders.
    - Applying `%=` directly to a 1-based array index can produce 0, which is an invalid index. Normalize the result before using it in array access.

## Errors and edge cases

- The sign of the remainder follows the left operand. For example, `-7 %= 3` leaves the value as `-1`.

## Examples

### Reducing a value in place

Replaces `nValue` with the remainder of dividing it by 7. `23 % 7 = 2`.

```ssl
:PROCEDURE ReduceToRemainder;
	:DECLARE nValue, nOriginal, sMessage;

	nValue := 23;
	nOriginal := nValue;

	nValue %= 7;

	sMessage := "Remainder of " + LimsString(nOriginal) + " divided by 7 is " + LimsString(
		nValue);
	UsrMes(sMessage);

	:RETURN nValue;
:ENDPROC;

/* Usage;
DoProc("ReduceToRemainder");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Remainder of 23 divided by 7 is 2
```

### Wrapping a circular slot counter

Uses a zero-based slot offset incremented with `%=` to wrap around a 5-slot buffer. After 8 writes, slots 1-3 hold the most recent writes (6-8) and slots 4-5 hold the earlier ones (4-5).

```ssl
:PROCEDURE ProcessCircularSlots;
	:DECLARE nBufferSize, nSlotOffset, nSlotIndex, nWriteCount, nIndex;
	:DECLARE aBuffer;

	nBufferSize := 5;
	nSlotOffset := 0;
	nWriteCount := 0;
	aBuffer := {"", "", "", "", ""};

	:FOR nIndex := 1 :TO 8;
		nWriteCount += 1;

		nSlotIndex := nSlotOffset + 1;
		aBuffer[nSlotIndex] := "Write " + LimsString(nWriteCount);

		nSlotOffset += 1;
		nSlotOffset %= nBufferSize;
	:NEXT;

	:FOR nIndex := 1 :TO ALen(aBuffer);
		UsrMes("Slot " + LimsString(nIndex) + ": " + aBuffer[nIndex]);
	:NEXT;

	:RETURN aBuffer;
:ENDPROC;

/* Usage;
DoProc("ProcessCircularSlots");
```

[`UsrMes`](../functions/UsrMes.md) displays (one line per slot):

```text
Slot 1: Write 6
Slot 2: Write 7
Slot 3: Write 8
Slot 4: Write 4
Slot 5: Write 5
```

### Normalizing a negative wraparound result

Shows that `%=` with a negative left operand produces a negative remainder. After `nWrappedOffset %= 5` on `-7`, the value is `-2`; adding `nWindowSize` normalizes it to `3`.

```ssl
:PROCEDURE NormalizeNegativeOffset;
	:DECLARE nOffset, nWindowSize, nWrappedOffset;

	nOffset := -7;
	nWindowSize := 5;
	nWrappedOffset := nOffset;

	nWrappedOffset %= nWindowSize;

	:IF nWrappedOffset < 0;
		nWrappedOffset += nWindowSize;
	:ENDIF;

	UsrMes("Normalized offset: " + LimsString(nWrappedOffset));

	:RETURN nWrappedOffset;
:ENDPROC;

/* Usage;
DoProc("NormalizeNegativeOffset");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Normalized offset: 3
```

## Related elements

- [`assignment`](assignment.md)
- [`modulo`](modulo.md)
