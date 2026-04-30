---
title: "PUBLIC"
summary: "Declares global variables that can be accessed from any scope in the program."
id: ssl.keyword.public
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# PUBLIC

Declares global variables that can be accessed from any scope in the program.

The `:PUBLIC` keyword declares one or more names as public variables. Like [`:DECLARE`](DECLARE.md), it is a regular statement, so SSL allows it anywhere a statement is valid in a script or procedure body. Each declared public variable becomes part of the shared public-variable store, starts with the empty string `""`, and can then be read or updated from any scope that runs in the same program context.

## Behavior

`:PUBLIC` creates shared variable names rather than routine-local working variables. After a public name is declared, assignments to that name update the same shared value across procedures and script-level code.

Key runtime behavior:

- Each name in the list is created as a public variable and initialized to the empty string `""`.
- Later assignments update the shared public value, not a private copy.
- `:PUBLIC` is a regular statement, so SSL permits it in normal statement flow instead of requiring it at the top of the script.
- Public variables remain available until the current program context clears
  them.

## When to use

- When multiple procedures in the same running script need to share state.
- When script-level code and procedure code must read and update the same variable.
- When an integration or workflow expects a shared value to remain available after control moves into another scope.

## Syntax

```ssl
:PUBLIC variable1[, variable2, ...];
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `variable1[, variable2, ...]` | Identifier list | Yes | One or more public variable names separated by commas. |

## Keyword group

**Group:** Declarations
**Role:** modifier

## Best practices

!!! success "Do"
    - Use `:PUBLIC` sparingly for state that genuinely must be shared across scopes.
    - Keep public names clear and stable because any scope can read or overwrite them.
    - Prefer declaring public variables near the workflow entry point so shared state is easy to discover.

!!! failure "Don't"
    - Use `:PUBLIC` for routine-local working values that could stay in [`:DECLARE`](DECLARE.md) or be passed as parameters. That creates hidden coupling.
    - Assume `:PUBLIC` is required at the top of the file. SSL allows it later in normal statement flow, so placement is a readability choice.
    - Reuse a generic public name like `sValue` or `bFlag` across unrelated workflows. Shared names are easy to overwrite accidentally.

## Caveats

- `:PUBLIC` is valid in script and procedure statement flow. It is not a class
  field declaration.
- Public variables start as the empty string `""`, not [`NIL`](../literals/nil.md).
- Colon-prefixed keywords are case-sensitive, so write `:PUBLIC` in uppercase.

## Examples

### Sharing state between procedures

Declares a public variable at script level and reads it from two procedures. With `sBasePath` set to `"C:\STARLIMS\Config"`, both procedures see the same value.

```ssl
:PUBLIC sBasePath;

sBasePath := "C:\STARLIMS\Config";

:PROCEDURE DisplayConfig;
    :DECLARE sMessage;

    sMessage := "Base path is: " + sBasePath;
    UsrMes(sMessage);
    /* Displays the configured base path;
:ENDPROC;

:PROCEDURE CheckConfig;
    :DECLARE bIsSet;

    bIsSet := .NOT. Empty(sBasePath);

    :IF bIsSet;
        UsrMes("Config path has been set");
    :ELSE;
        UsrMes("Config path is empty");
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("DisplayConfig");
DoProc("CheckConfig");
```

### Declaring a public variable inside a setup procedure

Shows that `:PUBLIC` can appear in normal procedure flow and still create shared state for later procedures. `InitializeWorkflow` declares and sets the public variables; `RunWorkflow` reads them without declaring them locally.

```ssl
:PROCEDURE InitializeWorkflow;
    :DECLARE sOrderNo;

    sOrderNo := "ORD-2024-0042";

    :PUBLIC sCurrentOrderNo, bWorkflowReady;

    sCurrentOrderNo := sOrderNo;
    bWorkflowReady := .T.;
    UsrMes("Workflow initialized for order " + sCurrentOrderNo);
    /* Displays the initialized order number;
:ENDPROC;

:PROCEDURE RunWorkflow;
    :DECLARE sMessage;

    :IF .NOT. bWorkflowReady;
        UsrMes("Workflow is not initialized");
        :RETURN .F.;
    :ENDIF;

    sMessage := "Running workflow for order " + sCurrentOrderNo;
    UsrMes(sMessage);
    /* Displays the active workflow order;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("InitializeWorkflow");
DoProc("RunWorkflow");
```

## Related

- [`DECLARE`](DECLARE.md)
- [`PARAMETERS`](PARAMETERS.md)
