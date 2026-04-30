---
title: "IsInvariantDate"
summary: "Checks whether a date value has an unspecified (invariant) kind."
id: ssl.function.isinvariantdate
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# IsInvariantDate

Checks whether a date value has an unspecified (invariant) kind.

`IsInvariantDate()` returns [`.T.`](../literals/true.md) when `dDate` has an unspecified `DateTimeKind` and [`.F.`](../literals/false.md) when it is local or UTC. Passing [`NIL`](../literals/nil.md) or a non-date value raises an error.

## When to use

- When you need to distinguish between invariant (unspecified) dates and those with a defined context (local or UTC).
- When validating input from sources where date kind may affect downstream logic or data integrity.
- When building workflows that require special handling for uninitialized or default date values.

## Syntax

```ssl
IsInvariantDate(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | The date value to check for an unspecified `DateTimeKind`. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when `dDate` has an unspecified `DateTimeKind`; [`.F.`](../literals/false.md) otherwise.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `Argument: date cannot be null.` |
| `dDate` is not a date value. | `Argument: date must be of date type` |

## Best practices

!!! success "Do"
    - Always validate that your input is a date before calling this function.
    - Use `IsInvariantDate` to clearly separate invariant date logic from local and UTC handling.
    - Combine with [`MakeDateInvariant`](MakeDateInvariant.md) or [`MakeDateLocal`](MakeDateLocal.md) for comprehensive date workflows.

!!! failure "Don't"
    - Assume that user-provided or external values are already of date type — validate before calling to avoid runtime errors.
    - Attempt to infer date kind using property checks or workarounds. This function provides a single-point, reliable check for invariance.
    - Ignore potential default or uninitialized dates in business logic. Unspecified dates can introduce subtle bugs if left unchecked.

## Caveats

- This function does not convert or mutate the input value — it only inspects it.

## Examples

### Block a workflow when the review date is invariant

Call `IsInvariantDate` on a date produced by [`CToD`](CToD.md) with an empty string. An empty date string yields an invariant date, so the [`:IF`](../keywords/IF.md) branch fires and [`ErrorMes`](ErrorMes.md) blocks the workflow. If a proper date were supplied, the [`:ELSE`](../keywords/ELSE.md) branch would fire and [`InfoMes`](InfoMes.md) would display the approval message.

```ssl
:PROCEDURE CheckReviewDateInvariant;
	:DECLARE dReviewDate, bIsInvariant;

	dReviewDate := CToD("");
	bIsInvariant := IsInvariantDate(dReviewDate);

	:IF bIsInvariant;
		ErrorMes("Workflow blocked: review date is uninitialized");
	:ELSE;
		InfoMes("Workflow approved: review date is properly set");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("CheckReviewDateInvariant");
```

### Count user-set versus invariant dates across imported records

Iterate over a list of sample records, each represented as a three-element array of `{dReceived, dAnalyzed, dReported}` dates, and use `IsInvariantDate` to count how many date fields are set versus still invariant. With the data below, three fields have real dates and six are invariant, and the warning fires because `nInvariantDates` is greater than zero.

```ssl
:PROCEDURE ValidateImportedDates;
	:DECLARE aRecords, aDates;
	:DECLARE nIndex, nDateIndex, nUserDates, nInvariantDates, sMsg;

	nUserDates := 0;
	nInvariantDates := 0;

	aRecords := {
		{CToD("04/08/2026"), CToD(""), CToD("")},
		{CToD("04/07/2026"), CToD("04/08/2026"), CToD("")},
		{CToD(""), CToD(""), CToD("")}
	};

	:FOR nIndex := 1 :TO ALen(aRecords);
		aDates := aRecords[nIndex];

		:FOR nDateIndex := 1 :TO ALen(aDates);
			:IF IsInvariantDate(aDates[nDateIndex]);
				nInvariantDates := nInvariantDates + 1;
			:ELSE;
				nUserDates := nUserDates + 1;
			:ENDIF;
		:NEXT;
	:NEXT;

	sMsg := "Imported dates: " + LimsString(nUserDates) + " user-set, "
			+ LimsString(nInvariantDates) + " invariant/unset";
	UsrMes(sMsg);

	:IF nInvariantDates > 0;
		sMsg := "Warning: " + LimsString(nInvariantDates) + " date fields require completion";
		UsrMes(sMsg);
	:ENDIF;

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ValidateImportedDates");
```

## Related

- [`MakeDateInvariant`](MakeDateInvariant.md)
- [`MakeDateLocal`](MakeDateLocal.md)
- [`ValidateDate`](ValidateDate.md)
- [`boolean`](../types/boolean.md)
- [`date`](../types/date.md)
