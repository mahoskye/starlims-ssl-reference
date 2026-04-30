---
title: "Empty"
summary: "Returns .T. when a value is considered empty by SSL; otherwise returns .F."
id: ssl.function.empty
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Empty

Returns [`.T.`](../literals/true.md) when a value is considered empty by SSL, otherwise [`.F.`](../literals/false.md).

`Empty()` applies SSL's built-in emptiness rules to a single value. It returns [`.T.`](../literals/true.md) for [`NIL`](../literals/nil.md), trimmed-empty strings, numeric `0`, boolean [`.F.`](../literals/false.md), empty dates, and arrays with no elements. It returns [`.F.`](../literals/false.md) for regular object instances, even when they have no custom properties.

## When to use

- When you need one check that works across strings, numbers, dates, booleans, arrays, and [`NIL`](../literals/nil.md).
- When validating input before saving data or running business logic.
- When you want to reject blank strings that contain only spaces, tabs, or line breaks.
- When you need to distinguish an empty array from an array that contains data.

## Syntax

```ssl
Empty(vValue)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vValue` | any | yes | — | Value to test with SSL's built-in emptiness rules. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when `vValue` is empty by SSL rules; otherwise [`.F.`](../literals/false.md).

| Input kind | `Empty()` result | Notes |
|------------|------------------|-------|
| [`NIL`](../literals/nil.md) | [`.T.`](../literals/true.md) | Passing [`NIL`](../literals/nil.md) returns true. |
| String | [`.T.`](../literals/true.md) when the string is empty after trimming spaces, tabs, carriage returns, and line feeds | `"   "` and an empty string both return [`.T.`](../literals/true.md). |
| Number | [`.T.`](../literals/true.md) when the value is `0` | Non-zero numbers return [`.F.`](../literals/false.md). |
| Boolean | [`.T.`](../literals/true.md) when the value is [`.F.`](../literals/false.md) | [`.T.`](../literals/true.md) returns [`.F.`](../literals/false.md). |
| Date | [`.T.`](../literals/true.md) when the value is an empty date | This is the same empty-date state used by date functions such as [`CToD`](CToD.md). |
| Array | [`.T.`](../literals/true.md) when the array has no elements | An array containing values returns [`.F.`](../literals/false.md), even if some elements are empty. |
| Object | [`.F.`](../literals/false.md) for regular object instances | Use explicit property checks when you need to validate object content. |

## Best practices

!!! success "Do"
    - Use `Empty()` for general-purpose validation when the value type may vary.
    - Use `Empty()` after parsing or lookup operations that return empty dates, blank strings, or empty arrays.
    - Combine `Empty()` with explicit object-property checks when validating structured objects.

!!! failure "Don't"
    - Assume `Empty()` treats every object with no visible data as empty. Regular SSL objects still return [`.F.`](../literals/false.md).
    - Use only a null check when SSL also treats `0`, [`.F.`](../literals/false.md), blank strings, and empty dates as empty.
    - Use `Empty()` when `0` or [`.F.`](../literals/false.md) are meaningful business values that must stay distinct from missing input.

## Examples

### Block save when a required note is blank

Use `Empty()` to reject a note that is empty or contains only whitespace.

```ssl
:PROCEDURE ValidateSampleNote;
	:DECLARE sSampleID, sUserNote, bCanSave;

	sSampleID := "LAB-2024-0042";
	sUserNote := "   ";
	bCanSave := .T.;

	:IF Empty(sUserNote);
		bCanSave := .F.;
		UsrMes("Sample " + sSampleID + " requires a note before saving");
	:ENDIF;

	:RETURN bCanSave;
:ENDPROC;

/* Usage;
DoProc("ValidateSampleNote");
```

[`UsrMes`](UsrMes.md) displays:

```text
Sample LAB-2024-0042 requires a note before saving
```

### Keep only meaningful values from mixed input

Filter out values that SSL treats as empty, including [`NIL`](../literals/nil.md), `0`, [`.F.`](../literals/false.md), and blank strings.

```ssl
:PROCEDURE FilterMeaningfulValues;
	:DECLARE aInput, aKept, vValue, sSummary;
	:DECLARE nKept, nIndex;

	aInput := {"Active", 0, .F., "", "Pending", NIL, 42, .T., "  "};
	aKept := {};
	nKept := 0;

	:FOR nIndex := 1 :TO ALen(aInput);
		vValue := aInput[nIndex];

		:IF !Empty(vValue);
			AAdd(aKept, vValue);
			nKept += 1;
		:ENDIF;
	:NEXT;

	sSummary := "Kept " + LimsString(nKept) + " of "
				+ LimsString(ALen(aInput)) + " input values";

	UsrMes(sSummary);

	:RETURN aKept;
:ENDPROC;

/* Usage;
DoProc("FilterMeaningfulValues");
```

[`UsrMes`](UsrMes.md) displays:

```text
Kept 4 of 9 input values
```

### Validate optional workflow inputs by type

Use `Empty()` for strings, dates, and arrays, but validate object content with property checks instead of assuming an object itself will be empty. With the sample inputs here, `dDueDate` is empty, so the procedure returns [`.F.`](../literals/false.md) after displaying the due-date message.

```ssl
:PROCEDURE ValidateWorkflowInputs;
	:DECLARE sStepName, dDueDate, aTests, oOwner, sMessage;

	sStepName := "Review Sample";
	dDueDate := CToD("");
	aTests := {};
	oOwner := CreateUdObject();

	oOwner:DisplayName := "";

	:IF Empty(sStepName);
		UsrMes("Step name is required");
		:RETURN .F.;
	:ENDIF;

	:IF Empty(dDueDate);
		UsrMes("Due date is required");
		:RETURN .F.;
	:ENDIF;

	:IF Empty(aTests);
		UsrMes("At least one test is required");
		:RETURN .F.;
	:ENDIF;

	:IF !HasProperty(oOwner, "DisplayName") .OR. Empty(oOwner:DisplayName);
		UsrMes("Owner display name is required");
		:RETURN .F.;
	:ENDIF;

	sMessage := "Workflow inputs are complete";
	UsrMes(sMessage);

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ValidateWorkflowInputs");
```

## Related

- [`CToD`](CToD.md)
- [`HasProperty`](HasProperty.md)
- [`IsDefined`](IsDefined.md)
- [`Nothing`](Nothing.md)
- [`boolean`](../types/boolean.md)
