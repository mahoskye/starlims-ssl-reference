---
title: "CreateGUID"
summary: "Generates a new GUID string in uppercase."
id: ssl.function.createguid
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CreateGUID

Generates a new GUID string in uppercase.

Use `CreateGUID` when you need a fresh identifier for records, correlation IDs, or temporary keys. The function takes no parameters and returns a newly generated uppercase GUID string.

## When to use

- When assigning a unique key that must remain distinct across records or systems.
- When generating correlation IDs for logging, integration, or import processing.
- When creating temporary identifiers for files, queues, or other short-lived work items.

## Syntax

```ssl
CreateGUID()
```

## Parameters

This function takes no parameters.

## Returns

**[string](../types/string.md)** — A newly generated GUID string in standard hyphenated uppercase form.

## Best practices

!!! success "Do"
    - Store and use GUIDs as strings exactly as returned.
    - Use the generated value for identifiers that must be unique across records or systems.
    - Validate incoming GUID text with [`IsGuid`](IsGuid.md) when the value did not come directly from `CreateGUID`.

!!! failure "Don't"
    - Truncate or reshape the GUID before storing it. That can break systems that expect a full GUID value.
    - Use GUIDs where ordered or human-friendly identifiers are required.
    - Treat external text as valid GUID data without checking it first.

## Caveats

- The returned value is uppercase and includes hyphens.
- The function returns a string, not a numeric or sequential identifier.
- Use a separate validation step such as [`IsGuid`](IsGuid.md) for GUID values received from users, files, or external systems.

## Examples

### Assign a GUID to a new record

Generates a GUID, assigns it to a new object, and displays the value. The GUID value differs on every call.

```ssl
:PROCEDURE PrepareOrderRecord;
	:DECLARE sOrderId, oOrder;

	oOrder := CreateUdObject();
	sOrderId := CreateGUID();

	oOrder:orderId := sOrderId;

	UsrMes("Prepared order record with ID: " + sOrderId);
	/* Displays the prepared order ID;

	:RETURN oOrder;
:ENDPROC;

/* Usage;
DoProc("PrepareOrderRecord");
```

### Reuse one correlation ID across steps

Generates one GUID and uses it in three separate messages so related work can be correlated by the same ID. All three lines show the same GUID, and the value differs on every call.

```ssl
:PROCEDURE LogRequestAcrossSteps;
	:DECLARE sRequestId, sMessage;

	sRequestId := CreateGUID();

	sMessage := "Received request " + sRequestId;
	UsrMes(sMessage);
	/* Displays the request ID;

	sMessage := "Queued inventory update for " + sRequestId;
	UsrMes(sMessage);
	/* Displays the inventory queue ID;

	sMessage := "Queued laboratory work for " + sRequestId;
	UsrMes(sMessage);
	/* Displays the laboratory queue ID;
:ENDPROC;

/* Usage;
DoProc("LogRequestAcrossSteps");
```

### Assign batch and row IDs during import

Generates one batch GUID shared across all rows and one unique row GUID per item, then saves each row with both identifiers.

```ssl
:PROCEDURE PrepareImportRows;
	:PARAMETERS nCount;
	:DEFAULT nCount, 50;
	:DECLARE aRows, oImportBatch, sBatchId, nIndex, oRow;
	:DECLARE nPrepared, sLogEntry;

	aRows := {};
	sBatchId := CreateGUID();
	nPrepared := 0;

	:FOR nIndex := 1 :TO nCount;
		oRow := CreateUdObject();
		oRow:batchId := sBatchId;
		oRow:rowId := CreateGUID();
		oRow:rowNumber := nIndex;
		AAdd(aRows, oRow);

		nPrepared += 1;
	:NEXT;

	oImportBatch := CreateUdObject();
	oImportBatch:batchId := sBatchId;
	oImportBatch:rows := aRows;
	oImportBatch:count := nPrepared;
	oImportBatch:createdDate := Today();

	sLogEntry := "Prepared batch " + sBatchId + " with "
				 + LimsString(nPrepared) + " import rows";
	UsrMes(sLogEntry);
	/* Displays the prepared batch summary;

	:RETURN oImportBatch;
:ENDPROC;

:PROCEDURE SaveImportRows;
	:PARAMETERS nCount;
	:DEFAULT nCount, 100;
	:DECLARE oBatch, aRows, sSQL, bInserted, oRow;
	:DECLARE nIndex, nRowCount;

	oBatch := DoProc("PrepareImportRows", {nCount});
	aRows := oBatch:rows;
	nRowCount := Len(aRows);

	sSQL := "
			INSERT INTO import_queue (batch_id, row_id, ROW_NUMBER)
			VALUES (?, ?, ?)
		";

	:FOR nIndex := 1 :TO nRowCount;
		oRow := aRows[nIndex];

		bInserted := RunSQL(sSQL,, {oRow:batchId, oRow:rowId, oRow:rowNumber});

		:IF !bInserted;
			ErrorMes("Failed to insert import row: " + oRow:rowId);
			/* Displays an insert failure with the row ID;
		:ENDIF;
	:NEXT;

	UsrMes("Saved " + LimsString(nRowCount) + " import rows for batch "
			+ oBatch:batchId);
	/* Displays the saved batch summary;
:ENDPROC;

/* Usage;
DoProc("SaveImportRows", {100});
```

## Related

- [`IsGuid`](IsGuid.md)
- [`string`](../types/string.md)
- [`object`](../types/object.md)
