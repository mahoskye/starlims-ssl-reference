---
title: "greater-than-or-equal"
summary: "Compares two values of the same supported type and returns .T. when the left operand is greater than or equal to the right operand."
id: ssl.operator.greater-than-or-equal
element_type: operator
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# greater-than-or-equal

## What it does

Compares two values of the same supported type and returns [`.T.`](../literals/true.md) when the left operand is greater than or equal to the right operand.

The `>=` operator supports number, date, and string comparisons. Numbers are compared numerically; dates are compared chronologically; strings are compared with case-sensitive invariant ordering. `>=` includes equality: it returns [`.T.`](../literals/true.md) when the values are equal or when the left operand is larger.

If the operands are different types, or if the type does not support `>=`, the comparison raises a runtime error.

## When to use it

- When a threshold check should pass for values above the boundary and for the boundary value itself.
- When filtering dates from a cutoff date forward, including the cutoff date.
- When comparing string keys using SSL's built-in lexicographic ordering.

## Syntax

```ssl
vLeft >= vRight
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [number](../types/number.md) | [number](../types/number.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the left number is greater than or equal to the right number. |
| [date](../types/date.md) | [date](../types/date.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the left date is later than or the same as the right date. |
| [string](../types/string.md) | [string](../types/string.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the left string sorts after or exactly matches the right string in case-sensitive invariant order. |

## Precedence

- **Precedence:** Relational
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Use `>=` when equality should pass along with greater values.
    - Make sure both operands are the same supported type before comparing.
    - Treat string comparisons as case-sensitive invariant ordering, not as user-locale sorting.

!!! failure "Don't"
    - Use [`greater-than`](greater-than.md) ([`>`](greater-than.md)) when the boundary value should also pass. Use `>=` for inclusive checks.
    - Compare unlike types such as a number and a string. That raises a runtime error instead of returning a boolean value.
    - Rely on `>=` to perform implicit type conversion. Convert values explicitly before comparing them.

## Examples

### Validating a minimum passing score

Checks whether `nScore` meets or exceeds `nMinPassing`. With 72 >= 70, the comparison is [`.T.`](../literals/true.md) and the passing branch runs.

```ssl
:PROCEDURE CheckPassingScore;
	:DECLARE nScore, nMinPassing, bIsPassing, sMessage;

	nScore := 72;
	nMinPassing := 70;
	bIsPassing := nScore >= nMinPassing;

	:IF bIsPassing;
		sMessage := "Student passed with a score of " + LimsString(nScore);
	:ELSE;
		sMessage := "Student did not pass. Score: " + LimsString(nScore) + " minimum: " + LimsString(
			nMinPassing);
	:ENDIF;

	UsrMes(sMessage);

	:RETURN bIsPassing;
:ENDPROC;

/* Usage;
DoProc("CheckPassingScore");
```

`UsrMes` displays:

```text
Student passed with a score of 72
```

### Filtering log dates from a cutoff forward

Includes log dates that fall on or after `dReferenceDate`. The cutoff is 01/15/2024, so three of the four entries qualify.

```ssl
:PROCEDURE FilterActivityLogs;
	:DECLARE dReferenceDate, dLogDate, bIsEligible, aLogs, nIndex, nMatchCount;

	dReferenceDate := CToD("01/15/2024");
	aLogs := {
		CToD("01/10/2024"),
		CToD("01/15/2024"),
		CToD("01/20/2024"),
		CToD("02/01/2024")
	};
	nMatchCount := 0;

	:FOR nIndex := 1 :TO ALen(aLogs);
		dLogDate := aLogs[nIndex];
		bIsEligible := dLogDate >= dReferenceDate;

		:IF bIsEligible;
			nMatchCount += 1;
			UsrMes("Included log " + LimsString(nIndex) + " dated " + DToC(dLogDate));
		:ENDIF;
	:NEXT;

	UsrMes("Matching logs: " + LimsString(nMatchCount));

	:RETURN nMatchCount;
:ENDPROC;

/* Usage;
DoProc("FilterActivityLogs");
```

`UsrMes` displays one line per matching log, then the total:

```text
Included log 2 dated 01/15/2024
Included log 3 dated 01/20/2024
Included log 4 dated 02/01/2024
Matching logs: 3
```

### Routing batch IDs from a lexical boundary

Uses string ordering to check whether a batch ID is at or after a boundary. `"BATCH-200"` is lexicographically >= `"BATCH-150"`.

```ssl
:PROCEDURE CheckBatchBoundary;
	:DECLARE sBatchId, sBoundary, bAtOrAfter;

	sBatchId := "BATCH-200";
	sBoundary := "BATCH-150";
	bAtOrAfter := sBatchId >= sBoundary;

	:IF bAtOrAfter;
		UsrMes("Batch " + sBatchId + " is at or after the boundary");
	:ELSE;
		UsrMes("Batch " + sBatchId + " is before the boundary");
	:ENDIF;

	:RETURN bAtOrAfter;
:ENDPROC;

/* Usage;
DoProc("CheckBatchBoundary");
```

`UsrMes` displays:

```text
Batch BATCH-200 is at or after the boundary
```

## Related elements

- [`greater-than`](greater-than.md)
- [`less-than`](less-than.md)
- [`less-than-or-equal`](less-than-or-equal.md)
