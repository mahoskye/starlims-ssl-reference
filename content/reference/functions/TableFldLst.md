---
title: "TableFldLst"
summary: "Returns the field names for a table on a selected database connection."
id: ssl.function.tablefldlst
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# TableFldLst

Returns the field names for a table on a selected database connection.

`TableFldLst` returns an array of strings containing the field names for `sTableName`. Pass `sConnectionName` to use a specific database connection. If `sConnectionName` is [`NIL`](../literals/nil.md), SSL replaces it with the current default connection before the lookup runs.

`sTableName` is required. Passing [`NIL`](../literals/nil.md) for `sTableName` raises an immediate error. Passing an empty string for `sConnectionName` or `sTableName` causes the lower database layer to raise an input-parameter error. If the selected connection cannot be opened, or the table metadata cannot be read, the call can also fail with a database error.

Use [`IsTable`](IsTable.md) when you only need to know whether a table exists.
Use [`IsTableFld`](IsTableFld.md) when you only need to test one field.

## When to use

- When you need the full list of fields before building dynamic SQL.
- When import or export logic must validate a table's available columns.
- When runtime UI or mapping code needs schema metadata.
- When a script can run against more than one database connection.

## Syntax

```ssl
TableFldLst([sConnectionName], sTableName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sConnectionName` | [string](../types/string.md) | no | default connection when [`NIL`](../literals/nil.md) | Database connection name to inspect. Empty string is not treated as omitted. |
| `sTableName` | [string](../types/string.md) | yes | — | Name of the table whose fields should be returned. |

## Returns

**[array](../types/array.md)** — Array of field names for the selected table.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sTableName` is [`NIL`](../literals/nil.md). | `The table name or field name parameter is null.` |
| `sConnectionName` or `sTableName` is an empty string. | `The input parameters are incorrect.` |

## Best practices

!!! success "Do"
    - Pass [`NIL`](../literals/nil.md) for `sConnectionName` only when you intentionally want the default connection.
    - Use the returned array for schema-driven tasks such as validation, mapping, or dynamic query generation.
    - Wrap the call in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the connection or table name may be invalid at runtime.
    - Use [`IsTable`](IsTable.md) or [`IsTableFld`](IsTableFld.md) when you only need an existence check.

!!! failure "Don't"
    - Treat `""` as the same as omitting `sConnectionName`. Only [`NIL`](../literals/nil.md) falls back to the default connection.
    - Assume missing tables return an empty array. Database lookup failures can raise errors instead.
    - Use this function for one-field checks when [`IsTableFld`](IsTableFld.md) is clearer and cheaper.
    - Rely on undocumented ordering of the returned field names.

## Caveats

- The function returns names only. It does not return types, sizes, or other column metadata.
- `sConnectionName` falls back only when it is [`NIL`](../literals/nil.md), not when it is `""`.

## Examples

### List all fields for a known table

Call `TableFldLst` with an explicit connection name and use the returned array length to confirm the field count.

```ssl
:PROCEDURE ShowSampleFields;
    :DECLARE aFieldNames, sConnectionName, sTableName;

    sConnectionName := "LAB";
    sTableName := "sample";

    aFieldNames := TableFldLst(sConnectionName, sTableName);

    UsrMes("sample has " + LimsString(ALen(aFieldNames)) + " fields");
    /* Displays: sample has <n> fields;

    :RETURN aFieldNames;
:ENDPROC;

DoProc("ShowSampleFields");
```

### Validate required fields on the default connection

Pass [`NIL`](../literals/nil.md) for the connection to use the default, then scan the returned array for each required field name and collect any that are absent.

```ssl
:PROCEDURE GetMissingSampleFields;
    :DECLARE aFieldNames, aRequiredFields, aMissingFields, sTableName, sFieldName, nIndex;

    sTableName := "sample";
    aRequiredFields := {"sample_id", "status", "received_date"};
    aMissingFields := {};
    aFieldNames := TableFldLst(NIL, sTableName);

    :FOR nIndex := 1 :TO ALen(aRequiredFields);
        sFieldName := aRequiredFields[nIndex];

        :IF AScan(aFieldNames, sFieldName) == 0;
            AAdd(aMissingFields, sFieldName);
        :ENDIF;
    :NEXT;

    :RETURN aMissingFields;
:ENDPROC;

DoProc("GetMissingSampleFields");
```

### Catch runtime metadata errors before continuing

Wrap the call in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) to handle connection or table errors and return an empty array as a safe fallback instead of propagating the failure.

```ssl
:PROCEDURE TryLoadAuditFields;
    :DECLARE aFieldNames, oErr;

    :TRY;
        aFieldNames := TableFldLst("LAB", "audit_log");

        :RETURN aFieldNames;
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("Unable to read audit_log fields: " + oErr:Description);
        /* Displays on failure: audit_log read failed;

        :RETURN {};
    :ENDTRY;
:ENDPROC;

DoProc("TryLoadAuditFields");
```

## Related

- [`IsTable`](IsTable.md)
- [`IsTableFld`](IsTableFld.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
