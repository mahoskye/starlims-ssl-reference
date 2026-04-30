---
title: "minus"
summary: "Subtracts numbers, trims trailing spaces before string concatenation, or performs date arithmetic depending on operand types."
id: ssl.operator.minus
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# minus

## What it does

Subtracts numbers, trims trailing spaces before string concatenation, or performs date arithmetic depending on operand types.

The `-` operator supports four binary combinations. With two numbers, it returns the arithmetic difference. With two strings, it trims trailing space characters from the left operand, then appends the right operand. With a date on the left and a number on the right, it returns a new date that is that many days earlier. With two dates, it returns the difference in days as a number.

The operator does not perform implicit type conversion. Mixed-type combinations such as string minus number or number minus date are not supported and raise a runtime error.

## When to use it

- When subtracting one numeric value from another.
- When joining two strings but you want trailing spaces removed from the left operand first.
- When moving a date backward by a known number of days.
- When calculating the day difference between two date values.

## Syntax

```ssl
vLeft - vRight
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [number](../types/number.md) | [number](../types/number.md) | [number](../types/number.md) | Subtracts the right numeric value from the left. |
| [string](../types/string.md) | [string](../types/string.md) | [string](../types/string.md) | Trims trailing spaces from the left operand, then concatenates the right operand. |
| [date](../types/date.md) | [number](../types/number.md) | [date](../types/date.md) | Subtracts the specified number of days from the date. |
| [date](../types/date.md) | [date](../types/date.md) | [number](../types/number.md) | Returns the difference in days between the two dates. |

## Precedence

- **Precedence:** Additive
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Use `-` for exact numeric subtraction when both operands are numbers.
    - Use `-` between strings when you want the left operand's trailing spaces removed before concatenation.
    - Subtract a number from a date to move backward by that many days.
    - Subtract one date from another when you need the day difference as a number.

!!! failure "Don't"
    - Expect `-` to remove characters or substrings from a string. For strings, it only trims trailing spaces from the left operand and then appends the right operand.
    - Rely on implicit coercion between strings, numbers, and dates. Unsupported operand pairs raise a runtime error.
    - Expect `date - date` to return a date. That form returns a numeric day difference.

## Errors and edge cases

- For strings, only trailing space characters on the left operand are trimmed; leading spaces and the right operand are left unchanged.

## Examples

### Subtracting two numbers

Computes the arithmetic difference of 100 and 30.

```ssl
:PROCEDURE SubtractNumbers;
	:DECLARE nMinuend, nSubtrahend, nResult;

	nMinuend := 100;
	nSubtrahend := 30;
	nResult := nMinuend - nSubtrahend;

	UsrMes("100 minus 30 equals " + LimsString(nResult));

	:RETURN nResult;
:ENDPROC;

/* Usage;
DoProc("SubtractNumbers");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
100 minus 30 equals 70
```

### Trimming trailing spaces before joining strings

Shows that `-` trims trailing spaces from the left operand before appending the right operand. `"Sample   "` becomes `"Sample"`, then `"Analysis"` is appended.

```ssl
:PROCEDURE TrimAndJoinStrings;
	:DECLARE sFirst, sSecond, sResult;

	sFirst := "Sample   ";
	sSecond := "Analysis";

	sResult := sFirst - sSecond;

	UsrMes("Joined: [" + sResult + "]");

	:RETURN sResult;
:ENDPROC;

/* Usage;
DoProc("TrimAndJoinStrings");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Joined: [SampleAnalysis]
```

### Subtracting days from a date and computing the interval

Moves `dDueDate` back by 3 days to get a reminder date, then calculates the number of days between today and the due date.

```ssl
:PROCEDURE CalculateDateDifference;
	:DECLARE dDueDate, dReminderDate, dToday, nDaysUntilDue, sMessage;

	dDueDate := CToD("03/15/2024");
	dReminderDate := dDueDate - 3;
	dToday := CToD("03/10/2024");

	nDaysUntilDue := dDueDate - dToday;

	sMessage := "Reminder date: " + DToC(dReminderDate) + ", days until due: " + LimsString(
		nDaysUntilDue);
	UsrMes(sMessage);

	:RETURN nDaysUntilDue;
:ENDPROC;

/* Usage;
DoProc("CalculateDateDifference");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Reminder date: 03/12/2024, days until due: 5
```

## Related elements

- [`subtract-assign`](subtract-assign.md)
- [`plus`](plus.md)
