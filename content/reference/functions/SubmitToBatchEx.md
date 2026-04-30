---
title: "SubmitToBatchEx"
summary: "Submits SSL code to batch execution and returns the submitted job identifier."
id: ssl.function.submittobatchex
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SubmitToBatchEx

Submits SSL code to batch execution and returns the submitted job identifier.

`SubmitToBatchEx()` accepts one SSL code string and returns the batch ID for the
submitted job. If `sCode` is [`NIL`](../literals/nil.md) or `""`, the function returns `""` and does not submit anything.

Unlike [`SubmitToBatch`](SubmitToBatch.md), this function does not accept batch parameters, credentials, or a routing mode. The submission is forwarded through the internal batch mode and still returns only the job ID, not the batch script's [`:RETURN`](../keywords/RETURN.md) value.

## When to use

- When you need the simplest way to submit SSL code for background execution.
- When the batch script does not need input parameters.
- When later workflow needs the returned batch ID for tracking or correlation.

## Syntax

```ssl
SubmitToBatchEx(sCode)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCode` | [string](../types/string.md) | yes | — | SSL source code to submit. If [`NIL`](../literals/nil.md) or empty, nothing is submitted and the function returns `""`. |

## Returns

**[string](../types/string.md)** — The submitted batch job identifier. Returns `""` when `sCode` is [`NIL`](../literals/nil.md) or an empty string.

## Best practices

!!! success "Do"
    - Pass a non-empty SSL code string when you intend to create a batch job.
    - Capture the returned batch ID if later workflow needs to check or relate the submission.
    - Use [`SubmitToBatch`](SubmitToBatch.md) instead when the batch code needs input parameters or other submission options.

!!! failure "Don't"
    - Assume empty code raises an error. The function returns `""` and skips submission.
    - Expect the function to pass parameters into the batch script. `SubmitToBatchEx()` only accepts the code string.
    - Treat the return value as the batch script's result. It is only the submission ID.

## Caveats

- `SubmitToBatchEx()` always submits through the internal batch mode.
- The function does not accept a parameter array, caption, alternate credentials, or a mode override.
- The function does not wait for the batch job to complete before returning.

## Examples

### Submit code for deferred processing

Submit a small SSL block and keep the returned batch ID for later tracking.

```ssl
:PROCEDURE SubmitDataForBatchProcessing;
    :DECLARE sCode, sBatchId;

    sCode := "
        :DECLARE sStatus;
        sStatus := 'Queued from SubmitToBatchEx';

        InfoMes(sStatus);
        :RETURN sStatus;
    ";

    sBatchId := SubmitToBatchEx(sCode);

    UsrMes("Submitted batch job: " + sBatchId);
    /* Displays batch ID on success;

    :RETURN sBatchId;
:ENDPROC;

/* Usage;
DoProc("SubmitDataForBatchProcessing");
```

### Queue independent background jobs and validate each ID

Submit several jobs separately so each one gets its own batch ID, then check
which submissions succeeded.

```ssl
:PROCEDURE QueueNightlyRefreshes;
    :DECLARE sCode1, sCode2, sCode3;
    :DECLARE sBatchId1, sBatchId2, sBatchId3;

    sCode1 := "
        InfoMes('Refresh daily KPIs');
        :RETURN 'Daily';
    ";
    sCode2 := "
        InfoMes('Refresh monthly rollup');
        :RETURN 'Monthly';
    ";
    sCode3 := "
        InfoMes('Refresh lab audit');
        :RETURN 'Audit';
    ";

    sBatchId1 := SubmitToBatchEx(sCode1);
    sBatchId2 := SubmitToBatchEx(sCode2);
    sBatchId3 := SubmitToBatchEx(sCode3);

    :IF Empty(sBatchId1);
        UsrMes("Daily KPIs submission was skipped or failed");
    :ELSE;
        UsrMes("Queued daily KPIs as batch " + sBatchId1);
        /* Displays batch ID on success;
    :ENDIF;

    :IF Empty(sBatchId2);
        UsrMes("Monthly rollup submission was skipped or failed");
    :ELSE;
        UsrMes("Queued monthly rollup as batch " + sBatchId2);
        /* Displays batch ID on success;
    :ENDIF;

    :IF Empty(sBatchId3);
        UsrMes("Lab audit submission was skipped or failed");
    :ELSE;
        UsrMes("Queued lab audit as batch " + sBatchId3);
        /* Displays batch ID on success;
    :ENDIF;

    :RETURN sBatchId1;
:ENDPROC;

/* Usage;
DoProc("QueueNightlyRefreshes");
```

## Related

- [`BatchSupport`](../classes/BatchSupport.md)
- [`InBatchProcess`](InBatchProcess.md)
- [`SubmitToBatch`](SubmitToBatch.md)
- [`string`](../types/string.md)
