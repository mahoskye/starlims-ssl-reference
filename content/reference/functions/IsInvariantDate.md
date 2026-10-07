---
title: "IsInvariantDate"
summary: "Checks whether a date value has an unspecified (invariant) kind."
id: ssl.function.isinvariantdate
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# IsInvariantDate

Checks whether a date value has an unspecified (invariant) kind.

`IsInvariantDate()` returns [`.T.`](../literals/true.md) when `dDate` has an unspecified `DateTimeKind` and [`.F.`](../literals/false.md) when it is local or UTC. Passing [`NIL`](../literals/nil.md) or a non-date value raises an error.

## When to use

- When you need to distinguish between invariant (unspecified) dates and those with a defined context (local or UTC).
- When validating input from sources where date kind may affect downstream logic or data integrity.
- When a date should be marked local with [`MakeDateLocal`](MakeDateLocal.md) only if it is still invariant.

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
    - Treat an invariant date as empty or unset. Dates built with [`CToD`](CToD.md) are invariant even when they hold a real date; use [`Empty`](Empty.md) to detect an empty date.

## Caveats

- This function does not convert or mutate the input value — it only inspects it.
- In observed runtime behavior, dates built with [`CToD`](CToD.md) are invariant, both for a real date and for the empty date `CToD("")`. The kind says nothing about whether a date is set.

## Examples

### Mark an invariant review date as local

A date built with [`CToD`](CToD.md) is invariant, even when it holds a real date. The first [`:IF`](../keywords/IF.md) branch fires and [`MakeDateLocal`](MakeDateLocal.md) marks the date local in place, so the second check fires too.

```ssl
:PROCEDURE NormalizeReviewDate;
	:DECLARE dReviewDate;

	dReviewDate := CToD("04/08/2026");

	:IF IsInvariantDate(dReviewDate);
		UsrMes("Review date is invariant, marking it as local");
		MakeDateLocal(dReviewDate);
	:ENDIF;

	:IF .NOT. IsInvariantDate(dReviewDate);
		UsrMes("Review date is now local");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("NormalizeReviewDate");
```

[`UsrMes`](UsrMes.md) logs:

```text
Review date is invariant, marking it as local
Review date is now local
```

### Count local versus invariant dates across imported records

Iterate over a list of sample records, each represented as a three-element array of `{dReceived, dAnalyzed, dReported}` dates, and use `IsInvariantDate` to count how many date fields are local versus invariant. Dates built with [`CToD`](CToD.md) are invariant, and [`MakeDateLocal`](MakeDateLocal.md) marks a date local, so with the data below three fields are local and six are invariant. The warning fires because `nInvariantDates` is greater than zero.

```ssl
:PROCEDURE CountImportedDateKinds;
	:DECLARE aRecords, aDates;
	:DECLARE nIndex, nDateIndex, nLocalDates, nInvariantDates, sMsg;

	nLocalDates := 0;
	nInvariantDates := 0;

	aRecords := {
		{MakeDateLocal(CToD("04/06/2026")), CToD("04/07/2026"), CToD("04/08/2026")},
		{MakeDateLocal(CToD("04/07/2026")), MakeDateLocal(CToD("04/08/2026")), CToD("04/09/2026")},
		{CToD("04/08/2026"), CToD("04/09/2026"), CToD("04/10/2026")}
	};

	:FOR nIndex := 1 :TO ALen(aRecords);
		aDates := aRecords[nIndex];

		:FOR nDateIndex := 1 :TO ALen(aDates);
			:IF IsInvariantDate(aDates[nDateIndex]);
				nInvariantDates := nInvariantDates + 1;
			:ELSE;
				nLocalDates := nLocalDates + 1;
			:ENDIF;
		:NEXT;
	:NEXT;

	sMsg := "Imported dates: " + LimsString(nLocalDates) + " local, "
			+ LimsString(nInvariantDates) + " invariant";
	UsrMes(sMsg);

	:IF nInvariantDates > 0;
		sMsg := "Warning: " + LimsString(nInvariantDates) + " date fields are invariant";
		UsrMes(sMsg);
	:ENDIF;

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("CountImportedDateKinds");
```

## Related

- [`MakeDateInvariant`](MakeDateInvariant.md)
- [`MakeDateLocal`](MakeDateLocal.md)
- [`ValidateDate`](ValidateDate.md)
- [`boolean`](../types/boolean.md)
- [`date`](../types/date.md)
