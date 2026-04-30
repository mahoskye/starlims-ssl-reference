---
title: "LimsXOr"
summary: "Calculates the bitwise exclusive OR of two integer-valued numbers."
id: ssl.function.limsxor
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LimsXOr

Calculates the bitwise exclusive OR of two integer-valued numbers.

`LimsXOr` accepts two numeric arguments and returns their bitwise XOR result. Both arguments must be whole numbers. If either argument is [`NIL`](../literals/nil.md), or if either numeric value has a fractional part, the call raises an error instead of returning a result.

## When to use

- When you need to toggle selected bits in an integer by applying a mask.
- When you need to identify which bits differ between two integer flag values.
- When you need a reversible combine-and-restore pattern for integer values.

## Syntax

```ssl
LimsXOr(nVal1, nVal2)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nVal1` | [number](../types/number.md) | yes | — | First operand. Must be an integer-valued number. |
| `nVal2` | [number](../types/number.md) | yes | — | Second operand. Must be an integer-valued number. |

## Returns

**[number](../types/number.md)** — The bitwise XOR of `nVal1` and `nVal2`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `nVal1` or `nVal2` is [`NIL`](../literals/nil.md). The runtime raises the same message regardless of which argument is [`NIL`](../literals/nil.md). | `First argument cannot be null.` |
| `nVal1` or `nVal2` has a fractional part. | `Xor is available only for integer numbers.` |

## Best practices

!!! success "Do"
    - Use `LimsXOr` with integer flags and masks.
    - Validate or normalize values before the call when inputs may contain decimals.
    - Use XOR's reversible behavior when you need to toggle or restore integer bits.

!!! failure "Don't"
    - Pass fractional numeric values such as `7.5`. The function only accepts integer-valued numbers.
    - Assume a missing argument is treated as zero. [`NIL`](../literals/nil.md) raises an error.
    - Use `LimsXOr` for logical true-or-false comparisons. It is a numeric bitwise operation.

## Examples

### Toggle one flag bit

Use XOR with a mask to flip one bit in an integer value.

```ssl
:PROCEDURE ToggleFlagBit;
    :DECLARE nFlags, nMask, nResult;

    nFlags := 5;
    nMask := 4;

    nResult := LimsXOr(nFlags, nMask);

    UsrMes("Original flags: " + LimsString(nFlags));
    UsrMes("Updated flags: " + LimsString(nResult));

    :RETURN nResult;
:ENDPROC;

/* Usage;
DoProc("ToggleFlagBit");
```

`UsrMes` displays:

```text
Original flags: 5
Updated flags: 1
```

### Find which bits changed between two values

Compare two integer flag values and report the positions that differ.

```ssl
:PROCEDURE ListChangedBits;
    :DECLARE nOriginal, nUpdated, nDiff, nMask, aChanged, nIndex;

    nOriginal := 42;
    nUpdated := 46;
    nDiff := LimsXOr(nOriginal, nUpdated);
    nMask := 1;
    aChanged := {};

    :FOR nIndex := 1 :TO 8;
        :IF _AND(nDiff, nMask) != 0;
            AAdd(aChanged, nIndex);
        :ENDIF;

        nMask := nMask * 2;
    :NEXT;

    UsrMes("Changed bit positions: " + LimsString(aChanged));

    :RETURN aChanged;
:ENDPROC;

/* Usage;
DoProc("ListChangedBits");
```

[`UsrMes`](UsrMes.md) displays:

```
Changed bit positions: {3}
```

### Encode and restore a value with the same key

XOR is reversible: applying the same key twice restores the original value.

```ssl
:PROCEDURE EncodeAndRestore;
    :DECLARE nSample, nKey, nEncoded, nDecoded;

    nSample := 123;
    nKey := 87;

    nEncoded := LimsXOr(nSample, nKey);
    nDecoded := LimsXOr(nEncoded, nKey);

    UsrMes("Original: " + LimsString(nSample));
    UsrMes("Encoded: " + LimsString(nEncoded));
    UsrMes("Decoded: " + LimsString(nDecoded));

    :RETURN nDecoded;
:ENDPROC;

/* Usage;
DoProc("EncodeAndRestore");
```

`UsrMes` displays:

```text
Original: 123
Encoded: 44
Decoded: 123
```

## Related

- [`_XOR`](_XOR.md)
- [`_AND`](_AND.md)
- [`_OR`](_OR.md)
- [`number`](../types/number.md)
