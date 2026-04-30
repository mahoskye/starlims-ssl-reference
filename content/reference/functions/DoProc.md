---
title: "DoProc"
summary: "Calls a procedure by name at runtime."
id: ssl.function.doproc
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DoProc

Calls a procedure by name at runtime.

`DoProc` takes a procedure name and an optional argument array. A one-segment name calls a procedure in the current script. A three-segment name is passed through the same runtime path used by [`ExecFunction`](ExecFunction.md).

The second argument, when supplied, must be an array. `DoProc` does not enforce an exact argument count before dispatch. Extra values are ignored, and missing positions are left for the target procedure to handle.

## When to use

- When the target procedure is chosen from configuration or other runtime data.
- When you need one code path to dispatch to several named procedures.
- When you want late-bound behavior instead of a direct procedure call.

## Syntax

```ssl
DoProc(sProcedureName, [aArguments]);
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sProcedureName` | [string](../types/string.md) | yes | — | Procedure name to invoke. Use a one-segment name for a procedure in the current script, or a three-segment name to dispatch through the same runtime path as [`ExecFunction`](ExecFunction.md). |
| `aArguments` | [array](../types/array.md) | no | omitted | Positional argument array for the target procedure. If omitted, the call runs with no supplied arguments. |

## Returns

**any** — Returns the target procedure's return value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| The procedure name is missing. | `Please provide at least one parameter for DoProc` |
| The name has exactly two segments or more than three segments. | `Invalid procedure name: {name}` |
| `aArguments` is provided but is not an array. | `Wrong parameters for {name}` |
| A one-segment name does not resolve in the current script. | `Method {name} not found in script {scriptName}!` |

## Best practices

!!! success "Do"
    - Keep runtime procedure names explicit and predictable.
    - Pass an array for `aArguments`, even when you only need one argument.
    - Use `DoProc` for runtime-selected script procedures, not for ordinary local control flow.
    - Validate the arguments in the caller when the target signature matters.
    - Inside class methods, call sibling or inherited methods with `Me:` or `Base:` instead.

!!! failure "Don't"
    - Pass a scalar as the second argument. `DoProc` expects an array there.
    - Assume argument-count mismatches raise an immediate `DoProc` error.
    - Use a two-segment procedure name. That format is rejected.
    - Use `DoProc` inside class methods.

## Caveats

- One-segment names are resolved case-insensitively in the current script.
- Three-segment names are passed into the executor path instead of local method lookup.

## Examples

### Call a local procedure by name

Dispatches to two local procedures by name: one that logs a message and one that maps a status code to a description string, then prints the returned description.

```ssl
:PROCEDURE CallProcedureDynamically;
	:DECLARE sProcName, aArgs, sResult;

	sProcName := "LogMessage";
	aArgs := {"Sample analysis complete", "INFO"};

	DoProc(sProcName, aArgs);
	sResult := DoProc("GetStatusText", {200});

	UsrMes(LimsString(sResult));
	/* Displays returned status text;
:ENDPROC;


:PROCEDURE LogMessage;
	:PARAMETERS sMessage, sLevel;
	:DECLARE sLogEntry;

	sLogEntry := "[" + sLevel + "] " + sMessage;

	UsrMes(sLogEntry);
	/* Displays the formatted log entry;
:ENDPROC;


:PROCEDURE GetStatusText;
	:PARAMETERS nCode;
	:DECLARE sDescription;

	:BEGINCASE;
	:CASE nCode == 200;
		sDescription := "Success";
		:EXITCASE;
	:CASE nCode == 404;
		sDescription := "Not Found";
		:EXITCASE;
	:OTHERWISE;
		sDescription := "Unknown Status";
		:EXITCASE;
	:ENDCASE;

	:RETURN sDescription;
:ENDPROC;

/* Usage example;
DoProc("CallProcedureDynamically");
```

### Use a runtime-selected local procedure

Selects one of two handler procedures based on a boolean flag and dispatches to it at runtime, showing how the same call site routes to different behavior.

```ssl
:PROCEDURE RouteStatusMessage;
	:PARAMETERS bIsError, sMessage;
	:DECLARE sTarget;

	sTarget := "ShowInfoMessage";

	:IF bIsError;
		sTarget := "ShowErrorMessage";
	:ENDIF;

	DoProc(sTarget, {sMessage});

	:RETURN sTarget;
:ENDPROC;


:PROCEDURE ShowInfoMessage;
	:PARAMETERS sMessage;

	UsrMes("INFO: " + sMessage);
:ENDPROC;


:PROCEDURE ShowErrorMessage;
	:PARAMETERS sMessage;

	ErrorMes("ERROR: " + sMessage);
:ENDPROC;

/* Usage example;
DoProc("RouteStatusMessage", {.T., "Something failed"});
```

### Dispatch to an external procedure path

Builds a three-segment procedure name at runtime and dispatches to it using `DoProc`, demonstrating the external executor path.

```ssl
:PROCEDURE SubmitConfiguredStep;
	:PARAMETERS sStepName, sSampleID, sUserName;
	:DECLARE sProcName, vResult;

	sProcName := "Workflow.SampleActions." + sStepName;

	vResult := DoProc(sProcName, {sSampleID, sUserName});

	UsrMes("Dispatched: " + sProcName);

	:RETURN vResult;
:ENDPROC;

/* Usage example;
DoProc("SubmitConfiguredStep", {"ProcessSample", "S-001", "jsmith"});
```

[`UsrMes`](UsrMes.md) displays:

```text
Dispatched: Workflow.SampleActions.ProcessSample
```

## Related

- [`ExecFunction`](ExecFunction.md)
- [`ExecInternal`](ExecInternal.md)
- [`ExecUdf`](ExecUdf.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
