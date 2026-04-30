---
title: "MakeDateInvariant"
summary: "Marks a date, or selected date columns in an array, as invariant."
id: ssl.function.makedateinvariant
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# MakeDateInvariant

Marks a date, or selected date columns in an array, as invariant.

`MakeDateInvariant` changes the date kind to invariant for a single date value or for selected columns in an array. It updates the supplied value in place and returns the same date or array. The function changes the date kind metadata only; it does not shift the calendar date or time value.

## When to use

- When a date must be treated as invariant before storage, comparison, or JSON output.
- When imported rows contain date columns that should all use invariant kind.
- When you need the inverse of [`MakeDateLocal`](MakeDateLocal.md) for existing date values.

## Syntax

```ssl
MakeDateInvariant(vDate, [vColumnsIndex])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vDate` | [date](../types/date.md) or [array](../types/array.md) | yes | — | A single date value, a one-dimensional array of dates, or an array of rows containing date values. |
| `vColumnsIndex` | [number](../types/number.md) or [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Required when `vDate` is an array. Use a single column index or an array of column indices to choose which positions to mark as invariant. |

## Returns

**[date](../types/date.md) or [array](../types/array.md)** — The same value passed in, after its date kind is changed to invariant.

- When `vDate` is a single date, the function returns that same date value.
- When `vDate` is an array, the function returns that same array after updating the selected positions.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `vDate` is [`NIL`](../literals/nil.md). | `Argument: vDate cannot be null.` |
| `vDate` is not a date or array. | `Argument: vDate is neither a Date nor an Array.` |
| `vDate` is an array and `vColumnsIndex` is [`NIL`](../literals/nil.md) or omitted. | `Argument: vColumnsIndex cannot be null.` |
| `vColumnsIndex` is not a number or array. | `Argument: vColumnsIndex is neither a Number nor an Array.` |
| A selected position in `vDate` does not contain a date. | `Column: <index> doesn't contain date values.` |

## Best practices

!!! success "Do"
    - Use `MakeDateInvariant(vDate)` for a single date and omit `vColumnsIndex`.
    - Pass explicit column numbers when converting dates inside arrays or rowsets.
    - Pair it with [`IsInvariantDate`](IsInvariantDate.md) when you need to verify the result.

!!! failure "Don't"
    - Pass strings, numbers, or mixed-type target columns. The function raises an error when a selected value is not a date.
    - Omit `vColumnsIndex` when `vDate` is an array. Array input requires a column number or an array of column numbers.
    - Treat this as a time-zone conversion. It changes the date kind only; it does not adjust the stored date or time.

## Caveats

- For array input, missing positions are skipped, but existing selected values must be dates.

## Examples

### Mark a single date as invariant

Mark a converted date as invariant, then verify the result with [`IsInvariantDate`](IsInvariantDate.md).

```ssl
:PROCEDURE NormalizeUserSubmittedDate;
    :DECLARE dUserDate, dInvariantDate, bInvariant;

    dUserDate := CToD("03/15/2024");
    dInvariantDate := MakeDateInvariant(dUserDate);
    bInvariant := IsInvariantDate(dInvariantDate);

    UsrMes("Invariant kind applied: " + LimsString(bInvariant));

    :RETURN dInvariantDate;
:ENDPROC;

/* Usage;
DoProc("NormalizeUserSubmittedDate");
```

[`UsrMes`](UsrMes.md) displays:

```text
Invariant kind applied: True
```

### Mark one date column in a row array as invariant

Mark column 2 (the date column) as invariant in each row and confirm the change with [`IsInvariantDate`](IsInvariantDate.md).

```ssl
:PROCEDURE StandardizeImportedDates;
    :DECLARE aRows, aInvariantRows, nIndex;

    aRows := {
        {"S-001", CToD("01/15/2024"), "Open"},
        {"S-002", CToD("02/20/2024"), "Closed"},
        {"S-003", CToD("03/25/2024"), "Open"}
    };

    aInvariantRows := MakeDateInvariant(aRows, 2);

    :FOR nIndex := 1 :TO ALen(aInvariantRows);
        UsrMes(
            "Row " + LimsString(nIndex) + " date is invariant: " +
            LimsString(IsInvariantDate(aInvariantRows[nIndex, 2]))
        );
        /* Displays each row status;
    :NEXT;

    :RETURN aInvariantRows;
:ENDPROC;

/* Usage;
DoProc("StandardizeImportedDates");
```

### Mark multiple date columns in each row as invariant

Pass `aColumns` as an array of column indexes to mark both date columns (positions 2 and 3) as invariant in a single call.

```ssl
:PROCEDURE PrepareAuditDates;
    :DECLARE aAuditRows, aColumns, aPreparedRows, nIndex;

    aAuditRows := {
        {"AUD-001", CToD("04/01/2024"), CToD("04/03/2024"), "Open"},
        {"AUD-002", CToD("04/02/2024"), CToD("04/04/2024"), "Closed"}
    };
    aColumns := {2, 3};

    aPreparedRows := MakeDateInvariant(aAuditRows, aColumns);

    :FOR nIndex := 1 :TO ALen(aPreparedRows);
        UsrMes(
            aPreparedRows[nIndex, 1] + ": received=" +
            LimsString(IsInvariantDate(aPreparedRows[nIndex, 2])) +
            ", reported=" +
            LimsString(IsInvariantDate(aPreparedRows[nIndex, 3]))
        );
        /* Displays each audit row status;
    :NEXT;

    :RETURN aPreparedRows;
:ENDPROC;

/* Usage;
DoProc("PrepareAuditDates");
```

## Related

- [`IsInvariantDate`](IsInvariantDate.md)
- [`MakeDateLocal`](MakeDateLocal.md)
- [`date`](../types/date.md)
- [`array`](../types/array.md)
