---
title: "date"
summary: "The date type represents calendar-based values in SSL. Use it for date arithmetic, ordering, formatting, and serialization without converting values to strings first."
id: ssl.type.date
element_type: type
status: published
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

[`UsrMes`](../functions/UsrMes.md) displays:

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

[`InfoMes`](../functions/InfoMes.md) displays (values vary by current date and time zone):

```text
Invariant JSON: "2026-04-23T14:30:00"
Local JSON: "2026-04-23T14:30:00+05:00"
```

## Related elements

- [`number`](number.md)
- [`string`](string.md)
- [`boolean`](boolean.md)
