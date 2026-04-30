---
title: "RunSQL"
summary: "Executes a SQL statement and returns whether execution completed without an uncaught SQL error."
id: ssl.function.runsql
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# RunSQL

Executes a SQL statement and returns whether execution completed without an uncaught SQL error.

`RunSQL` is the non-query database helper for SQL that changes data or schema. It executes the SQL text on the specified connection, or on the default connection when `sConnectionName` is omitted. Use positional `?` placeholders in the SQL text and pass the corresponding values in `aValues`.

The function returns [`.T.`](../literals/true.md) when execution succeeds. If SQL error ignoring is enabled, `RunSQL` can return [`.F.`](../literals/false.md) instead of raising for a handled SQL error. When that happens, inspect [`GetLastSQLError`](GetLastSQLError.md) for details. `RunSQL` does not return rows; use [`LSearch`](LSearch.md), [`LSelect`](LSelect.md), [`LSelect1`](LSelect1.md), [`LSelectC`](LSelectC.md), or [`SQLExecute`](SQLExecute.md) when you need query results.

## When to use

- When you need to run `INSERT`, `UPDATE`, `DELETE`, or DDL statements.
- When your SQL should use positional `?` parameters rather than named `?varName?` substitution.
- When the script only needs success or failure status, not returned rows.
- When you want to pair the update with [`LimsRecordsAffected`](LimsRecordsAffected.md) or [`GetLastSQLError`](GetLastSQLError.md) in follow-up logic.

## Syntax

```ssl
RunSQL(sCommandString, [sConnectionName], [aValues])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCommandString` | [string](../types/string.md) | yes | — | SQL statement to execute. Use positional `?` placeholders for bound values. |
| `sConnectionName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Database connection name. If omitted, SSL uses the default connection. |
| `aValues` | any | no | [`NIL`](../literals/nil.md) | Values bound to the positional `?` placeholders. Pass an array for multiple values. A single non-array value is accepted and treated as a one-item parameter list. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the statement executes successfully; [`.F.`](../literals/false.md) when a handled SQL error occurs while SQL error ignoring is enabled (check [`GetLastSQLError`](GetLastSQLError.md) for details).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sCommandString` is [`NIL`](../literals/nil.md) or empty. | `The command string is null.` |
| SSL cannot resolve the connection's DBMS. | `Cannot determine the database engine name.` |
| `sConnectionName` does not identify a configured connection. | `The provider name: <sConnectionName> not found.` |
| `aValues` is a multidimensional array. | `The current array has more than 1 dimension.` |
| The number of `?` placeholders does not match the supplied values. | `Parameters count mismatch` |

## Best practices

!!! success "Do"
    - Use positional `?` placeholders with `aValues` instead of building values directly into SQL text.
    - Check the boolean result when your script enables SQL error ignoring.
    - Use [`LimsRecordsAffected`](LimsRecordsAffected.md) after a successful call when row-count validation matters.
    - Use a transaction when several `RunSQL` calls must succeed or fail together.

!!! failure "Don't"
    - Use `?varName?` syntax with `RunSQL`; that form is for [`SQLExecute`](SQLExecute.md) only.
    - Use `RunSQL` for `SELECT` result retrieval; it does not return rows.
    - Pass a multidimensional array to `aValues`.
    - Concatenate unchecked input into SQL text when a positional parameter will do the job safely.

## Caveats

- `aValues` must line up with the positional `?` placeholders in order.
- A single third argument such as `sValue` is accepted, but arrays are clearer once more than one parameter is involved.
- Some SQL errors can still raise even with error ignoring enabled.

## Examples

### Insert one audit row with positional parameters

Use `?` placeholders to pass three bound values to an `INSERT` statement, avoiding string concatenation entirely.

```ssl
:PROCEDURE InsertAuditEntry;
    :DECLARE sSQL, sUserName, sAction, sRecordID, bSuccess;

    sUserName := "JSMITH";
    sAction := "SAMPLE_APPROVED";
    sRecordID := "SAM-2024-0042";

    sSQL := "
        INSERT INTO audit_log (
            user_name, action, record_id, log_date
        )
        VALUES (
            ?, ?, ?, SYSDATE
        )
    ";

    bSuccess := RunSQL(sSQL,, {sUserName, sAction, sRecordID});

    :RETURN bSuccess;
:ENDPROC;

/* Usage;
DoProc("InsertAuditEntry");
```

### Update one row and verify rows affected

Run an `UPDATE` on a named connection and call [`LimsRecordsAffected`](LimsRecordsAffected.md) to confirm the row was actually found and changed.

```ssl
:PROCEDURE ReleaseSample;
    :PARAMETERS sSampleID;
    :DECLARE sSQL, bSuccess, nRows;

    sSQL := "
        UPDATE sample SET
            status = ?,
            released_date = SYSDATE
        WHERE sample_id = ?
    ";

    bSuccess := RunSQL(sSQL, "DATABASE", {"RELEASED", sSampleID});

    :IF !bSuccess;
        :RETURN .F.;
    :ENDIF;

    nRows := LimsRecordsAffected();

    :RETURN nRows > 0;
:ENDPROC;

/* Usage;
DoProc("ReleaseSample", {"SAM-2024-0042"});
```

### Ignore SQL errors temporarily and inspect the stored error

Enable error ignoring for a best-effort `UPDATE`, then restore the previous settings and surface the stored SQL error if the statement failed.

```ssl
:PROCEDURE TryOptionalUpdate;
    :PARAMETERS sSampleID;
    :DECLARE sSQL, bSuccess, bPrevIgnore, bPrevShow, oErr;

    sSQL := "
        UPDATE sample SET
            optional_flag = ?
        WHERE sample_id = ?
    ";

    bPrevIgnore := IgnoreSqlErrors(.T.);
    bPrevShow := ShowSqlErrors(.F.);

    :TRY;
        bSuccess := RunSQL(sSQL,, {"Y", sSampleID});

        :IF !bSuccess;
            oErr := GetLastSQLError();

            :IF oErr != NIL;
                /* Displays on failure: Optional update failed;
                UsrMes(
                    "Optional update failed: " + oErr:Description
                );
            :ENDIF;
        :ENDIF;
    :FINALLY;
        ShowSqlErrors(bPrevShow);
        IgnoreSqlErrors(bPrevIgnore);
    :ENDTRY;

    :RETURN bSuccess;
:ENDPROC;

/* Usage;
DoProc("TryOptionalUpdate", {"SAM-2024-0042"});
```

## Related

- [`GetLastSQLError`](GetLastSQLError.md)
- [`IgnoreSqlErrors`](IgnoreSqlErrors.md)
- [`LimsRecordsAffected`](LimsRecordsAffected.md)
- [`LSearch`](LSearch.md)
- [`LSelect`](LSelect.md)
- [`LSelect1`](LSelect1.md)
- [`LSelectC`](LSelectC.md)
- [`SQLExecute`](SQLExecute.md)
- [`ShowSqlErrors`](ShowSqlErrors.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
