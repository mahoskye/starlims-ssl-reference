---
title: "LSelect1"
summary: "Executes a parameterized SQL SELECT command and returns the result as an array of rows."
id: ssl.function.lselect1
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LSelect1

Executes a parameterized SQL `SELECT` command and returns the result as an array of rows.

`LSelect1` runs a `SELECT` query and returns the result as an SSL array where each item is a row array. Use `?` placeholders in the SQL and pass the matching values in `aArrayOfValues`. If no rows match, the function returns an empty array.

If `sConnectionName` is omitted, `LSelect1` uses the default database connection. `bNullAsBlank` defaults to [`.T.`](../literals/true.md), which converts database `NULL` values to blank SSL defaults for the column type. `aInvariantDateCols` lets you mark date columns that should be returned without timezone conversion.

## When to use

- When you need all rows from a `SELECT` as an SSL array of row arrays.
- When your query uses positional `?` parameters.
- When you need to control how database `NULL` values and date columns are mapped into SSL values.

## Syntax

```ssl
LSelect1(sCommandString, [sConnectionName], [aArrayOfValues], [bNullAsBlank], [aInvariantDateCols])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCommandString` | [string](../types/string.md) | yes | — | SQL `SELECT` statement to execute. Use positional `?` placeholders for parameters. |
| `sConnectionName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Database connection name. If omitted, SSL uses the default connection. |
| `aArrayOfValues` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Values bound to the `?` placeholders in `sCommandString`, in order. |
| `bNullAsBlank` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | When [`.T.`](../literals/true.md), database `NULL` values are converted to blank SSL defaults for the column type. |
| `aInvariantDateCols` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Date columns to preserve without timezone conversion. Entries can be 1-based column indexes or column names. |

## Returns

**[array](../types/array.md)** — An array of rows. Each row is an array of column values in select-list order. Returns an empty array when the query matches no rows.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sCommandString` is [`NIL`](../literals/nil.md) or empty. | `The command string is null.` |
| `aArrayOfValues` is multidimensional. | `The current array has more than 1 dimension.` |
| `sConnectionName` does not match a configured connection. | `The provider name: <sConnectionName> not found.` |
| The connection cannot resolve a database engine. | `Cannot determine the database engine name.` |
| The number of `?` placeholders does not match the number of supplied values. | `Parameters count mismatch` |

## Best practices

!!! success "Do"
    - Check `ALen(aRows)` before processing the result.
    - Use `?` placeholders with `aArrayOfValues` instead of concatenating values into SQL.
    - Pass `bNullAsBlank` explicitly when downstream logic depends on how database `NULL` values are surfaced.
    - Use `aInvariantDateCols` for date columns that must keep their stored value without timezone adjustment.

!!! failure "Don't"
    - Use `?varName?` syntax with `LSelect1`. That syntax is for [`SQLExecute`](SQLExecute.md), not `LSelect1`.
    - Assume a successful call returned data. An empty result is still a valid array.
    - Pass a multidimensional values array.
    - Use invariant date handling unless the date column really needs to bypass timezone conversion.

## Caveats

- A database connection is closed after the reader is consumed, even when the query raises an error.

## Examples

### Fetch rows and handle an empty result

Query all samples ordered by ID. When the result is empty, report it and return immediately. Otherwise, print one line per row.

```ssl
:PROCEDURE FetchSampleRecordsForGrid;
    :DECLARE sSQL, aSamples, nIndex, sSampleID, sSampleName, sStatus;

    sSQL := "
        SELECT sample_id, sample_name, status
        FROM sample
        ORDER BY sample_id
    ";

    aSamples := LSelect1(sSQL);

    :IF ALen(aSamples) == 0;
        UsrMes("No samples were found");
        :RETURN aSamples;
    :ENDIF;

    :FOR nIndex := 1 :TO ALen(aSamples);
        sSampleID := aSamples[nIndex, 1];
        sSampleName := aSamples[nIndex, 2];
        sStatus := aSamples[nIndex, 3];
        UsrMes("Sample: " + sSampleID + " | Name: " + sSampleName + " | Status: " + sStatus);
        /* Displays one line per row;
    :NEXT;

    :RETURN aSamples;
:ENDPROC;

/* Usage;
DoProc("FetchSampleRecordsForGrid");
```

### Build a dynamic WHERE clause with parameter binding

Accumulate `?` placeholders and matching values into `aParams` as filters are applied, then pass `aParams` to `LSelect1` with a skipped connection argument.

```ssl
:PROCEDURE QuerySamplesByStatus;
    :PARAMETERS sStatusFilter, sDepartmentFilter;
    :DEFAULT sStatusFilter, "ALL";
    :DEFAULT sDepartmentFilter, "ALL";
    :DECLARE sSQL, aParams, aResults, nIndex, nRowCount, sOutput;

    aParams := {};

    sSQL := "
        SELECT sample_id, sample_name, status, department, received_date
        FROM sample
        WHERE 1 = 1
    ";

    :IF sStatusFilter != "ALL";
        sSQL := sSQL + " AND status = ?";
        AAdd(aParams, sStatusFilter);
    :ENDIF;

    :IF sDepartmentFilter != "ALL";
        sSQL := sSQL + " AND department = ?";
        AAdd(aParams, sDepartmentFilter);
    :ENDIF;

    sSQL := sSQL + " ORDER BY received_date DESC";

    aResults := LSelect1(sSQL,, aParams);

    :IF ALen(aResults) == 0;
        UsrMes("No samples matched the selected filters");
        :RETURN aResults;
    :ENDIF;

    nRowCount := ALen(aResults);
    UsrMes("Found " + LimsString(nRowCount) + " sample(s)");
    /* Displays the matched row count;

    :FOR nIndex := 1 :TO nRowCount;
        sOutput := "Sample: " + LimsString(aResults[nIndex, 1])
            + " | Name: " + LimsString(aResults[nIndex, 2])
            + " | Status: " + LimsString(aResults[nIndex, 3])
            + " | Dept: " + LimsString(aResults[nIndex, 4]);
        UsrMes(sOutput);
        /* Displays one matching row per line;
    :NEXT;

    :RETURN aResults;
:ENDPROC;

/* Usage;
DoProc("QuerySamplesByStatus");
```

### Preserve date columns without timezone conversion

Pass column indexes in `aInvariantDateCols` to prevent timezone adjustment on the `create_date` and `result_date` columns.

```ssl
:PROCEDURE GetSamplesWithInvariantDates;
    :PARAMETERS dStartDate;
    :DECLARE sSQL, aResults, aInvariantCols, nIndex, nRowCount;
    :DECLARE sSampleID, dCreateDate, dResultDate, sStatus, sOutput;

    aInvariantCols := {2, 3};

    sSQL := "
        SELECT sample_id, create_date, result_date, status
        FROM sample
        WHERE status IN ('P', 'R')
          AND create_date >= ?
        ORDER BY create_date
    ";

    aResults := LSelect1(sSQL, "DATABASE", {dStartDate}, .T., aInvariantCols);

    nRowCount := ALen(aResults);

    :IF nRowCount == 0;
        UsrMes("No dated samples were found");
        :RETURN aResults;
    :ENDIF;

    :FOR nIndex := 1 :TO nRowCount;
        sSampleID := aResults[nIndex, 1];
        dCreateDate := aResults[nIndex, 2];
        dResultDate := aResults[nIndex, 3];
        sStatus := aResults[nIndex, 4];
        sOutput := "Sample: " + LimsString(sSampleID)
            + " | Created: " + DToC(dCreateDate)
            + " | Result: " + DToC(dResultDate)
            + " | Status: " + sStatus;
        UsrMes(sOutput);
        /* Displays one dated row per line;
    :NEXT;

    :RETURN aResults;
:ENDPROC;

/* Usage;
DoProc("GetSamplesWithInvariantDates", {Today()});
```

## Related

- [`LSearch`](LSearch.md)
- [`LSelect`](LSelect.md)
- [`LSelectC`](LSelectC.md)
- [`RunSQL`](RunSQL.md)
- [`SQLExecute`](SQLExecute.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
- [`boolean`](../types/boolean.md)
