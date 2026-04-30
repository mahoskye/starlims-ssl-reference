---
title: "DocPauseWorkflow"
summary: "Temporarily halts workflow processing to prevent further steps until manual intervention or review."
id: ssl.function.docpauseworkflow
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocPauseWorkflow

Temporarily halts workflow processing to prevent further steps until manual intervention or review.

`DocPauseWorkflow` attempts to pause the Documentum workflow identified by `sWorkflowId`. It returns [`.T.`](../literals/true.md) when the pause operation succeeds and [`.F.`](../literals/false.md) when it does not. If `sWorkflowId` is [`NIL`](../literals/nil.md), the function raises an exception before attempting the pause.

## When to use

- When a workflow must stop progressing until someone reviews or intervenes.
- When business rules require temporarily suspending a workflow before the next step.
- When administrative scripts need to pause a known workflow by ID.

## Syntax

```ssl
DocPauseWorkflow(sWorkflowId)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sWorkflowId` | [string](../types/string.md) | yes | — | Identifier of the Documentum workflow to pause |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) if the workflow was paused successfully; otherwise [`.F.`](../literals/false.md)

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sWorkflowId` is [`NIL`](../literals/nil.md). | `sWorkflowId argument cannot be null` |

## Best practices

!!! success "Do"
    - Validate or obtain the workflow ID before calling the function.
    - Check the boolean return value and handle [`.F.`](../literals/false.md) explicitly.
    - Use surrounding workflow logic to decide whether to retry, report, or defer manual review.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sWorkflowId`. That raises an exception.
    - Assume every workflow ID can be paused successfully.
    - Ignore a [`.F.`](../literals/false.md) result and continue as if the workflow was paused.

## Caveats

- The function returns only a boolean result; it does not provide a reason when the pause does not succeed.

## Examples

### Pause an ongoing workflow for review

Calls `DocPauseWorkflow` and builds a result message from the boolean return, then displays it. On success the message confirms the pause; on failure it reports which workflow could not be paused.

```ssl
:PROCEDURE PauseWorkflowForReview;
	:DECLARE sWorkflowId, bPaused, sMessage;

	sWorkflowId := "WF-2024-0042";
	bPaused := DocPauseWorkflow(sWorkflowId);

	:IF bPaused;
		sMessage := "Workflow " + sWorkflowId + " paused for review";
	:ELSE;
		sMessage := "Failed to pause workflow " + sWorkflowId;
	:ENDIF;

	UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("PauseWorkflowForReview");
```

`UsrMes` displays:

```text
Workflow WF-2024-0042 paused for review
```

On failure, `UsrMes` displays:

```text
Failed to pause workflow WF-2024-0042
```

### Pause a workflow only when review is required

Guards the pause call behind a `bReviewRequired` flag so the workflow is only halted when business rules require it, returning [`.F.`](../literals/false.md) immediately when review is not needed.

```ssl
:PROCEDURE PauseWorkflowIfReviewRequired;
	:PARAMETERS sWorkflowId, bReviewRequired;
	:DECLARE bPaused;

	bPaused := .F.;

	:IF bReviewRequired;
		bPaused := DocPauseWorkflow(sWorkflowId);

		:IF bPaused;
			UsrMes("Workflow " + sWorkflowId + " paused for review");
		:ELSE;
			UsrMes("Workflow " + sWorkflowId + " could not be paused");
		:ENDIF;
	:ENDIF;

	:RETURN bPaused;
:ENDPROC;

/* Usage;
DoProc("PauseWorkflowIfReviewRequired", {"WF-2024-0042", .T.});
```

[`UsrMes`](UsrMes.md) displays either `Workflow WF-2024-0042 paused for review` or `Workflow WF-2024-0042 could not be paused`.

### Pause multiple workflows and collect the results

Iterates a list of workflow IDs, records each result into a summary object, and reports the overall count of successful and failed pause operations.

```ssl
:PROCEDURE PauseWorkflowBatch;
	:PARAMETERS aWorkflowIds;
	:DECLARE oSummary, sWorkflowId, bPaused;
	:DECLARE nPaused, nFailed, nIndex;

	oSummary := CreateUdObject();
	oSummary:pausedIds := {};
	oSummary:failedIds := {};

	nPaused := 0;
	nFailed := 0;

	:FOR nIndex := 1 :TO ALen(aWorkflowIds);
		sWorkflowId := aWorkflowIds[nIndex];
		bPaused := DocPauseWorkflow(sWorkflowId);

		:IF bPaused;
			AAdd(oSummary:pausedIds, sWorkflowId);
			nPaused := nPaused + 1;
		:ELSE;
			AAdd(oSummary:failedIds, sWorkflowId);
			nFailed := nFailed + 1;
		:ENDIF;
	:NEXT;

	oSummary:pausedCount := nPaused;
	oSummary:failedCount := nFailed;

	:IF nFailed > 0;
		UsrMes(
			"Paused " + LimsString(nPaused) + " workflows. Failed: " +
			LimsString(nFailed)
		);
		/* Displays when some workflows fail: pause summary;
	:ELSE;
		UsrMes("Paused " + LimsString(nPaused) + " workflows");
		/* Displays when all workflows pause: pause summary;
	:ENDIF;

	:RETURN oSummary;
:ENDPROC;

/* Usage;
DoProc("PauseWorkflowBatch", {{"WF-2024-0042", "WF-2024-0043"}});
```

## Related

- [`DocResumeWorkflow`](DocResumeWorkflow.md)
- [`DocStopWorkflow`](DocStopWorkflow.md)
- [`DocGetWorkflowStatus`](DocGetWorkflowStatus.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
