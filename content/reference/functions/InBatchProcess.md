---
title: "InBatchProcess"
summary: "Returns whether the current SSL execution context is running in a batch process."
id: ssl.function.inbatchprocess
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# InBatchProcess

Returns whether the current SSL execution context is running in a batch process.

`InBatchProcess()` is a parameterless function that reads the current runtime context and returns a boolean result. Use it when the same script needs one path for background batch execution and another for interactive execution.

## When to use

- When a script should suppress user-facing prompts during background work.
- When you need different logging, notification, or follow-up behavior in batch and interactive runs.
- When writing shared code that may run both from a user action and from a
  submitted batch job.

## Syntax

```ssl
InBatchProcess()
```

## Parameters

This function takes no parameters.

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the current execution context is running in batch process mode; otherwise [`.F.`](../literals/false.md).

## Best practices

!!! success "Do"
    - Use `InBatchProcess()` to choose between batch-safe and interactive behavior.
    - Use quieter logging in batch code when a popup or prompt would be inappropriate.
    - Keep the branch close to the behavior it controls so the context decision stays easy to follow.

!!! failure "Don't"
    - Track batch state with your own flag when the runtime can answer it directly.
    - Assume code always runs interactively if the same routine can also be submitted to batch.
    - Use [`ErrorMes`](ErrorMes.md) for ordinary context reporting when [`UsrMes`](UsrMes.md) or [`InfoMes`](InfoMes.md) is sufficient.

## Caveats

- `InBatchProcess()` only tells you whether the current context is in batch mode.
- The function does not identify a batch job or provide batch metadata.

## Examples

### Skip a popup during batch execution

Use a non-interactive message in batch and a user popup in interactive execution, showing the most direct application of the `InBatchProcess()` check.

```ssl
:PROCEDURE NotifyCompletion;
    :DECLARE bIsBatch, sMessage;

    bIsBatch := InBatchProcess();
    sMessage := "Sample release processing completed";

    :IF bIsBatch;
        /* Batch run uses non-interactive logging;
        InfoMes(sMessage);
    :ELSE;
        /* Interactive run can show a user message;
        UsrMes(sMessage);
    :ENDIF;

    :RETURN bIsBatch;
:ENDPROC;

/* Usage;
DoProc("NotifyCompletion");
```

### Reuse one procedure in both interactive and batch paths

Execute the work immediately when already in batch; submit it to a new batch job otherwise. The batch ID returned by [`SubmitToBatchEx`](SubmitToBatchEx.md) is system-assigned and varies per call.

```ssl
:PROCEDURE ProcessQueuedAudit;
    :DECLARE bIsBatch, sCode, sBatchId;

    bIsBatch := InBatchProcess();

    :IF bIsBatch;
        /* Already in batch so do the work now;
        InfoMes("Running audit work inside batch context");
    :ELSE;
        sCode := "InfoMes('Running audit work inside batch context');";
        sBatchId := SubmitToBatchEx(sCode);

        /* Displays submitted batch ID;
        UsrMes("Submitted audit work to batch: " + sBatchId);
    :ENDIF;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ProcessQueuedAudit");
```

## Related

- [`BatchSupport`](../classes/BatchSupport.md)
- [`SubmitToBatch`](SubmitToBatch.md)
- [`SubmitToBatchEx`](SubmitToBatchEx.md)
- [`boolean`](../types/boolean.md)
