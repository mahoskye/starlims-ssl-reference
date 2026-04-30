---
title: "DocDelegateWorkitem"
summary: "Delegates a Documentum workflow work item to another user and returns whether the delegation succeeded."
id: ssl.function.docdelegateworkitem
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocDelegateWorkitem

Delegates a Documentum workflow work item to another user and returns whether the delegation succeeded.

`DocDelegateWorkitem` takes a work item identifier and a target user. If either argument is [`NIL`](../literals/nil.md), the function raises an argument-null error immediately. Otherwise it attempts the delegation and returns [`.T.`](../literals/true.md) on success. The function returns [`.F.`](../literals/false.md) when the underlying delegation call returns false or when the call throws an exception. Use [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) to check whether a failed call also recorded a Documentum error.

## When to use

- When you need to reassign a Documentum workflow work item to another user
  from SSL code.
- When your script needs a boolean success result instead of relying on
  exceptions for routine delegation failures.
- When you want to distinguish a plain [`.F.`](../literals/false.md) result from a failed call that also recorded a Documentum error.

## Syntax

```ssl
DocDelegateWorkitem(sWorkitemId, sTargetUser)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sWorkitemId` | [string](../types/string.md) | yes | — | Identifier of the work item to delegate. Passing [`NIL`](../literals/nil.md) raises an error. |
| `sTargetUser` | [string](../types/string.md) | yes | — | User name that should receive the delegated work item. Passing [`NIL`](../literals/nil.md) raises an error. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the work item is delegated successfully; otherwise [`.F.`](../literals/false.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sWorkitemId` is [`NIL`](../literals/nil.md). | `sWorkitemId argument cannot be null` |
| `sTargetUser` is [`NIL`](../literals/nil.md). | `sTargetUser argument cannot be null` |

## Best practices

!!! success "Do"
    - Validate both `sWorkitemId` and `sTargetUser` before calling so the function does not raise on [`NIL`](../literals/nil.md) input.
    - Check the boolean return value before continuing workflow logic that assumes the delegation succeeded.
    - If the function returns [`.F.`](../literals/false.md), check [`DocCommandFailed`](DocCommandFailed.md) before relying on [`DocGetErrorMessage`](DocGetErrorMessage.md) for the failure reason.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sWorkitemId` or `sTargetUser`. That raises an argument-null exception instead of returning [`.F.`](../literals/false.md).
    - Assume the delegation succeeded just because the call completed. The function can return [`.F.`](../literals/false.md) for failed delegation attempts.
    - Ignore a failed result without checking whether Documentum recorded an error message for the attempt.

## Caveats

- A [`.F.`](../literals/false.md) return means the delegation did not succeed, but the boolean alone does not distinguish between a plain failed delegation and an exception.
- The previous Documentum failure state is cleared at the start of the call. If this delegation attempt fails with an exception, that exception becomes the current Documentum error.
- If the delegation returns [`.F.`](../literals/false.md) without throwing an exception, [`DocCommandFailed`](DocCommandFailed.md) remains [`.F.`](../literals/false.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) stays empty.

## Examples

### Delegate a work item and check the boolean result

Delegates a work item to a named user and displays success or failure based on the boolean return value.

```ssl
:PROCEDURE DelegateSingleWorkitem;
	:DECLARE sWorkitemId, sTargetUser, bDelegated;

	sWorkitemId := "WI-2024-00142";
	sTargetUser := "jsmith";

	bDelegated := DocDelegateWorkitem(sWorkitemId, sTargetUser);

	:IF bDelegated;
		UsrMes("Work item " + sWorkitemId + " delegated to " + sTargetUser);
	:ELSE;
		UsrMes("Could not delegate work item " + sWorkitemId);
	:ENDIF;

	:RETURN bDelegated;
:ENDPROC;

/* Usage;
DoProc("DelegateSingleWorkitem");
```

### Validate inputs and return a structured result with any Documentum message

Validates that both required values are non-empty before calling the function, then returns a result object carrying the success flag and any Documentum error message.

```ssl
:PROCEDURE TryDelegateWorkitem;
	:PARAMETERS sWorkitemId, sTargetUser;
	:DECLARE oResult;

	oResult := CreateUdObject();
	oResult:success := .F.;
	oResult:message := "";

	:IF Empty(sWorkitemId);
		oResult:message := "A work item ID is required";
		:RETURN oResult;
	:ENDIF;

	:IF Empty(sTargetUser);
		oResult:message := "A target user is required";
		:RETURN oResult;
	:ENDIF;

	oResult:success := DocDelegateWorkitem(sWorkitemId, sTargetUser);

	:IF oResult:success;
		oResult:message := "Delegation succeeded";
		:RETURN oResult;
	:ENDIF;

	oResult:message := "Delegation failed";

	:IF DocCommandFailed();
		oResult:message := DocGetErrorMessage();
	:ENDIF;

	:RETURN oResult;
:ENDPROC;

/* Usage;
DoProc("TryDelegateWorkitem", {"WI-2024-00142", "jsmith"});
```

### Delegate a batch of work items and collect per-item outcomes

Iterates a work item ID array parameter, skips any blank IDs, delegates each valid item to the target user, and returns an array of result objects with the outcome and any Documentum message for each item.

```ssl
:PROCEDURE DelegateWorkitemBatch;
	:PARAMETERS aWorkitemIds, sTargetUser;
	:DECLARE aResults, nIndex, oItemResult, sWorkitemId;

	aResults := {};

	:IF Empty(sTargetUser);
		UsrMes("A target user is required before batch delegation");
		:RETURN aResults;
	:ENDIF;

	:FOR nIndex := 1 :TO ALen(aWorkitemIds);
		sWorkitemId := aWorkitemIds[nIndex];
		oItemResult := CreateUdObject();
		oItemResult:workitemId := sWorkitemId;
		oItemResult:success := .F.;
		oItemResult:message := "";

		:IF Empty(sWorkitemId);
			oItemResult:message := "Skipped empty work item ID";
			AAdd(aResults, oItemResult);
			:LOOP;
		:ENDIF;

		oItemResult:success := DocDelegateWorkitem(sWorkitemId, sTargetUser);

		:IF oItemResult:success;
			oItemResult:message := "Delegated successfully";
		:ELSE;
			oItemResult:message := "Delegation failed";

			:IF DocCommandFailed();
				oItemResult:message := DocGetErrorMessage();
			:ENDIF;
		:ENDIF;

		AAdd(aResults, oItemResult);
	:NEXT;

	:RETURN aResults;
:ENDPROC;

/* Usage;
DoProc(
	"DelegateWorkitemBatch",
	{{"WI-2024-00142", "WI-2024-00143"}, "jsmith"}
);
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocAcquireWorkitem`](DocAcquireWorkitem.md)
- [`DocCompleteWorkitem`](DocCompleteWorkitem.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocGetWorkflowStatus`](DocGetWorkflowStatus.md)
- [`DocGetWorkitemProperties`](DocGetWorkitemProperties.md)
- [`DocRepeatWorkitem`](DocRepeatWorkitem.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
