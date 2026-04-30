---
title: "or"
summary: "Combines two boolean expressions and returns .T. when either operand is .T.."
id: ssl.operator.or
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# or

## What it does

Combines two boolean expressions and returns [`.T.`](../literals/true.md) when either operand is [`.T.`](../literals/true.md).

The `.OR.` operator performs logical disjunction. It evaluates the left operand first and evaluates the right operand only when the left side is [`.F.`](../literals/false.md). This short-circuit behavior makes `.OR.` useful when one successful check is enough to satisfy the condition, or when a cheap left-hand check can avoid a more expensive fallback.

`.OR.` is left-associative and binds less tightly than [`.AND.`](and.md), so `a .OR. b .AND. c` is interpreted as `a .OR. (b .AND. c)`. `.OR.` is a logical operator — for bitwise integer operations see [`_OR()`](../functions/_OR.md).

## When to use it

- When at least one of several boolean conditions should allow the branch to continue.
- When a fast local check should avoid a slower fallback check when it already succeeds.
- When combining alternative permission, status, or validation flags.

## Syntax

```ssl
leftBoolean .OR. rightBoolean
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when either operand is [`.T.`](../literals/true.md). If the left operand is [`.T.`](../literals/true.md), the right operand is not evaluated. |

## Precedence

- **Precedence:** Logical OR
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Put the cheapest or most likely-true condition on the left so the right side is skipped more often.
    - Use `.OR.` for fallback checks where one successful condition is enough, such as `bIsLocal .OR. bHasRemoteAccess`.
    - Add parentheses when mixing `.OR.` with `.AND.` to make grouping obvious.

!!! failure "Don't"
    - Use `.OR.` with strings, numbers, arrays, objects, dates, or [`NIL`](../literals/nil.md). It only supports boolean operands.
    - Put required side-effect code on the right and expect it always to run. A true left operand skips it.
    - Use `.OR.` when every condition must pass. That is an [`.AND.`](and.md) case instead.

## Errors and edge cases

- Either operand being non-boolean raises a runtime error.

## Examples

### Allowing either of two access flags

Grants access when either `bIsAdmin` or `bHasOverride` is [`.T.`](../literals/true.md). With `bIsAdmin = .T.`, the left side is [`.T.`](../literals/true.md) and `bHasOverride` is not evaluated.

```ssl
:PROCEDURE CheckAccessPermission;
	:DECLARE bIsAdmin, bHasOverride, bCanAccess, sMessage;

	bIsAdmin := .T.;
	bHasOverride := .F.;
	bCanAccess := bIsAdmin .OR. bHasOverride;

	:IF bCanAccess;
		sMessage := "Access granted";
	:ELSE;
		sMessage := "Access denied";
	:ENDIF;

	UsrMes(sMessage);

	:RETURN bCanAccess;
:ENDPROC;

/* Usage;
DoProc("CheckAccessPermission");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Access granted
```

### Using a fallback when the primary search finds nothing

Considers a sample found when it appears in either the current results or the archive. With `bLocalFound = .F.` and `bArchiveFound = .T.`, the `.OR.` is [`.T.`](../literals/true.md).

```ssl
:PROCEDURE CheckSamplePresence;
	:DECLARE sSampleID, bLocalFound, bArchiveFound, bSampleFound, sMessage;

	sSampleID := "DEMO-001";
	bLocalFound := .F.;  /* not in current results;
	bArchiveFound := .T.;  /* found in archive;

	bSampleFound := bLocalFound .OR. bArchiveFound;

	:IF bSampleFound;
		sMessage := "Sample " + sSampleID + " was found";
	:ELSE;
		sMessage := "Sample " + sSampleID + " was not found";
	:ENDIF;

	UsrMes(sMessage);

	:RETURN bSampleFound;
:ENDPROC;

/* Usage;
DoProc("CheckSamplePresence");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Sample DEMO-001 was found
```

### Skipping a fallback query when the local check already passes

Places the local boolean check on the left so the archive query runs only when the current status is not already acceptable. With `sCurrentStatus = "READY"`, `bIsReadyNow` is [`.T.`](../literals/true.md) and the `.OR.` short-circuits without running the query.

```ssl
:PROCEDURE AllowProcessing;
	:DECLARE sSampleID, sCurrentStatus;
	:DECLARE bIsReadyNow, bCanProcess;

	sSampleID := "LAB-2024-0042";
	sCurrentStatus := "READY";

	bIsReadyNow := sCurrentStatus == "READY";

	bCanProcess := bIsReadyNow .OR. !Empty(LSearch("
	    SELECT status
	    FROM sample_audit
	    WHERE sample_id = ?
	      AND status = ?
	", "",, {sSampleID, "READY"}));

	:IF !bCanProcess;
		UsrMes("Sample " + sSampleID + " is not ready to process");

		:RETURN .F.;
	:ENDIF;

	UsrMes("Processing can continue");

	:RETURN bCanProcess;
:ENDPROC;

/* Usage;
DoProc("AllowProcessing");
```

[`UsrMes`](../functions/UsrMes.md) displays (`bIsReadyNow` is [`.T.`](../literals/true.md), so the [`LSearch`](../functions/LSearch.md) is never executed):

```
Processing can continue
```

## Related elements

- [`and`](and.md)
- [`not`](not.md)
- [`bang`](bang.md)
