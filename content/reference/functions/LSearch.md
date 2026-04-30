---
title: "LSearch"
summary: "Returns a single value from a SQL query, or a caller-supplied fallback when the query produces no scalar result."
id: ssl.function.lsearch
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LSearch

Returns a single value from a SQL query, or a caller-supplied fallback when the query produces no scalar result.

`LSearch` executes a parameterized SQL statement and returns the first scalar value produced by the query. Use it when you need one value, not a result set. If the query returns no row, or the scalar value is database `NULL`, the function returns `vDefaultValue` instead. `LSearch` uses positional `?` placeholders with `aArrayOfValues`; unlike [`SQLExecute`](SQLExecute.md), it does not support `?varName?` substitution.

When the database returns a date/time value, SSL surfaces it as a `DATE`. Other results are returned in their native scalar form.

## When to use

- When you need a single lookup value such as a status, count, code, or date.
- When missing data should fall back to a known value instead of raising a business-level error.
- When you want parameterized SQL without building values directly into the query text.
- When you need a simple scalar query and do not need rows or columns returned as an array or dataset.

## Syntax

```ssl
LSearch(sCommandString, vDefaultValue, [sConnectionName], [aArrayOfValues])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCommandString` | [string](../types/string.md) | yes | — | SQL statement to execute. Use positional `?` placeholders for parameter values. |
| `vDefaultValue` | any | yes | — | Value returned when the query returns no row or the scalar result is database `NULL`. |
| `sConnectionName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Database connection name. If omitted, SSL uses the default connection. |
| `aArrayOfValues` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Values bound to the positional `?` placeholders in `sCommandString`. |

## Returns

**any** — The scalar result from the query, or `vDefaultValue` when no scalar value is returned.

Common return shapes include:

- **string / number / logic** — Returned as the database value for the first scalar column.
- **[date](../types/date.md)** — Returned when the database value is a date/time value.
- **other values** — Surfaced as returned by the query when the scalar value is not one of the common primitive cases above.
- **`vDefaultValue`** — Returned when the query finds no row or the scalar value is database `NULL`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sCommandString` is [`NIL`](../literals/nil.md) or empty. | `The command string is null.` |
| The connection cannot resolve a database engine. | `Cannot determine the database engine name.` |
| `sConnectionName` does not identify a configured connection. | `The provider name: <sConnectionName> not found.` |
| `aArrayOfValues` contains nested arrays. | `The current array has more than 1 dimension.` |
| The number of `?` placeholders does not match the number of supplied values. | `Parameters count mismatch` |

## Best practices

!!! success "Do"
    - Pass an explicit fallback that matches how your script should behave when no row is found.
    - Use positional `?` placeholders with `aArrayOfValues` instead of concatenating values into SQL text.
    - Use [`NIL`](../literals/nil.md) as the fallback when you need to distinguish missing data from an empty string or zero.
    - Switch to [`LSelect`](LSelect.md), [`LSelect1`](LSelect1.md), or [`LSelectC`](LSelectC.md) when you need rows rather than one scalar value.

!!! failure "Don't"
    - Use `?varName?` syntax with `LSearch`. That substitution style is for [`SQLExecute`](SQLExecute.md) only.
    - Treat `LSearch` as a multi-row query helper. It is meant for a single scalar result.
    - Pass a multidimensional array to `aArrayOfValues`; it raises an error before execution.
    - Rely on an implicit fallback. Decide whether your missing-data case should return `""`, `0`, [`NIL`](../literals/nil.md), [`.F.`](../literals/false.md), or another explicit value.

## Caveats

- `LSearch` falls back only when the scalar result is missing or database `NULL`. An actual empty string from the database is returned as-is.

## Examples

### Return a default string when no row is found

Query the status of a sample by ID. When no matching row exists, `LSearch` returns the fallback `"Unknown"` instead of raising an error.

```ssl
:PROCEDURE GetSampleStatus;
    :PARAMETERS sSampleID;
    :DECLARE sStatus;

    sStatus := LSearch("
        SELECT status
        FROM sample
        WHERE sample_id = ?
    ", "Unknown", "DATABASE", {sSampleID});

    :RETURN sStatus;
:ENDPROC;

/* Usage;
DoProc("GetSampleStatus", {"SMP-001"});
```

### Use a numeric fallback with COUNT(*)

Count open tasks for a sample. If no tasks match the filter, `LSearch` returns `0` rather than [`NIL`](../literals/nil.md) or an empty result.

```ssl
:PROCEDURE GetOpenTaskCount;
    :PARAMETERS sSampleID;
    :DECLARE nTaskCount;

    nTaskCount := LSearch("
        SELECT COUNT(*)
        FROM ordtask
        WHERE sample_id = ?
          AND status = ?
    ", 0, "DATABASE", {sSampleID, "Open"});

    :RETURN nTaskCount;
:ENDPROC;

/* Usage;
DoProc("GetOpenTaskCount", {"SMP-001"});
```

### Use [`NIL`](../literals/nil.md) to distinguish a missing date from a real one

Use [`NIL`](../literals/nil.md) as the fallback so that a missing approval date is distinguishable from a genuine date value. After the query, a [`NIL`](../literals/nil.md) result means the invoice has not yet been approved.

```ssl
:PROCEDURE ShowApprovalDate;
    :PARAMETERS sInvoiceID;
    :DECLARE dApprovalDate, oErr;

    :TRY;
        dApprovalDate := LSearch("
            SELECT approved_date
            FROM financial_approvals
            WHERE invoice_id = ?
              AND status = ?
        ", NIL, "DATABASE", {sInvoiceID, "A"});

        :IF dApprovalDate = NIL;
            UsrMes("Invoice " + sInvoiceID + " has not been approved yet");
            :RETURN NIL;
        :ENDIF;

        UsrMes(
            "Invoice " + sInvoiceID + " was approved on " + DToC(dApprovalDate)
        );
        /* Displays approval date;

        :RETURN dApprovalDate;
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("Approval lookup failed: " + oErr:Description);
        /* Displays on failure: approval lookup failed;
        :RETURN NIL;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ShowApprovalDate", {"INV-001"});
```

## Related

- [`LSelect`](LSelect.md)
- [`LSelect1`](LSelect1.md)
- [`LSelectC`](LSelectC.md)
- [`RunSQL`](RunSQL.md)
- [`SQLExecute`](SQLExecute.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
