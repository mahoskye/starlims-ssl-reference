---
title: "LSelect"
summary: "Executes a SQL SELECT statement and returns the result as a two-dimensional SSL array."
id: ssl.function.lselect
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LSelect

Executes a SQL `SELECT` statement and returns the result as a two-dimensional SSL array.

`LSelect` runs a query using positional `?` placeholders and returns one array element per row, with each row represented as an array of column values. `LSelect` only works when `aFieldList` is omitted. If you pass a value for `aFieldList`, the call raises an error instead of filtering the returned columns.

`sConnectionName` defaults to the standard database connection when omitted. `bNullAsBlank` defaults to [`.T.`](../literals/true.md). `aInvariantDateCols` can identify date columns by name or by 1-based column index.

## When to use

- When you need rows and columns returned as an SSL array rather than one scalar value.
- When your SQL uses positional `?` placeholders and you want to bind values through `aArrayOfValues`.
- When you want control over how database `NULL` values and date columns are surfaced in the returned array.
- When the current `LSelect` behavior is sufficient and you are not relying on the unimplemented `aFieldList` argument.

## Syntax

```ssl
LSelect(sCommandString, [aFieldList], [sConnectionName], [aArrayOfValues], [bNullAsBlank], [aInvariantDateCols])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCommandString` | [string](../types/string.md) | yes | — | SQL statement to execute. Use positional `?` placeholders for parameter binding. |
| `aFieldList` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Not implemented. This argument must be omitted or skipped. Passing any array value raises `aFieldList != NULL - Not implemented yet.` |
| `sConnectionName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Database connection name. If omitted, SSL uses the default connection. |
| `aArrayOfValues` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Values bound to the positional `?` placeholders in `sCommandString`. |
| `bNullAsBlank` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Controls how database `NULL` values are surfaced. When [`.T.`](../literals/true.md), `NULL` values become type defaults such as `""`, `0`, [`.F.`](../literals/false.md), or an empty date. When [`.F.`](../literals/false.md), `NULL` values are returned as [`NIL`](../literals/nil.md). |
| `aInvariantDateCols` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Date columns to keep invariant. Pass either column names or 1-based column indexes. |

## Returns

**[array](../types/array.md)** — A two-dimensional array of query results.

- Each top-level element is one row.
- Each row is an array of column values.
- If the query returns no rows, `LSelect` returns an empty array.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aFieldList` is supplied. | `aFieldList != NULL - Not implemented yet.` |
| `sCommandString` is [`NIL`](../literals/nil.md) or empty. | `The command string is null.` |
| `sConnectionName` does not match a configured connection. | `The provider name: <sConnectionName> not found.` |
| The connection cannot resolve a database engine. | `Cannot determine the database engine name.` |
| `aArrayOfValues` contains nested arrays. | `The current array has more than 1 dimension.` |
| The number of `?` placeholders does not match the number of supplied values. | `Parameters count mismatch` |

## Best practices

!!! success "Do"
    - Skip `aFieldList` entirely. The current `LSelect` implementation does not support it.
    - Use positional `?` placeholders with `aArrayOfValues` instead of concatenating values into SQL text.
    - Choose `bNullAsBlank` deliberately so your script handles missing database values the way you expect.
    - Use `aInvariantDateCols` when returned date columns must not be shifted by timezone conversion.

!!! failure "Don't"
    - Pass `{}` or any other value for `aFieldList`; `LSelect` raises an error instead of filtering columns.
    - Use `?varName?` syntax with `LSelect`. That style is for [`SQLExecute`](SQLExecute.md), not `LSelect`.
    - Pass a multidimensional array in `aArrayOfValues`; query preparation fails before execution.
    - Assume `bNullAsBlank` means every `NULL` becomes an empty string. Numeric, logic, and date columns surface their own empty default values.

## Caveats

- `LSelect` currently behaves like [`LSelect1`](LSelect1.md) because the `aFieldList` path is not implemented.
- If you need to skip `aFieldList` and still pass later arguments, keep the skipped-argument commas adjacent, for example `LSelect(sSQL,,"DATABASE",{sID});`.
- `aInvariantDateCols` is interpreted either as names or as numeric indexes. Use one style consistently within the same array.

## Examples

### Fetch rows with the default connection

Skip `aFieldList` and `sConnectionName` with adjacent commas, then pass the value array. Each row is printed in a loop.

```ssl
:PROCEDURE GetOpenSamples;
	:DECLARE sSQL, aRows, nIndex;

	sSQL :=
		"
	    SELECT sample_id, status
	    FROM sample
	    WHERE status = ?
	    ORDER BY sample_id
	";

	aRows := LSelect(sSQL,,, {"Open"});

	:FOR nIndex := 1 :TO ALen(aRows);
		UsrMes("Sample " + LimsString(aRows[nIndex, 1]) + " is " + LimsString(aRows[nIndex, 2]));
		/* Displays one line per returned row;
	:NEXT;

	:RETURN aRows;
:ENDPROC;

/* Usage;
DoProc("GetOpenSamples");
```

### Filter by status and date on a named connection

Filter by two parameters on a named connection. The procedure returns the result array without messaging — the caller decides what to do with it.

```ssl
:PROCEDURE GetRecentSamplesByStatus;
	:PARAMETERS sStatus, dCutoff;
	:DEFAULT sStatus, "Logged";
	:DEFAULT dCutoff, Today() - 7;
	:DECLARE sSQL, aRows;

	sSQL :=

		"
	    SELECT sample_id, status, received_date
	    FROM sample
	    WHERE status = ?
	      AND received_date >= ?
	    ORDER BY received_date DESC
	";

	aRows := LSelect(sSQL,, "DATABASE", {sStatus, dCutoff});

	:RETURN aRows;
:ENDPROC;

/* Usage;
DoProc("GetRecentSamplesByStatus");
```

### Preserve database NULLs and mark invariant date columns

Pass [`.F.`](../literals/false.md) for `bNullAsBlank` and name both date columns in `aInvariantDateCols` so that `NULL` closed dates come back as [`NIL`](../literals/nil.md) and both dates bypass timezone conversion.

```ssl
:PROCEDURE GetAuditWindow;
	:PARAMETERS dStartDate, dEndDate;
	:DECLARE sSQL, aRows, nIndex, dClosedDate;

	sSQL :=
		"
	    SELECT audit_id, opened_date, closed_date
	    FROM audit_log
	    WHERE opened_date >= ?
	      AND opened_date < ?
	    ORDER BY opened_date
	";

	aRows := LSelect(sSQL,, "DATABASE", {dStartDate, dEndDate}, .F., {"opened_date", "closed_date"});

	:FOR nIndex := 1 :TO ALen(aRows);
		dClosedDate := aRows[nIndex, 3];

		:IF dClosedDate = NIL;
			UsrMes("Audit " + LimsString(aRows[nIndex, 1]) + " is still open");
			/* Displays when no closed date is returned;
		:ELSE;
			UsrMes("Audit " + LimsString(aRows[nIndex, 1]) + " closed on " + DToC(dClosedDate));
			/* Displays the audit close date;
		:ENDIF;
	:NEXT;

	:RETURN aRows;
:ENDPROC;

/* Usage;
DoProc("GetAuditWindow", {Today() - 7, Today()});
```

## Related

- [`LSearch`](LSearch.md)
- [`LSelect1`](LSelect1.md)
- [`LSelectC`](LSelectC.md)
- [`RunSQL`](RunSQL.md)
- [`SQLExecute`](SQLExecute.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
- [`boolean`](../types/boolean.md)
