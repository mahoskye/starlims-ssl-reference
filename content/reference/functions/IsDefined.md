---
title: "IsDefined"
summary: "Determines whether a variable name is currently defined."
id: ssl.function.isdefined
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# IsDefined

Determines whether a variable name is currently defined.

`IsDefined` accepts a variable name as a non-empty string and returns [`.T.`](../literals/true.md) when that name resolves in the current local scope, a caller scope, or public scope. It returns [`.F.`](../literals/false.md) when the name is not defined. If you pass [`NIL`](../literals/nil.md), an empty string, or a non-string value, the function raises an exception instead of returning [`.F.`](../literals/false.md).

Use `IsDefined` when the variable name is only known at runtime and you need to check for existence before reading it with functions such as [`GetByName`](GetByName.md) or changing your script flow.

## When to use

- When a variable name comes from runtime data and you need to know whether it exists.
- When you want to guard a later [`GetByName`](GetByName.md) call.
- When you support optional local or public variables in the same script flow.
- When you need to branch differently depending on whether a setup variable was created.

## Syntax

```ssl
IsDefined(sVarName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sVarName` | [string](../types/string.md) | yes | — | Name of the variable to check for existence. Must be non-empty. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the name resolves in the current local scope, a caller scope, or public scope; [`.F.`](../literals/false.md) when no variable with that name exists.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sVarName` is [`NIL`](../literals/nil.md). | `Argument 'sVarName' cannot be null!` |
| `sVarName` is not a string or is empty. | `Argument 'sVarName' must be a non-empty string!` |

## Best practices

!!! success "Do"
    - Pass a runtime variable name string, not the variable value itself.
    - Use `IsDefined()` before [`GetByName`](GetByName.md) when a variable may or may not exist.
    - Use [`Empty`](Empty.md) separately when you need to know whether a defined variable also has content.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md), `""`, or a non-string value and expect [`.F.`](../literals/false.md). Those inputs raise exceptions.
    - Use `IsDefined()` to check object properties such as `oConfig:ModuleName`; it checks variable names, not member paths.
    - Use [`Empty`](Empty.md) as a substitute for existence checks. A variable can be defined and still be empty.

## Caveats

- Variable lookup follows normal SSL variable resolution: current local scope,
  then caller scopes, then public scope.
- The name comparison is case-insensitive, consistent with SSL variable names.
- `IsDefined()` checks whether the variable exists, not whether its value is empty.

## Examples

### Confirm a variable is defined before reading it

Check with `IsDefined` before branching on the variable's value. Because `sWorkflowStatus` is assigned above the check, the true branch runs and the false branch is shown only for completeness.

```ssl
:PROCEDURE CheckWorkflowStatus;
    :DECLARE sWorkflowStatus, sMessage, bHasWorkflowStatus;

    sWorkflowStatus := "Active";

    bHasWorkflowStatus := IsDefined("sWorkflowStatus");

    /* Use the variable only after confirming it exists;
    :IF bHasWorkflowStatus;
        sMessage := "Workflow status is: " + sWorkflowStatus;
        UsrMes(sMessage);  /* Displays: Workflow status is: Active;
    :ELSE;
        sMessage := "Workflow status variable not defined";
        UsrMes(sMessage);  /* Displays: Workflow status variable not defined;
    :ENDIF;

    :RETURN;
:ENDPROC;

/* Usage;
DoProc("CheckWorkflowStatus");
```

### Report which names from a candidate list are defined

Iterate over a list of candidate variable names and build a comma-separated summary of those currently in scope. The single [`UsrMes`](UsrMes.md) call at the end shows either the list of available names or a not-defined message.

```ssl
:PROCEDURE SummarizeAvailableInputs;
    :PARAMETERS aCandidateVars;
    :DECLARE nIndex, sVarName, sAvailable, sMessage;

    /* Build a readable list of the names that currently exist;
    sAvailable := "";

    :FOR nIndex := 1 :TO ALen(aCandidateVars);
        sVarName := aCandidateVars[nIndex];

        :IF IsDefined(sVarName);
            :IF Empty(sAvailable);
                sAvailable := sVarName;
            :ELSE;
                sAvailable := sAvailable + ", " + sVarName;
            :ENDIF;
        :ENDIF;
    :NEXT;

    :IF Empty(sAvailable);
        sMessage := "No optional input variables are defined";
    :ELSE;
        sMessage := "Available input variables: " + sAvailable;
    :ENDIF;

    UsrMes(sMessage);

    :RETURN sAvailable;
:ENDPROC;

/* Usage;
DoProc("SummarizeAvailableInputs", {{"sCacheKey", "sContextId"}});
```

[`UsrMes`](UsrMes.md) displays:

```text
Available input variables: sCacheKey, sContextId
```

### Resolve the first non-empty variable from a candidate list

Walk a list of candidate variable names and read the first one that is both defined and non-empty using [`GetByName`](GetByName.md). The `IsDefined` check prevents [`GetByName`](GetByName.md) from raising an error on a missing name.

```ssl
:PROCEDURE ResolveBatchIdentifier;
    :PARAMETERS aCandidateVars;
    :DECLARE nIndex, sVarName, vBatchValue, sBatchId;

    sBatchId := "";

    /* Read the first available variable from a list of supported names;
    :FOR nIndex := 1 :TO ALen(aCandidateVars);
        sVarName := aCandidateVars[nIndex];

        :IF IsDefined(sVarName);
            vBatchValue := GetByName(sVarName);

            :IF ! Empty(vBatchValue);
                sBatchId := LimsString(vBatchValue);
                :EXITFOR;
            :ENDIF;
        :ENDIF;
    :NEXT;

    :IF Empty(sBatchId);
        ErrorMes("No batch identifier variable is available");
        :RETURN .F.;
    :ENDIF;

    UsrMes("Using batch identifier: " + sBatchId);
    /* Displays selected batch identifier;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ResolveBatchIdentifier", {{"sBatchId", "sOrderNo"}});
```

## Related

- [`CreateLocal`](CreateLocal.md)
- [`CreatePublic`](CreatePublic.md)
- [`Empty`](Empty.md)
- [`GetByName`](GetByName.md)
- [`LKill`](LKill.md)
- [`Nothing`](Nothing.md)
- [`SetByName`](SetByName.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
