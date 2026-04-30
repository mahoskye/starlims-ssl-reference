---
title: "less-than-or-equal"
summary: "Compares two values of the same supported type and returns .T. when the left operand is less than or equal to the right operand."
id: ssl.operator.less-than-or-equal
element_type: operator
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# less-than-or-equal

## What it does

Compares two values of the same supported type and returns [`.T.`](../literals/true.md) when the left operand is less than or equal to the right operand.

The `<=` operator supports number, date, and string comparisons. Numbers are compared numerically, dates are compared chronologically, and strings are compared with case-sensitive invariant ordering. `<=` includes equality: it returns [`.T.`](../literals/true.md) when the values are equal or when the left operand is smaller.

If the operands are different types, or if the type does not support `<=`, the comparison raises a runtime error instead of returning a boolean value.

## When to use it

- When a threshold check should pass for values below the boundary and for the
  boundary value itself.
- When filtering dates up to a cutoff date, including the cutoff date.
- When comparing string keys using SSL's built-in lexicographic ordering.

## Syntax

```ssl
vLeft <= vRight
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [number](../types/number.md) | [number](../types/number.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the left number is less than or equal to the right number. |
| [date](../types/date.md) | [date](../types/date.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the left date is earlier than or the same as the right date. |
| [string](../types/string.md) | [string](../types/string.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the left string sorts before or exactly matches the right string in case-sensitive invariant order. |

## Precedence

- **Precedence:** Relational
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Use `<=` when equality should pass along with lower values.
    - Make sure both operands are the same supported type before comparing.
    - Treat string comparisons as case-sensitive invariant ordering, not as user-locale sorting.

!!! failure "Don't"
    - Use [`less-than`](less-than.md) when the boundary value should also pass. Use `<=` for inclusive checks.
    - Compare unlike types such as a number and a string. That raises a runtime error instead of returning a boolean value.
    - Rely on `<=` to perform implicit type conversion. Convert values explicitly before comparing them.

## Errors and edge cases

- Either operand being [`NIL`](../literals/nil.md) raises a runtime error instead of returning a boolean value.
- String comparisons are case-sensitive and culture-invariant, which can give results that differ from end-user alphabetical expectations.

## Examples

### Validating an upper numeric limit

Checks whether `nCurrentTemp` stays at or below `nSafeLimit`. With 8.5 <= 10.0, the result is [`.T.`](../literals/true.md) and the within-limit branch runs.

```ssl
:PROCEDURE CheckMaximumTemperature;
	:DECLARE nSafeLimit, nCurrentTemp, bWithinLimit, sMessage;

	nSafeLimit := 10.0;
	nCurrentTemp := 8.5;
	bWithinLimit := nCurrentTemp <= nSafeLimit;

	:IF bWithinLimit;
		sMessage := "Temperature is within the safe limit";
	:ELSE;
		sMessage := "Temperature exceeds the safe limit";
	:ENDIF;

	UsrMes(sMessage + ": " + LimsString(nCurrentTemp));

	:RETURN bWithinLimit;
:ENDPROC;

/* Usage;
DoProc("CheckMaximumTemperature");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Temperature is within the safe limit: 8.5
```

### Accepting records up to a cutoff date

Checks whether `dEntryDate` falls on or before `dCutoff`. With 03/28/2024 <= 03/31/2024, the result is [`.T.`](../literals/true.md) and the within-cutoff branch runs.

```ssl
:PROCEDURE CheckDateCutoff;
	:DECLARE dEntryDate, dCutoff, bIsValid, sMessage;

	dEntryDate := CToD("03/28/2024");
	dCutoff := CToD("03/31/2024");
	bIsValid := dEntryDate <= dCutoff;

	:IF bIsValid;
		sMessage := "Entry date is within the cutoff period";
	:ELSE;
		sMessage := "Entry date exceeds the cutoff period";
	:ENDIF;

	UsrMes(sMessage + ": " + DToC(dEntryDate));

	:RETURN bIsValid;
:ENDPROC;

/* Usage;
DoProc("CheckDateCutoff");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Entry date is within the cutoff period: 03/28/2024
```

### Comparing batch keys against an inclusive boundary

Uses `<=` on strings to check whether a batch key sorts before or at the processing boundary. `"BATCH-042"` is lexicographically less than `"BATCH-100"`, so the result is [`.T.`](../literals/true.md).

```ssl
:PROCEDURE CheckBatchBoundary;
	:DECLARE sBatchId, sBoundary, bInRange, sMessage;

	sBatchId := "BATCH-042";
	sBoundary := "BATCH-100";
	bInRange := sBatchId <= sBoundary;

	:IF bInRange;
		sMessage := "Batch is within the processing boundary";
	:ELSE;
		sMessage := "Batch is beyond the processing boundary";
	:ENDIF;

	UsrMes(sMessage + ": " + sBatchId);

	:RETURN bInRange;
:ENDPROC;

/* Usage;
DoProc("CheckBatchBoundary");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Batch is within the processing boundary: BATCH-042
```

## Related elements

- [`less-than`](less-than.md)
- [`greater-than-or-equal`](greater-than-or-equal.md)
