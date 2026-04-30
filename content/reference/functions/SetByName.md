---
title: "SetByName"
summary: "Assigns a value to a variable whose name is supplied at runtime."
id: ssl.function.setbyname
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SetByName

Assigns a value to a variable whose name is supplied at runtime.

`SetByName()` takes a variable name and a value, then writes that value to the matching variable. It first looks for an existing local variable in the current scope, then in caller scopes, then in public variables. If no existing variable is found, the runtime either creates a new local variable or raises an error, depending on the current `AllowUndeclaredVars` setting. The function returns the same value that was assigned.

Use `SetByName()` when the target variable name is only known at runtime, such as in generic helpers, import routines, or configuration-driven code.

## When to use

- When the target variable name comes from data, configuration, or user input.
- When a helper procedure needs to update a caller variable by name.
- When you need one routine to work with either local or public variables.
- When you want to pair dynamic writes with [`GetByName`](GetByName.md) for runtime variable access.

## Syntax

```ssl
SetByName(sName, vValue)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sName` | [string](../types/string.md) | yes | — | Name of the variable to update |
| `vValue` | any | yes | — | Value to assign |

## Returns

**any** — The same `vValue` that was assigned.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sName` is [`NIL`](../literals/nil.md) or empty. | `Variable name cannot be missing.` |
| No matching variable exists and undeclared-variable creation is disabled. | `Variable [<sName>] is undefined!` |

## Best practices

!!! success "Do"
    - Validate or normalize the variable name before calling `SetByName()`.
    - Use [`GetByName`](GetByName.md) when you need to confirm the final value after a dynamic write.
    - Prefer [`CreateLocal`](CreateLocal.md) or [`CreatePublic`](CreatePublic.md) when you explicitly want to create a variable in a known scope.
    - Be deliberate about scope, because `SetByName()` can update a caller variable instead of creating a new current-scope local.

!!! failure "Don't"
    - Pass an empty name or unchecked input directly into `SetByName()`.
    - Assume the function always creates a new variable. It only does that when undeclared-variable creation is enabled.
    - Use `SetByName()` when a direct variable assignment is already possible and clearer.
    - Assume the target is always in the current local scope. The runtime may update a caller or public variable instead.

## Caveats

- Variable names are resolved case-insensitively.
- If the name exists in a caller scope but not the current scope, `SetByName()` updates the caller variable.
- If the name does not match any local or public variable and undeclared-variable creation is enabled, a new local variable is created in the current scope.
- If the name does not match any local or public variable and undeclared-variable creation is disabled, the call raises an error.
- When a variable is resolved in a caller scope or created after a miss, the runtime's undefined-variable callback may run if one has been registered.

## Examples

### Update an existing local variable by name

Use a string variable name to update a local that is already declared.

```ssl
:PROCEDURE DemoSetByNameLocal;
    :DECLARE sTargetName, sStatus, sResultValue;

    sTargetName := "sStatus";
    sStatus := "Pending";

    sResultValue := SetByName(sTargetName, "Complete");

    UsrMes("Result: " + LimsString(sResultValue));
    UsrMes("Updated status: " + sStatus);

    :RETURN sResultValue;
:ENDPROC;

/* Usage;
DoProc("DemoSetByNameLocal");
```

### Update a public variable by runtime name

If no local matches, `SetByName()` can update an existing public variable.

```ssl
:PROCEDURE DemoSetByNamePublic;
    :DECLARE sTargetName, sResultValue, sPublicValue;

    sTargetName := "sMode";
    CreatePublic(sTargetName, "TEST");

    sResultValue := SetByName(sTargetName, "PROD");
    sPublicValue := GetByName(sTargetName);

    UsrMes("Returned value: " + LimsString(sResultValue));
    UsrMes("Public value: " + LimsString(sPublicValue));

    :RETURN sPublicValue;
:ENDPROC;

/* Usage;
DoProc("DemoSetByNamePublic");
```

### Update a caller variable from a helper procedure

This example shows that `SetByName()` can write to a variable defined in the calling scope.

```ssl
:PROCEDURE DemoSetByNameCaller;
    :DECLARE sStatus;

    sStatus := "Queued";
    DoProc("ApplyStatus", {"sStatus", "Released"});

    UsrMes("Caller status: " + sStatus);
    :RETURN sStatus;
:ENDPROC;

:PROCEDURE ApplyStatus;
    :PARAMETERS sTargetName, sNewValue;
    :DECLARE sResultValue;

    sResultValue := SetByName(sTargetName, sNewValue);

    UsrMes("Helper assigned: " + LimsString(sResultValue));
    :RETURN sResultValue;
:ENDPROC;

/* Usage;
DoProc("DemoSetByNameCaller");
```

## Related

- [`CreateLocal`](CreateLocal.md)
- [`CreatePublic`](CreatePublic.md)
- [`GetByName`](GetByName.md)
- [`IsDefined`](IsDefined.md)
- [`string`](../types/string.md)
