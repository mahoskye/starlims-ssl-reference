---
title: "LSelectC"
summary: "Executes a SQL SELECT statement and returns the result as a two-dimensional SSL array."
id: ssl.function.lselectc
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LSelectC

Executes a SQL `SELECT` statement and returns the result as a two-dimensional SSL array.

`LSelectC` accepts positional `?` placeholders in the SQL text and binds values from `aArrayOfValues`. The returned value is an array of rows, where each row is an array of column values in select-list order.

`LSelectC` only works when `aFieldList` is omitted. If you supply `aFieldList`, the function raises an error instead of filtering the returned columns. `sConnectionName` defaults to the standard database connection when omitted. `bNullAsBlank` defaults to [`.T.`](../literals/true.md). When `aInvariantDateCols` is supplied, it can identify date columns by name or by 1-based column index.

## When to use

- When you need a `SELECT` result as an SSL array of rows.
- When your SQL uses positional `?` placeholders rather than `?varName?` substitution.
- When you need control over how database `NULL` values and date columns are surfaced in the result.
- When the current `LSelectC` behavior is sufficient and you are not relying on the unimplemented `aFieldList` argument.

## Syntax

```ssl
LSelectC(sCommandString, [aFieldList], [sConnectionName], [aArrayOfValues], [bNullAsBlank], [aInvariantDateCols])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCommandString` | [string](../types/string.md) | yes | — | SQL `SELECT` statement to execute. Use positional `?` placeholders for parameter binding. |
| `aFieldList` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Not implemented. This argument must be omitted or skipped. Passing any array value raises `aFieldList != NULL - Not implemented yet.` |
| `sConnectionName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Database connection name. If omitted, SSL uses the default connection. |
| `aArrayOfValues` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Values bound to the positional `?` placeholders in `sCommandString`, in order. |
| `bNullAsBlank` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Controls how database `NULL` values are surfaced. When [`.T.`](../literals/true.md), `NULL` values become empty SSL defaults for the column type. When [`.F.`](../literals/false.md), `NULL` values are returned as [`NIL`](../literals/nil.md). |
| `aInvariantDateCols` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Date columns to keep invariant. Pass either column names or 1-based column indexes. |

## Returns

**[array](../types/array.md)** — A two-dimensional array of query results.

- Each top-level element is one row.
- Each row is an array of column values.
- If the query returns no rows, `LSelectC` returns an empty array.

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
    - Skip `aFieldList` entirely. The current `LSelectC` implementation does not support it.
    - Use positional `?` placeholders with `aArrayOfValues` instead of concatenating values into SQL text.
    - Choose `bNullAsBlank` deliberately so your script handles missing database values the way you expect.
    - Use `aInvariantDateCols` when returned date columns must not be shifted by timezone conversion.

!!! failure "Don't"
    - Pass `{}` or any other value for `aFieldList`; `LSelectC` raises an error instead of filtering columns.
    - Use `?varName?` syntax with `LSelectC`. That style is for [`SQLExecute`](SQLExecute.md), not `LSelectC`.
    - Pass a multidimensional array in `aArrayOfValues`; query preparation fails before execution.
    - Assume `bNullAsBlank` means every `NULL` becomes an empty string. Numeric, logic, and date columns surface their own empty default values.

## Caveats

- `LSelectC` currently behaves the same as [`LSelect`](LSelect.md).
- If you need to skip `aFieldList` and still pass later arguments, keep the skipped-argument commas adjacent, for example `LSelectC(sSQL,, "DATABASE", {sID});`.
- `aInvariantDateCols` is interpreted either as names or as numeric indexes. Use one style consistently within the same array.

## Examples

### Fetch rows with the default connection

Skip `aFieldList` and `sConnectionName` using adjacent commas, then pass the parameter value array. Each row is printed in a loop.

```ssl
:PROCEDURE GetOpenSamples;
    :DECLARE sSQL, aRows, nIndex;

    sSQL := "
        SELECT sample_id, status
        FROM sample
        WHERE status = ?
        ORDER BY sample_id
    ";

    aRows := LSelectC(sSQL,,,{"Open"});

    :FOR nIndex := 1 :TO ALen(aRows);
        UsrMes("Sample " + aRows[nIndex, 1] + " is " + aRows[nIndex, 2]);
        /* Displays one line per row with the sample ID and status;
    :NEXT;

    :RETURN aRows;
:ENDPROC;

/* Usage;
DoProc("GetOpenSamples");
```

### Preserve database NULL values as NIL

Pass [`.F.`](../literals/false.md) for `bNullAsBlank` so that database `NULL` notes are surfaced as [`NIL`](../literals/nil.md) rather than an empty string, allowing an explicit check on each row.

```ssl
:PROCEDURE GetSamplesWithOptionalNotes;
    :DECLARE sSQL, aRows, nIndex, vNote;

    sSQL := "
        SELECT sample_id, notes
        FROM sample
        WHERE status = ?
        ORDER BY sample_id
    ";

    aRows := LSelectC(sSQL,,,{"Pending"}, .F.);

    :FOR nIndex := 1 :TO ALen(aRows);
        vNote := aRows[nIndex, 2];

        :IF vNote = NIL;
            UsrMes("Sample " + aRows[nIndex, 1] + " has no note");
        :ELSE;
            UsrMes("Sample " + aRows[nIndex, 1] + " note: " + vNote);
            /* Displays the note text for rows that have one;
        :ENDIF;
    :NEXT;

    :RETURN aRows;
:ENDPROC;

/* Usage;
DoProc("GetSamplesWithOptionalNotes");
```

### Keep selected date columns invariant

Pass column index `2` in `aInvariantCols` so the `received_date` column is returned without timezone adjustment.

```ssl
:PROCEDURE GetSamplesForDateReview;
    :DECLARE sSQL, aRows, aInvariantCols, nIndex, dReceived;

    sSQL := "
        SELECT sample_id, received_date, status
        FROM sample
        WHERE status = ?
        ORDER BY received_date
    ";

    aInvariantCols := {2};
    aRows := LSelectC(sSQL,,,{"Logged"}, .T., aInvariantCols);

    :FOR nIndex := 1 :TO ALen(aRows);
        dReceived := aRows[nIndex, 2];
        UsrMes("Sample " + aRows[nIndex, 1] + " received on " + DToC(dReceived));
        /* Displays one line per row with the received date;
    :NEXT;

    :RETURN aRows;
:ENDPROC;

/* Usage;
DoProc("GetSamplesForDateReview");
```

## Related

- [`LSearch`](LSearch.md)
- [`LSelect`](LSelect.md)
- [`LSelect1`](LSelect1.md)
- [`RunSQL`](RunSQL.md)
- [`SQLExecute`](SQLExecute.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
- [`boolean`](../types/boolean.md)
