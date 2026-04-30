---
title: "_OR"
summary: "Returns the bitwise inclusive OR of two whole-number operands."
id: ssl.function._or
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# _OR

Returns the bitwise inclusive OR of two whole-number operands.

`_OR` combines the bits from two numeric values and returns a numeric result. Both operands must already be whole numbers. If either operand has a fractional part, the call fails with a runtime error indicating that integers are expected. If either operand is not numeric, the runtime raises an operator error for `_OR`.

## When to use

- When you need to set bits that appear in either of two integer masks.
- When you are combining flag values into one packed numeric field.
- When you need integer-only bitwise logic rather than boolean `.OR.` logic.

## Syntax

```ssl
_OR(nValue1, nValue2)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nValue1` | [number](../types/number.md) | yes | — | First whole-number operand. |
| `nValue2` | [number](../types/number.md) | yes | — | Second whole-number operand. |

## Returns

**[number](../types/number.md)** — Numeric result whose bits are set when they are set in `nValue1`, `nValue2`, or both.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| Either operand is not a whole number. | `SSLDouble: <value> _OR <v>: invalid operand(s). Expected integers.` |
| Either operand is [`NIL`](../literals/nil.md). | `SSLDouble - invalid operand: (of type null) for operator: _OR.` |
| `_OR` is called on a non-numeric type. | `the operator/method: _OR is not implemented on type: <type>. Operand: <operand>` |

## Best practices

!!! success "Do"
    - Validate that both operands are whole numbers before calling `_OR`.
    - Use `_OR` to add flags to a packed integer mask.
    - Use `.OR.` for boolean conditions and reserve `_OR` for integer bit work.

!!! failure "Don't"
    - Pass fractional numbers and expect SSL to round them for you.
    - Use `_OR` as a substitute for boolean `.OR.` in conditions.
    - Mix numeric and non-numeric values in the same `_OR` call.

## Caveats

- `_OR(5, 2)` returns `7`, because `0101 OR 0010` produces `0111`.

## Examples

### Combine two flags

Combine two simple flag values into one mask.

```ssl
:PROCEDURE CombineFlags;
    :DECLARE nReadFlag, nWriteFlag, nCombinedFlags;

    nReadFlag := 1;
    nWriteFlag := 2;

    nCombinedFlags := _OR(nReadFlag, nWriteFlag);

    UsrMes(LimsString(nCombinedFlags));
:ENDPROC;

/* Usage;
DoProc("CombineFlags");
```

[`UsrMes`](UsrMes.md) displays:

```text
3
```

### Add a mask to an existing value

Set selected bits in an existing packed value.

```ssl
:PROCEDURE SetArchiveAndReviewFlags;
    :DECLARE nCurrentFlags, nMask, nUpdatedFlags;

    nCurrentFlags := 1;
    nMask := 6;

    nUpdatedFlags := _OR(nCurrentFlags, nMask);

    UsrMes("Original flags: " + LimsString(nCurrentFlags));
    /* Displays: Original flags: 1;
    UsrMes("Mask: " + LimsString(nMask));
    /* Displays: Mask: 6;
    UsrMes("Updated flags: " + LimsString(nUpdatedFlags));
    /* Displays: Updated flags: 7;
:ENDPROC;

/* Usage;
DoProc("SetArchiveAndReviewFlags");
```

### Validate external values before calling `_OR`

Check both type and whole-number status before doing bitwise work.

```ssl
:PROCEDURE SafeBitwiseOr;
    :PARAMETERS vLeft, vRight;
    :DECLARE bLeftValid, bRightValid, nResult;

    bLeftValid := LimsTypeEx(vLeft) == "NUMERIC"
			      .AND. Integer(vLeft) == vLeft;
    bRightValid := LimsTypeEx(vRight) == "NUMERIC"
		           .AND. Integer(vRight) == vRight;

    :IF !(bLeftValid .AND. bRightValid);
        UsrMes("Both operands must be whole numbers.");
        :RETURN;
    :ENDIF;

    nResult := _OR(vLeft, vRight);

    UsrMes("Result: " + LimsString(nResult));
    /* Displays: bitwise OR result on success;
:ENDPROC;

/* Usage;
DoProc("SafeBitwiseOr", {5, 3});
```

## Related

- [`_AND`](_AND.md)
- [`_NOT`](_NOT.md)
- [`_XOR`](_XOR.md)
- [`number`](../types/number.md)
