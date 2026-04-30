---
title: "SubmitToBatch"
summary: "Submits SSL code to a batch worker and returns the submitted job identifier."
id: ssl.function.submittobatch
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SubmitToBatch

Submits SSL code to a batch worker and returns the submitted job identifier.

`SubmitToBatch()` queues or starts background execution for the supplied SSL code string. The return value is the batch job ID, not the execution result. If `sCode` is [`NIL`](../literals/nil.md) or an empty string, the function returns `""` and does not submit anything.

The `parameters` argument is interpreted in one of two supported ways:

- an array of positional script parameters for the submitted code
- an object with a `Parameters` array and/or a `Caption` string

If `mode` is omitted or not recognized, the runtime uses the system batch mode setting. If that setting is also not recognized, submission falls back to queue mode. If `userName` or `password` is omitted, the current session credentials are used.

## When to use

- When code should run in the background instead of blocking the current script.
- When the submitted batch needs input parameters.
- When you need a batch job ID so the work can be tracked or correlated later.
- When you want to add a caption to the submitted job for easier identification.

## Syntax

```ssl
SubmitToBatch(sCode, [vParameters], [sMode], [sUserName], [sPassword])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCode` | [string](../types/string.md) | yes | — | SSL source code to run in batch. If [`NIL`](../literals/nil.md) or empty, nothing is submitted and the function returns `""`. |
| `vParameters` | [array](../types/array.md) or [object](../types/object.md) | no | omitted | Either an array of positional parameters for the submitted code, or an object containing `Parameters` (array) and optional `Caption` (string). |
| `sMode` | [string](../types/string.md) | no | system batch mode, then `queue` | Batch routing mode. Recognized values are `"queue"`, `"external"`, and `"internal"`. Unrecognized values are treated as omitted. |
| `sUserName` | [string](../types/string.md) | no | current session user | Username to use for the batch submission. |
| `sPassword` | [string](../types/string.md) | no | current session password | Password to use for the batch submission. |

## Returns

**[string](../types/string.md)** — The submitted batch job identifier. Returns `""` when `sCode` is [`NIL`](../literals/nil.md) or an empty string.

## Best practices

!!! success "Do"
    - Pass an array when the submitted code expects positional parameters.
    - Use an object with `Parameters` and `Caption` when you want both runtime inputs and a readable job label.
    - Capture the returned batch ID if later workflow needs to track or correlate the submission.
    - Omit `userName` and `password` unless the batch must run under different credentials.

!!! failure "Don't"
    - Assume the function returns the batch execution result. It returns a submission ID.
    - Pass arbitrary object properties and expect them to become script parameters. Only `Parameters` and `Caption` are recognized from the object form.
    - Rely on an invalid `sMode` string to select a specific worker path. Unrecognized values are treated as omitted.
    - Submit empty code and assume an error will be raised. The function returns `""` and skips submission.

## Caveats

- The submitted batch receives the supplied script parameters plus the current session and sticky variables.
- An object passed through `vParameters` is not unpacked generically. Only `Parameters` and `Caption` affect submission.
- `SubmitToBatch()` does not wait for the batch job to complete before returning.

## Examples

### Submit a simple background job

Submit a small block of SSL code and keep the returned batch ID.

```ssl
:PROCEDURE SubmitSimpleBatch;
    :DECLARE sCode, sBatchId;

    sCode := "
        :DECLARE sStatus;
        sStatus := 'Queued';

        :RETURN sStatus;
    ";

    sBatchId := SubmitToBatch(sCode);
    UsrMes("Submitted batch job: " + sBatchId);
    /* Displays submitted batch ID;

    :RETURN sBatchId;
:ENDPROC;

/* Usage;
DoProc("SubmitSimpleBatch");
```

### Pass positional parameters and choose queue mode

Submit code that expects positional parameters and route it explicitly through queue mode.

```ssl
:PROCEDURE QueueSampleAudit;
    :DECLARE sCode, sBatchId;

    sCode := "
        :PARAMETERS sSampleId, sAction;
        :DECLARE sMessage;

        sMessage := sAction + ': ' + sSampleId;
        InfoMes(sMessage);

        :RETURN sMessage;
    ";

    sBatchId := SubmitToBatch(sCode, {"SAM-00042", "Audit"}, "queue");
    UsrMes("Queued sample audit as batch " + sBatchId);
    /* Displays queued batch ID;

    :RETURN sBatchId;
:ENDPROC;

/* Usage;
DoProc("QueueSampleAudit");
```

### Use a caption object and alternate credentials

Pass both `Parameters` and `Caption` through the object form, while supplying explicit credentials for the batch run.

```ssl
:PROCEDURE SubmitLabeledBatch;
    :PARAMETERS sUserName, sPassword;
    :DECLARE sCode, sBatchId, oBatchArgs;

    sCode := "
        :PARAMETERS sSampleId, sAction;
        :DECLARE sLog;

        sLog := sAction + ' for ' + sSampleId;
        InfoMes(sLog);

        :RETURN sLog;
    ";

    oBatchArgs := CreateUdObject();
    oBatchArgs:Parameters := {"SAM-10425", "Release"};
    oBatchArgs:Caption := "Nightly release follow-up";

    sBatchId := SubmitToBatch(
        sCode,
        oBatchArgs,
        "external",
        sUserName,
        sPassword
    );

    UsrMes("Submitted labeled batch " + sBatchId);
    /* Displays submitted labeled batch ID;

    :RETURN sBatchId;
:ENDPROC;

/* Usage;
DoProc("SubmitLabeledBatch", {"svc_batch", "password"});
```

## Related

- [`BatchSupport`](../classes/BatchSupport.md)
- [`InBatchProcess`](InBatchProcess.md)
- [`SubmitToBatchEx`](SubmitToBatchEx.md)
- [`array`](../types/array.md)
- [`object`](../types/object.md)
- [`string`](../types/string.md)
