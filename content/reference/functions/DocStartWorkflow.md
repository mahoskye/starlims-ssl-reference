---
title: "DocStartWorkflow"
summary: "Starts a Documentum workflow and returns the created workflow ID together with the start-activity performers."
id: ssl.function.docstartworkflow
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocStartWorkflow

Starts a Documentum workflow and returns the created workflow ID together with the start-activity performers.

`DocStartWorkflow` accepts a workflow identifier and can also accept a document ID [array](../types/array.md) and package name. On success it returns a two-element SSL [array](../types/array.md): `aWorkflowInfo[1]` is the created workflow ID and `aWorkflowInfo[2]` contains the performer value returned for the start activity. When the workflow needs a document package, calling the function without document IDs raises an error. When `sPackageName` is omitted or blank in that document-package path, Documentum uses `Package0`.

## When to use

- When you need to start a Documentum workflow from SSL and capture the created workflow ID.
- When the workflow start step uses document attachments and you need to pass document IDs.
- When you need the start-step performer list for follow-up routing or logging.

## Syntax

```ssl
DocStartWorkflow(sWorkflowId, [aDocumentIds], [sPackageName])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sWorkflowId` | [string](../types/string.md) | yes | — | Workflow identifier to start. Passing [`NIL`](../literals/nil.md) raises an SSL argument error. Passing `""` or whitespace raises a workflow validation error. |
| `aDocumentIds` | [array](../types/array.md) | no | omitted | Document IDs to attach when the workflow start path expects documents. |
| `sPackageName` | [string](../types/string.md) | no | `"Package0"` when the document-package path is used and the value is omitted or blank | Package name used when attaching `aDocumentIds` to the workflow start activity. |

## Returns

**[array](../types/array.md)** — A two-element SSL array.

| Position | Type | Description |
|----------|------|-------------|
| `aWorkflowInfo[1]` | [string](../types/string.md) | The created workflow ID returned by Documentum |
| `aWorkflowInfo[2]` | [array](../types/array.md) or [`NIL`](../literals/nil.md) | Start-activity performers. This is typically an array of performer names, but it can be [`NIL`](../literals/nil.md) when no performer value is returned. |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sWorkflowId` is [`NIL`](../literals/nil.md). | `sWorkflowId argument cannot be null` |
| `sWorkflowId` is blank. | `You must specify workflow's path or workflow's id!` |
| The workflow cannot be resolved. | `Failed: Object does not exist` |
| The workflow is not installed. | `The workflow is not installed!` |
| The current user cannot start the workflow. | `The current user has no permissions to start the workflow!` |
| The workflow start path requires documents but none are supplied. | `The workflow requires at least one document!` |

## Best practices

!!! success "Do"
    - Pass `aDocumentIds` as an array, even when you are attaching only one document.
    - Read the returned values with SSL's 1-based indexing: `aWorkflowInfo[1]` for the workflow ID and `aWorkflowInfo[2]` for performers.
    - Omit `sPackageName` when the default package name is acceptable.

!!! failure "Don't"
    - Document or code against zero-based positions such as index `0`. SSL arrays are 1-based.
    - Assume `aDocumentIds` is always optional. Some workflows require at least one document at startup.
    - Assume `aWorkflowInfo[2]` always contains a populated performer array. Check the returned value before iterating it.

## Caveats

- A workflow can start without a document package only when its start path does not require one.
- The returned workflow ID is the created Documentum workflow instance ID, not necessarily the same text you passed in as `sWorkflowId`.

## Examples

### Start a workflow without documents

Starts a simple workflow by ID without document attachments and displays the created workflow instance ID.

```ssl
:PROCEDURE StartSimpleWorkflow;
    :DECLARE sWorkflowId, aWorkflowInfo, sStartedId;

    sWorkflowId := "QCReview";
    aWorkflowInfo := DocStartWorkflow(sWorkflowId);
    sStartedId := aWorkflowInfo[1];

    UsrMes("Started workflow " + sStartedId);

    :RETURN aWorkflowInfo;
:ENDPROC;

/* Usage;
DoProc("StartSimpleWorkflow");
```

[`UsrMes`](UsrMes.md) displays:

```text
Started workflow [created workflow ID]
```

### Start a workflow with attached documents

Passes a document ID array and a package name when starting, then reads the performer list from `aWorkflowInfo[2]` and lists each assigned performer.

```ssl
:PROCEDURE StartWorkflowWithDocuments;
    :DECLARE sWorkflowId, aDocumentIds, sPackageName;
    :DECLARE aWorkflowInfo, aPerformers, nIndex;

    sWorkflowId := "QCReview";
    aDocumentIds := {"0900000180001234", "0900000180001235"};
    sPackageName := "ReviewDocs";

    aWorkflowInfo := DocStartWorkflow(sWorkflowId, aDocumentIds, sPackageName);
    aPerformers := aWorkflowInfo[2];

    :IF .NOT. Empty(aPerformers);
        :FOR nIndex := 1 :TO ALen(aPerformers);
            UsrMes("Assigned to " + aPerformers[nIndex]);  /* Displays one message per performer;
        :NEXT;
    :ENDIF;

    :RETURN aWorkflowInfo;
:ENDPROC;

/* Usage;
DoProc("StartWorkflowWithDocuments");
```

### Start a workflow with error handling

Wraps the start call in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) to handle workflow exceptions, using [`GetLastSSLError`](GetLastSSLError.md) to extract the error description on failure.

```ssl
:PROCEDURE StartWorkflowSafe;
    :PARAMETERS sWorkflowId, aDocumentIds;
    :DECLARE aWorkflowInfo, oError;

    :TRY;
        aWorkflowInfo := DocStartWorkflow(sWorkflowId, aDocumentIds);
        UsrMes("Started workflow " + aWorkflowInfo[1]);
		/* Displays the started workflow ID;

        :RETURN aWorkflowInfo;
    :CATCH;
        oError := GetLastSSLError();
        ErrorMes("Unable to start workflow: " + oError:Description);
        /* Displays the failure reason;

        :RETURN {};
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("StartWorkflowSafe", {"QCReview", {"0900000180001234"}});
```

## Related

- [`DocGetTasks`](DocGetTasks.md)
- [`DocStopWorkflow`](DocStopWorkflow.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
