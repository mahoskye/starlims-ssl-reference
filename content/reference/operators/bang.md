---
title: "bang"
summary: "Performs boolean negation, returning the opposite boolean value."
id: ssl.operator.bang
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# bang

## What it does

Performs boolean negation, returning [`.T.`](../literals/true.md) for [`.F.`](../literals/false.md) and [`.F.`](../literals/false.md) for [`.T.`](../literals/true.md).

The [`!`](not.md) operator is the symbolic form of logical negation in SSL. It applies to a single boolean expression and returns the opposite boolean value. Like [`.NOT.`](not.md), it is a unary prefix operator — write it before the operand or parenthesized expression you want to invert.

`!bValue` and `.NOT. bValue` perform the same logical operation. Use parentheses when negating a larger expression, such as `!(bReady .AND. bReleased)`, so the grouping is explicit to readers.

[`!`](not.md) works on boolean values only and raises a runtime error for other operand types. It does not perform any truthy or falsy coercion.

## When to use it

- When you want a short inline form of boolean negation.
- When you need to invert the result of a boolean expression such as `Empty(...)`.
- When negating a compound condition with explicit parentheses improves clarity.

## Syntax

```ssl
!booleanExpression
!(compoundExpression)
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| n/a | [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | Returns the logical negation of the operand. |

## Precedence

- **Precedence:** Unary
- **Associativity:** right

## Notes for daily SSL work

!!! success "Do"
    - Use [`!`](not.md) for concise boolean negation in conditions such as `! Empty(oSample)`.
    - Wrap compound expressions in parentheses, such as `!(bReady .AND. bReleased)`.
    - Follow the surrounding codebase style when choosing between [`!`](not.md) and [`.NOT.`](not.md).

!!! failure "Don't"
    - Use [`!`](not.md) on strings, numbers, arrays, objects, or dates. It only supports boolean operands.
    - Rely on readers to infer grouping in longer expressions. Add parentheses around the expression being negated.
    - Treat [`!`](not.md) as a general-purpose truthiness operator. SSL does not coerce non-boolean values here.

## Errors and edge cases

- [`!`](not.md) is a prefix unary operator, not a postfix operator.
- Double negation such as `!!bFlag` is valid and evaluates back to the original boolean value.
- [`!`](not.md) is different from the bitwise [`_NOT`](../functions/_NOT.md)`()` function, which is for integer bit patterns rather than boolean logic.

## Examples

### Inverting a boolean flag

Assigns the negation of `bIsReady` to `bCanStart`. With `bIsReady` set to [`.F.`](../literals/false.md), `bCanStart` becomes [`.T.`](../literals/true.md) and the first branch runs.

```ssl
:PROCEDURE CheckReadyState;
    :DECLARE bIsReady, bCanStart, sMessage;

    bIsReady := .F.;
    bCanStart := !bIsReady;

    :IF bCanStart;
        sMessage := "Sample can start";
    :ELSE;
        sMessage := "Sample is still blocked";
    :ENDIF;

    UsrMes(sMessage);

    :RETURN bCanStart;
:ENDPROC;

/* Usage;
DoProc("CheckReadyState");
;
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Sample can start
```

### Negating a compound condition

Wraps the entire `.AND.` expression in parentheses so [`!`](not.md) inverts the combined result. With `bIsComplete = .T.` and `bIsReleased = .F.`, the `.AND.` evaluates to [`.F.`](../literals/false.md), which [`!`](not.md) inverts to [`.T.`](../literals/true.md), entering the not-ready branch.

```ssl
:PROCEDURE ValidateRelease;
    :DECLARE sSampleID, bIsComplete, bIsReleased, sMessage;

    sSampleID := "LAB-2024-0042";
    bIsComplete := .T.;
    bIsReleased := .F.;

    :IF !(bIsComplete .AND. bIsReleased);
        sMessage := "Sample " + sSampleID + " is not ready for release";
        UsrMes(sMessage);

        :RETURN .F.;
    :ENDIF;

    UsrMes("Sample " + sSampleID + " is ready for release");

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ValidateRelease");
;
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Sample LAB-2024-0042 is not ready for release
```

## Related elements

- [`and`](and.md)
- [`or`](or.md)
- [`not`](not.md)
