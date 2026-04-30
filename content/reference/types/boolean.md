---
title: "boolean"
summary: "Represents logical true/false values in SSL."
id: ssl.type.boolean
element_type: type
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# boolean

## What it is

Represents logical true/false values in SSL.

The boolean type holds one of two logical values: [`.T.`](../literals/true.md) or [`.F.`](../literals/false.md). Use booleans for conditions, flags, validation results, and other yes-or-no decisions. Boolean values support logical operators, equality checks, cloning, and JSON serialization. They do not support indexing, ordering operators, or containment.

Boolean values participate in logical expressions with `.AND.`, `.OR.`, and `.NOT.`. In SSL expression evaluation, `.AND.` and `.OR.` short-circuit, so the right-hand expression is only evaluated when needed to determine the result.

Equality on booleans is strict: the other operand must also be a boolean. Comparing a boolean to a string, number, array, or object raises a runtime error rather than returning [`.F.`](../literals/false.md).

[`Empty`](../functions/Empty.md) has a boolean-specific meaning for boolean values. It returns [`.T.`](../literals/true.md) when the value is [`.F.`](../literals/false.md) and [`.F.`](../literals/false.md) when the value is [`.T.`](../literals/true.md), so for booleans it behaves the same as logical negation rather than acting as an "uninitialized" check.

## Creating values

Boolean values are created with the [`.T.`](../literals/true.md) and [`.F.`](../literals/false.md) literals.

```ssl
bFlag := .T.;
bOther := .F.;
```

- **Runtime type:** `LOGIC`
- **Literal syntax:** [`.T.`](../literals/true.md) (true), [`.F.`](../literals/false.md) (false)

## Operators

| Operator | Symbol | Returns | Behavior |
| --- | --- | --- | --- |
| [`and`](../operators/and.md) | `.AND.` | boolean | Logical AND. Returns [`.T.`](../literals/true.md) only when both operands are boolean true. Short-circuits evaluation. |
| [`or`](../operators/or.md) | `.OR.` | boolean | Logical OR. Returns [`.T.`](../literals/true.md) when either operand is boolean true. Short-circuits evaluation. |
| [`not`](../operators/not.md) | `.NOT.` | boolean | Logical negation of a boolean value. [`!`](../operators/not.md) is also supported. |
| [`equals`](../operators/equals.md) | [`=`](../operators/equals.md) | boolean | Equality comparison. Returns [`.T.`](../literals/true.md) when both operands are booleans with the same value. |
| [`strict-equals`](../operators/strict-equals.md) | [`==`](../operators/strict-equals.md) | boolean | Exact equality comparison. For booleans, behaves the same as [`=`](../operators/equals.md). |

## Members

### Properties

| Member | Returns | Description |
| --- | --- | --- |
| `value` | boolean | The stored boolean value. |

### Methods

| Member | Returns | Description |
| --- | --- | --- |
| `And(vValue)` | boolean | Returns the logical AND of this boolean and another boolean value. Raises a runtime error for non-boolean operands. |
| `Or(vValue)` | boolean | Returns the logical OR of this boolean and another boolean value. Raises a runtime error for non-boolean operands. |
| `Not()` | boolean | Returns the negated boolean value. |
| `Eq(vValue)` | boolean | Returns [`.T.`](../literals/true.md) when both operands are booleans with the same value. Raises a runtime error for non-boolean operands. |
| `EqEq(vValue)` | boolean | Exact equality check. For booleans, this behaves the same as `Eq(vValue)`. |
| `IsEmpty()` | boolean | Returns [`.T.`](../literals/true.md) when the boolean is [`.F.`](../literals/false.md) and [`.F.`](../literals/false.md) when the boolean is [`.T.`](../literals/true.md). |
| [`ToJson()`](../functions/ToJson.md) | [string](string.md) | Returns the JSON boolean text `true` or `false`. |
| `clone()` | boolean | Returns a copy of the boolean value. |

## Indexing

- **Supported:** false
- **Behavior:** Not applicable. Boolean values cannot be indexed.

## Notes for daily SSL work

!!! success "Do"
    - Use [`.T.`](../literals/true.md) and [`.F.`](../literals/false.md) explicitly for assignments, comparisons, and return values.
    - Use `.NOT.` or [`!`](../operators/not.md) when you mean logical negation.
    - Use [`==`](../operators/strict-equals.md) when you want exact equality, even though [`=`](../operators/equals.md) and [`==`](../operators/strict-equals.md) behave the same for booleans.

!!! failure "Don't"
    - Use [`Empty`](../functions/Empty.md) as an "initialized" check. On booleans it behaves like negation, not presence testing.
    - Compare booleans directly to numbers or strings such as `.F. = 0` or `.T. = "true"`. Those comparisons raise runtime errors.
    - Use non-boolean values where boolean operators expect [`.T.`](../literals/true.md) or [`.F.`](../literals/false.md).

## Examples

### Checking combined conditions with logical AND

Tracks two readiness flags and combines them with `.AND.`. Both must be [`.T.`](../literals/true.md) for the sample to be publishable.

```ssl
:PROCEDURE CheckSampleStatus;
	:DECLARE bIsReady, bHasResults, bCanPublish, sStatus;

	bIsReady := .T.;
	bHasResults := .T.;

	bCanPublish := bIsReady .AND. bHasResults;

	:IF bCanPublish;
		sStatus := "Ready for review";
	:ELSE;
		sStatus := "Cannot publish yet";
	:ENDIF;

	UsrMes(sStatus);

	:RETURN sStatus;
:ENDPROC;

/* Usage;
DoProc("CheckSampleStatus");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Ready for review
```

### Validation with combined boolean conditions

Guards a sample submission with several independent checks and returns early when any check fails. With `sSampleId = "S-001"`, `nVolume = 50`, and `bCertified = .T.`, all three checks pass and the procedure returns `"Submission valid"`.

```ssl
:PROCEDURE ValidateSampleSubmission;
	:PARAMETERS sSampleId, nVolume, bCertified;
	:DECLARE bIdOk, bVolumeOk, bCertOk;

	bIdOk := Len(sSampleId) > 0;
	bVolumeOk := nVolume > 0 .AND. nVolume <= 1000;
	bCertOk := bCertified == .T.;

	:IF .NOT. bIdOk;
		:RETURN "Missing sample ID";
	:ENDIF;

	:IF .NOT. bVolumeOk;
		:RETURN "Volume out of range";
	:ENDIF;

	:IF .NOT. bCertOk;
		:RETURN "Sample not certified";
	:ENDIF;

	:RETURN "Submission valid";
:ENDPROC;

/* Usage;
DoProc("ValidateSampleSubmission", {"S-001", 50, .T.});
```

### Serializing boolean flags to JSON and restoring state

Packs three boolean flags into a JSON object using [`ToJson()`](../functions/ToJson.md), parses the JSON back with [`FromJson`](../functions/FromJson.md), and validates that each field is a `"LOGIC"` type.

```ssl
:PROCEDURE RoundTripBooleanFlags;
	:DECLARE bActive, bVerified, bLocked;
	:DECLARE sJson, oState, bRestoreOk;

	bActive := .T.;
	bVerified := .F.;
	bLocked := .T.;

	sJson := '{"active":' + bActive:ToJson() +
			 ',"verified":' + bVerified:ToJson() +
			 ',"locked":' + bLocked:ToJson() + '}';

	oState := FromJson(sJson);

	bRestoreOk := (LimsTypeEx(oState:active) == "LOGIC") .AND.
				  (LimsTypeEx(oState:verified) == "LOGIC") .AND.
				  (LimsTypeEx(oState:locked) == "LOGIC");

	:IF bRestoreOk .AND. oState:active .AND. .NOT. oState:verified;
		UsrMes("State restored correctly");
	:ENDIF;

	:RETURN bRestoreOk;
:ENDPROC;

/* Usage;
DoProc("RoundTripBooleanFlags");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
State restored correctly
```

## Related elements

- [`true`](../literals/true.md)
- [`false`](../literals/false.md)
- [`nil`](../literals/nil.md)
- [`Empty`](../functions/Empty.md)
- [`LimsTypeEx`](../functions/LimsTypeEx.md)
