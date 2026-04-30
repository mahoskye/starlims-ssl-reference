---
title: "subtract-assign"
summary: "Updates a variable, property, or array element in place by applying - and then storing the result back into the left side."
id: ssl.operator.subtract-assign
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# subtract-assign

## What it does

Updates a variable, property, or array element in place by applying [`-`](minus.md) and then storing the result back into the left side.

The subtract-assign operator (`-=`) is a compound assignment operator. It performs the same supported subtraction as [`minus`](minus.md), then writes the updated value back to the left operand. `x -= y` behaves like "read `x`, compute `x - y`, store the result in `x`", and the expression evaluates to the updated left-side value.

Supported combinations are limited to the combinations implemented by [`minus`](minus.md):

- Number `-=` number
- String `-=` string
- Date `-=` number
- Date `-=` date

No implicit type coercion is performed. Mixed types and unsupported operand types raise errors.

## When to use it

- Decrease a numeric value in place.
- Append text while trimming trailing spaces from the existing left string.
- Move a date backward by a number of days and store the new date.
- Replace a date-valued target with the day difference produced by `date - date`.

## Syntax

```ssl
target -= value;
```

`target` must be an assignable left-hand side such as a variable, property, or array element.

## Type behavior

| Left | Right | Result | Behavior |
| --- | --- | --- | --- |
| [number](../types/number.md) | [number](../types/number.md) | [number](../types/number.md) | Subtracts the right numeric value from the left value and stores the difference. |
| [string](../types/string.md) | [string](../types/string.md) | [string](../types/string.md) | Trims trailing spaces from the left operand, then appends the right string and stores the result. |
| [date](../types/date.md) | [number](../types/number.md) | [date](../types/date.md) | Subtracts the right value as days from the left date and stores the new date. |
| [date](../types/date.md) | [date](../types/date.md) | [number](../types/number.md) | Computes the day difference and stores that numeric result back into the left target. |

## Precedence

- **Precedence:** Assignment
- **Associativity:** right

## Notes for daily SSL work

!!! success "Do"
    - Use `-=` for in-place numeric decrements, totals, and countdown values.
    - Use `-=` with strings only when you specifically want trailing spaces removed from the left string before appending.
    - Use a separate target or an explicit temporary when `date -= date` would make the code clearer.

!!! failure "Don't"
    - Rely on implicit coercion such as string-minus-number or date-minus-string. Unsupported type pairs raise errors.
    - Treat `-=` on strings as character removal. For strings, it trims trailing spaces from the left operand and then appends the right operand.
    - Forget that `date -= date` stores a number, not a date, back into the left target.

## Errors and edge cases

- A non-assignable left side is rejected before the update is performed.
- For strings, only trailing space characters on the left operand are trimmed. Leading spaces and the right operand are left unchanged.
- `date -= date` changes the stored value to a number, so a later date-specific operation on that same target will no longer behave as a date operation.

## Examples

### Decreasing a numeric total

Reduces a numeric value in place without repeating the left operand. Starting from `nOnHand = 25` and issuing 4 units, the result is 21.

```ssl
:PROCEDURE ReduceInventory;
    :DECLARE nOnHand, nIssued, sMessage;

    nOnHand := 25;
    nIssued := 4;

    nOnHand -= nIssued;

    sMessage := "Remaining quantity: " + LimsString(nOnHand);
    UsrMes(sMessage);

    :RETURN nOnHand;
:ENDPROC;

/* Usage;
DoProc("ReduceInventory");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Remaining quantity: 21
```

### Trimming and appending to a string

Uses `-=` to remove trailing spaces from the left string before appending the suffix. `"Sample   " -= "Review"` trims the three trailing spaces from `"Sample   "`, then appends `"Review"` to produce `"SampleReview"`.

```ssl
:PROCEDURE BuildDisplayLabel;
    :DECLARE sLabel, sSuffix;

    sLabel := "Sample   ";
    sSuffix := "Review";

    sLabel -= sSuffix;

    UsrMes("Display label: [" + sLabel + "]");

    :RETURN sLabel;
:ENDPROC;

/* Usage;
DoProc("BuildDisplayLabel");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Display label: [SampleReview]
```

### Replacing a date with a day difference

Shows two uses in sequence: `dReminderDate -= 3` moves the date back 3 days, while `nDaysUntilDue -= dToday` replaces the date with the numeric day count (5 days between 03/10/2024 and 03/15/2024).

```ssl
:PROCEDURE CalculateDaysUntilDue;
    :DECLARE dDueDate, dToday, dReminderDate, nDaysUntilDue, sMessage;

    dDueDate := CToD("03/15/2024");
    dToday := CToD("03/10/2024");
    dReminderDate := dDueDate;
    nDaysUntilDue := dDueDate;

    dReminderDate -= 3;
    nDaysUntilDue -= dToday;

    sMessage := "Reminder date: " + DToC(dReminderDate) +
        ", days until due: " + LimsString(nDaysUntilDue);
    UsrMes(sMessage);

    :RETURN nDaysUntilDue;
:ENDPROC;

/* Usage;
DoProc("CalculateDaysUntilDue");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Reminder date: 03/12/2024, days until due: 5
```

## Related elements

- [`assignment`](assignment.md)
- [`minus`](minus.md)
- [`add-assign`](add-assign.md)
