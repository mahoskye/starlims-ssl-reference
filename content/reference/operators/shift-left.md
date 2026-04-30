---
title: "shift-left"
summary: "Shifts the bits of one integer number to the left by the number of positions specified by another integer number."
id: ssl.operator.shift-left
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# shift-left

## What it does

Shifts the bits of one integer number to the left by the number of positions specified by another integer number.

The `<<` operator performs a bitwise left shift. Both operands must be numbers, and both must be whole numbers at runtime. SSL shifts the left operand left by the number of positions in the right operand and returns the result as a number. Each position shifted left is equivalent to multiplying by 2.

## When to use it

- When multiplying an integer by a power of two as part of bitwise logic.
- When building or applying bitmasks.
- When packing byte or flag values into a larger integer.

## Syntax

```ssl
nResult := nLeft << nShiftCount;
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [number](../types/number.md) | [number](../types/number.md) | [number](../types/number.md) | Shifts the left integer value left by the number of positions specified by the right integer value. Both operands must be numeric integers. |

## Precedence

- **Precedence:** Shift
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Validate or normalize values so both operands are integer numbers before shifting.
    - Use `<<` for masks, flags, and encoded numeric values where bit position matters.
    - Keep the shift count explicit so the intent of the bit layout is easy to read.

!!! failure "Don't"
    - Pass decimal numbers or values from dynamic input without checking them first. Fractional operands raise a runtime error.
    - Use `<<` as a substitute for general arithmetic when bitwise intent is not part of the logic.
    - Assume the operator validates whether a shift count is sensible for your business rule. It only enforces numeric integer operands.

## Errors and edge cases

- If either operand is numeric but not an integer, SSL raises `Invalid operand(s). Expected integers.`

## Examples

### Multiplying by a power of two

Shifts 5 left by 3 positions, equivalent to 5 × 2³ = 40.

```ssl
:PROCEDURE MultiplyByPowerOfTwo;
	:DECLARE nValue, nShifted, sMessage;

	nValue := 5;
	nShifted := nValue << 3;

	sMessage := "5 << 3 = " + LimsString(nShifted);
	UsrMes(sMessage);

	:RETURN nShifted;
:ENDPROC;

/* Usage;
DoProc("MultiplyByPowerOfTwo");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
5 << 3 = 40
```

### Building a flag mask for a specific bit position

Creates a mask for bit position 4 (`1 << 3 = 8`), then sets that bit in `nFlags` using [`_OR`](../functions/_OR.md). Starting from 5 (binary: 0101), the result is 13 (binary: 1101).

```ssl
:PROCEDURE SetPermissionFlag;
	:DECLARE nFlags, nBitPos, nMask, nUpdated, sMessage;

	nFlags := 5;
	nBitPos := 4;
	nMask := 1 << (nBitPos - 1);
	nUpdated := _OR(nFlags, nMask);

	sMessage := "Flags=" + LimsString(nFlags) + ", Mask=" 
				+ LimsString(nMask) + ", Updated="
				+ LimsString(nUpdated);
	UsrMes(sMessage);

	:RETURN nUpdated;
:ENDPROC;

/* Usage;
DoProc("SetPermissionFlag");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Flags=5, Mask=8, Updated=13
```

### Packing two bytes into one value

Shifts the high byte left by 8 positions and adds the low byte to build a 16-bit value. With `nHighByte = 3` and `nLowByte = 15`: `(3 << 8) + 15 = 783`.

```ssl
:PROCEDURE PackBytes;
	:PARAMETERS nHighByte, nLowByte;
	:DECLARE nPacked, sMessage;

	:IF nHighByte != Integer(nHighByte) .OR. nLowByte != Integer(nLowByte);
		UsrMes("Both byte values must be integers");
		:RETURN 0;
	:ENDIF;

	nPacked := (nHighByte << 8) + nLowByte;

	sMessage := "Packed value: " + LimsString(nPacked);
	UsrMes(sMessage);

	:RETURN nPacked;
:ENDPROC;

/* Usage;
DoProc("PackBytes", {3, 15});
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Packed value: 783
```

## Related elements

- [`shift-right`](shift-right.md)
