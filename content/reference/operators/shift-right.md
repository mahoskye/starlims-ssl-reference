---
title: "shift-right"
summary: "Shifts the bits of one integer number to the right by the number of positions specified by another integer number."
id: ssl.operator.shift-right
element_type: operator
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# shift-right

## What it does

Shifts the bits of one integer number to the right by the number of positions specified by another integer number.

The `>>` operator performs a bitwise right shift. Both operands must be numbers, and both must be whole numbers at runtime. SSL shifts the left operand right by the number of positions in the right operand and returns the result as a number. Each position shifted right is equivalent to dividing by 2 with sign preservation for negative values.

## When to use it

- When dividing an integer by a power of two as part of bitwise logic.
- When extracting a bit field from a packed integer value.
- When shifting signed integer values while preserving the sign bit.

## Syntax

```ssl
nResult := nLeft >> nShiftCount;
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [number](../types/number.md) | [number](../types/number.md) | [number](../types/number.md) | Shifts the left integer value right by the number of positions specified by the right integer value. Both operands must be numeric integers. |

## Precedence

- **Precedence:** Shift
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Validate or normalize values so both operands are integer numbers before shifting.
    - Use `>>` for masks, flags, and packed numeric values where bit position matters.
    - Keep the shift count explicit so the intent of the bit layout is easy to read.

!!! failure "Don't"
    - Pass decimal numbers or values from dynamic input without checking them first. Fractional operands raise a runtime error.
    - Use `>>` as a substitute for general arithmetic when bitwise intent is not part of the logic.
    - Assume the operator validates whether a shift count is sensible for your business rule. It only enforces numeric integer operands.

## Errors and edge cases

- If either operand is numeric but not an integer, SSL raises `Invalid operand(s). Expected integers.`

## Examples

### Dividing by a power of two

Shifts 64 right by 2 positions, equivalent to 64 ÷ 2² = 16.

```ssl
:PROCEDURE DivideByPowerOfTwo;
	:DECLARE nValue, nShifted, sMessage;

	nValue := 64;
	nShifted := nValue >> 2;

	sMessage := "64 >> 2 = " + LimsString(nShifted);
	UsrMes(sMessage);

	:RETURN nShifted;
:ENDPROC;

/* Usage;
DoProc("DivideByPowerOfTwo");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
64 >> 2 = 16
```

### Preserving the sign of a negative value

Shifts -64 right by 2 positions. The result is -16 (sign is preserved).

```ssl
:PROCEDURE ShiftNegativeValue;
	:DECLARE nValue, nShifted, sMessage;

	nValue := -64;
	nShifted := nValue >> 2;

	sMessage := LimsString(nValue) + " >> 2 = " + LimsString(nShifted);
	UsrMes(sMessage);

	:RETURN nShifted;
:ENDPROC;

/* Usage;
DoProc("ShiftNegativeValue");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
-64 >> 2 = -16
```

### Extracting a packed flag group

Shifts the desired bits into the low positions, then masks the extracted field. With `nPackedFlags = 112` (binary: 1110000), priority bits 4–6 are shifted right 4 → 7 (0b111), then masked with 7.

```ssl
:PROCEDURE ExtractPriority;
	:PARAMETERS nPackedFlags;
	:DECLARE nPriority, sMessage;

	:IF nPackedFlags != Integer(nPackedFlags);
		UsrMes("Packed flags must be an integer");
		:RETURN 0;
	:ENDIF;

	nPriority := _AND(nPackedFlags >> 4, 7);

	sMessage := "Priority bits: " + LimsString(nPriority);
	UsrMes(sMessage);

	:RETURN nPriority;
:ENDPROC;

/* Usage;
DoProc("ExtractPriority", {112});
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Priority bits: 7
```

## Related elements

- [`shift-left`](shift-left.md)
