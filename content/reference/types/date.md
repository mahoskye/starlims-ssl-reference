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

Dates have no SSL-defined `:` members. Calls such as `dValue:IsEmpty()`, `dValue:ToJson()`, `dValue:clone()`, `dValue:MakeInvariant()`, `dValue:MakeLocal()` and `dValue:ChangeKind(n)` raise `Run-time error: Invalid method: …`, and `dValue:value` raises `Invalid property: value`. Work with dates through the operators above, the date functions, and the .NET members below:

| Task | Use |
|---|---|
| Test for an empty date | [`Empty`](../functions/Empty.md) |
| Format as text | [`DToC`](../functions/DToC.md), [`DateToString`](../functions/DateToString.md), or `dValue:ToString(sFormat)`, a .NET member |
| Compact `yyyyMMdd` text | [`DToS`](../functions/DToS.md) |
| Read the year, month or day | [`Year`](../functions/Year.md), [`Month`](../functions/Month.md), [`Day`](../functions/Day.md) |
| Add or subtract days | [`+`](../operators/plus.md) and [`-`](../operators/minus.md) with a number of days |
| Add months or years | [`DateAdd`](../functions/DateAdd.md)`(dValue, n, "month")`, or `dValue:AddMonths(n)` and `dValue:AddYears(n)`, .NET members |
| Serialize to JSON | [`ToJson`](../functions/ToJson.md) |

## Calling .NET `DateTime` methods

Public methods and properties of .NET's `System.DateTime` can be called on a non-empty `date` value with the `:` method-call syntax. Member names are case-sensitive: `dValue:AddDays(1)` and `dValue:Year` work, but `dValue:adddays(1)` raises `Invalid method: adddays` and `dValue:year` raises `Invalid property: year` (see [Member names and case](../../guides/native-members.md#member-names-and-case)).

This is particularly useful for arithmetic that SSL's [`+`](../operators/plus.md) and [`-`](../operators/minus.md) operators do not cover, since those only add or subtract whole-day offsets. `System.DateTime` offers month-aware and year-aware arithmetic — for example `AddMonths(n)`, `AddYears(n)`, `AddHours(n)`, `AddMinutes(n)` — and component accessors such as `Year`, `Month`, `Day`, `DayOfWeek`, and `DayOfYear`.

`dValue:ToString()` with no format gives the date and time in the server's format, such as `9/30/2026 12:00:00 AM`. It is not a fixed `MM/dd/yyyy` form. Pass a format, such as `dValue:ToString("yyyy-MM-dd")`, when the output format matters.

Any member access on an empty date raises an error. Always guard with [`Empty`](../functions/Empty.md) before calling a .NET member.

This passthrough is an interop convenience, not part of the SSL language surface. The members are not declared in SSL and do not appear in editor autocomplete. Prefer SSL-native date functions for portability, and reserve direct .NET calls for behavior the SSL library does not cover. See [Native Members on SSL Values](../../guides/native-members.md) for the members verified on STARLIMS v11 and how to check others.

### Example: month-aware date arithmetic

Uses .NET's `AddMonths(nMonths)` method to compute a date three months after a start date. SSL's [`+`](../operators/plus.md) operator only adds whole-day offsets, so month-aware arithmetic — which correctly handles end-of-month and leap-year edge cases — needs `AddMonths` or [`DateAdd`](../functions/DateAdd.md) with `"month"`.

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
    - Check [`Empty`](../functions/Empty.md) before using a date in business rules or display logic.
    - Use [`+`](../operators/plus.md) and [`-`](../operators/minus.md) with numeric day offsets instead of converting dates to strings.
    - Use date-to-date subtraction when you need a day count.
    - Format output with an explicit format, such as `dValue:ToString("yyyy-MM-dd")`, when the display format matters.

!!! failure "Don't"
    - Treat a date like a string or number for comparison logic. Use the date comparison operators directly.
    - Assume an empty date behaves like a real scheduled value. Validate with [`Empty`](../functions/Empty.md) first.
    - Use `[]` indexing on a date. Dates are scalar values, not collections.
    - Assume `dValue:ToString()` with no format gives `MM/dd/yyyy`. It gives the date and time in the server's format, such as `9/30/2026 12:00:00 AM`.
    - Use [`ToJson`](../functions/ToJson.md) for display. It is for JSON serialization, not user-facing text.

## Examples

### Validating a required date

Checks for an empty date before continuing. `CToD("")` returns an empty date, so [`Empty`](../functions/Empty.md) returns [`.T.`](../literals/true.md) and the procedure exits early.

```ssl
:PROCEDURE ValidateRequiredDate;
    :DECLARE dSubmittedDate, sMessage;

    dSubmittedDate := CToD("");

    :IF Empty(dSubmittedDate);
        UsrMes("Required date is missing");
        :RETURN .F.;
    :ENDIF;

    sMessage := "Date received: " + dSubmittedDate:ToString("yyyy-MM-dd");
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

    sMessage := "Due date: " + dDueDate:ToString("yyyy-MM-dd");
    InfoMes(sMessage);

    :RETURN dDueDate;
:ENDPROC;

/* Usage;
DoProc("CheckTaskDueDate");
```

### Formatting a date with and without a format

Builds a fixed date and formats it three ways. `ToString()` with no format follows the server's date and time settings, so its output varies by server. The explicit format and [`DToS`](../functions/DToS.md) do not.

```ssl
:PROCEDURE ShowDateFormats;
    :DECLARE dSampled, sDefault, sIso, sCompact;

    dSampled := DateFromNumbers(2026, 9, 30);

    sDefault := dSampled:ToString();
    sIso := dSampled:ToString("yyyy-MM-dd");
    sCompact := DToS(dSampled);

    UsrMes("Default: " + sDefault);
    UsrMes("ISO: " + sIso);
    UsrMes("DToS: " + sCompact);

    :RETURN sIso;
:ENDPROC;

/* Usage;
DoProc("ShowDateFormats");
```

[`UsrMes`](../functions/UsrMes.md) logs (the first line varies with the server's settings):

```text
Default: 9/30/2026 12:00:00 AM
ISO: 2026-09-30
DToS: 20260930
```

## Caveats

- A `:` member call on a date reaches a .NET `DateTime` member (e.g. `dValue:AddMonths(2)`). A member that doesn't exist, or doesn't accept the arguments given, raises an error such as `Run-time error: Invalid method: Split`. Check a member before relying on it; see [Native Members](../../guides/native-members.md).

## Related elements

- [`number`](number.md)
- [`string`](string.md)
- [`boolean`](boolean.md)
