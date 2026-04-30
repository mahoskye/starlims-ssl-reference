---
title: "and"
summary: "Combines two boolean expressions and returns .T. only when both are .T.."
id: ssl.operator.and
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# and

## What it does

Combines two boolean expressions and returns [`.T.`](../literals/true.md) only when both are [`.T.`](../literals/true.md).

The `.AND.` operator performs logical conjunction. It evaluates the left operand first and evaluates the right operand only when the left side is [`.T.`](../literals/true.md). This short-circuit behavior makes `.AND.` the standard guard operator for conditions that would be unsafe, unnecessary, or expensive to evaluate unless an earlier check has already passed. In expression parsing, `.AND.` is left-associative and binds more tightly than `.OR.`, so `a .OR. b .AND. c` is interpreted as `a .OR. (b .AND. c)`.

## When to use it

- When multiple boolean conditions must all be true.
- When the right-hand check should run only after a safe precondition passes.
- When a cheap left-hand check can skip an expensive right-hand check.

## Syntax

```ssl
leftBoolean .AND. rightBoolean
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) only when both operands are [`.T.`](../literals/true.md). If the left operand is [`.F.`](../literals/false.md), the right operand is not evaluated. |

## Precedence

- **Precedence:** Higher than [`.OR.`](or.md) and lower than equality and relational comparisons
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Put the cheapest or most likely-false condition on the left so the right side is skipped more often.
    - Use `.AND.` to guard operations that would fail on missing data, such as `! Empty(oSample) .AND. oSample:Status == "COMPLETE"`.
    - Add parentheses when mixing `.AND.` with `.OR.` to make grouping obvious.

!!! failure "Don't"
    - Put an expensive lookup on the left when a simple flag check could reject the condition first.
    - Access a property, method, or array element on the left and expect a later condition to protect it. The left operand always runs.
    - Rely on readers to infer precedence in a long mixed logical expression. Group it explicitly.

## Errors and edge cases

- `.AND.` is a logical operator. Use boolean expressions on both sides.
- Only the right operand is skipped. Any side effects in the left operand still happen.
- `.AND.` is not the integer bitwise AND operator. For bitwise integer operations, use [`_AND`](../functions/_AND.md)`(a, b)`.

## Examples

### Requiring both conditions to pass

Grants access only when both `bIsLoggedIn` and `bIsActive` are [`.T.`](../literals/true.md). With both flags true, `.AND.` evaluates to [`.T.`](../literals/true.md) and the access-granted branch runs.

```ssl
:PROCEDURE CheckAccess;
	:DECLARE bIsLoggedIn, bIsActive, sAccessMessage;

	bIsLoggedIn := .T.;
	bIsActive := .T.;

	:IF bIsLoggedIn .AND. bIsActive;
		sAccessMessage := "Access granted";
	:ELSE;
		sAccessMessage := "Access denied";
	:ENDIF;

	UsrMes(sAccessMessage);

	:RETURN sAccessMessage;
:ENDPROC;

/* Usage;
DoProc("CheckAccess");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Access granted
```

### Guarding a property lookup with a nil check

Short-circuits on the left side when `oSample` is [`NIL`](../literals/nil.md). Because `! Empty(NIL)` is [`.F.`](../literals/false.md), the right-hand property access is never evaluated and `sStatus` stays at its default.

```ssl
:PROCEDURE SafePropertyAccess;
	:DECLARE oSample, oSafeSample, sStatus, bHasSample;

	oSample := NIL;
	sStatus := "Unknown or missing";
	bHasSample := ! Empty(oSample);

	:IF bHasSample;
		oSafeSample := oSample;
	:ENDIF;

	/* The property lookup runs only when the left side confirms a sample is present;
	:IF bHasSample .AND. oSafeSample:Status == "COMPLETE";
		sStatus := "Complete";
	:ENDIF;

	UsrMes("Status: " + sStatus);

	:RETURN sStatus;
:ENDPROC;

/* Usage;
DoProc("SafePropertyAccess");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Status: Unknown or missing
```

### Skipping a database lookup with a cheap guard

Sets `bShouldCheckDb` to [`.F.`](../literals/false.md) so `.AND.` short-circuits before the [`LSearch`](../functions/LSearch.md) call runs. With the guard false, `bSampleReleased` stays [`.F.`](../literals/false.md) and the database is never queried.

```ssl
:PROCEDURE ValidateReleasedSample;
	:DECLARE bShouldCheckDb, bSampleReleased, sSampleID;

	bShouldCheckDb := .F.;
	bSampleReleased := .F.;
	sSampleID := "SMP-1001";

	bSampleReleased := bShouldCheckDb .AND. ! Empty(LSearch("
	    SELECT release_date
	    FROM sample
	    WHERE sample_id = ?
	", "",, {sSampleID}));

	:IF bSampleReleased;
		UsrMes("Sample is released");
	:ELSE;
		UsrMes("Sample is not released or the database check was skipped");
	:ENDIF;

	:RETURN bSampleReleased;
:ENDPROC;

/* Usage;
DoProc("ValidateReleasedSample");
```

## Related elements

- [`or`](or.md)
- [`not`](not.md)
- [`bang`](bang.md)
