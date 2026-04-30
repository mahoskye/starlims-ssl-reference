---
title: "Month"
summary: "Extracts the numeric month from a date value."
id: ssl.function.month
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Month

Extracts the numeric month from a date value.

`Month()` returns the month component of a date as a number. For a valid date, the result is `1` through `12`. If the input is an empty date, the function returns `0`. Passing [`NIL`](../literals/nil.md) or a value that is not a date raises an error.

## When to use

- When you need the numeric month for filtering, grouping, or comparisons.
- When applying calendar rules such as quarter checks or seasonal workflows.
- When combining month checks with [`Year`](Year.md) so records from different years do not get mixed together.

## Syntax

```ssl
Month(dDate)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `dDate` | [date](../types/date.md) | yes | — | The date value from which to extract the month number. |

## Returns

**[number](../types/number.md)** — Returns `1` to `12` for a valid date, or `0` when `dDate` is an empty date.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `dDate` is [`NIL`](../literals/nil.md). | `Argument: dDate cannot be null.` |
| `dDate` is not a date value. | `Argument: dDate must be of date type` |

## Best practices

!!! success "Do"
    - Use `Month()` when you need a numeric month value for logic or reporting.
    - Treat a return value of `0` as an empty date case.
    - Pair `Month()` with [`Year`](Year.md) when records can span multiple years.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) or non-date values. `Month()` raises an error instead of converting them.
    - Treat `0` as a real month number. It only indicates an empty date.
    - Group only by month when year also matters. `March 2024` and `March 2025` are different buckets.

## Caveats

- `Month()` returns only the numeric month. Use [`CMonth`](CMonth.md) when you need the month name instead.

## Examples

### Get the month number from a date

Extract the month from a known date and display it. `CToD("03/15/2024")` falls in March, so `Month()` returns `3`.

```ssl
:PROCEDURE GetReceiveMonth;
    :DECLARE dReceiveDate, nMonth;

    dReceiveDate := CToD("03/15/2024");
    nMonth := Month(dReceiveDate);

    UsrMes("Received in month " + LimsString(nMonth));

    :RETURN nMonth;
:ENDPROC;

/* Usage;
DoProc("GetReceiveMonth");
```

[`UsrMes`](UsrMes.md) displays:

```text
Received in month 3
```

### Guard against an empty date before using the month value

`CToD("")` produces an empty date, which `Month()` converts to `0`. The guard on `nMonth == 0` routes that case to a safe message instead of treating `0` as a valid month.

```ssl
:PROCEDURE CheckReviewMonth;
    :DECLARE dReviewDate, nMonth;

    dReviewDate := CToD("");
    nMonth := Month(dReviewDate);

    :IF nMonth == 0;
        UsrMes(
            "No month is available because the date is empty"
        );  /* Displays the empty-date message;
    :ELSE;
        UsrMes("Review month is " + LimsString(nMonth));  /* Displays the month number when present;
    :ENDIF;

    :RETURN nMonth;
:ENDPROC;

/* Usage;
DoProc("CheckReviewMonth");
```

### Filter records for a target month and year

Use the defaults (`nTargetMonth = 3`, `nTargetYear = 2024`) to filter four sample runs. Two runs fall in March 2024; the March 2025 run and the April 2024 run are excluded.

```ssl
:PROCEDURE FilterRunsByMonthYear;
    :PARAMETERS nTargetMonth, nTargetYear;
    :DEFAULT nTargetMonth, 3;
    :DEFAULT nTargetYear, 2024;
    :DECLARE aRuns, aMatches, nIndex, dRunDate;

    aRuns := {
        {"RUN-001", CToD("03/15/2024")},
        {"RUN-002", CToD("03/20/2024")},
        {"RUN-003", CToD("03/05/2025")},
        {"RUN-004", CToD("04/01/2024")}
    };
    aMatches := {};

    :FOR nIndex := 1 :TO ALen(aRuns);
        dRunDate := aRuns[nIndex, 2];

        :IF Month(dRunDate) == nTargetMonth
            .AND. Year(dRunDate) == nTargetYear;
            AAdd(aMatches, aRuns[nIndex, 1]);
        :ENDIF;
    :NEXT;

    UsrMes(
        "Found "
        + LimsString(ALen(aMatches))
        + " run(s) for "
        + LimsString(nTargetMonth)
        + "/"
        + LimsString(nTargetYear)
    );

    :RETURN aMatches;
:ENDPROC;

/* Usage;
DoProc("FilterRunsByMonthYear");
```

[`UsrMes`](UsrMes.md) displays:

```text
Found 2 run(s) for 3/2024
```

## Related

- [`CMonth`](CMonth.md)
- [`DOW`](DOW.md)
- [`DOY`](DOY.md)
- [`Day`](Day.md)
- [`JDay`](JDay.md)
- [`NoOfDays`](NoOfDays.md)
- [`Year`](Year.md)
- [`number`](../types/number.md)
- [`date`](../types/date.md)
