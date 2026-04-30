---
title: "IsTableFld"
summary: "Checks whether a field exists in a table for a selected database connection."
id: ssl.function.istablefld
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# IsTableFld

Checks whether a field exists in a table for a selected database connection.

`IsTableFld` returns [`.T.`](../literals/true.md) when the named field is present in the named table and [`.F.`](../literals/false.md) when it is not found. Pass `sConnectionName` to select a specific database connection. If `sConnectionName` is [`NIL`](../literals/nil.md), SSL replaces it with the default connection before the lookup runs.

`sTableName` and `sFieldName` are required. Passing [`NIL`](../literals/nil.md) for either raises an immediate error. Passing an empty string for `sConnectionName`, `sTableName`, or `sFieldName` causes the lower database layer to raise the input-parameter error. Use [`IsTable`](IsTable.md) when you only need to check whether a table exists, and [`TableFldLst`](TableFldLst.md) when you need the list of fields.

## When to use

- When you need to confirm a field exists before building SQL or mapping data.
- When upgrade or deployment code must verify required schema fields.
- When a script can run against more than one database connection.
- When you need a simple boolean check instead of a full field list.

## Syntax

```ssl
IsTableFld(sConnectionName, sTableName, sFieldName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sConnectionName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Database connection name to check against. [`NIL`](../literals/nil.md) falls back to the default connection; empty string is not treated as omitted. |
| `sTableName` | [string](../types/string.md) | yes | — | Name of the table to inspect. |
| `sFieldName` | [string](../types/string.md) | yes | — | Name of the field to test for existence. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) if the field exists in the selected table; otherwise [`.F.`](../literals/false.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sTableName` or `sFieldName` is [`NIL`](../literals/nil.md). | `The table name or field name parameter is null` |
| `sConnectionName`, `sTableName`, or `sFieldName` is an empty string. | `The input parameters are incorrect.` |

## Best practices

!!! success "Do"
    - Check the result before generating SQL, importing data, or reading optional fields.
    - Use [`NIL`](../literals/nil.md) for `sConnectionName` only when you intentionally want the default connection.
    - Use [`IsTable`](IsTable.md) for table-only checks and [`TableFldLst`](TableFldLst.md) when you need all field names.

!!! failure "Don't"
    - Assume invalid input returns [`.F.`](../literals/false.md). [`NIL`](../literals/nil.md) and empty-string cases can raise errors instead.
    - Treat `""` as the same as omitting `sConnectionName`. Only [`NIL`](../literals/nil.md) falls back to the default connection.
    - Pass an empty `sFieldName` expecting a table-only check. Use [`IsTable`](IsTable.md) for that case.

## Caveats

- The function checks one table and one field name at a time.
- It reports existence only; it does not return field metadata.
- If the selected connection cannot be opened, the call can fail for reasons unrelated to field existence.

## Examples

### Check a field before reading it

Check whether `received_date` exists in the `sample` table on the `LAB` connection before issuing the query. If the field is absent the guard fires and returns early, avoiding a runtime SQL error.

```ssl
:PROCEDURE GetSamplesWithOptionalDate;
    :DECLARE sConnectionName, sTableName, sFieldName, aSamples;

    sConnectionName := "LAB";
    sTableName := "sample";
    sFieldName := "received_date";

    :IF !IsTableFld(sConnectionName, sTableName, sFieldName);
        UsrMes("received_date is not available in sample");
        :RETURN {};
    :ENDIF;

    aSamples := SQLExecute("
        SELECT sample_id, received_date
        FROM sample
    ", sConnectionName);

    :RETURN aSamples;
:ENDPROC;

/* Usage;
DoProc("GetSamplesWithOptionalDate");
```

### Use the default connection explicitly

Pass [`NIL`](../literals/nil.md) as the connection name to target the default database connection. The two [`UsrMes`](UsrMes.md) calls are mutually exclusive; only one fires depending on whether the field is found.

```ssl
:PROCEDURE CheckAuditCommentField;
    :DECLARE bHasComment;

    bHasComment := IsTableFld(NIL, "audit_log", "comment_text");

    :IF bHasComment;
        UsrMes("comment_text is available in the default connection");
        :RETURN .T.;
    :ENDIF;

    UsrMes("comment_text is not available in the default connection");
    :RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("CheckAuditCommentField");
```

### Validate several required fields before processing

Collect the names of any required fields that are absent from the `result` table, then block the export if any are missing. `GetMissingResultFields` builds the list; `StartResultExport` calls it and reports an error when the list is non-empty.

```ssl
:PROCEDURE GetMissingResultFields;
    :PARAMETERS sConnectionName;
    :DECLARE aRequiredFields, aMissingFields, sTableName, sFieldName, nIndex;

    sTableName := "result";
    aRequiredFields := {"result_id", "sample_id", "status", "approved_by"};
    aMissingFields := {};

    :FOR nIndex := 1 :TO ALen(aRequiredFields);
        sFieldName := aRequiredFields[nIndex];

        :IF !IsTableFld(sConnectionName, sTableName, sFieldName);
            AAdd(aMissingFields, sFieldName);
        :ENDIF;
    :NEXT;

    :RETURN aMissingFields;
:ENDPROC;

:PROCEDURE StartResultExport;
    :DECLARE aMissingFields;

    aMissingFields := DoProc("GetMissingResultFields", {"LAB"});

    :IF ALen(aMissingFields) > 0;
        ErrorMes("result is missing one or more required fields");

        :RETURN .F.;
    :ENDIF;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("StartResultExport");
```

## Related

- [`IsTable`](IsTable.md)
- [`TableFldLst`](TableFldLst.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
