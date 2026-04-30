---
title: "ExtractCol"
summary: "Extracts one column from a two-dimensional array and returns the extracted values as a new array."
id: ssl.function.extractcol
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ExtractCol

Extracts one column from a two-dimensional [array](../types/array.md) and returns the extracted values as a new array.

`ExtractCol` reads the specified 1-based column from each row in a two-dimensional array and builds a new array containing those values in the same order. `aTarget` must be an array whose elements are also arrays. If `aTarget` is empty, `ExtractCol` returns an empty array immediately.

## When to use

- When extracting a single field from every record in a tabular data array for processing or reporting.
- When performing aggregate or statistical operations on values from a specific column across multiple entries.
- When transforming or preparing two-dimensional array data for input into another API, visual component, or export routine.

## Syntax

```ssl
ExtractCol(aTarget, nColumn)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aTarget` | [array](../types/array.md) | yes | — | Two-dimensional source array. Each top-level element must be a row array. |
| `nColumn` | [number](../types/number.md) | yes | — | 1-based column index to extract from each row. |

## Returns

**[array](../types/array.md)** — A new array containing the value from `nColumn` for each row in `aTarget`, in row order.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aTarget` is [`NIL`](../literals/nil.md). | `Target array cannot be null.` |
| `nColumn` is [`NIL`](../literals/nil.md) and `aTarget` is not empty. | `Column number cannot be null.` |
| `nColumn` is not an integer. | `Column number must be an integer value.` |
| `nColumn` is less than `1`. | `Column number cannot be less than one.` |
| Any row is not an array. | `Target must be an array of arrays (a two dimensional array).` |
| `nColumn` exceeds the length of any row. | `Column number cannot exceed the number of elements in any sub-array.` |

## Best practices

!!! success "Do"
    - Validate `nColumn` and the shape of `aTarget` before calling.
    - Use one-based column indexing as required.
    - Check for an empty result before chaining the extracted values into later work.

!!! failure "Don't"
    - Assume every row has the same shape. A short or malformed row raises an error for the whole call.
    - Use zero-based or negative indices. Indexes less than one will always raise an error.
    - Pass a one-dimensional array. `ExtractCol` expects each top-level element to be a row array.

## Caveats

- An empty `aTarget` returns an empty array immediately, before `nColumn` is validated.

## Examples

### Extract a single field from every record

Extracts the first column (user ID) from a set of user records and displays each extracted value. This pattern isolates one field from all rows without iterating over the source array manually.

```ssl
:PROCEDURE ExtractUserIDs;
	:DECLARE aUserRecords, aUserIDs, nIndex;

	aUserRecords := {
		{"U001", "Alice Smith", "Laboratory"},
		{"U002", "Bob Jones", "Quality"},
		{"U003", "Carol White", "Laboratory"},
		{"U004", "David Brown", "Operations"}
	};

	aUserIDs := ExtractCol(aUserRecords, 1);

	:FOR nIndex := 1 :TO ALen(aUserIDs);
		UsrMes(LimsString(aUserIDs[nIndex]));
	:NEXT;

	:RETURN aUserIDs;
:ENDPROC;

/* Usage;
DoProc("ExtractUserIDs");
```

[`UsrMes`](UsrMes.md) displays one value per iteration:

```text
U001
U002
U003
U004
```

### Sum a numeric column across all rows

Extracts the third column (order total) from each row and accumulates the values into a running sum. The approach avoids manually indexing into each row when only one column is needed.

```ssl
:PROCEDURE SumOrderTotals;
	:DECLARE aOrders, aTotals, nSum, nCount, nIndex, sReport;

	aOrders := {
		{"ORD-1001", 3, 150.00},
		{"ORD-1002", 1, 42.50},
		{"ORD-1003", 5, 320.75},
		{"ORD-1004", 2, 89.00},
		{"ORD-1005", 4, 210.25}
	};

	aTotals := ExtractCol(aOrders, 3);

	nSum := 0;

	:FOR nIndex := 1 :TO ALen(aTotals);
		nSum += aTotals[nIndex];
	:NEXT;

	nCount := ALen(aOrders);
	sReport := "Processed " + LimsString(nCount)
				+ " orders totaling " + LimsString(nSum);

	UsrMes(sReport);

	:RETURN nSum;
:ENDPROC;

/* Usage;
DoProc("SumOrderTotals");
```

[`UsrMes`](UsrMes.md) displays:

```text
Processed 5 orders totaling 812.5
```

### Use extracted keys in a follow-up query

Queries open orders for a customer, extracts the order number column from the result, and passes those keys as a parameter to a second query that loads matching tasks.

```ssl
:PROCEDURE LoadTasksForCustomer;
	:PARAMETERS sCustomerID;
	:DECLARE aOrderRows, aOrdNos, aTaskRows;

	aOrderRows := LSelect1("
	    SELECT ordno, status
	    FROM orders
	    WHERE customer_id = ?
	      AND status = ?
	",, {sCustomerID, "Logged"});

	:IF ALen(aOrderRows) == 0;
		:RETURN {};
	:ENDIF;

	aOrdNos := ExtractCol(aOrderRows, 1);

	aTaskRows := SQLExecute("
	    SELECT ordno, testcode, status
	    FROM ordtask
	    WHERE ordno IN (?aOrdNos?)
	    ORDER BY ordno, testcode
	");

	:RETURN aTaskRows;
:ENDPROC;

/* Usage;
DoProc("LoadTasksForCustomer", {"CUST-001"});
```

## Related

- [`BuildArray2`](BuildArray2.md)
- [`BuildString2`](BuildString2.md)
- [`array`](../types/array.md)
- [`number`](../types/number.md)
