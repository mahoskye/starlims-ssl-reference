---
title: "DocStopWorkflow"
summary: "Stops a Documentum workflow by its workflow ID."
id: ssl.function.docstopworkflow
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocStopWorkflow

Stops a Documentum workflow by its workflow ID.

`DocStopWorkflow` calls the active Documentum interface and asks it to stop the workflow identified by `sWorkflowId`. It returns [`.T.`](../literals/true.md) when the stop call reports success and [`.F.`](../literals/false.md) when the call does not succeed.

The SSL wrapper rejects a [`NIL`](../literals/nil.md) `sWorkflowId` and raises an exception before the Documentum stop call runs. After a [`.F.`](../literals/false.md) result, use [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) to check whether the active Documentum context recorded an error.

## When to use

- When you need to stop a workflow and already know its workflow ID.
- When cleanup or recovery logic must stop in-flight Documentum workflows.
- When an administrative script needs a boolean success result from the stop request.

## Syntax

```ssl
DocStopWorkflow(sWorkflowId)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sWorkflowId` | [string](../types/string.md) | yes | — | Workflow ID to stop |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the Documentum stop call reports success; otherwise [`.F.`](../literals/false.md)

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sWorkflowId` is [`NIL`](../literals/nil.md). | `sWorkflowId argument cannot be null` |

## Best practices

!!! success "Do"
    - Initialize the Documentum interface before calling this function.
    - Check the boolean result immediately after the call.
    - After a [`.F.`](../literals/false.md) result, use [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) for diagnostics.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sWorkflowId`.
    - Assume [`.F.`](../literals/false.md) tells you why the stop request failed.
    - Make another Documentum call before reading the current error state when a stop fails.

## Caveats

- This page documents a required non-[`NIL`](../literals/nil.md) argument. The wrapper does not add a separate empty-string check.
- The function depends on an active Documentum interface context.

## Examples

### Stop one workflow

Initializes the Documentum interface, stops a single workflow by ID, and displays a success or failure message.

```ssl
:PROCEDURE StopOneWorkflow;
    :DECLARE sWorkflowId, bStopped;

    sWorkflowId := "WF-2024-00142";

    DocInitDocumentumInterface();

    bStopped := DocStopWorkflow(sWorkflowId);

    :IF bStopped;
        UsrMes("Stopped workflow " + sWorkflowId);
        /* Displays the stopped workflow ID;
    :ELSE;
        UsrMes("Could not stop workflow " + sWorkflowId);
        /* Displays the workflow ID on failure;
    :ENDIF;

    DocEndDocumentumInterface();
:ENDPROC;

/* Usage;
DoProc("StopOneWorkflow");
```

### Read the Documentum error after a failed stop

Logs in to Documentum before stopping, then reads the error message from [`DocCommandFailed`](DocCommandFailed.md) when the stop returns [`.F.`](../literals/false.md).

```ssl
:PROCEDURE StopWorkflowWithMessage;
    :DECLARE sWorkflowId, bStopped, sErrMsg;

    sWorkflowId := "WF-2024-00142";

    DocInitDocumentumInterface();

    :IF .NOT. DocLoginToDocumentum("Repository", "doc_user", "secret");
        ErrorMes("Documentum login failed: " + DocGetErrorMessage());
        /* Displays the login error;
        DocEndDocumentumInterface();

        :RETURN;
    :ENDIF;

    bStopped := DocStopWorkflow(sWorkflowId);

    :IF bStopped;
        UsrMes("Stopped workflow " + sWorkflowId);
        /* Displays the stopped workflow ID;
    :ELSE;
        sErrMsg := "";

        :IF DocCommandFailed();
            sErrMsg := DocGetErrorMessage();
        :ENDIF;

        ErrorMes("Failed to stop workflow " + sWorkflowId + ": " + sErrMsg);
        /* Displays the workflow ID and error on failure;
    :ENDIF;

    DocEndDocumentumInterface();
:ENDPROC;

/* Usage;
DoProc("StopWorkflowWithMessage");
```

### Stop a list of workflows and continue on failures

Iterates a workflow ID array, stopping each one and collecting failure IDs, with an option to exit early on first failure. Displays a final count of stopped and failed workflows.

```ssl
:PROCEDURE StopWorkflowBatch;
    :PARAMETERS aWorkflowIds, bContinueOnError;
    :DEFAULT bContinueOnError, .T.;
    :DECLARE nIndex, nCount, nStopped, nFailed;
    :DECLARE sWorkflowId, sErrMsg, aFailedIds;

    nCount := ALen(aWorkflowIds);
    nStopped := 0;
    nFailed := 0;
    aFailedIds := {};

    :IF nCount == 0;
        UsrMes("No workflows supplied");

        :RETURN 0;
    :ENDIF;

    DocInitDocumentumInterface();

    :IF .NOT. DocLoginToDocumentum("Repository", "doc_user", "secret");
        ErrorMes("Documentum login failed: " + DocGetErrorMessage());
        /* Displays the login error;
        DocEndDocumentumInterface();

        :RETURN 0;
    :ENDIF;

    :FOR nIndex := 1 :TO nCount;
        sWorkflowId := aWorkflowIds[nIndex];
        sErrMsg := "";

        :IF DocStopWorkflow(sWorkflowId);
            nStopped += 1;
            UsrMes("Stopped workflow " + sWorkflowId);
            /* Displays each stopped workflow ID;
        :ELSE;
            nFailed += 1;
            AAdd(aFailedIds, sWorkflowId);

            :IF DocCommandFailed();
                sErrMsg := DocGetErrorMessage();
            :ENDIF;

            ErrorMes("Failed to stop workflow " + sWorkflowId + ": " + sErrMsg);
            /* Displays the workflow ID and error on failure;

            :IF .NOT. bContinueOnError;
                :EXITFOR;
            :ENDIF;
        :ENDIF;
    :NEXT;

    UsrMes(
        "Stopped: " + LimsString(nStopped)
        + ", Failed: " + LimsString(nFailed)
    );
    /* Displays the final stopped and failed counts;

    :IF ALen(aFailedIds) > 0;
        UsrMes("Failed workflow IDs collected: " + LimsString(ALen(aFailedIds)));
        /* Displays the number of failed workflow IDs collected;
    :ENDIF;

    DocEndDocumentumInterface();

    :RETURN nStopped;
:ENDPROC;

/* Usage;
DoProc("StopWorkflowBatch", {{"WF-2024-00142", "WF-2024-00143"}, .T.});
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocEndDocumentumInterface`](DocEndDocumentumInterface.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
