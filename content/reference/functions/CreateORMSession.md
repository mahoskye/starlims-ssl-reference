---
title: "CreateORMSession"
summary: "Creates the shared ORM session object for the current SSL runtime, or returns the existing one if it has already been created."
id: ssl.function.createormsession
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CreateORMSession

Creates the shared ORM session object for the current SSL runtime, or returns the existing one if it has already been created.

`CreateORMSession` gives SSL one shared ORM session object for the current runtime context. The first call creates that object. Later calls return the same shared session instead of creating another one.

The function also registers ORM-aware table-update checking. When a supported table update runs, SSL calls the session's `UpdatingTable` member with the table name and the update operation's friendly name. The member must return [`.T.`](../literals/true.md) to allow the update or [`.F.`](../literals/false.md) to block it.

## When to use

- When you need one shared ORM session object that can be reused across related SSL code.
- When you want table updates to be allowed or denied through the session's `UpdatingTable` callback.
- When you need repeated calls to return the same session object instead of creating separate session instances.

## Syntax

```ssl
CreateORMSession()
```

## Parameters

This function takes no parameters.

## Returns

**[object](../types/object.md)** — The shared ORM session object.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `UpdatingTable` does not return [`.T.`](../literals/true.md) or [`.F.`](../literals/false.md). | `The method OrmSession:UpdatingTable must return a boolean value` |
| `UpdatingTable` returns [`.F.`](../literals/false.md). | `Not permitted to update table [tableName] when ORM changes are pending` |

## Best practices

!!! success "Do"
    - Call `CreateORMSession` once and reuse the returned object in related code paths.
    - Keep `UpdatingTable` as a simple rule that decides whether a table update should proceed.
    - Return only [`.T.`](../literals/true.md) or [`.F.`](../literals/false.md) from `UpdatingTable`.

!!! failure "Don't"
    - Assume each call creates a fresh session object. The function returns the shared session once it already exists.
    - Return strings, numbers, or [`NIL`](../literals/nil.md) from `UpdatingTable`. A non-boolean return value causes a runtime error.
    - Block updates unintentionally with an overly broad `UpdatingTable` rule.

## Caveats

- `CreateORMSession` does not call `UpdatingTable` by itself. The check runs later when a supported table update is about to execute.

## Examples

### Control table updates with UpdatingTable

Creates an ORM session and assigns a code block to `UpdatingTable` that permits updates only on the `ORDTASK` table through the `LIMS` connection. The [`RunSQL`](RunSQL.md) call triggers the check, which allows or blocks the update based on the table and connection name.

```ssl
:PROCEDURE UpdateAllowedTable;
	:PARAMETERS nTaskID, sNewStatus;
	:DECLARE oOrmSession, bUpdated;

	oOrmSession := CreateORMSession;

	oOrmSession:UpdatingTable := {|sTableName, sConnectionName|
        Upper(sTableName) == "ORDTASK"
            .AND. sConnectionName == "LIMS"
    };

	bUpdated := RunSQL("
	    UPDATE ordtask SET
	        status = ?
	    WHERE task_id = ?
	", "LIMS", {sNewStatus, nTaskID});

	:RETURN bUpdated;
:ENDPROC;

/* Usage;
DoProc("UpdateAllowedTable", {1001, "APPROVED"});
```

## Related

- [`RunSQL`](RunSQL.md)
- [`BeginLimsTransaction`](BeginLimsTransaction.md)
- [`LimsSqlConnect`](LimsSqlConnect.md)
- [`object`](../types/object.md)
- [`boolean`](../types/boolean.md)
