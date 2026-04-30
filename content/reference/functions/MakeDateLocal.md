---
title: "MakeDateLocal"
summary: "Sets a date value, or selected date columns in an array, to local date kind in place."
id: ssl.function.makedatelocal
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# MakeDateLocal

Sets a date value, or selected date columns in an array, to local date kind in place.

`MakeDateLocal` updates the supplied value and returns the same value. When `vDate` is a single date, the function changes that date to local kind and returns it. When `vDate` is an array, the function updates only the columns identified by `vColumnsIndex` in each row. It does not create a copy.

For array input, the function accepts either a single column number or an array of column numbers. Empty arrays are returned unchanged. A one-dimensional array is treated as a single row. If a targeted column contains a non-date value, the function raises an error.

Use [`IsInvariantDate`](IsInvariantDate.md) to check whether a date is still invariant, and use [`MakeDateInvariant`](MakeDateInvariant.md) when you need to set the kind back to invariant.

## When to use

- When a date should be treated as local rather than invariant.
- When an array contains date columns that need to be updated in place before later processing.
- When you want to change only specific columns instead of every value in a row.

## Syntax

```ssl
MakeDateLocal(vDate, [vColumnsIndex])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vDate` | [date](../types/date.md) or [array](../types/array.md) | yes | — | The date to update, or an array whose targeted columns contain dates. |
| `vColumnsIndex` | [number](../types/number.md) or [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | The column number, or array of column numbers, to update when `vDate` is an array. Required when `vDate` is an array; ignored for a single date. |

## Returns

**[date](../types/date.md) or [array](../types/array.md)** — The same value passed in, updated in place.

- If `vDate` is a date, the function returns that same date after setting it to local kind.
- If `vDate` is an array, the function returns that same array after updating the targeted date columns.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `vDate` is [`NIL`](../literals/nil.md). | `Argument: vDate cannot be null.` |
| `vDate` is not a date or array. | `Argument: vDate is neither a Date nor an Array.` |
| `vDate` is an array and `vColumnsIndex` is [`NIL`](../literals/nil.md) or omitted. | `Argument: vColumnsIndex cannot be null.` |
| `vColumnsIndex` is not a number or array. | `Argument: vColumnsIndex is neither a Number nor an Array.` |
| A targeted column in `vDate` does not contain a date. | `Column: <index> doesn't contain date values.` |

## Best practices

!!! success "Do"
    - Pass `vColumnsIndex` only when the first argument is an array.
    - Validate that every targeted column contains dates before updating an array in place.
    - Use [`MakeDateInvariant`](MakeDateInvariant.md) when you need the date kind to remain invariant instead of local.

!!! failure "Don't"
    - Assume the function creates a new date or array. It mutates the value you pass in.
    - Pass text, numbers, or mixed columns as date targets.
    - Pass `vColumnsIndex` when working with a single date and expect it to affect behavior.

## Caveats

- If a targeted column position is missing in a row, the function skips it.

## Examples

### Change a single date to local kind

Mark a date invariant, then switch it back to local with `MakeDateLocal`. Both [`UsrMes`](UsrMes.md) calls fire because the two [`:IF`](../keywords/IF.md) conditions are independent.

```ssl
:PROCEDURE DemoteDateToLocal;
	:DECLARE dRunDate;

	dRunDate := CToD("04/15/2024");
	MakeDateInvariant(dRunDate);

	:IF IsInvariantDate(dRunDate);
		UsrMes("The date starts as invariant.");
	:ENDIF;

	MakeDateLocal(dRunDate);

	:IF .NOT. IsInvariantDate(dRunDate);
		UsrMes("The same date value is now marked as local.");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("DemoteDateToLocal");
```

[`UsrMes`](UsrMes.md) displays:

```text
The date starts as invariant.
The same date value is now marked as local.
```

### Update selected date columns in a row array

Mark columns 2 and 3 as invariant, then immediately switch them back to local using the same column index array.

```ssl
:PROCEDURE LocalizeOrderDates;
	:DECLARE aRows, aDateCols;

	aRows := {
		{"ORD-101", CToD("04/01/2024"), CToD("04/03/2024"), "Pending"},
		{"ORD-102", CToD("04/05/2024"), CToD("04/08/2024"), "Released"}
	};

	aDateCols := {2, 3};

	MakeDateInvariant(aRows, aDateCols);
	MakeDateLocal(aRows, aDateCols);

	UsrMes("Selected date columns were updated in place.");

	:RETURN aRows;
:ENDPROC;

/* Usage;
DoProc("LocalizeOrderDates");
```

[`UsrMes`](UsrMes.md) displays:

```text
Selected date columns were updated in place.
```

### Handle a non-date value in a targeted column

Target column 2 which holds a status string rather than a date. `MakeDateLocal` raises an error that is caught and displayed.

```ssl
:PROCEDURE TryLocalizeInvalidColumn;
	:DECLARE aRows, nBadCol, oErr;

	aRows := {
		{CToD("04/01/2024"), "Pending", 100},
		{CToD("04/02/2024"), "Released", 200}
	};

	nBadCol := 2;

	:TRY;
		MakeDateLocal(aRows, nBadCol);
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes(oErr:Description);
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("TryLocalizeInvalidColumn");
```

[`ErrorMes`](ErrorMes.md) displays:

```text
Column: 2 doesn't contain date values.
```

## Related

- [`IsInvariantDate`](IsInvariantDate.md)
- [`MakeDateInvariant`](MakeDateInvariant.md)
- [`date`](../types/date.md)
- [`array`](../types/array.md)
