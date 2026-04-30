---
title: "power-assign"
summary: "Raises a numeric value to a numeric power and stores the result back into the left side."
id: ssl.operator.power-assign
element_type: operator
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# power-assign

## What it does

Raises a numeric value to a numeric power and stores the result back into the
left side.

The `^=` operator is the compound-assignment form of [`power`](power.md)
([`^`](power.md)). It evaluates the current left-side value, applies
exponentiation with the right-side value, and writes the result back to the
same target. `nValue ^= nExponent;` is the concise form of
`nValue := nValue ^ nExponent;`.

`^=` follows the same runtime type rules as [`^`](power.md): exponentiation is
supported only for number-with-number operands. SSL does not perform implicit
type coercion for this operator.

## When to use it

- When updating the same numeric variable, property, or array element in place
  after exponentiation.
- When replacing `target := target ^ value;` with a shorter equivalent form.
- When keeping repeated numeric transformations concise inside loops.

## Syntax

```ssl
target ^= value;
```

`target` must be an assignable left-hand side: a variable, property, or array
element.

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [number](../types/number.md) | [number](../types/number.md) | [number](../types/number.md) | Raises the left value to the power of the right value and stores the result back in the left operand. |

## Precedence

- **Precedence:** Assignment
- **Associativity:** right

## Notes for daily SSL work

!!! success "Do"
    - Use `^=` when updating the same numeric target in place.
    - Use `^=` inside loops when repeatedly applying the same exponentiation pattern.
    - Use parentheses in the right-side power expression when evaluation order needs to be explicit.

!!! failure "Don't"
    - `^=` only accepts number operands; using it with strings, dates, arrays, objects, or booleans raises a runtime error.
    - Assume SSL will coerce text or [`NIL`](../literals/nil.md) into numbers for `^=`.
    - Use a non-assignable expression on the left side.

## Errors and edge cases

- The left side must be assignable. Expressions such as `(nValue + 1) ^= 2;` are invalid.

## Examples

### Building a power series by squaring in place

Repeatedly squares `nValue` with `^= 2`. Starting from 2: 4, 16, 256, 65536.

```ssl
:PROCEDURE BuildPowerSeries;
	:DECLARE nValue, nIndex, sSeries;

	nValue := 2;
	sSeries := "";

	:FOR nIndex := 1 :TO 4;
		nValue ^= 2;
		sSeries += LimsString(nValue);

		:IF nIndex < 4;
			sSeries += ", ";
		:ENDIF;
	:NEXT;

	UsrMes("Squared in place: " + sSeries);

	:RETURN nValue;
:ENDPROC;

/* Usage;
DoProc("BuildPowerSeries");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Squared in place: 4, 16, 256, 65536
```

### Updating array elements with per-item exponents

Applies a different exponent to each element: 2^3=8, 3^2=9, 4^2=16.

```ssl
:PROCEDURE ReweightReadings;
	:DECLARE aReadings, aExponents, nIndex, nCount, nTotal, sMessage;

	aReadings := {2, 3, 4};
	aExponents := {3, 2, 2};
	nCount := ALen(aReadings);
	nTotal := 0;

	:FOR nIndex := 1 :TO nCount;
		aReadings[nIndex] ^= aExponents[nIndex];
		nTotal += aReadings[nIndex];
	:NEXT;

	sMessage := "Adjusted readings: " + LimsString(aReadings[1]) 
				+ ", " + LimsString(aReadings[2]) + ", "
				+ LimsString(aReadings[3]);
	UsrMes(sMessage);

	:RETURN nTotal;
:ENDPROC;

/* Usage;
DoProc("ReweightReadings");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Adjusted readings: 8, 9, 16
```

## Related elements

- [`power`](power.md)
- [`assignment`](assignment.md)
