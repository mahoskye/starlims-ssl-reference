---
title: "TablesImport"
summary: "Loads one imported table at a time from a folder structure and returns it as a CDataTable."
id: ssl.class.tablesimport
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# TablesImport

Loads one imported table at a time from a folder structure and returns it as a [`CDataTable`](CDataTable.md).

Create `TablesImport{sFolder}` with the root folder that contains your imported tables, then call `GetTable(sName)` to load a specific table. `GetTable(sName)` looks for the table file at `<sFolder>/<sName>/<sName>.txt`, tries XML first, then falls back to the text-table importer. Imported columns are returned writable, non-auto-incrementing, and allowed to contain null values.

## When to use

- When you need to load reference or setup tables from an import folder.
- When your workflow receives table data as STARLIMS import files rather than from SQL or UI input.
- When you want the imported result as a [`CDataTable`](CDataTable.md) for further SSL processing.

## Constructors

### `TablesImport{sFolder}`

Creates an importer for a specific root folder.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sFolder` | [string](../types/string.md) | yes | Root folder that contains per-table subfolders and files. |

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `NullAsBlank` | [boolean](../types/boolean.md) | read-write | Accepted property on the class, but it does not change how `GetTable()` imports data. |
| `IncludeORIGREC` | [boolean](../types/boolean.md) | read-write | When [`.F.`](../literals/false.md), `GetTable()` removes the `ORIGREC` column from the returned table if that column exists. |
| `ErrMsg` | [string](../types/string.md) | read-only | Error text set when `GetTable()` fails. |

## Methods

| Name | Returns | Description |
|------|---------|-------------|
| `GetTable(sName)` | [object](../types/object.md) | Loads one table from the import folder and returns it as a [`CDataTable`](CDataTable.md), or [`NIL`](../literals/nil.md) when loading fails. |

### `GetTable`

Loads one table from the import folder.

It reads `<sFolder>/<sName>/<sName>.txt`, tries XML first, then falls back to the text-table importer. On success, the returned table is named after `sName`. If `IncludeORIGREC` is [`.F.`](../literals/false.md), the `ORIGREC` column is removed when present.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sName` | [string](../types/string.md) | yes | Table name. The class looks for `<sFolder>/<sName>/<sName>.txt`. |

**Returns:** [object](../types/object.md) — [`CDataTable`](CDataTable.md) on success, or [`NIL`](../literals/nil.md) when loading fails.

**Raises:**
- `sName argument cannot be null.` (runtime message reads `TName arg. can not be null`)

## Inheritance

**Base class:** `EnterpriseImpExBase`

## Best practices

!!! success "Do"
    - Check the return value from `GetTable()` before using the table.
    - Read `ErrMsg` when `GetTable()` returns [`NIL`](../literals/nil.md).
    - Set `IncludeORIGREC` before loading tables if your script needs to keep or remove that column consistently.

!!! failure "Don't"
    - Assume the table loaded successfully. Missing files, unreadable files, and invalid import content cause `GetTable()` to return [`NIL`](../literals/nil.md).
    - Rely on `NullAsBlank` to change imported values. This class accepts the property, but `GetTable()` does not use it.
    - Pass [`NIL`](../literals/nil.md) as the table name. That raises an error instead of returning [`NIL`](../literals/nil.md).

## Caveats

- `GetTable()` only checks the conventional import path `<sFolder>/<sName>/<sName>.txt`.
- `NullAsBlank` is writable on the class, but `GetTable()` does not use it.
- Passing [`NIL`](../literals/nil.md) for `sName` raises an error instead of returning [`NIL`](../literals/nil.md) and setting `ErrMsg`.
- `IncludeORIGREC` only affects the returned table when the imported data actually contains an `ORIGREC` column.

## Examples

### Load an imported table

Loads a lookup table from an import folder and reports either the row count or the load error. It checks the return value before using the table and reads `ErrMsg` to get the failure reason when loading fails.

```ssl
:PROCEDURE LoadSampleTypes;
    :DECLARE sFolder, sTableName, oImport, oTable, sError;

    sFolder := "C:/STARLIMS/Import/LookupTables";
    sTableName := "sampletypes";

    oImport := TablesImport{sFolder};
    oImport:IncludeORIGREC := .F.;

    oTable := oImport:GetTable(sTableName);

    :IF oTable == NIL;
        sError := oImport:ErrMsg;

        :IF Empty(sError);
            UsrMes("Unable to load table " + sTableName);
        :ELSE;
            UsrMes(
                "Unable to load table " + sTableName + ": " + sError
            ); /* Displays on failure: table load error;
        :ENDIF;

        :RETURN NIL;
    :ENDIF;

    UsrMes(
        "Loaded " + sTableName + " with "
        + LimsString(oTable:RowsCount) + " rows"
    ); /* Displays loaded row count;

    :RETURN oTable;
:ENDPROC;

/* Usage;
DoProc("LoadSampleTypes");
```

## Related

- [`CDataTable`](CDataTable.md)
- [`object`](../types/object.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
