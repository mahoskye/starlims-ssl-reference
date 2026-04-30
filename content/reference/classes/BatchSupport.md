---
title: "BatchSupport"
summary: "Provides batch-status checks and memory usage information for the current SSL process."
id: ssl.class.batchsupport
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# BatchSupport

Provides batch-status checks and memory usage information for the current SSL process.

`BatchSupport` lets you check whether a batch is still running and inspect the current process's physical and virtual memory usage. Use a batch name to query batches tracked by the application, or pass an integer process ID to test whether that operating system process exists. The class also exposes the number of active batches in the current application.

## When to use

- When your script needs to check whether a submitted batch is still running.
- When you need the current application's active batch count.
- When you want to log or monitor the current process's physical or virtual memory usage.
- When coordinating follow-up work that should wait for a named batch to finish.

## Constructors

### `BatchSupport{}`

Creates a `BatchSupport` instance bound to the current SSL process so its memory properties can be read.

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `ActiveBatchesNumber` | [number](../types/number.md) | read-only | Number of active batches in the current application. |
| `PhysicalMemory` | [number](../types/number.md) | read-only | Current process physical memory usage in bytes. Returns `-1` after `Dispose()`. |
| `VirtualMemory` | [number](../types/number.md) | read-only | Current process virtual memory usage in bytes. Returns `-1` after `Dispose()`. |

## Methods

| Name | Returns | Description |
|------|---------|-------------|
| `Dispose()` | none | Releases the instance's process resources. |
| `IsRunning(vBatchId)` | [boolean](../types/boolean.md) | Checks whether a named batch or integer process ID is currently running. |

### `Dispose`

Releases the resources used to read process memory information.

**Returns:** none — No return value.

### `IsRunning`

Checks whether the supplied batch identifier is running.

- If `vBatchId` is a string, `IsRunning()` checks the application's tracked batch names.
- If `vBatchId` is a number, it must be an integer process ID.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `vBatchId` | [string](../types/string.md) or [number](../types/number.md) | yes | Batch name or integer process ID to check. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the batch or process is running, otherwise [`.F.`](../literals/false.md).

**Raises:**

- **When `vBatchId` is [`NIL`](../literals/nil.md):** `Argument: vBatchId cannot be null.`
- **When `vBatchId` is a non-integer number:** `Argument: vBatchId must be an integer.`
- **When `vBatchId` is an empty string:** `Invalid argument`

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Use a batch name when checking batches submitted through the SSL batch system.
    - Use integer process IDs only when you specifically need operating system process checks.
    - Call `Dispose()` when you are finished reading memory information from a long-lived instance.
    - Use `ActiveBatchesNumber` for overall load monitoring and `IsRunning()` for a specific batch or process.

!!! failure "Don't"
    - Pass empty or [`NIL`](../literals/nil.md) identifiers to `IsRunning()`. Those values raise argument errors.
    - Pass decimal numbers to `IsRunning()`. Numeric identifiers must be whole-number process IDs.
    - Treat `ActiveBatchesNumber` as a per-batch status check. It only reports the total active count.
    - Expect memory properties to keep working after `Dispose()`. They return `-1` after disposal.

## Caveats

- `ActiveBatchesNumber` counts all active batches in the application, not just batches started by this `BatchSupport` instance.
- When `IsRunning()` receives a numeric process ID that does not exist or cannot be opened, it returns [`.F.`](../literals/false.md) instead of raising an error.
- Calling `Dispose()` more than once is safe.

## Examples

### Check whether a named batch is running

Create a `BatchSupport` instance and check a batch by its SSL batch name.

```ssl
:PROCEDURE CheckBatchStatus;
	:DECLARE oBatch, bIsRunning, sBatchId;

	sBatchId := "DailyWorkOrderProcessing";
	oBatch := BatchSupport{};
	bIsRunning := oBatch:IsRunning(sBatchId);

	:IF bIsRunning;
		UsrMes("Batch " + sBatchId + " is currently running");
	:ELSE;
		UsrMes("Batch " + sBatchId + " is not running");
	:ENDIF;

	oBatch:Dispose();

	:RETURN bIsRunning;
:ENDPROC;

/* Usage;
DoProc("CheckBatchStatus");
```

### Monitor memory while checking a process ID

Use an integer process ID and record the current process memory metrics.

```ssl
:PROCEDURE MonitorBatchProcess;
	:DECLARE oBatch, nProcessId, bIsRunning;
	:DECLARE nActiveBatches, nPhysicalMb, nVirtualMb;

	nProcessId := 12345;
	oBatch := BatchSupport{};

	nActiveBatches := Integer(oBatch:ActiveBatchesNumber);
	nPhysicalMb := Integer(oBatch:PhysicalMemory / 1024 / 1024);
	nVirtualMb := Integer(oBatch:VirtualMemory / 1024 / 1024);
	bIsRunning := oBatch:IsRunning(nProcessId);

	UsrMes("Active batches: " + LimsString(nActiveBatches));
	UsrMes("Physical memory MB: " + LimsString(nPhysicalMb));
	UsrMes("Virtual memory MB: " + LimsString(nVirtualMb));

	:IF bIsRunning;
		UsrMes("Process " + LimsString(nProcessId) + " is running");
	:ELSE;
		UsrMes("Process " + LimsString(nProcessId) + " is not running");
	:ENDIF;

	oBatch:Dispose();
:ENDPROC;

/* Usage;
DoProc("MonitorBatchProcess");
```

### Validate identifiers and handle errors

Catch the argument errors raised for unsupported `IsRunning()` inputs.

```ssl
:PROCEDURE ValidateBatchIdentifiers;
	:DECLARE oBatch, aBatchIds, vBatchId, oErr;
	:DECLARE nIndex, bIsRunning;

	oBatch := BatchSupport{};
	aBatchIds := {"BATCH_001", 12001, "", 12.5, NIL};

	:FOR nIndex := 1 :TO ALen(aBatchIds);
		vBatchId := aBatchIds[nIndex];

		:TRY;
			bIsRunning := oBatch:IsRunning(vBatchId);

			:IF bIsRunning;
				UsrMes("Identifier is running: " + LimsString(vBatchId));
			:ELSE;
				UsrMes("Identifier is not running: "
						+ LimsString(vBatchId));
			:ENDIF;
		:CATCH;
			oErr := GetLastSSLError();
			UsrMes("Batch check failed: " + oErr:Description);
		:ENDTRY;
	:NEXT;

	oBatch:Dispose();

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ValidateBatchIdentifiers");
```

## Related

- [`InBatchProcess`](../functions/InBatchProcess.md)
- [`SubmitToBatch`](../functions/SubmitToBatch.md)
- [`SubmitToBatchEx`](../functions/SubmitToBatchEx.md)
