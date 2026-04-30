---
title: "assignment"
summary: "Stores a value in a variable, object property, or array element and evaluates to the assigned value."
id: ssl.operator.assignment
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# assignment

## What it does

Stores a value in a variable, object property, or array element and evaluates to the assigned value.

The assignment operator (`:=`) writes the right-hand expression into an assignable target on the left. In SSL, valid targets are variables, object-property access such as `oTask:Status`, and indexed elements such as `aItems[1]`. The left side must be an assignable target; using `:=` against a literal, function result, or other non-storable expression is a compile-time error.

The expression evaluates to the value that was assigned, so chained assignments such as `sStatus := sDefault := "PENDING";` are valid and right-associative.

Assignment replaces the target's current value without requiring the previous and new values to have the same type. For arrays and objects, plain assignment shares the same underlying value rather than making an independent copy, so later updates through either name can be visible from the other.

## When to use it

- When you need to initialize or replace a variable's current value.
- When you need to update an object property or an array element in place.
- When several targets should intentionally receive the same value through a chained assignment.

## Syntax

```ssl
target := value;
```

Common target forms:

```ssl
sValue := "Ready";
oTask:Status := "Logged";
aItems[2] := "Updated";
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| variable | any | same as right | Stores the right-hand value in the variable |
| object property | any | same as right | Stores the right-hand value in the property |
| array element | any | same as right | Stores the right-hand value in the indexed element |

## Precedence

- **Precedence:** Assignment
- **Associativity:** right

## Notes for daily SSL work

!!! success "Do"
    - Put assignments on their own lines when they represent a distinct step in the logic.
    - Use assignment to update variables, properties, and array elements directly instead of rebuilding surrounding state unnecessarily.
    - Use chained assignment only when every target should receive the exact same value.

!!! failure "Don't"
    - Assign to undeclared variables and assume SSL will always create them for you. In normal code, undeclared targets can raise a runtime error.
    - Hide important state changes inside dense expressions when a standalone assignment would be clearer.
    - Assume `aCopy := aOriginal;` creates an independent array or object. Both names can still refer to the same underlying value.

## Errors and edge cases

- Invalid targets raise a compile-time error: `Assignment: invalid left-hand side ...`.
- Assigning to an undeclared variable can raise the runtime error `Variable [name] is undefined!`.
- Compound operators such as [`add-assign`](add-assign.md) ([`+=`](add-assign.md)), [`subtract-assign`](subtract-assign.md) ([`-=`](subtract-assign.md)), [`multiply-assign`](multiply-assign.md) ([`*=`](multiply-assign.md)), [`divide-assign`](divide-assign.md) ([`/=`](divide-assign.md)), [`modulo-assign`](modulo-assign.md) ([`%=`](modulo-assign.md)), and [`power-assign`](power-assign.md) ([`^=`](power-assign.md)) are separate operators that combine an operation with assignment.

## Examples

### Assigning a calculation result

Stores the computed total in `nSubtotal` using `:=` and displays it.

```ssl
:PROCEDURE CalculateOrderTotal;
    :DECLARE nUnitPrice, nQuantity, nSubtotal;

    nUnitPrice := 29.95;
    nQuantity := 3;

    nSubtotal := nUnitPrice * nQuantity;

    UsrMes("Subtotal: " + LimsString(nSubtotal));

    :RETURN nSubtotal;
:ENDPROC;

/* Usage;
DoProc("CalculateOrderTotal");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Subtotal: 89.85
```

### Assigning to a property and an array element

Updates `oTask:Status` via property assignment and `aSteps[3]` via index assignment.

```ssl
:PROCEDURE UpdateTaskState;
    :DECLARE oTask, aSteps;

    oTask := CreateLocal();
    aSteps := {"Queued", "Running", "Pending Review"};

    oTask:Status := "Running";
    aSteps[3] := "Reviewed";

    UsrMes("Task status: " + oTask:Status);
    /* Displays the updated task status;
    UsrMes("Final step: " + aSteps[3]);
    /* Displays the updated final step;

    :RETURN oTask:Status;
:ENDPROC;

/* Usage;
DoProc("UpdateTaskState");
```

### Chained assignment and shared array reference

Uses one chained assignment to set both `sPrimary` and `sSecondary` to the same string. Then shows that assigning an array to a second variable shares the same underlying value; modifying `aAlias[2]` is also visible through `aOriginal`.

```ssl
:PROCEDURE InitializeSharedState;
    :DECLARE sPrimary, sSecondary, aOriginal, aAlias;

    sPrimary := sSecondary := "PENDING";

    aOriginal := {"Queued", "Running", "Complete"};
    aAlias := aOriginal;

    aAlias[2] := "Reviewed";

    UsrMes("Primary: " + sPrimary + ", Secondary: " + sSecondary);
    /* Displays both assigned status values;
    UsrMes("Original second item: " + aOriginal[2]);
    /* Displays the shared second array item;

    :RETURN aOriginal[2];
:ENDPROC;

/* Usage;
DoProc("InitializeSharedState");
```

## Related elements

- [`add-assign`](add-assign.md)
- [`subtract-assign`](subtract-assign.md)
- [`multiply-assign`](multiply-assign.md)
- [`divide-assign`](divide-assign.md)
- [`modulo-assign`](modulo-assign.md)
- [`power-assign`](power-assign.md)
- [`index`](index.md)
