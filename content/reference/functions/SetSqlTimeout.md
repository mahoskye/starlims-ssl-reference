---
title: "SetSqlTimeout"
summary: "Sets the SQL command timeout for a database connection and returns the previous timeout value for that same connection."
id: ssl.function.setsqltimeout
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SetSqlTimeout

Sets the SQL command timeout for a database connection and returns the previous timeout value for that same connection.

`SetSqlTimeout(nTimeout, sConnection)` applies a new timeout value in seconds and returns the timeout that was in effect before the change. If `nTimeout` is omitted or [`NIL`](../literals/nil.md), the function uses `30`. If `sConnection` is omitted, [`NIL`](../literals/nil.md), or an empty string, the current default connection is used.

The function validates only the public argument types before applying the change: `nTimeout` must be an integer-valued number when supplied, and `sConnection` must be a string when supplied.

## When to use

- When you need a longer timeout around a known slow query or batch update.
- When you want to tighten the timeout for a specific operation and then restore the previous setting.
- When different named connections need different timeout values during the same script.

## Syntax

```ssl
SetSqlTimeout([nTimeout], [sConnection])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nTimeout` | [number](../types/number.md) | no | `30` | New SQL command timeout in seconds. When supplied, it must be an integer-valued number. |
| `sConnection` | [string](../types/string.md) | no | current default connection | Connection name to update. If omitted, [`NIL`](../literals/nil.md), or `""`, the current default connection is used. |

## Returns

**[number](../types/number.md)** — The previous SQL command timeout for the targeted connection.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `nTimeout` is supplied but is not an integer-valued number. | `Argument 'nTimeout' must be an integer.` |
| `sConnection` is supplied but is not a string. | `Argument 'sConnection' must be a string.` |

## Best practices

!!! success "Do"
    - Save the returned timeout value and restore it after the temporary operation finishes.
    - Keep timeout changes scoped to the smallest practical block of database work.
    - Pass an explicit connection name when the script works with more than one database connection.

!!! failure "Don't"
    - Pass fractional values such as `3.5`; the function rejects non-integer numbers.
    - Assume a timeout change resets automatically after the next query.
    - Change one named connection and expect the timeout on other connections to change with it.

## Caveats

- This function changes the timeout on the targeted connection immediately.

## Examples

### Temporarily extend the timeout on the default connection

Save the previous timeout, extend it for a slow query, then restore the original value in [`:FINALLY`](../keywords/FINALLY.md) so the default connection is always left in a known state.

```ssl
:PROCEDURE LoadRecentOrders;
	:DECLARE dCutoff, nPrevTimeout, aOrders;

	dCutoff := Today() - 7;
	nPrevTimeout := SetSqlTimeout(90);

	:TRY;
		aOrders := SQLExecute("
		    SELECT ordno, status, logdate
		    FROM orders
		    WHERE logdate >= ?dCutoff?
		    ORDER BY logdate DESC
		");

		UsrMes("Loaded " + LimsString(ALen(aOrders)) + " recent orders");
		/* Displays loaded recent orders count;
	:FINALLY;
		SetSqlTimeout(nPrevTimeout);
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("LoadRecentOrders");
```

### Apply a timeout to a specific named connection

Extend the timeout on a named connection before a long update, then restore it in [`:FINALLY`](../keywords/FINALLY.md) regardless of whether the update succeeds.

```ssl
:PROCEDURE RefreshArchiveSummary;
	:DECLARE sConnection, nPrevTimeout, bUpdated;

	sConnection := "ARCHIVE";
	bUpdated := .F.;
	nPrevTimeout := SetSqlTimeout(180, sConnection);

	:TRY;
		bUpdated := RunSQL("
		    UPDATE archive_jobs SET
		        status = ?,
		        completed_date = SYSDATE
		    WHERE status = ?
		      AND completed_date IS NULL
		",
			sConnection, {"Complete", "Running"});

		:IF bUpdated;
			InfoMes("Archive summary refresh completed");
		:ENDIF;
	:FINALLY;
		SetSqlTimeout(nPrevTimeout, sConnection);
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("RefreshArchiveSummary");
```

### Save and restore timeouts independently across two connections

Set different timeouts on two named connections, query each, then restore both original values in [`:FINALLY`](../keywords/FINALLY.md) in reverse order.

```ssl
:PROCEDURE CompareOperationalAndArchiveCounts;
	:DECLARE nOpsPrevTimeout, nArchivePrevTimeout;
	:DECLARE aOpsRows, aArchiveRows;

	nOpsPrevTimeout := SetSqlTimeout(45, "LIMS");
	nArchivePrevTimeout := SetSqlTimeout(180, "ARCHIVE");

	:TRY;
		aOpsRows := SQLExecute("
		    SELECT COUNT(*) AS row_count
		    FROM orders
		    WHERE status = 'Logged'
		",
			"LIMS");

		aArchiveRows := SQLExecute("
		    SELECT COUNT(*) AS row_count
		    FROM orders_archive
		    WHERE archived_flag = 'Y'
		",
			"ARCHIVE");

		InfoMes(
			"Operational rows: " + LimsString(aOpsRows[1, 1])
			+ ", archive rows: " + LimsString(aArchiveRows[1, 1])
		);
		/* Displays operational and archive row counts;
	:FINALLY;
		SetSqlTimeout(nArchivePrevTimeout, "ARCHIVE");
		SetSqlTimeout(nOpsPrevTimeout, "LIMS");
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("CompareOperationalAndArchiveCounts");
```

## Related

- [`GetDefaultConnection`](GetDefaultConnection.md)
- [`IgnoreSqlErrors`](IgnoreSqlErrors.md)
- [`ShowSqlErrors`](ShowSqlErrors.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
