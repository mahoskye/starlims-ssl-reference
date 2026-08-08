---
title: "date"
summary: "The date type represents calendar-based values in SSL. Use it for date arithmetic, ordering, formatting, and serialization without converting values to strings first."
id: ssl.type.date
element_type: type
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# date

## What it is

The date type represents calendar-based values in SSL. Use it for date arithmetic, ordering, formatting, and serialization without converting values to strings first.

Date values are usually created by date-returning functions such as [`Today`](../functions/Today.md), [`Now`](../functions/Now.md), [`CToD`](../functions/CToD.md), or [`StringToDate`](../functions/StringToDate.md). SSL does not provide a date literal, so you build or parse dates through functions. Dates support adding or subtracting a numeric day offset, subtracting one date from another to get a day count, and comparing two dates with the standard equality and ordering operators. Date values are not indexable.

## Creating values

SSL has no date literal. Create date values with functions that return dates.

```ssl
dToday := Today();
dNow := Now();
dParsed := CToD("04/15/2026");
```

- **Runtime type:** `DATE`
- **Literal syntax:** None. Use [`Today`](../functions/Today.md), [`Now`](../functions/Now.md), [`CToD`](../functions/CToD.md), or [`StringToDate`](../functions/StringToDate.md).

## Operators

| Operator | Symbol | Returns | Behavior |
| --- | --- | --- | --- |
| [`plus`](../operators/plus.md) | [`+`](../operators/plus.md) | date | Adds a numeric day offset and returns a new date. If the left-hand date is empty, the result stays empty. |
| [`minus`](../operators/minus.md) | [`-`](../operators/minus.md) | date or [number](number.md) | Subtracts a numeric day offset and returns a new date, or subtracts one date from another and returns the difference in days. |
| [`equals`](../operators/equals.md) | [`=`](../operators/equals.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) when two dates have the same stored value. |
| [`strict-equals`](../operators/strict-equals.md) | [`==`](../operators/strict-equals.md) | [boolean](boolean.md) | Behaves the same as [`=`](../operators/equals.md) for date values. |
| [`not-equals`](../operators/not-equals.md) | [`!=`](../operators/not-equals.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) when two dates differ. |
| [`less-than`](../operators/less-than.md) | [`<`](../operators/less-than.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) when the left date is earlier than the right date. |
| [`greater-than`](../operators/greater-than.md) | [`>`](../operators/greater-than.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) when the left date is later than the right date. |
| [`less-than-or-equal`](../operators/less-than-or-equal.md) | [`<=`](../operators/less-than-or-equal.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) when the left date is earlier than or equal to the right date. |
| [`greater-than-or-equal`](../operators/greater-than-or-equal.md) | [`>=`](../operators/greater-than-or-equal.md) | [boolean](boolean.md) | Returns [`.T.`](../literals/true.md) when the left date is later than or equal to the right date. |

## Members

| Member | Kind | Returns | Description |
| --- | --- | --- | --- |
| `value` | Property | `date` | Gets or sets the stored date value. |
| `IsEmpty()` | Method | [`boolean`](boolean.md) | Returns [`.T.`](../literals/true.md) when the date is empty, [`.F.`](../literals/false.md) otherwise. |
| `ToString()` | Method | [`string`](string.md) | Formats the date using the default `MM/dd/yyyy` display format. Returns `"  /  /    "` when the date is empty. |
| `ToString(sFormat)` | Method | [`string`](string.md) | Formats the date using a caller-supplied format string. Returns `"  /  /    "` when the date is empty. |
| [`ToJson()`](../functions/ToJson.md) | Method | [`string`](string.md) | Serializes the date to an ISO 8601 date/time string wrapped as JSON text. Returns `null` for empty dates. |
| `clone()` | Method | `date` | Creates a copy of the current date value. |
| `MakeInvariant()` | Method | [`NIL`](../literals/nil.md) | Marks the date as a wall-clock value with no time-zone offset in JSON output. |
| `MakeLocal()` | Method | [`NIL`](../literals/nil.md) | Marks the date as a local-time value so JSON output includes the local offset. |
| `ChangeKind(nKind)` | Method | [`NIL`](../literals/nil.md) | Changes how the stored date is interpreted for later serialization. |

## Calling .NET `DateTime` methods

In addition to the SSL-defined members above, any public method or property on .NET's `System.DateTime` is callable on a non-empty `date` value with the `:` method-call syntax. The runtime forwards `dValue:Name(args)` to the underlying .NET date by name, so the surface is effectively the full `System.DateTime` API.

This is particularly useful for arithmetic that SSL's [`+`](../operators/plus.md) and [`-`](../operators/minus.md) operators do not cover, since those only add or subtract whole-day offsets. `System.DateTime` offers month-aware and year-aware arithmetic — for example `AddMonths(n)`, `AddYears(n)`, `AddHours(n)`, `AddMinutes(n)` — and component accessors such as `Year`, `Month`, `Day`, `DayOfWeek`, and `DayOfYear`.

Empty dates cannot be dispatched through this passthrough. The underlying .NET value of an empty date is `null`, and calling a method on it raises a null-reference error. Always guard with [`Empty`](../functions/Empty.md) before reaching for .NET members.

This passthrough is an interop convenience, not part of the SSL language surface. The members are not declared in SSL and do not appear in editor autocomplete. Prefer the SSL-defined date members and SSL-native date functions for portability, and reserve direct .NET calls for behavior the SSL library does not cover.

### Example: month-aware date arithmetic

Uses .NET's `AddMonths(nMonths)` method to compute a date three months after a start date. SSL's [`+`](../operators/plus.md) operator only adds whole-day offsets, so month-aware arithmetic — which correctly handles end-of-month and leap-year edge cases — is only available through this passthrough.

```ssl
:PROCEDURE ComputeReviewDate;
    :DECLARE dStartDate, dReviewDate;

    dStartDate := CToD("01/31/2026");

    :IF Empty(dStartDate);
        UsrMes("Start date is required");
        :RETURN .F.;
    :ENDIF;

    dReviewDate := dStartDate:AddMonths(3);

    UsrMes(dReviewDate:ToString("MM/dd/yyyy"));

    :RETURN dReviewDate;
:ENDPROC;

/* Usage;
DoProc("ComputeReviewDate");
```

[`UsrMes`](../functions/UsrMes.md) logs:

```text
04/30/2026
```

January 31 plus three months lands on April 30, because April has only 30 days. `AddMonths` clamps to the last day of the target month.

## Indexing

- **Supported:** false
- **Behavior:** Date values do not support `[]` indexing.

## Notes for daily SSL work

!!! success "Do"
    - Check `IsEmpty()` before using a date in business rules or display logic.
    - Use [`+`](../operators/plus.md) and [`-`](../operators/minus.md) with numeric day offsets instead of converting dates to strings.
    - Use date-to-date subtraction when you need a day count.
    - Format output explicitly with `ToString()` or [`DToC`](../functions/DToC.md) when the display format matters.

!!! failure "Don't"
    - Treat a date like a string or number for comparison logic. Use the date comparison operators directly.
    - Assume an empty date behaves like a real scheduled value. Validate with `IsEmpty()` first.
    - Use `[]` indexing on a date. Dates are scalar values, not collections.
    - Assume [`ToJson()`](../functions/ToJson.md) and `ToString()` produce the same output. [`ToJson()`](../functions/ToJson.md) is for JSON serialization, not user-facing display.

## Examples

### Validating a required date

Checks for an empty date before continuing. `CToD("")` returns an empty date, so `IsEmpty()` returns [`.T.`](../literals/true.md) and the procedure exits early.

```ssl
:PROCEDURE ValidateRequiredDate;
    :DECLARE dSubmittedDate, sMessage;

    dSubmittedDate := CToD("");

    :IF dSubmittedDate:IsEmpty();
        UsrMes("Required date is missing");
        :RETURN .F.;
    :ENDIF;

    sMessage := "Date received: " + dSubmittedDate:ToString();
    InfoMes(sMessage);

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ValidateRequiredDate");
```

[`UsrMes`](../functions/UsrMes.md) logs:

```text
Required date is missing
```

### Calculating a due date and days remaining

Adds 14 days to a start date, then compares the due date with today to show days overdue or remaining. Output varies depending on the current date.

```ssl
:PROCEDURE CheckTaskDueDate;
    :DECLARE dToday, dStartDate, dDueDate;
    :DECLARE nDaysRemaining, sMessage;

    dToday := Today();
    dStartDate := CToD("04/01/2026");
    dDueDate := dStartDate + 14;

    :IF dDueDate < dToday;
        nDaysRemaining := dToday - dDueDate;
        sMessage := "Task is overdue by " + LimsString(nDaysRemaining) + " days";
        InfoMes(sMessage);
    :ELSE;
        nDaysRemaining := dDueDate - dToday;
        sMessage := "Task is due in " + LimsString(nDaysRemaining) + " days";
        InfoMes(sMessage);
    :ENDIF;

    sMessage := "Due date: " + dDueDate:ToString("YYYY-MM-DD");
    InfoMes(sMessage);

    :RETURN dDueDate;
:ENDPROC;

/* Usage;
DoProc("CheckTaskDueDate");
```

### Controlling JSON serialization output

Clones the current date twice, marks one as invariant and one as local, then serializes both to show how the output format differs. Output includes the current timestamp and varies each time the example runs.

```ssl
:PROCEDURE ShowDateJsonModes;
    :DECLARE dSourceDate, dInvariantDate, dLocalDate;
    :DECLARE sInvariantJson, sLocalJson;

    dSourceDate := Now();

    dInvariantDate := dSourceDate:clone();
    dInvariantDate:MakeInvariant();
    sInvariantJson := dInvariantDate:ToJson();

    dLocalDate := dSourceDate:clone();
    dLocalDate:MakeLocal();
    sLocalJson := dLocalDate:ToJson();

    InfoMes("Invariant JSON: " + sInvariantJson);
    InfoMes("Local JSON: " + sLocalJson);

    :RETURN;
:ENDPROC;

/* Usage;
DoProc("ShowDateJsonModes");
```

[`InfoMes`](../functions/InfoMes.md) logs (values vary by current date and time zone):

```text
Invariant JSON: "2026-04-23T14:30:00"
Local JSON: "2026-04-23T14:30:00+05:00"
```

## Caveats

- Member access with `:` forwards to the underlying .NET DateTime object when no SSL-side member matches (e.g. `dValue:AddMonths(2)`). A member that is not listed on this page can still be valid — it resolves against the .NET object at runtime instead of raising an unknown-member error.

## Related elements

- [`number`](number.md)
- [`string`](string.md)
- [`boolean`](boolean.md)
