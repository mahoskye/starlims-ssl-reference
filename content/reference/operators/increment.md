---
title: "increment"
summary: "Increases a number variable by one, modifying its value in place."
id: ssl.operator.increment
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# increment

## What it does

Increases a number variable by one, modifying its value in place.

The `++` operator adds one to a numeric variable. It supports both prefix (`++variable`) and postfix (`variable++`) forms. Both forms increment the variable in place, but they differ in what they return when used inside a larger expression: prefix returns the new (incremented) value; postfix returns the original value before incrementing.

`++` is equivalent to `variable += 1` but more concise. The operand must be a variable holding a number. Using `++` on a non-numeric variable, a literal, or an expression result raises a runtime error.

## When to use it

- When you need to increase a numeric counter by one in place.
- When brevity is preferred over [`add-assign`](add-assign.md) (`+= 1`).

## Syntax

Postfix form — returns original value, then increments:

```ssl
variable++
```

Prefix form — increments, then returns new value:

```ssl
++variable
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [number](../types/number.md) | n/a | [number](../types/number.md) | Adds 1 to the variable in place. |

## Precedence

- **Precedence:** Unary
- **Associativity:** none

## Notes for daily SSL work

!!! success "Do"
    - Use `++` for concise incrementing of loop counters or numeric accumulators.
    - Use the prefix form (`++variable`) when the incremented value is needed immediately in the same expression.

!!! failure "Don't"
    - Use `++` on non-variable or non-numeric values. Only variables holding numbers can be incremented.
    - Assume prefix and postfix always behave identically inside expressions. Prefix returns the new value; postfix returns the old value.

## Examples

### Incrementing a counter in a loop

Increments `nCount` on each of five iterations using postfix `++`. The `nIndex` loop variable drives the loop count independently.

```ssl
:PROCEDURE IncrementCounter;
    :DECLARE nCount, nMax, nIndex, sMessage;

    nMax := 5;
    nCount := 0;

    :FOR nIndex := 1 :TO nMax;
        nCount++;
        sMessage := "Iteration " + LimsString(nCount) + " complete";
        UsrMes(sMessage);
    :NEXT;

    :RETURN nCount;
:ENDPROC;

/* Usage;
DoProc("IncrementCounter");
```

[`UsrMes`](../functions/UsrMes.md) displays (one line per iteration):

```text
Iteration 1 complete
Iteration 2 complete
Iteration 3 complete
Iteration 4 complete
Iteration 5 complete
```

### Prefix vs postfix return values

Shows that postfix `++` assigns the original value before incrementing, while prefix `++` returns the already-incremented value. Starting from 5, postfix captures 5 and leaves `nCounter` at 6; prefix then increments to 7 and returns 7.

```ssl
:PROCEDURE DemoIncrementForms;
    :DECLARE nCounter, nCapturedPostfix, nCapturedPrefix, sOutput;

    nCounter := 5;

    /* Postfix: assigns original value, then increments;
    nCapturedPostfix := nCounter++;

    /* Prefix: increments first, then returns new value;
    nCapturedPrefix := ++nCounter;

    sOutput := "Postfix captured: " + LimsString(nCapturedPostfix) + ", nCounter after postfix: 6";
    UsrMes(sOutput);

    sOutput := "Prefix captured: " + LimsString(nCapturedPrefix) + ", nCounter after prefix: 7";
    UsrMes(sOutput);

    :RETURN nCounter;
:ENDPROC;

/* Usage;
DoProc("DemoIncrementForms");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Postfix captured: 5, nCounter after postfix: 6
Prefix captured: 7, nCounter after prefix: 7
```

## Related elements

- [`decrement`](decrement.md)
- [`add-assign`](add-assign.md)
