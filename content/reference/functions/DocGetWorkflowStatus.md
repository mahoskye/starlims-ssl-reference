---
title: "DocGetWorkflowStatus"
summary: "Returns the current runtime status for a Documentum workflow."
id: ssl.function.docgetworkflowstatus
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocGetWorkflowStatus

Returns the current runtime status for a Documentum workflow.

The function looks up the workflow identified by `sWorkflowId` and returns a status string. For known runtime states, the returned value is one of `"Dormant"`, `"Running"`, `"Finished"`, `"Paused"`, `"Terminated"`, or `"Unknown"`.

If the workflow ID no longer exists in Documentum, the function returns `"Finished"`. If the underlying Documentum call fails for another reason, the function returns an empty string and the Documentum error state can be inspected with [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md).

## When to use

- When you need the current workflow state for display or logging.
- When business logic should react differently to running, paused, finished, or terminated workflows.
- When you need to distinguish a finished workflow from a failed status lookup.

## Syntax

```ssl
DocGetWorkflowStatus(sWorkflowId)
```

## Parameters

| Name | Type | Required | Default | Description |
| ---- | ---- | -------- | ------- | ----------- |
| `sWorkflowId` | [string](../types/string.md) | yes | — | Documentum workflow identifier |

## Returns

**[string](../types/string.md)** — The workflow status.

| Return value | Meaning |
| ------------ | ------- |
| `"Dormant"` | The workflow exists but is dormant |
| `"Running"` | The workflow is running |
| `"Finished"` | The workflow is finished, or the workflow ID is no longer found |
| `"Paused"` | The workflow is paused |
| `"Terminated"` | The workflow was terminated |
| `"Unknown"` | The runtime state could not be mapped to a known status |
| `""` | The status lookup failed |

## Exceptions

| Trigger | Exception message |
| ------- | ----------------- |
| `sWorkflowId` is [`NIL`](../literals/nil.md). | `sWorkflowId argument cannot be null` |

## Best practices

!!! success "Do"
    - Branch on the documented status values and keep a fallback path for `"Unknown"`.
    - Treat `"Finished"` as the result for completed workflows and for workflow IDs that are no longer found.
    - Check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) when the function returns an empty string.

!!! failure "Don't"
    - Assume an empty string means the workflow finished. It means the lookup failed.
    - Treat missing workflow IDs as an error case by default. This function maps that case to `"Finished"`.
    - Pass a [`NIL`](../literals/nil.md) workflow identifier.

## Examples

### Display the current workflow status

Fetches the current status of a workflow and displays it, using a default workflow ID when none is supplied.

```ssl
:PROCEDURE ShowWorkflowStatus;
	:PARAMETERS sWorkflowId;
	:DEFAULT sWorkflowId, "WF-12345";
	:DECLARE sStatus;

	sStatus := DocGetWorkflowStatus(sWorkflowId);

	UsrMes("Workflow " + sWorkflowId + " status: " + sStatus);
:ENDPROC;

/* Usage;
DoProc("ShowWorkflowStatus");
```

[`UsrMes`](UsrMes.md) displays:

```text
Workflow WF-12345 status: Running
```

### Branch on the returned status

Branches on the documented status values, with a fallback for unknown and empty results.

```ssl
:PROCEDURE HandleWorkflowStatus;
	:PARAMETERS sWorkflowId;
	:DEFAULT sWorkflowId, "WF-12345";
	:DECLARE sStatus;

	sStatus := DocGetWorkflowStatus(sWorkflowId);

	:BEGINCASE;
	:CASE sStatus == "Running";
		UsrMes("Workflow is still in progress.");
		:EXITCASE;
	:CASE sStatus == "Dormant";
		UsrMes("Workflow is dormant.");
		:EXITCASE;
	:CASE sStatus == "Paused";
		UsrMes("Workflow is paused and may need attention.");
		:EXITCASE;
	:CASE sStatus == "Finished";
		UsrMes("Workflow is finished.");
		:EXITCASE;
	:CASE sStatus == "Terminated";
		UsrMes("Workflow was terminated.");
		:EXITCASE;
	:OTHERWISE;
		UsrMes("Workflow returned status: " + sStatus);
		:EXITCASE;
	:ENDCASE;
:ENDPROC;

/* Usage;
DoProc("HandleWorkflowStatus");
```

### Distinguish a failed lookup from a finished workflow

Reads the workflow status and separates three outcomes: a failed lookup (empty string), a finished or no-longer-existing workflow, and an active workflow in any other state.

```ssl
:PROCEDURE CheckWorkflowStatusSafe;
	:PARAMETERS sWorkflowId;
	:DEFAULT sWorkflowId, "WF-12345";
	:DECLARE sStatus, sDocError;

	sStatus := DocGetWorkflowStatus(sWorkflowId);

	:IF sStatus == "";
		sDocError := DocGetErrorMessage();
		ErrorMes("Documentum status lookup failed: " + sDocError);

		:RETURN;
	:ENDIF;

	:IF sStatus == "Finished";
		UsrMes("Workflow is finished or no longer exists.");
		:RETURN;
	:ENDIF;

	UsrMes("Workflow status: " + sStatus);
:ENDPROC;

/* Usage;
DoProc("CheckWorkflowStatusSafe");
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`string`](../types/string.md)
