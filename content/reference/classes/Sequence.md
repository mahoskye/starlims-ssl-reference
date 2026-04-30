---
title: "Sequence"
summary: "Creates and manages a database sequence for a table field on Oracle or SQL Server."
id: ssl.class.sequence
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Sequence

Creates and manages a database sequence for a table field on Oracle or SQL Server.

`Sequence` gives SSL scripts a compact API for creating, resetting, dropping, and querying a database sequence. You construct it with a platform name, table name, field name, and an optional prefix. The object derives a sequence name from those values, uses `StartWith` when creating the sequence on both platforms, and uses `CacheSize` when creating the sequence on SQL Server.

## When to use

- When a script needs a database sequence for a specific table field.
- When deployment or setup logic must create or remove sequences.
- When imported data requires the next generated value to start from a known number.
- When the same sequence definition must be pointed at another database with `SetDatabase()`.

## Constructors

### `Sequence{sPlatforma, sTableName, sFieldName}`

Creates a sequence object with an empty prefix.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sPlatforma` | [string](../types/string.md) | yes | Database platform. `"ORACLE"` selects Oracle behavior. Any other value uses SQL Server behavior. |
| `sTableName` | [string](../types/string.md) | yes | Table name used to derive the sequence name. |
| `sFieldName` | [string](../types/string.md) | yes | Field name used to derive the sequence name. |

### `Sequence{sPlatforma, sTableName, sFieldName, sPrefix}`

Creates a sequence object with an additional name suffix.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sPlatforma` | [string](../types/string.md) | yes | Database platform. `"ORACLE"` selects Oracle behavior. Any other value uses SQL Server behavior. |
| `sTableName` | [string](../types/string.md) | yes | Table name used to derive the sequence name. |
| `sFieldName` | [string](../types/string.md) | yes | Field name used to derive the sequence name. |
| `sPrefix` | [string](../types/string.md) | no | Optional suffix added to the derived sequence name. If omitted or passed as [`NIL`](../literals/nil.md), an empty suffix is used. |

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `SequenceName` | [string](../types/string.md) | read-only | Derived sequence name for the current table, field, and prefix. |
| `StartWith` | [number](../types/number.md) | read-write | First value used when `Create()` creates the sequence. Default is `1`. |
| `CacheSize` | [number](../types/number.md) | read-write | Cache size used when SQL Server creates the sequence. Default is `50`. Oracle creation ignores this property. |
| `Exists` | [boolean](../types/boolean.md) | read-only | [`.T.`](../literals/true.md) when the sequence exists in the current database. |
| `NextValue` | [number](../types/number.md) | read-only | Retrieves the next value from the current database sequence. |

## Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `Create()` | none | Creates the sequence in the current database. |
| `Reset(nNewValue)` | none | Changes the next starting value for the sequence. |
| `Drop()` | none | Drops the sequence from the current database. |
| `SetDatabase(sNewDatabase)` | none | Changes the database used for later operations. |

### `Create`

Creates the sequence in the current database using the current `StartWith` setting.

On SQL Server, the created sequence uses the current `CacheSize`. On Oracle, the created sequence uses Oracle's ordered, non-cached form.

**Returns:** none — No return value.

### `Reset`

Changes the sequence to start again from `nNewValue`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `nNewValue` | [number](../types/number.md) | yes | New starting value for the sequence. |

**Returns:** none — No return value.

### `Drop`

Drops the sequence from the current database.

**Returns:** none — No return value.

### `SetDatabase`

Changes the database used for later property lookups and method calls.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sNewDatabase` | [string](../types/string.md) | yes | Database name to use for later operations. |

**Returns:** none — No return value.

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Set `StartWith` before `Create()` when the sequence must begin at a known value.
    - Check `Exists` before calling `Drop()` or before assuming `NextValue` is available.
    - Use `SetDatabase()` before sequence operations when the work should target a non-default database.

!!! failure "Don't"
    - Assume `CacheSize` changes Oracle behavior, because it is only used when SQL Server creates the sequence.
    - Treat any non-`"ORACLE"` platform value as validation-safe input, because it falls back to SQL Server behavior.
    - Use `Reset()` on Oracle when the sequence cannot be safely recreated, because Oracle does not support resetting in place and the operation resets the sequence by recreating it.

## Caveats

- `SequenceName` is derived from the table name and field name, both converted to uppercase, and always starts with `C_`. When a prefix is supplied, it is appended in uppercase after the field name.
- `Create()` handles create failures by showing a message rather than exposing a dedicated return value.
- `Drop()`, `Exists`, `NextValue`, and `Reset()` still depend on the target database being reachable and the sequence being valid in that database.
- Oracle and SQL Server do not reset sequences the same way. Oracle reset recreates the sequence, while SQL Server resets the existing sequence in place.
- Very long Oracle-derived sequence names may not remain human-readable because the name is shortened before use.

## Examples

### Create a sequence and read the next value

Creates a SQL Server sequence for a sample table with a custom starting value and cache size, then reads the next value. Checks `Exists` first to avoid creating a sequence that is already present.

```ssl
:PROCEDURE CreateSampleSequence;
    :DECLARE oSeq, nNextValue;

    oSeq := Sequence{"SQLSERVER", "sample", "sample_id"};
    oSeq:StartWith := 1000;
    oSeq:CacheSize := 20;

    :IF .NOT. oSeq:Exists;
        oSeq:Create();
    :ENDIF;

    nNextValue := oSeq:NextValue;
    UsrMes("Next sample id: " + LimsString(nNextValue));
:ENDPROC;

/* Usage;
DoProc("CreateSampleSequence");
```

### Reset after importing existing records

Queries the highest existing ID in the table to determine the next safe starting value, then either creates the sequence fresh or resets it if one already exists.

```ssl
:PROCEDURE SyncSampleSequence;
    :DECLARE oSeq, nMaxId, nStartValue;

    oSeq := Sequence{"SQLSERVER", "sample", "sample_id"};

    nMaxId := LSearch("
	    SELECT MAX(sample_id)
	    FROM sample
	", 0);

    nStartValue := nMaxId + 1;

    :IF .NOT. oSeq:Exists;
        oSeq:StartWith := nStartValue;
        oSeq:Create();
    :ELSE;
        oSeq:Reset(nStartValue);
    :ENDIF;

    UsrMes("Sequence synchronized to start at " + LimsString(nStartValue));
:ENDPROC;

/* Usage;
DoProc("SyncSampleSequence");
```

### Target another database before sequence operations

Builds an Oracle sequence object with a prefix, redirects it to a named database with `SetDatabase`, then creates the sequence only if it does not already exist there.

```ssl
:PROCEDURE CreateHistorySequence;
    :DECLARE oSeq;

    oSeq := Sequence{"ORACLE", "result_log", "result_id", "audit"};
    oSeq:SetDatabase("HISTORYDB");
    oSeq:StartWith := 5000;

    :IF .NOT. oSeq:Exists;
        oSeq:Create();
        UsrMes("Created sequence " + oSeq:SequenceName + " in HISTORYDB");
        /* Displays the created sequence name and target database;
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("CreateHistorySequence");
```

## Related

- [`LSearch`](../functions/LSearch.md)
- [`RunSQL`](../functions/RunSQL.md)
- [`SQLExecute`](../functions/SQLExecute.md)
- [`object`](../types/object.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
- [`boolean`](../types/boolean.md)
