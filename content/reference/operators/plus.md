---
title: "plus"
summary: "Adds numbers, concatenates strings, or adds days to dates depending on operand types."
id: ssl.operator.plus
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# plus

## What it does

Adds numbers, concatenates strings, or adds days to dates depending on operand types.

The `+` operator supports three operand combinations:

- With two numbers, it returns their arithmetic sum.
- With two strings, it concatenates the left string and the right string.
- With a date on the left and a number on the right, it returns a new date offset by that many days.

`+` does not perform implicit type conversion. Mixed-type combinations such as `string + number` or `number + date` are not supported and raise a runtime error. Operand order matters for date arithmetic: `date + number` is supported, but `number + date` is not.

## When to use it

- When adding two numbers, such as calculating totals, sums, or increments.
- When joining two strings together, like assembling names or codes.
- When shifting a date by a day offset, such as moving a due date forward with a positive number or backward with a negative number.

## Syntax

```ssl
left + right
```

## Type behavior

| Left | Right | Result | Behavior |
| --- | --- | --- | --- |
| [number](../types/number.md) | [number](../types/number.md) | [number](../types/number.md) | Adds the two numeric values. |
| [string](../types/string.md) | [string](../types/string.md) | [string](../types/string.md) | Concatenates the two strings. |
| [date](../types/date.md) | [number](../types/number.md) | [date](../types/date.md) | Adds the numeric day offset to the date. |

## Precedence

- **Precedence:** Additive
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Confirm operand types before using `+`, especially in dynamic code.
    - Use `+` only for the supported pairs: `number + number`, `string + string`, and `date + number`.
    - Convert values explicitly before concatenation: `LimsString(nCount)` or `DToC(dDate)`.
    - Keep the date on the left side for date arithmetic.

!!! failure "Don't"
    - Rely on implicit coercion such as `"Count: " + nCount`. Unsupported type pairs raise a runtime error.
    - Use `+` with arrays, objects, booleans, or other unsupported operand types.
    - Assume `number + date` works the same as `date + number`. Date addition is only defined with the date on the left.

## Errors and edge cases

- An empty date on the left produces an empty date result.

## Examples

### Adding two invoice amounts

Computes the total by adding two number values. 150 + 75 = 225.

```ssl
:PROCEDURE CalculateSum;
	:DECLARE nField1, nField2, nResult;

	nField1 := 150;
	nField2 := 75;
	nResult := nField1 + nField2;

	UsrMes("Total charge: " + LimsString(nResult));

	:RETURN nResult;
:ENDPROC;

/* Usage;
DoProc("CalculateSum");
```

`UsrMes` displays:

```text
Total charge: 225
```

### Concatenating a full name from two strings

Joins `sFirstName` and `sLastName` with a space between them.

```ssl
:PROCEDURE ConcatUserNames;
	:DECLARE sFirstName, sLastName, sFullName;

	sFirstName := "Jane";
	sLastName := "Smith";
	sFullName := sFirstName + " " + sLastName;

	UsrMes(sFullName);

	:RETURN sFullName;
:ENDPROC;

/* Usage;
DoProc("ConcatUserNames");
```

`UsrMes` displays:

```text
Jane Smith
```

### Adding days to a date value

Calculates a due date by adding 14 days to a start date. `01/15/2024 + 14` yields `01/29/2024`.

```ssl
:PROCEDURE CalculateDueDate;
	:DECLARE dStart, nLeadDays, dDue;

	dStart := CToD("01/15/2024");
	nLeadDays := 14;
	dDue := dStart + nLeadDays;

	UsrMes("Due date: " + DToC(dDue));

	:RETURN dDue;
:ENDPROC;

/* Usage;
DoProc("CalculateDueDate");
```

`UsrMes` displays:

```text
Due date: 01/29/2024
```

## Related elements

- [`add-assign`](add-assign.md)
- [`minus`](minus.md)
