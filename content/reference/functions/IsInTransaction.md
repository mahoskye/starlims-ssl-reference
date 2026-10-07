---
title: "IsInTransaction"
summary: "Returns .T. if the specified database connection currently has an open transaction."
id: ssl.function.isintransaction
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# IsInTransaction

Returns [`.T.`](../literals/true.md) if the specified database connection currently has an open transaction.

`IsInTransaction` checks whether the connection identified by `vConnection` is currently inside a transaction. `vConnection` can be a connection name or a [`SQLConnection`](../classes/SQLConnection.md) object returned by [`GetConnectionByName`](GetConnectionByName.md). If `vConnection` is [`NIL`](../literals/nil.md) or empty, the function checks the default connection. If the supplied name does not match a known connection, or if the internal database collection is unavailable, an error is raised. This function does not alter, begin, or end transactions.

## When to use

- When your logic must decide between transactional or non-transactional execution depending on active transaction state.
- When ensuring that a critical operation (e.g., bulk update, audit trail write) only proceeds inside an open transaction.
- When constructing robust error-handling or compensation routines around transactional operations.

## Syntax

```ssl
IsInTransaction([vConnection])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vConnection` | [string](../types/string.md) or [SQLConnection](../classes/SQLConnection.md) | no | [`NIL`](../literals/nil.md) | Connection name or connection object specifying which database connection to check. If [`NIL`](../literals/nil.md) or empty, the default connection is used. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) if the specified connection is currently within a transaction; [`.F.`](../literals/false.md) if not.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `vConnection` names an unknown connection. | `The provider name: <name> not found.` |
| The runtime database collection has not been initialized. | `The internal database collection is null` |

## Best practices

!!! success "Do"
    - Pass explicit, known-good connection names when checking transaction state.
    - Use a `bStarted` flag set from [`BeginLimsTransaction`](BeginLimsTransaction.md), not `IsInTransaction`, to decide whether your code should end a transaction.
    - Use with [`BeginLimsTransaction`](BeginLimsTransaction.md) and [`EndLimsTransaction`](EndLimsTransaction.md) for end-to-end transaction management.

!!! failure "Don't"
    - Pass user-supplied or dynamic connection names without validating them first. Invalid names raise errors.
    - Use this function as a transaction manager or depth counter. It checks boolean state only.
    - Treat [`.T.`](../literals/true.md) as proof that your code began the transaction. A helper that ends the transaction after this check ends its caller's transaction.
    - Assume the function returns [`.F.`](../literals/false.md) for unknown connections. It raises an error instead.

## Caveats

- If `vConnection` is [`NIL`](../literals/nil.md), empty, or missing, the default connection is used.
- `vConnection` can be a connection name or a [`SQLConnection`](../classes/SQLConnection.md) object returned by [`GetConnectionByName`](GetConnectionByName.md).
- Passing an unknown connection name raises an error rather than returning [`.F.`](../literals/false.md).
- If the internal database collection is unavailable, an error is raised and the function does not return a value.
- Returns [`.T.`](../literals/true.md) for any open transaction on the connection, including one a caller began and at any nesting depth. It cannot tell a routine whether it owns the transaction, and it does not report the nesting depth; use [`GetTransactionsCount`](GetTransactionsCount.md) for that.

## Examples

### Require the caller's transaction before a dependent write

A helper that writes an audit row only when a caller already has a transaction open, so the row commits or rolls back with the caller's work. The helper did not begin that transaction, so it does not end it.

```ssl
:PROCEDURE WriteAuditEntry;
	:PARAMETERS sSampleID;
	:DECLARE bInTrans;

	bInTrans := IsInTransaction();

	:IF bInTrans;
		RunSQL(
			"INSERT INTO audit_log (sample_id, action) VALUES (?, ?)",,
			{sSampleID, "STATUS_CHANGE"}
		);
		UsrMes("Audit entry added to the open transaction");
	:ELSE;
		UsrMes("No open transaction, audit entry not written");
	:ENDIF;

	/* The caller began the transaction, so the caller ends it;
	:RETURN bInTrans;
:ENDPROC;

/* Usage;
DoProc("WriteAuditEntry", {"S-001"});
```

Called with no transaction open, [`UsrMes`](UsrMes.md) logs:

```text
No open transaction, audit entry not written
```

### Check a named connection with error handling

Pass an explicit connection name and wrap the call in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) to handle unknown connection errors gracefully. The catch block retrieves the error with [`GetLastSSLError`](GetLastSSLError.md) and logs it via [`ErrorMes`](ErrorMes.md).

```ssl
:PROCEDURE CheckNamedConnectionTransaction;
	:PARAMETERS sConnectionName;
	:DECLARE bInTransaction, oErr;

	:TRY;
		bInTransaction := IsInTransaction(sConnectionName);

		:IF bInTransaction;
			UsrMes(sConnectionName + " has an active transaction");
		:ELSE;
			UsrMes(sConnectionName + " has no active transaction");
		:ENDIF;

		:RETURN bInTransaction;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("Transaction check failed: " + oErr:Description);
		/* Logs on failure: transaction check failed;
		:RETURN .F.;
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("CheckNamedConnectionTransaction", {"DATABASE"});
```

## Related

- [`BeginLimsTransaction`](BeginLimsTransaction.md)
- [`EndLimsTransaction`](EndLimsTransaction.md)
- [`GetConnectionByName`](GetConnectionByName.md)
- [`GetTransactionsCount`](GetTransactionsCount.md)
- [`SQLConnection`](../classes/SQLConnection.md)
- [`boolean`](../types/boolean.md)
