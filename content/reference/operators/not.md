---
title: "not"
summary: "Performs boolean negation, returning .T. for .F. and .F. for .T.."
id: ssl.operator.not
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# not

## What it does

Performs boolean negation, returning [`.T.`](../literals/true.md) for [`.F.`](../literals/false.md) and [`.F.`](../literals/false.md) for [`.T.`](../literals/true.md).

The `.NOT.` operator is SSL's keyword form of logical negation. It applies to a single boolean operand and returns the opposite boolean value. It is equivalent to [`bang`](bang.md) (`!`), but uses the keyword-style syntax that is often clearer in longer conditions. `.NOT.` works on boolean values and raises a runtime error for other operand types.

`.NOT.` is a unary operator, so it is parsed before [`.AND.`](and.md) and [`.OR.`](or.md) expressions. For compound conditions, wrap the full expression in parentheses: `.NOT. (bReady .AND. bReleased)`.

## When to use it

- When inverting a single boolean flag such as `bIsReady`.
- When negating a compound boolean expression with explicit grouping.
- When the surrounding codebase prefers keyword-style logical operators.

## Syntax

```ssl
.NOT. booleanExpression
.NOT. (compoundExpression)
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| n/a | [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | Returns the logical negation of the operand. `.NOT. .T.` becomes [`.F.`](../literals/false.md), and `.NOT. .F.` becomes [`.T.`](../literals/true.md). |

## Precedence

- **Precedence:** Unary
- **Associativity:** right

## Notes for daily SSL work

!!! success "Do"
    - Use `.NOT.` for clear boolean negation in conditions such as `.NOT. bIsReleased`.
    - Wrap compound expressions in parentheses: `.NOT. (bReady .AND. bReleased)`.
    - Keep `.NOT.` for boolean logic only; convert or compare values to booleans before negating.

!!! failure "Don't"
    - Apply `.NOT.` to strings, numbers, arrays, objects, or dates. It only supports boolean operands.
    - Rely on readers to infer grouping in longer expressions. Add parentheses around the expression being negated.
    - Confuse `.NOT.` with [`_NOT()`](../functions/_NOT.md), which is the bitwise integer operation rather than logical negation.

## Errors and edge cases

- `.NOT.` is a prefix unary operator, not a postfix operator.
- Double negation such as `.NOT. .NOT. bFlag` is valid and evaluates back to the original boolean value.

## Examples

### Inverting a readiness flag

Sets `bCanStart` to the opposite of `bIsReady`. With `bIsReady = .F.`, the result is [`.T.`](../literals/true.md) and the ready branch runs.

```ssl
:PROCEDURE CheckReadyState;
	:DECLARE bIsReady, bCanStart, sMessage;

	bIsReady := .F.;
	bCanStart := .NOT. bIsReady;

	:IF bCanStart;
		sMessage := "Sample can start";
	:ELSE;
		sMessage := "Sample is still blocked";
	:ENDIF;

	UsrMes(sMessage);

	:RETURN bCanStart;
:ENDPROC;

/* Usage example;
DoProc("CheckReadyState");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Sample can start
```

### Negating a compound release check

Wraps the compound condition in parentheses so `.NOT.` applies to both flags together. With `bIsComplete = .T.` and `bIsReleased = .F.`, the compound is [`.F.`](../literals/false.md) and `.NOT.` produces [`.T.`](../literals/true.md).

```ssl
:PROCEDURE ValidateRelease;
	:DECLARE sSampleID, bIsComplete, bIsReleased, sMessage;

	sSampleID := "LAB-2024-0042";
	bIsComplete := .T.;
	bIsReleased := .F.;

	:IF .NOT. (bIsComplete .AND. bIsReleased);
		sMessage := "Sample " + sSampleID + " is not ready for release";
		UsrMes(sMessage);

		:RETURN .F.;
	:ENDIF;

	UsrMes("Sample " + sSampleID + " is ready for release");

	:RETURN .T.;
:ENDPROC;

/* Usage example;
DoProc("ValidateRelease");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Sample LAB-2024-0042 is not ready for release
```

### Checking whether a result text is present

Uses `.NOT. Empty(sResultText)` to test whether a result text was populated. With `sResultText = "PASS"`, [`Empty`](../functions/Empty.md) returns [`.F.`](../literals/false.md) and `.NOT.` flips it to [`.T.`](../literals/true.md), so `bIsApproved` is [`.T.`](../literals/true.md).

```ssl
:PROCEDURE CheckSampleForApproval;
	:DECLARE sSampleID, sStatus, sResultText, sMessage;
	:DECLARE bHasResult, bIsApproved;

	sSampleID := "LAB-2024-0042";
	sStatus := "COMPLETE";
	sResultText := "PASS";

	bHasResult := .NOT. Empty(sResultText);
	bIsApproved := sStatus == "COMPLETE" .AND. bHasResult;

	:IF .NOT. bIsApproved;
		sMessage := "Sample " + sSampleID + " cannot be approved yet";
		UsrMes(sMessage);

		:RETURN .F.;
	:ENDIF;

	UsrMes("Sample " + sSampleID + " is ready for approval");

	:RETURN .T.;
:ENDPROC;

/* Usage example;
DoProc("CheckSampleForApproval");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Sample LAB-2024-0042 is ready for approval
```

## Related elements

- [`and`](and.md)
- [`or`](or.md)
- [`bang`](bang.md)
