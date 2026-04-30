---
title: "greater-than"
summary: "Compares two values of the same supported type and returns .T. when the left operand is strictly greater than the right operand."
id: ssl.operator.greater-than
element_type: operator
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# greater-than

## What it does

Compares two values of the same supported type and returns [`.T.`](../literals/true.md) when the left operand is strictly greater than the right operand.

The `>` operator supports number, date, and string comparisons. Numbers are compared numerically; dates are compared chronologically; strings are compared with case-sensitive invariant ordering. `>` returns [`.T.`](../literals/true.md) only when the left operand sorts after the right operand.

If the operands are different types, or if the type does not support `>`, the comparison raises a runtime error instead of returning a boolean value.

## When to use it

- When a value must be strictly above a numeric threshold.
- When checking whether one date occurs after another.
- When comparing string keys with SSL's built-in case-sensitive ordering.

## Syntax

```ssl
vLeft > vRight
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [number](../types/number.md) | [number](../types/number.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the left number is greater than the right number. |
| [date](../types/date.md) | [date](../types/date.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the left date is later than the right date. |
| [string](../types/string.md) | [string](../types/string.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the left string sorts after the right string in case-sensitive invariant order. |

## Precedence

- **Precedence:** Relational
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Use `>` only with matching supported types: number, date, or string.
    - Use [`greater-than-or-equal`](greater-than-or-equal.md) when the boundary value should also pass.
    - Validate or normalize input before comparing dynamic values.

!!! failure "Don't"
    - Rely on implicit type conversion between strings, numbers, or dates. `>` raises a runtime error for mismatched types.
    - Use `>` when equality should pass. Use [`greater-than-or-equal`](greater-than-or-equal.md) for inclusive checks.
    - Assume string ordering follows user-locale rules. SSL uses case-sensitive invariant ordering.

## Errors and edge cases

- Either operand being [`NIL`](../literals/nil.md) raises a runtime error instead of returning a boolean.
- String comparisons are case-sensitive and culture-invariant, which can give results that differ from end-user alphabetical expectations.

## Examples

### Checking a numeric threshold

Compares `nUserInput` against `nMinimumThreshold`. With 75 > 50, the result is [`.T.`](../literals/true.md) and the exceeds branch runs.

```ssl
:PROCEDURE CheckMinimumThreshold;
	:DECLARE nUserInput, nMinimumThreshold, bExceedsMinimum, sResult;

	nUserInput := 75;
	nMinimumThreshold := 50;
	bExceedsMinimum := nUserInput > nMinimumThreshold;

	:IF bExceedsMinimum;
		sResult := "Input exceeds the minimum threshold";
	:ELSE;
		sResult := "Input does not exceed the minimum threshold";
	:ENDIF;

	UsrMes(sResult);

	:RETURN bExceedsMinimum;
:ENDPROC;

/* Usage;
DoProc("CheckMinimumThreshold");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Input exceeds the minimum threshold
```

### Checking whether a due date has passed

Compares a current date against a deadline. With 04/20/2026 > 04/15/2026, `bOverdue` is [`.T.`](../literals/true.md) and the overdue branch runs.

```ssl
:PROCEDURE CheckDeadline;
	:DECLARE dCurrentDate, dDueDate, bOverdue, sStatusMessage;

	dCurrentDate := CToD("04/20/2026");
	dDueDate := CToD("04/15/2026");
	bOverdue := dCurrentDate > dDueDate;

	:IF bOverdue;
		sStatusMessage := "The item is overdue. Deadline: " + DToC(dDueDate);
	:ELSE;
		sStatusMessage := "The item is still on track. Deadline: " + DToC(dDueDate);
	:ENDIF;

	InfoMes(sStatusMessage);

	:RETURN bOverdue;
:ENDPROC;

/* Usage;
DoProc("CheckDeadline");
```

[`InfoMes`](../functions/InfoMes.md) displays:

```text
The item is overdue. Deadline: 04/15/2026
```

### Comparing string keys

Uses `>` to test whether one batch key sorts after another. `"BATCH-200"` is lexicographically greater than `"BATCH-150"` because `"2"` > `"1"`.

```ssl
:PROCEDURE CompareBatchKeys;
	:DECLARE sBatchId, sBoundary, bIsAfterBoundary, sMessage;

	sBatchId := "BATCH-200";
	sBoundary := "BATCH-150";
	bIsAfterBoundary := sBatchId > sBoundary;

	:IF bIsAfterBoundary;
		sMessage := "Batch " + sBatchId + " is after the boundary";
	:ELSE;
		sMessage := "Batch " + sBatchId + " is not after the boundary";
	:ENDIF;

	InfoMes(sMessage);

	:RETURN bIsAfterBoundary;
:ENDPROC;

/* Usage;
DoProc("CompareBatchKeys");
```

[`InfoMes`](../functions/InfoMes.md) displays:

```text
Batch BATCH-200 is after the boundary
```

## Related elements

- [`greater-than-or-equal`](greater-than-or-equal.md)
- [`less-than`](less-than.md)
- [`less-than-or-equal`](less-than-or-equal.md)
