---
title: "not-equals"
summary: "Returns .T. when two values are not strictly equal under SSL equality rules."
id: ssl.operator.not-equals
element_type: operator
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# not-equals

## What it does

Returns [`.T.`](../literals/true.md) when two values are not strictly equal under SSL equality rules.

The `!=` operator is SSL's preferred not-equals form. It uses the same strict comparison path as [`strict-equals`](strict-equals.md) ([`==`](strict-equals.md)), then negates the result. Aliases are [`not-equals-legacy`](not-equals-legacy.md) ([`<>`](not-equals-legacy.md)) and [`hash`](hash.md) ([`#`](hash.md)). All three compile to the same behavior.

For strings, `!=` uses exact comparison, not prefix matching. For example, `"Logged" != "Log"` returns [`.T.`](../literals/true.md) because strict equality returns [`.F.`](../literals/false.md). For numbers, booleans, and dates, it compares values directly. For arrays and objects, it compares references rather than walking contents.

Type-mismatch behavior depends on the left operand. A string on the left compared with a non-string on the right returns [`.T.`](../literals/true.md). A numeric, boolean, or date value on the left compared with an incompatible right operand raises a runtime invalid-operand error.

## When to use it

- When exact string inequality is required.
- When checking value inequality on numbers, booleans, and dates.
- When checking reference inequality on arrays and objects.
- When guarding dynamic comparisons where operand types may vary at runtime.

## Syntax

```ssl
bDifferent := vLeft != vRight;
```

## Type behavior

| Left | Right | Result | Behavior |
|------|-------|--------|----------|
| [string](../types/string.md) | [string](../types/string.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the strings are not exactly equal. |
| [string](../types/string.md) | non-string | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md). |
| [number](../types/number.md) | [number](../types/number.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the numeric values differ. |
| [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the boolean values differ. |
| [date](../types/date.md) | [date](../types/date.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the dates differ. |
| [array](../types/array.md) | [array](../types/array.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) unless both operands reference the same array instance. |
| [object](../types/object.md) | [object](../types/object.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) unless both operands reference the same object instance. |
| [`NIL`](../literals/nil.md) | [`NIL`](../literals/nil.md) | [boolean](../types/boolean.md) | Returns [`.F.`](../literals/false.md). |
| [`NIL`](../literals/nil.md) | non-[`NIL`](../literals/nil.md) | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md). |
| code block | any | error | Raises a runtime error. |

## Precedence

- **Precedence:** Equality
- **Associativity:** left

## Notes for daily SSL work

!!! success "Do"
    - Use `!=` in new code when you need strict inequality.
    - Guard dynamic values before comparing when the runtime types may differ.
    - Walk the structure yourself when a deep content comparison is needed for arrays and objects.

!!! failure "Don't"
    - Use `!=` when you want string prefix behavior. `!=` negates strict equality, not [`=`](equals.md).
    - Assume `!=` coerces numbers, booleans, or dates to other types automatically.
    - Mix `!=`, [`<>`](not-equals-legacy.md), and [`#`](hash.md) in the same code path without a style reason.

## Errors and edge cases

- Code block left operand raises `Cannot compare to a code block`.

## Examples

### Comparing exact string values

Checks whether two status strings differ. `"PENDING" != "COMPLETE"` is [`.T.`](../literals/true.md), so the changed branch runs.

```ssl
:PROCEDURE CheckStatusChange;
	:DECLARE sStoredStatus, sCurrentStatus, bChanged, sMessage;

	sStoredStatus := "PENDING";
	sCurrentStatus := "COMPLETE";
	bChanged := sStoredStatus != sCurrentStatus;

	:IF bChanged;
		sMessage := "Status changed from " + sStoredStatus + " to " + sCurrentStatus;
	:ELSE;
		sMessage := "Status did not change";
	:ENDIF;

	UsrMes(sMessage);

	:RETURN bChanged;
:ENDPROC;

/* Usage;
DoProc("CheckStatusChange");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Status changed from PENDING to COMPLETE
```

### Guarding operand types before numeric inequality

Checks runtime types first when a comparison may receive mixed values. With both values numeric, `4 != 3` is [`.T.`](../literals/true.md), and the mismatch branch runs.

```ssl
:PROCEDURE CheckReplicateMismatch;
	:DECLARE nExpected, nActual, sExpectedType, sActualType;
	:DECLARE bMismatch, sMessage;

	nExpected := 3;
	nActual := 4;
	sExpectedType := LimsTypeEx(nExpected);
	sActualType := LimsTypeEx(nActual);
	bMismatch := .F.;

	:IF sExpectedType == "NUMERIC" .AND. sActualType == "NUMERIC";
		bMismatch := nActual != nExpected;

		:IF bMismatch;
			sMessage := "Replicate count differs";
		:ELSE;
			sMessage := "Replicate count matches";
		:ENDIF;
	:ELSE;
		sMessage := "Comparison skipped because both values are not numeric";
	:ENDIF;

	UsrMes(sMessage);

	:RETURN bMismatch;
:ENDPROC;

/* Usage;
DoProc("CheckReplicateMismatch");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Replicate count differs
```

### Comparing object references, then comparing the values you care about

Shows that `!=` on two object variables indicates different instances even when the objects hold the same property values. With `oBaseline:status == oCandidate:status`, the status comparison returns [`.F.`](../literals/false.md).

```ssl
:PROCEDURE CheckSettingsDifference;
	:DECLARE oBaseline, oCandidate, bRefDiff, bStatusDiff, sMessage;

	oBaseline := CreateUdObject({{"status", "ACTIVE"}, {"priority", 1}});
	oCandidate := CreateUdObject({{"status", "ACTIVE"}, {"priority", 1}});

	bRefDiff := oBaseline != oCandidate;
	bStatusDiff := oBaseline:status != oCandidate:status;

	:IF bRefDiff .AND. !bStatusDiff;
		sMessage := "Objects are different instances but have the same status";
	:ELSE;
		:IF bRefDiff .AND. bStatusDiff;
			sMessage := "Objects are different instances and their status differs";
		:ELSE;
			sMessage := "Both variables refer to the same object instance";
		:ENDIF;
	:ENDIF;

	UsrMes(sMessage);

	:RETURN bRefDiff;
:ENDPROC;

/* Usage;
DoProc("CheckSettingsDifference");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Objects are different instances but have the same status
```

## Related elements

- [`equals`](equals.md)
- [`hash`](hash.md)
- [`not-equals-legacy`](not-equals-legacy.md)
