---
title: "DocResumeWorkflow"
summary: "Resumes a Documentum workflow identified by sWorkflowId."
id: ssl.function.docresumeworkflow
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocResumeWorkflow

Resumes a Documentum workflow identified by `sWorkflowId`.

`DocResumeWorkflow` takes one required string argument and returns [`.T.`](../literals/true.md) when the resume request succeeds. If the call does not succeed, it returns [`.F.`](../literals/false.md). If `sWorkflowId` is [`NIL`](../literals/nil.md), the function raises an exception before attempting the resume operation.

## When to use

- When you need to continue a known Documentum workflow from SSL.
- When workflow automation should attempt a resume and branch on a boolean result.
- When administrative scripts need a simple success or failure result for a resume request.

## Syntax

```ssl
DocResumeWorkflow(sWorkflowId)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sWorkflowId` | [string](../types/string.md) | yes | — | Identifier of the Documentum workflow to resume |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the workflow resume request succeeds; otherwise [`.F.`](../literals/false.md)

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sWorkflowId` is [`NIL`](../literals/nil.md). | `sWorkflowId argument cannot be null` |

## Best practices

!!! success "Do"
    - Validate that `sWorkflowId` is assigned before calling the function.
    - Check the boolean return value and handle [`.F.`](../literals/false.md) explicitly in your workflow logic.
    - Use [`DocGetWorkflowStatus`](DocGetWorkflowStatus.md) or surrounding workflow context when you only want to resume workflows in a known state.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sWorkflowId`. The function raises an error before attempting the resume.
    - Assume the resume succeeded without checking the return value.
    - Use [`ErrorMes`](ErrorMes.md) for ordinary [`.F.`](../literals/false.md) results when a non-critical user message or branch in logic is enough.

## Caveats

- A [`.F.`](../literals/false.md) result indicates that the resume request did not succeed, but the function does not return a separate failure message.

## Examples

### Resume one workflow by ID

Fetches a workflow by ID, branches on the boolean result to build an outcome message, and returns the boolean to the caller.

```ssl
:PROCEDURE ResumeWorkflowBasic;
    :DECLARE sWorkflowId, bResumed, sMessage;

    sWorkflowId := "WF-2024-0042";
    bResumed := DocResumeWorkflow(sWorkflowId);

    :IF bResumed;
        sMessage := "Workflow " + sWorkflowId + " resumed";
    :ELSE;
        sMessage := "Workflow " + sWorkflowId + " could not be resumed";
    :ENDIF;

    UsrMes(sMessage);

    :RETURN bResumed;
:ENDPROC;

/* Usage;
DoProc("ResumeWorkflowBasic");
```

[`UsrMes`](UsrMes.md) displays:

```
Workflow WF-2024-0042 resumed
```

On failure: `Workflow WF-2024-0042 could not be resumed`

### Resume only when the workflow is paused

Checks the current workflow status with [`DocGetWorkflowStatus`](DocGetWorkflowStatus.md) before calling `DocResumeWorkflow`, so the resume is only attempted when the workflow is in the `"Paused"` state.

```ssl
:PROCEDURE ResumePausedWorkflowOnly;
    :PARAMETERS sWorkflowId;
    :DECLARE sStatus, bResumed;

    bResumed := .F.;
    sStatus := DocGetWorkflowStatus(sWorkflowId);

    :IF sStatus == "Paused";
        bResumed := DocResumeWorkflow(sWorkflowId);

        :IF bResumed;
            /* Displays on successful resume from paused state;
            UsrMes("Workflow " + sWorkflowId + " resumed from paused state");
        :ELSE;
            /* Displays on failed resume from paused state;
            UsrMes("Workflow " + sWorkflowId + " was paused but did not resume");
        :ENDIF;
    :ELSE;
        /* Displays the current workflow status;
        UsrMes("Workflow " + sWorkflowId + " is currently " + sStatus);
    :ENDIF;

    :RETURN bResumed;
:ENDPROC;

/* Usage;
DoProc("ResumePausedWorkflowOnly", {"WF-2024-0042"});
```

### Resume multiple workflows and collect results

Iterates a list of workflow IDs, skips empty entries, and collects each resume outcome into a summary object, then displays a single count line for resumed, failed, and skipped workflows.

```ssl
:PROCEDURE ResumeWorkflowBatch;
    :PARAMETERS aWorkflowIds;
    :DECLARE oSummary, sWorkflowId, sMessage;
    :DECLARE bResumed, nIndex;

    oSummary := CreateUdObject();
    oSummary:resumedIds := {};
    oSummary:failedIds := {};
    oSummary:skippedIds := {};

    :FOR nIndex := 1 :TO ALen(aWorkflowIds);
        sWorkflowId := aWorkflowIds[nIndex];

        :IF Empty(sWorkflowId);
            AAdd(oSummary:skippedIds, sWorkflowId);
            :LOOP;
        :ENDIF;

        bResumed := DocResumeWorkflow(sWorkflowId);

        :IF bResumed;
            AAdd(oSummary:resumedIds, sWorkflowId);
        :ELSE;
            AAdd(oSummary:failedIds, sWorkflowId);
        :ENDIF;
    :NEXT;

    sMessage := "Resumed " + LimsString(ALen(oSummary:resumedIds))
        + " workflow(s), failed " + LimsString(ALen(oSummary:failedIds))
        + ", skipped " + LimsString(ALen(oSummary:skippedIds));

    /* Displays workflow counts;
    UsrMes(sMessage);

    :RETURN oSummary;
:ENDPROC;

/* Usage;
DoProc("ResumeWorkflowBatch", {{"WF-2024-0042", "WF-2024-0043"}});
```

## Related

- [`DocPauseWorkflow`](DocPauseWorkflow.md)
- [`DocStopWorkflow`](DocStopWorkflow.md)
- [`DocGetWorkflowStatus`](DocGetWorkflowStatus.md)
- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
