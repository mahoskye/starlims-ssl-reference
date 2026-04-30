---
title: "power"
summary: "Raises one number to the exponent of another number."
id: ssl.operator.power
element_type: operator
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# power

## What it does

Raises one number to the exponent of another number.

The `^` operator performs numeric exponentiation. It raises the left numeric
operand to the power of the right numeric operand, so `2 ^ 3` returns `8`. The
`^` operator is an exact alias of [`double-star-power`](double-star-power.md)
([`**`](double-star-power.md)). Both perform the same exponentiation operation.

Only `number ^ number` is supported. Exponentiation is right-associative, so `2 ^ 3 ^ 2` evaluates as `2 ^ (3 ^ 2) = 512`, not `(2 ^ 3) ^ 2 = 64`. Fractional and negative exponents are supported.

SSL does not perform implicit coercion for this operator. If the left operand is not numeric, the operator is not implemented for that type. If the left operand is numeric but the right operand is not, SSL raises an invalid-operand runtime error.

## When to use it

- When performing mathematical exponentiation (powers or roots) between two numbers.

## Syntax

```ssl
nResult := nBase ^ nExponent;
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [number](../types/number.md) | [number](../types/number.md) | [number](../types/number.md) | Raises the left operand to the power of the right operand. |
| any other type | any | error | Raises an operator-not-implemented runtime error because the left operand type does not support power. |
| [number](../types/number.md) | any other type | error | Raises an invalid-operand runtime error because the right operand is not numeric. |

## Precedence

- **Precedence:** Power
- **Associativity:** right

## Notes for daily SSL work

!!! success "Do"
    - Use `^` or [`**`](double-star-power.md) consistently in your codebase; they are exact aliases.
    - Validate operand types before exponentiating.
    - Use parentheses to clarify complex exponentiation expressions.

!!! failure "Don't"
    - Mix `^` and [`**`](double-star-power.md) without reason. Both are strict aliases, so mixing them adds noise without changing behavior.
    - Rely on implicit type coercion for non-numeric inputs. The operator only supports numeric operands.
    - Assume left-to-right evaluation for chained exponents. SSL evaluates exponentiation from the right.

## Errors and edge cases

- Exponentiation by a negative or fractional number yields non-integer results, which may not match integer math expectations.
- [`NIL`](../literals/nil.md) is not treated as `0` or `1`; using it as an operand raises a runtime error.

## Examples

### Calculating a simple power

Computes the cube of 5. 5 ^ 3 = 125.

```ssl
:PROCEDURE CalculateCube;
    :DECLARE nBase, nResult, sMessage;

    nBase := 5;
    nResult := nBase ^ 3;

    sMessage := "The cube of " + LimsString(nBase) + " is " + LimsString(nResult) + ".";
    UsrMes(sMessage);

    :RETURN nResult;
:ENDPROC;

/* Usage;
DoProc("CalculateCube");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
The cube of 5 is 125.
```

### Demonstrating right-associative evaluation

Shows that chained exponentiation groups from the right. `2 ^ 3 ^ 2` equals
`2 ^ 9 = 512`, not `8 ^ 2 = 64`.

```ssl
:PROCEDURE DemoRightAssociativity;
    :DECLARE nResult1, nResult2;

    nResult1 := 2 ^ 3 ^ 2;
    nResult2 := (2 ^ 3) ^ 2;

    :IF nResult1 == 512 .AND. nResult2 == 64;
        UsrMes("2 ^ 3 ^ 2 groups as 2 ^ (3 ^ 2)");
    :ENDIF;

    :RETURN nResult1;
:ENDPROC;

/* Usage;
DoProc("DemoRightAssociativity");
```

### Using fractional exponents and catching invalid operands

Shows `81 ^ 0.5 = 9` (square root) and `10 ^ -1 = 0.1` (reciprocal). The [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) handles the runtime error from `2 ^ "oops"`. The exact error description is runtime-dependent.

```ssl
:PROCEDURE PowerAdvancedDemo;
    :DECLARE nSquareRoot, nReciprocal, nResult, oErr, sMessage;

    nSquareRoot := 81 ^ 0.5;
    nReciprocal := 10 ^ -1;

    sMessage := "sqrt(81) = " + LimsString(nSquareRoot) + ", reciprocal of 10 = " + LimsString(nReciprocal);
    UsrMes(sMessage);

    :TRY;
        nResult := 2 ^ "oops";
    :CATCH;
        oErr := GetLastSSLError();
        UsrMes("Power failed: " + oErr:Description);
        /* Displays on failure: Power failed;
    :ENDTRY;

    :RETURN nSquareRoot;
:ENDPROC;

/* Usage;
DoProc("PowerAdvancedDemo");
```

## Related elements

- [`power-assign`](power-assign.md)
- [`double-star-power`](double-star-power.md)
