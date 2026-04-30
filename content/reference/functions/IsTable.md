---
title: "IsTable"
summary: "Checks whether a table exists in a database connection."
id: ssl.function.istable
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# IsTable

Checks whether a table exists in a database connection.

`IsTable` returns [`.T.`](../literals/true.md) when the named table is present in the selected database connection and [`.F.`](../literals/false.md) when it is not found. Pass a database connection name in `sConnectionName` to target a specific connection. If `sConnectionName` is [`NIL`](../literals/nil.md), SSL replaces it with the default connection before the database lookup runs.

The `sTableName` argument is required. Passing [`NIL`](../literals/nil.md) for `sTableName` raises an immediate error. Passing an empty string for `sConnectionName` or `sTableName` causes the underlying database layer to raise an input-parameter error.

## When to use

- When you need to verify a table before running logic that depends on it.
- When startup or deployment code should check required schema objects first.
- When a script can work against multiple database connections.

## Syntax

```ssl
IsTable(sConnectionName, sTableName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sConnectionName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Database connection name to check against. [`NIL`](../literals/nil.md) falls back to the default connection; empty string is not treated as omitted. |
| `sTableName` | [string](../types/string.md) | yes | — | Name of the table to test for existence. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) if the table exists in the selected connection; otherwise [`.F.`](../literals/false.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sTableName` is [`NIL`](../literals/nil.md). | `The table name parameter is null` |
| `sConnectionName` or `sTableName` is an empty string. | `The input parameters are incorrect.` |

## Best practices

!!! success "Do"
    - Check the result before running queries or updates that assume a table exists.
    - Pass the exact connection name and table name used in your environment.
    - Use [`NIL`](../literals/nil.md) for `sConnectionName` only when you intentionally want the default connection.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sTableName`; this raises an immediate error.
    - Treat an empty string as the same as omitting `sConnectionName`; empty strings raise an error instead of falling back.
    - Use `IsTable` as a substitute for retrieving column details; use a schema-inspection function when you need more than existence.

## Caveats

- The function reports only whether the table exists; it does not return schema details.
- The function checks one table name at a time.

## Examples

### Check a table before querying it

Guard the query with an existence check before calling [`SQLExecute`](SQLExecute.md). If the `sample` table does not exist on the `LAB` connection, the message fires and the procedure returns early with an empty array.

```ssl
:PROCEDURE GetSampleRows;
	:DECLARE sConnectionName, sTableName, aSamples;

	sConnectionName := "LAB";
	sTableName := "sample";

	:IF !IsTable(sConnectionName, sTableName);
		UsrMes("Table not found: " + sTableName);
		:RETURN {};
	:ENDIF;

	aSamples := SQLExecute("
	    SELECT sample_id, sample_name
	    FROM sample
	",
		sConnectionName);

	:RETURN aSamples;
:ENDPROC;

/* Usage;
DoProc("GetSampleRows");
```

### Use the default connection explicitly

Pass [`NIL`](../literals/nil.md) as the connection name to target the default connection. The [`UsrMes`](UsrMes.md) call fires only if `audit_log` is absent from that connection.

```ssl
:PROCEDURE LoadAuditRows;
	:DECLARE aAuditRows;

	:IF !IsTable(NIL, "audit_log");
		UsrMes("audit_log is not available in the default connection");
		:RETURN {};
	:ENDIF;

	aAuditRows := SQLExecute("
	    SELECT event_id, event_type, log_date
	    FROM audit_log
	    ORDER BY log_date DESC
	");

	:RETURN aAuditRows;
:ENDPROC;

/* Usage;
DoProc("LoadAuditRows");
```

### Validate a required table set before processing

Check that every table a module depends on exists before proceeding. `ValidateRequiredTables` returns the list of missing names; `StartModuleLoad` calls it and blocks startup if any are absent.

```ssl
:PROCEDURE ValidateRequiredTables;
	:PARAMETERS sConnectionName, aRequiredTables;
	:DECLARE aMissingTables, nIndex, sTableName;

	aMissingTables := {};

	:FOR nIndex := 1 :TO ALen(aRequiredTables);
		sTableName := aRequiredTables[nIndex];

		:IF !IsTable(sConnectionName, sTableName);
			AAdd(aMissingTables, sTableName);
		:ENDIF;
	:NEXT;

	:RETURN aMissingTables;
:ENDPROC;

:PROCEDURE StartModuleLoad;
	:DECLARE aMissingTables;

	aMissingTables := DoProc("ValidateRequiredTables", {
		"LAB",
		{"sample", "result", "ordtask"}
	});

	:IF ALen(aMissingTables) > 0;
		ErrorMes("Missing required tables for module startup");
		:RETURN .F.;
	:ENDIF;

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("StartModuleLoad");
```

## Related

- [`GetTables`](GetTables.md)
- [`IsTableFld`](IsTableFld.md)
- [`TableFldLst`](TableFldLst.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
