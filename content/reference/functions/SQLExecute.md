---
title: "SQLExecute"
summary: "Executes SQL and returns either query results or a success flag."
id: ssl.function.sqlexecute
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SQLExecute

Executes SQL and returns either query results or a success flag.

`SQLExecute` runs a SQL statement against the specified connection or the current default connection. When the prepared SQL begins with `SELECT`, it can return rows as an array, XML text, or a dataset object depending on `vReturnType`. Other statements return a boolean success value. This is the database function that supports named `?varName?` parameter substitution in the SQL text.

## When to use

- When you want to execute a `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or other SQL statement through one function.
- When named `?varName?` SQL parameters are more convenient than positional `?` placeholders.
- When you need control over query result format for `SELECT` statements.
- When you want SQL execution to use the current default connection unless you explicitly pass a connection name.

## Syntax

```ssl
SQLExecute(sCommandString, [sConnectionName], [bRollbackExistingTransaction], [bNullAsBlank], [aInvariantDateCols], [vReturnType], [sTableName], [bIncludeSchema], [bIncludeHeader])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCommandString` | [string](../types/string.md) | yes | — | SQL to execute. Must be a non-empty string. |
| `sConnectionName` | [string](../types/string.md) | no | current default connection | Connection name to run the SQL against. |
| `bRollbackExistingTransaction` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | For non-`SELECT` statements, rolls back the current transaction when execution fails and this argument is [`.T.`](../literals/true.md). |
| `bNullAsBlank` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) for returned `SELECT` results | Controls null-to-blank handling when materializing `SELECT` results. |
| `aInvariantDateCols` | [array](../types/array.md) | no | omitted | Array of date column positions to treat as invariant when materializing `SELECT` results. |
| `vReturnType` | [boolean](../types/boolean.md) or [string](../types/string.md) | no | `"array"` | When the prepared SQL begins with `SELECT`: [`.F.`](../literals/false.md) or non-`xml`/non-`dataset` strings return an array, [`.T.`](../literals/true.md) or `"xml"` returns XML text, and the exact string `"dataset"` returns a dataset object. Ignored for other statements. |
| `sTableName` | [string](../types/string.md) | no | omitted | Optional table name to use for XML or dataset-shaped results when the prepared SQL begins with `SELECT`. |
| `bIncludeSchema` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) when returning XML | Includes schema in XML output. Ignored for array returns, dataset-object returns, and non-`SELECT` statements. |
| `bIncludeHeader` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) when returning XML | Includes header information in XML output. Ignored for array returns, dataset-object returns, and non-`SELECT` statements. |

## Returns

**any**

When the prepared SQL begins with `SELECT`, the return value depends on `vReturnType`:

| Condition | Return type | Behavior |
|-----------|-------------|----------|
| `vReturnType` omitted | [array](../types/array.md) | Returns the rows as an array. |
| `vReturnType` is [`.F.`](../literals/false.md) | [array](../types/array.md) | Returns the rows as an array. |
| `vReturnType` is [`.T.`](../literals/true.md) | [string](../types/string.md) | Returns XML text. |
| `vReturnType` is `"xml"` | [string](../types/string.md) | Returns XML text. |
| `vReturnType` is `"dataset"` | [object](../types/object.md) | Returns a dataset object. |
| `vReturnType` is any other string | [array](../types/array.md) | Returns the rows as an array. |

For other statements, `SQLExecute` returns a boolean success value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sCommandString` is missing, empty, or not a string. | `1st argument must be a non-empty string` |
| `sConnectionName` is provided but is not a string. | `2nd argument must be a string` |
| `bRollbackExistingTransaction` is provided but is not a boolean. | `3rd argument must be a boolean` |
| `bNullAsBlank` is provided but is not a boolean. | `4th argument must be a boolean` |
| `aInvariantDateCols` is provided but is not an array. | `5th argument must be an array` |
| `vReturnType` is provided but is neither a boolean nor a string. | `6th argument must be a boolean/string` |
| `sTableName` is provided but is not a string. | `7th argument must be a string` |
| `bIncludeSchema` is provided but is not a boolean. | `8th argument must be a boolean` |
| `bIncludeHeader` is provided but is not a boolean. | `9th argument must be a boolean` |

## Best practices

!!! success "Do"
    - Use named `?varName?` placeholders instead of building SQL by concatenating values into the string.
    - Set `vReturnType` explicitly when downstream code depends on XML or dataset output.
    - Check the boolean return value for non-`SELECT` statements, especially when transaction behavior matters.

!!! failure "Don't"
    - Use `?varName?` syntax with [`RunSQL`](RunSQL.md), [`LSearch`](LSearch.md), [`LSelect`](LSelect.md), [`LSelect1`](LSelect1.md), [`LSelectC`](LSelectC.md), or [`GetDataSet`](GetDataSet.md); those functions use positional `?` placeholders with an explicit values array.
    - Assume every string `vReturnType` changes the output shape; only `"xml"` and `"dataset"` have special handling.
    - Concatenate user or runtime values directly into SQL text when `SQLExecute` can bind them for you.

## Caveats

- Returning large result sets as arrays, XML, or dataset objects can increase memory use.

## Examples

### Return rows as an array

Execute a parameterized `SELECT` using named `?varName?` substitution and receive the result as a two-dimensional array, one row per element.

```ssl
:PROCEDURE GetLoggedTasks;
	:PARAMETERS sStatus;
	:DEFAULT sStatus, "Logged";
	:DECLARE sSQL, aTasks, nIndex;

	sSQL :=
		"
	    SELECT ordno, testcode, status
	    FROM ordtask
	    WHERE status = ?sStatus?
	    ORDER BY ordno
	";

	aTasks := SQLExecute(sSQL);

	UsrMes("Found " + LimsString(ALen(aTasks)) + " row(s)");
	/* Displays row count;

	:FOR nIndex := 1 :TO ALen(aTasks);
		UsrMes(aTasks[nIndex, 1] + " - " + aTasks[nIndex, 2]);
		/* Displays task row;
	:NEXT;
:ENDPROC;

/* Usage;
DoProc("GetLoggedTasks");
```

### Run an UPDATE and verify success

Execute an `UPDATE` statement and check the boolean return value; use [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) to handle any database error, and roll back on failure by passing [`.T.`](../literals/true.md) as the third argument.

```ssl
:PROCEDURE CompleteTask;
	:PARAMETERS sOrdNo, sTestCode, sUserName;
	:DECLARE sSQL, bSuccess, oErr;

	sSQL :=
		"
	    UPDATE ordtask SET
	        status = 'Complete',
	        completed_by = ?sUserName?
	    WHERE ordno = ?sOrdNo?
	      AND testcode = ?sTestCode?
	";

	:TRY;
		bSuccess := SQLExecute(sSQL,, .T.);

		:IF !bSuccess;
			ErrorMes("Task update failed");
			:RETURN .F.;
		:ENDIF;

		UsrMes("Rows affected: " + LimsString(LimsRecordsAffected()));
		/* Displays affected-row count;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes(oErr:Description);
		/* Displays on failure: database error;
		:RETURN .F.;
	:ENDTRY;

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("CompleteTask", {"ORD-2024-001", "pH", "jsmith"});
```

### Return a dataset and traverse rows with 0-based .NET indexing

Request a dataset object instead of an array, then traverse its rows using the .NET `DataTable` and `DataRowCollection` properties with zero-based indexing.

```ssl
:PROCEDURE ExportBatchAsJson;
	:PARAMETERS sBatch;
	:DEFAULT sBatch, "";
	:DECLARE sSQL, oDs, oTable, oRows, oRow, nCount, nIndex;
	:DECLARE sSampleId, sStatus;

	:IF Empty(sBatch);
		RaiseError("Batch ID is required");
	:ENDIF;

	sSQL :=
		"
	    SELECT sample_id, status, received_date
	    FROM sample
	    WHERE batch_id = ?sBatch?
	    ORDER BY sample_id
	";

	oDs := SQLExecute(sSQL,,,,, "dataset");

	oTable := oDs:GetProperty("Tables")[0];
	oRows := oTable:GetProperty("Rows");
	nCount := oRows:GetProperty("Count");

	UsrMes("Batch " + sBatch + ": " + LimsString(nCount) + " sample(s)");
	/* Displays batch sample count;

	:FOR nIndex := 0 :TO nCount - 1;
		oRow := oRows[nIndex];
		sSampleId := oRow["sample_id"];
		sStatus := oRow["status"];
		UsrMes(sSampleId + " - " + sStatus);
		/* Displays sample status;
	:NEXT;
:ENDPROC;

/* Usage;
DoProc("ExportBatchAsJson", {"B-2024-001"});
```

## Related

- [`GetDataSet`](GetDataSet.md)
- [`LSearch`](LSearch.md)
- [`LSelect`](LSelect.md)
- [`LSelect1`](LSelect1.md)
- [`LSelectC`](LSelectC.md)
- [`LimsRecordsAffected`](LimsRecordsAffected.md)
- [`RunSQL`](RunSQL.md)
- [`array`](../types/array.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
