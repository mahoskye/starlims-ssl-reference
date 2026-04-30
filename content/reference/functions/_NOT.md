---
title: "_NOT"
summary: "Returns the bitwise complement of a whole-number operand."
id: ssl.function._not
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# _NOT

Returns the bitwise complement of a whole-number operand.

`_NOT` accepts one numeric operand and inverts its bits. `nOperand` must already be a whole number. If you pass a fractional number, the call fails with an invalid-operand error stating that integers are expected. If you pass a non-numeric value, the runtime raises the standard operator-not-implemented error for `_NOT`.

## When to use

- When you need the inverse of a bitmask before combining it with [`_AND`](_AND.md).
- When you are clearing specific bits in a flags field.
- When you are doing integer-only bitwise work and need bit inversion rather than boolean negation.

## Syntax

```ssl
_NOT(nOperand)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nOperand` | [number](../types/number.md) | yes | — | Whole-number value to invert. Fractional numbers are rejected. |

## Returns

**[number](../types/number.md)** — The bitwise complement of `nOperand`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `nOperand` is not a whole number. | `SSLDouble: _NOT : <value> : invalid operand. Expected integers.` |
| `_NOT` is called on a non-numeric type. | `the operator/method: _NOT is not implemented on type: <type>. Operand: <operand>` |

## Best practices

!!! success "Do"
    - Validate that the operand is a whole number before calling `_NOT`.
    - Use `_NOT` together with [`_AND`](_AND.md) when you need to clear selected bits from a mask.
    - Use `.NOT.` for boolean logic and reserve `_NOT` for integer bit operations.

!!! failure "Don't"
    - Pass fractional numbers and expect SSL to round or truncate them for you.
    - Use `_NOT` as a substitute for logical negation in conditions.
    - Assume the result preserves the same sign or magnitude as the input.

## Caveats

- `_NOT(0)` returns `-1`, so inverted masks are often negative.

## Examples

### Invert a simple mask

Show the direct result of applying `_NOT` to a whole number.

```ssl
:PROCEDURE ShowInvertedMask;
    :DECLARE nMask, nInverted;

    nMask := 12;
    nInverted := _NOT(nMask);

    UsrMes("Original mask: " + LimsString(nMask));
    UsrMes("Inverted mask: " + LimsString(nInverted));
:ENDPROC;

/* Usage;
DoProc("ShowInvertedMask");
```

`UsrMes` displays:

```text
Original mask: 12
Inverted mask: -13
```

### Clear selected flags with [`_AND`](_AND.md) and `_NOT`

Use `_NOT` to invert a clear-mask before applying [`_AND`](_AND.md).

```ssl
:PROCEDURE ClearSelectedFlags;
    :DECLARE nFlags, nClearMask, nResult;

    nFlags := 29;
    nClearMask := 12;

    nResult := _AND(nFlags, _NOT(nClearMask));

    UsrMes("Original flags: " + LimsString(nFlags));
    UsrMes("Clear mask: " + LimsString(nClearMask));
    UsrMes("Flags after clear: " + LimsString(nResult));
:ENDPROC;

/* Usage;
DoProc("ClearSelectedFlags");
```

`UsrMes` displays:

```text
Original flags: 29
Clear mask: 12
Flags after clear: 17
```

### Apply the same clear-mask to multiple values

Invert one mask once, then reuse it while updating a list of packed flag values.

```ssl
:PROCEDURE ClearArchiveBitFromBatch;
    :DECLARE aFlags, aUpdated, nClearMask, nKeepMask, nIndex;

    aFlags := {29, 13, 9, 31};
    aUpdated := {};
    nClearMask := 8;
    nKeepMask := _NOT(nClearMask);

    :FOR nIndex := 1 :TO ALen(aFlags);
        AAdd(aUpdated, _AND(aFlags[nIndex], nKeepMask));
    :NEXT;

    UsrMes("Original first value: " + LimsString(aFlags[1]));
    UsrMes("Updated first value: " + LimsString(aUpdated[1]));
    UsrMes("Updated item count: " + LimsString(ALen(aUpdated)));
:ENDPROC;

/* Usage;
DoProc("ClearArchiveBitFromBatch");
```

`UsrMes` displays:

```text
Original first value: 29
Updated first value: 21
Updated item count: 4
```

## Related

- [`_AND`](_AND.md)
- [`_OR`](_OR.md)
- [`_XOR`](_XOR.md)
- [`number`](../types/number.md)
