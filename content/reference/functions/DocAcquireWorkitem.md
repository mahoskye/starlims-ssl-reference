---
title: "DocAcquireWorkitem"
summary: "Acquires a Documentum work item and returns whether the acquisition succeeded."
id: ssl.function.docacquireworkitem
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocAcquireWorkitem

Acquires a Documentum work item and returns whether the acquisition succeeded.

`DocAcquireWorkitem` takes one required work item identifier. If `sWorkitemId` is [`NIL`](../literals/nil.md), the function raises an argument-null exception immediately. Otherwise it attempts the acquisition and returns [`.T.`](../literals/true.md) or [`.F.`](../literals/false.md) based on the underlying Documentum call result. Each call clears the current Documentum error state before running, then records the exception message only when the acquisition fails. After a [`.F.`](../literals/false.md) result, use [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) to inspect the recorded failure for that same call.

## When to use

- When a workflow step must explicitly acquire a work item before continuing.
- When your script needs a boolean success result instead of relying on exceptions for normal acquisition failures.
- When you want to inspect Documentum failure state with [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) after a [`.F.`](../literals/false.md) result.

## Syntax

```ssl
DocAcquireWorkitem(sWorkitemId)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sWorkitemId` | [string](../types/string.md) | yes | — | Identifier of the work item to acquire. Passing [`NIL`](../literals/nil.md) raises an error. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the work item is acquired successfully, or [`.F.`](../literals/false.md) when the underlying Documentum acquisition call fails or returns no result.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sWorkitemId` is [`NIL`](../literals/nil.md). | `sWorkitemId argument cannot be null` |

## Best practices

!!! success "Do"
    - Check the return value before running logic that depends on the work item being acquired.
    - Call [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after a failed acquisition when you need diagnostic detail.
    - Validate that `sWorkitemId` is not [`NIL`](../literals/nil.md) before calling the function.
    - Use the function within an active Documentum session that has already been initialized and logged in.

!!! failure "Don't"
    - Assume the work item was acquired just because the call completed. The function can return [`.F.`](../literals/false.md) for failed acquisitions.
    - Pass [`NIL`](../literals/nil.md) as the identifier. That raises an exception instead of returning [`.F.`](../literals/false.md).
    - Wait until after another Documentum call to inspect [`DocCommandFailed`](DocCommandFailed.md) or [`DocGetErrorMessage`](DocGetErrorMessage.md). A later call can replace the earlier failure state.
    - Discard a failed result without checking whether Documentum recorded an error message for the attempt.

## Caveats

- A [`.F.`](../literals/false.md) return means the acquisition did not succeed, but the boolean alone does not describe the cause.

## Examples

### Acquire a work item after logging in to Documentum

Logs in to a Documentum repository, acquires a specific work item, and displays whether the acquisition succeeded.

```ssl
:PROCEDURE AcquireWorkitemForProcessing;
	:DECLARE sDocBase, sUser, sPassword, sWorkitemId, bLoggedIn, bAcquired;

	sDocBase := "Repository1";
	sUser := "analyst";
	sPassword := "secret";
	sWorkitemId := "WI-2024-00147";

	DocInitDocumentumInterface();

	bLoggedIn := DocLoginToDocumentum(sDocBase, sUser, sPassword);

	:IF .NOT. bLoggedIn;
		ErrorMes("Documentum login failed: " + DocGetErrorMessage());
		DocEndDocumentumInterface();
		:RETURN .F.;
	:ENDIF;

	bAcquired := DocAcquireWorkitem(sWorkitemId);

	:IF bAcquired;
		UsrMes("Work item " + sWorkitemId + " acquired successfully");
	:ELSE;
		ErrorMes("Could not acquire work item " + sWorkitemId);
	:ENDIF;

	DocEndDocumentumInterface();

	:RETURN bAcquired;
:ENDPROC;

/* Usage;
DoProc("AcquireWorkitemForProcessing");
```

### Capture the Documentum error message immediately after a failed acquisition

Accepts the work item identifier as a procedure parameter, attempts acquisition, and builds a diagnostic error message by appending the Documentum error description when [`DocCommandFailed`](DocCommandFailed.md) reports a failure.

```ssl
:PROCEDURE AcquireWorkitemWithDiagnostics;
	:PARAMETERS sWorkitemId;
	:DECLARE sDocBase, sUser, sPassword, bLoggedIn, bAcquired, sErrMsg;

	sDocBase := "Repository1";
	sUser := "analyst";
	sPassword := "secret";

	DocInitDocumentumInterface();

	bLoggedIn := DocLoginToDocumentum(sDocBase, sUser, sPassword);

	:IF .NOT. bLoggedIn;
		ErrorMes("Documentum login failed: " + DocGetErrorMessage());
		DocEndDocumentumInterface();
		:RETURN .F.;
	:ENDIF;

	bAcquired := DocAcquireWorkitem(sWorkitemId);

	:IF .NOT. bAcquired;
		sErrMsg := "Work item " + sWorkitemId + " could not be acquired";

		:IF DocCommandFailed();
			sErrMsg := sErrMsg + ": " + DocGetErrorMessage();
		:ENDIF;

		ErrorMes(sErrMsg);
	:ENDIF;

	DocEndDocumentumInterface();

	:RETURN bAcquired;
:ENDPROC;

/* Usage;
DoProc("AcquireWorkitemWithDiagnostics", {"WI-2024-00147"});
```

### Acquire multiple work items and collect each failure message before the next call

Iterates a list of work item identifiers, acquires each one, and collects failure messages immediately after each failed attempt — before the next acquisition replaces the Documentum error state.

```ssl
:PROCEDURE AcquireWorkitemsInBatch;
	:DECLARE sDocBase, sUser, sPassword, aWorkitemIds, aFailures;
	:DECLARE sWorkitemId, sErrMsg, bLoggedIn, bAcquired, nIndex;

	sDocBase := "Repository1";
	sUser := "analyst";
	sPassword := "secret";
	aWorkitemIds := {"WI-2024-00147", "WI-2024-00148", "WI-2024-00149"};
	aFailures := {};

	DocInitDocumentumInterface();

	bLoggedIn := DocLoginToDocumentum(sDocBase, sUser, sPassword);

	:IF .NOT. bLoggedIn;
		ErrorMes("Documentum login failed: " + DocGetErrorMessage());
		DocEndDocumentumInterface();
		:RETURN {};
	:ENDIF;

	:FOR nIndex := 1 :TO ALen(aWorkitemIds);
		sWorkitemId := aWorkitemIds[nIndex];
		bAcquired := DocAcquireWorkitem(sWorkitemId);

		:IF .NOT. bAcquired;
			sErrMsg := sWorkitemId;

			:IF DocCommandFailed();
				sErrMsg := sErrMsg + ": " + DocGetErrorMessage();
			:ENDIF;

			AAdd(aFailures, sErrMsg);
		:ENDIF;
	:NEXT;

	DocEndDocumentumInterface();

	:RETURN aFailures;
:ENDPROC;

/* Usage;
DoProc("AcquireWorkitemsInBatch");
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
