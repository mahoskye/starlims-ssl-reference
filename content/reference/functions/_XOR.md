---
title: "_XOR"
summary: "Returns the bitwise exclusive OR of two whole-number operands."
id: ssl.function._xor
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# _XOR

Returns the bitwise exclusive OR of two whole-number operands.

`_XOR` compares the bits in two numeric values and sets a result bit only when the corresponding input bits differ. Both operands must be whole numbers. If either operand has a fractional part, SSL raises a runtime error indicating that integers are expected. If `_XOR` is used with a non-numeric value, SSL raises the standard runtime operator error for an unsupported operand.

## When to use

- When you need to toggle specific bits in an integer using a bitmask value.
- When you need to identify which flags changed between two packed values.
- When you are calculating a simple XOR-based checksum across integer values.

## Syntax

```ssl
_XOR(nValue1, nValue2)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nValue1` | [number](../types/number.md) | yes | — | The first operand for the bitwise XOR. Must be a whole number; fractional values raise a runtime error. |
| `nValue2` | [number](../types/number.md) | yes | — | The second operand for the bitwise XOR. Must be a whole number; fractional values raise a runtime error. |

## Returns

**[number](../types/number.md)** — Numeric result whose bits are set only where `nValue1` and `nValue2` differ.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| Either operand is not a whole number. | `SSLDouble:{value} _XOR {v}: invalid operand(s). Expected integers.` |
| `nValue2` is [`NIL`](../literals/nil.md). | `SSLDouble - invalid operand: (of type null) for operator: _XOR.` |
| `_XOR` is called on a non-numeric type. | `the operator/method: _XOR is not implemented on type: {type}. Operand: {operand}` |

## Best practices

!!! success "Do"
    - Validate that both operands are whole numbers before calling `_XOR`.
    - Use `_XOR` when you specifically need bits that differ between two values.
    - Use comments or named mask variables when the bit meaning is not obvious.

!!! failure "Don't"
    - Pass fractional numbers and expect SSL to round them automatically.
    - Use `_XOR` as a substitute for boolean logic in [`:IF`](../keywords/IF.md) conditions.
    - Use unnamed numeric literals when a bitmask variable would make the code clearer.

## Caveats

- `_XOR(5, 3)` returns `6`, because `0101 XOR 0011` produces `0110`.

## Examples

### Toggle a flag in an integer

Toggle one permission bit by XORing with a mask.

```ssl
:PROCEDURE TogglePermissionFlag;
	:DECLARE nPermissions, nToggleMask, nResult;

	nPermissions := 5;
	nToggleMask := 4;

	nResult := _XOR(nPermissions, nToggleMask);

	UsrMes("Original permissions: " + LimsString(nPermissions));
	UsrMes("Toggled permissions: " + LimsString(nResult));
:ENDPROC;

/* Usage;
DoProc("TogglePermissionFlag");
```

[`UsrMes`](UsrMes.md) displays:

```text
Original permissions: 5
Toggled permissions: 1
```

### Identify changed flags between two values

Compare an original flag set to an updated one and isolate the changed bits. `_XOR(3, 5)` returns `6` (`011 XOR 101 = 110`), and subsequent [`_AND`](_AND.md) checks identify which named flags changed.

```ssl
:PROCEDURE FindChangedFlags;
	:DECLARE nOriginalFlags, nUpdatedFlags, nChangedFlags;
	:DECLARE nArchiveMask, nReviewMask;

	nOriginalFlags := 3;
	nUpdatedFlags := 5;

	nArchiveMask := 2;
	nReviewMask := 4;

	nChangedFlags := _XOR(nOriginalFlags, nUpdatedFlags);

	UsrMes("Changed flags: " + LimsString(nChangedFlags));

	:IF _AND(nChangedFlags, nArchiveMask) == nArchiveMask;
		UsrMes("Archive flag changed.");
	:ENDIF;

	:IF _AND(nChangedFlags, nReviewMask) == nReviewMask;
		UsrMes("Review flag changed.");
	:ENDIF;

	:RETURN nChangedFlags;
:ENDPROC;

/* Usage;
DoProc("FindChangedFlags");
```

[`UsrMes`](UsrMes.md) displays:

```text
Changed flags: 6
Archive flag changed.
Review flag changed.
```

### Compute a checksum across a list of integers

Accumulate an XOR checksum across multiple values and compare it to an expected value. The XOR of `{170, 85, 204, 51, 136}` produces `136`, matching the expected checksum.

```ssl
:PROCEDURE VerifyXorChecksum;
	:DECLARE aValues, nChecksum, nExpectedChecksum, nIndex, bMatches;

	aValues := {170, 85, 204, 51, 136};
	nChecksum := 0;

	:FOR nIndex := 1 :TO ALen(aValues);
		nChecksum := _XOR(nChecksum, aValues[nIndex]);
	:NEXT;

	nExpectedChecksum := 136;
	bMatches := nChecksum == nExpectedChecksum;

	UsrMes("Computed checksum: " + LimsString(nChecksum));

	:IF bMatches;
		UsrMes("Checksum verified.");
	:ELSE;
		UsrMes("Checksum mismatch.");
	:ENDIF;

	:RETURN bMatches;
:ENDPROC;

/* Usage;
DoProc("VerifyXorChecksum");
```

[`UsrMes`](UsrMes.md) displays:

```text
Computed checksum: 136
Checksum verified.
```

## Related

- [`_AND`](_AND.md)
- [`_OR`](_OR.md)
- [`_NOT`](_NOT.md)
- [`LimsXOr`](LimsXOr.md)
- [`number`](../types/number.md)
