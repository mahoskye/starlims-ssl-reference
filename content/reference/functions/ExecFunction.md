---
title: "ExecFunction"
summary: "Invokes a function by name at runtime and returns the result."
id: ssl.function.execfunction
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ExecFunction

Invokes a function by name at runtime and returns the result.

`ExecFunction` takes a function name as a string and an optional argument
array, executes the named function, and returns whatever that function returns. A one-segment name resolves in the current script; a three-segment name is dispatched through the same external execution path used by [`DoProc`](DoProc.md). The second argument, when supplied, must be an array.

## When to use

- When building automation or scripts where the function to call is determined at runtime by configuration or rules.
- When passing a dynamic, potentially variable-length argument list to a function that is only determined during execution.
- When integrating plugins or modules where available functions and arguments are not known in advance.
- When dispatching to application logic or workflow steps based on database values, user settings, or other runtime sources.

## Syntax

```ssl
ExecFunction(sName, [aParameters])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sName` | [string](../types/string.md) | yes | — | The name of the function or method to execute. May include a namespace path (e.g., `"ServerScript.ClassName.MethodName"`). |
| `aParameters` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | An array of parameters to pass to the specified function or method when executed. |

## Returns

**any** — The return value from the executed function or method.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| Called with no arguments at all. | `Please provide at least one parameter for ExecFunction` |
| `aParameters` is provided but is not an array. | `Wrong parameters for {functionName}` |

## Best practices

!!! success "Do"
    - Verify that the function name exists and expects the correct arguments before calling.
    - When passing arguments, provide them as an array.
    - Handle errors from this function proactively to manage cases where the call fails or the function does not exist.

!!! failure "Don't"
    - Allow untrusted input to determine the function name or arguments without validation.
    - Omit the second argument or provide a non-array value when the target expects arguments.
    - Assume all calls will succeed or ignore errors from dynamic invocation.

## Caveats

- If the function name is misspelled, empty, or references a non-existent target, a runtime error is thrown with little context.
- All type validation is deferred to the time of invocation, so incorrect argument types or counts are only caught at runtime.

## Examples

### Call a runtime-selected function with arguments

Calls a function whose name is determined at runtime, passing a date-range argument array. The function name and arguments are data, so changing what runs requires only a configuration change, not a code change.

```ssl
:PROCEDURE RunConfiguredReport;
	:DECLARE sFunctionName, aArgs, vResult;

	sFunctionName := "Reports.OrderSummary";
	aArgs := {"2024-01-01", "2024-03-31"};

	vResult := ExecFunction(sFunctionName, aArgs);

	UsrMes("Result: " + LimsString(vResult));

	:RETURN vResult;
:ENDPROC;

/* Usage;
DoProc("RunConfiguredReport");
```

[`UsrMes`](UsrMes.md) displays:

```
Result: <return value of Reports.OrderSummary>
```

### Chain data-driven workflow steps

Iterates a list of workflow step names and calls each with `ExecFunction`. If any step returns a falsy value or raises an error, `bShouldContinue` is set to [`.F.`](../literals/false.md) and the loop exits early via [`:EXITFOR`](../keywords/EXITFOR.md).

```ssl
:PROCEDURE RunAutomatedChain;
	:DECLARE aWorkflowSteps, nIndex, nTotalSteps;
	:DECLARE sStepFunc, aStepArgs, vResult, bShouldContinue, sLogMsg;

	aWorkflowSteps := {
		{"MyApp.StepCheckConfig", {}},
		{"MyApp.StepUploadData", {"fileA.csv"}},
		{"MyApp.StepValidateResults", {}},
		{"MyApp.StepFinalize", {}}
	};

	nTotalSteps := ALen(aWorkflowSteps);
	bShouldContinue := .T.;

	:FOR nIndex := 1 :TO nTotalSteps;
		sStepFunc := aWorkflowSteps[nIndex, 1];
		aStepArgs := aWorkflowSteps[nIndex, 2];

		sLogMsg := "Starting step " + LimsString(nIndex) + ": " + sStepFunc;
		UsrMes(sLogMsg);

		:TRY;
			vResult := ExecFunction(sStepFunc, aStepArgs);

			:IF (LimsTypeEx(vResult) == "LOGIC") .AND. (.NOT. vResult);
				UsrMes("Step " + LimsString(nIndex) + " failed. Aborting chain.");
				bShouldContinue := .F.;
			:ENDIF;
		:CATCH;
			UsrMes("Error in step " + LimsString(nIndex) + ": " + sStepFunc);
			bShouldContinue := .F.;
		:ENDTRY;

		:IF .NOT. bShouldContinue;
			:EXITFOR;
		:ENDIF;
	:NEXT;

	:IF bShouldContinue;
		UsrMes("Workflow completed all steps successfully.");
	:ELSE;
		UsrMes("Workflow terminated early due to error or step failure.");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("RunAutomatedChain");
```

## Related

- [`DoProc`](DoProc.md)
- [`Eval`](Eval.md)
- [`ExecInternal`](ExecInternal.md)
- [`ExecUdf`](ExecUdf.md)
- [`PrmCount`](PrmCount.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
