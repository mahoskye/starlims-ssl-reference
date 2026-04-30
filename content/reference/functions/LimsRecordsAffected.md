---
title: "LimsRecordsAffected"
summary: "Returns the number of records affected by the most recent database operation."
id: ssl.function.limsrecordsaffected
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LimsRecordsAffected

Returns the number of records affected by the most recent database operation.

`LimsRecordsAffected` reads the row count from the most recent INSERT, UPDATE, or DELETE against the active connection. It takes no parameters. Returns `0` when called before any modification statement, after a SELECT, or after a failed operation. The count reflects only the last modifying statement - calling it multiple times without an intervening operation returns the same value.

## When to use

- When you need to confirm how many records were updated, inserted, or deleted by the most recent SQL statement.
- When validating that a batch operation affected the expected number of records in a workflow.
- When logging or auditing database changes for compliance and review.
- When rolling back logic after detecting an unexpected number of affected records.

## Syntax

```ssl
LimsRecordsAffected()
```

## Parameters

This function takes no parameters.

## Returns

**[number](../types/number.md)** — Number of records affected by the last database operation.

## Best practices

!!! success "Do"
    - Call immediately after the database operation you want to measure.
    - Use to verify critical batch processes by comparing expected and actual affected records.
    - Use in error handling routines to detect unintended changes.

!!! failure "Don't"
    - Rely on its value after running other queries. The count reflects only the most recent modification statement.
    - Assume all operations that modify data update this count reliably. Some drivers or non-standard SQL operations may behave differently.
    - Trust the count if there was an error or transaction rollback. Failed or rolled back operations reset or leave the count at 0.

## Caveats

- If the database connection changes context between operations, the result may not match the previous transaction.

## Examples

### Check update success after an inventory adjustment

Call `LimsRecordsAffected` immediately after an UPDATE to verify that exactly one row was modified. When the expected count matches, the success message fires; otherwise, a warning is shown.

```ssl
:PROCEDURE AdjustInventoryCount;
	:DECLARE sItemID, nExpected, nUpdated, bSuccess, sMessage;

	sItemID := "INV-2024-0042";
	nExpected := 1;

	bSuccess := RunSQL("
	    UPDATE inventory SET
	        quantity = quantity + 10
	    WHERE item_id = ?
	",
		, {sItemID});
	nUpdated := LimsRecordsAffected();

	:IF bSuccess .AND. nUpdated == nExpected;
		sMessage := "Inventory adjusted: " + LimsString(nUpdated) + " record updated for "
			+ sItemID;
	:ELSE;
		sMessage := "Warning: Expected " + LimsString(nExpected) + " update but got " + LimsString(
			nUpdated);
	:ENDIF;

	UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("AdjustInventoryCount");
```

`UsrMes` displays on success:

```text
Inventory adjusted: 1 record updated for INV-2024-0042
```

### Audit bulk deletion results for compliance reporting

Use `LimsRecordsAffected` inside a [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) block after a bulk DELETE to count the removed rows. If the DELETE fails, the catch block surfaces the error.

```ssl
:PROCEDURE AuditBulkDeletion;
	:PARAMETERS sCutoff;
	:DEFAULT sCutoff, "2024-01-01";
	:DECLARE nDeleted, oErr;

	:TRY;
		RunSQL("
		    DELETE FROM sample
		    WHERE status = 'I'
		      AND createdate < ?
		",
			, {sCutoff});
		nDeleted := LimsRecordsAffected();
		UsrMes("Bulk cleanup removed " + LimsString(nDeleted) + " records");
		/* Displays: Bulk cleanup removed records;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("Deletion audit failed: " + oErr:Description);
		/* Displays on failure: deletion audit failed;
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("AuditBulkDeletion");
```

## Related

- [`RunSQL`](RunSQL.md)
- [`SQLExecute`](SQLExecute.md)
- [`number`](../types/number.md)
