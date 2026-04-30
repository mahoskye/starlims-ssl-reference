---
title: "add-assign"
summary: "Updates a variable, property, or array element in place by applying + and then storing the result back into the left side."
id: ssl.operator.add-assign
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# add-assign

## What it does

Updates a variable, property, or array element in place by applying [`+`](plus.md) and
then storing the result back into the left side.

The add-assign operator (`+=`) is a compound assignment operator. It performs the same additions as [`+`](plus.md), then writes the updated value back to the left operand. In practice, `x += y` behaves like "read `x`, add `y`, store the result in `x`". The expression evaluates to the updated left-side value.

Supported type combinations are limited to those implemented by [`+`](plus.md):

- number `+=` number
- string `+=` string
- date `+=` number

No implicit type coercion is performed. Mixed types and unsupported operand types raise runtime errors.

## When to use it

- When increasing a numeric value in place.
- When appending text to an existing string.
- When advancing a date forward by a number of days.
- When accumulation code inside loops or repeated update steps should be concise.

## Syntax

```ssl
target += value;
```

`target` must be an assignable left-hand side such as a variable, property, or array element.

## Type behavior

| Left | Right | Result | Behavior |
| --- | --- | --- | --- |
| [number](../types/number.md) | [number](../types/number.md) | [number](../types/number.md) | Adds the right value to the left value and stores the sum |
| [string](../types/string.md) | [string](../types/string.md) | [string](../types/string.md) | Concatenates the right string onto the left string and stores the result |
| [date](../types/date.md) | [number](../types/number.md) | [date](../types/date.md) | Adds the right value as days to the left date and stores the new date |

## Precedence

- **Precedence:** Assignment
- **Associativity:** right

## Notes for daily SSL work

!!! success "Do"
    - Use `+=` for in-place numeric totals, counters, and similar accumulators.
    - Use `+=` when repeatedly appending to a string in several steps.
    - Convert values explicitly before concatenation, such as [`LimsString`](../functions/LimsString.md)`(nCount)`.

!!! failure "Don't"
    - Rely on implicit coercion such as string-plus-number. Unsupported type pairs raise runtime errors.
    - Use `+=` with arrays, objects, booleans, or other unsupported operand types.
    - Use `+=` when a full assignment expression would be clearer to the reader.

## Errors and edge cases

- `+=` uses the same type rules as [`+`](plus.md); it does not add any extra coercion.
- `date += number` adds days. To move a date backward, use a negative number or [`subtract-assign`](subtract-assign.md) ([`-=`](subtract-assign.md)).
- A left operand type that does not support [`+`](plus.md) raises a runtime error.
- A valid left operand type with an unsupported right operand raises a runtime error for an invalid operand.

## Examples

### Accumulating a running total

Adds five values from an array into `nTotal` using `+=`. The loop runs five iterations and the final total is 120.

```ssl
:PROCEDURE AccumulateTotal;
    :DECLARE nTotal, nValue, nIndex, aValues;

    nTotal := 0;
    aValues := {10, 25, 40, 15, 30};

    :FOR nIndex := 1 :TO ALen(aValues);
        nValue := aValues[nIndex];
        nTotal += nValue;
    :NEXT;

    UsrMes("Total: " + LimsString(nTotal));

    :RETURN nTotal;
:ENDPROC;

/* Usage;
DoProc("AccumulateTotal");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Total: 120
```

### Building a status message

Assembles a final message from six fragments using `+=` to append each piece in turn.

```ssl
:PROCEDURE BuildStatusMessage;
    :DECLARE sSampleID, sStatus, sMessage, nCount;

    sSampleID := "12345";
    sStatus := "Active";
    nCount := 42;

    sMessage := "Sample ";
    sMessage += sSampleID;
    sMessage += " - ";
    sMessage += sStatus;
    sMessage += " (";
    sMessage += LimsString(nCount);
    sMessage += " items)";

    UsrMes(sMessage);

    :RETURN sMessage;
:ENDPROC;

/* Usage;
DoProc("BuildStatusMessage");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Sample 12345 - Active (42 items)
```

### Scheduling follow-up dates

Advances `dFollowUp` by seven days on each of four iterations using `+=`, then displays the resulting dates starting from 01/15/2024 with a seven-day interval.

```ssl
:PROCEDURE ScheduleFollowUps;
    :DECLARE dCollected, dFollowUp, nIntervalDays, nIndex, aFollowUps;
    :DECLARE sLabel, sDate;

    dCollected := CToD("01/15/2024");
    nIntervalDays := 7;
    aFollowUps := {};

    dFollowUp := dCollected;

    :FOR nIndex := 1 :TO 4;
        dFollowUp += nIntervalDays;
        AAdd(aFollowUps, dFollowUp);
    :NEXT;

    :FOR nIndex := 1 :TO ALen(aFollowUps);
        sLabel := "Follow-up #" + LimsString(nIndex);
        sDate := DToC(aFollowUps[nIndex]);
        UsrMes(sLabel + ": " + sDate);
    :NEXT;

    :RETURN aFollowUps;
:ENDPROC;

/* Usage;
DoProc("ScheduleFollowUps");
```

[`UsrMes`](../functions/UsrMes.md) displays (one line per iteration):

```text
Follow-up #1: 01/22/2024
Follow-up #2: 01/29/2024
Follow-up #3: 02/05/2024
Follow-up #4: 02/12/2024
```

## Related elements

- [`assignment`](assignment.md)
- [`plus`](plus.md)
- [`subtract-assign`](subtract-assign.md)
