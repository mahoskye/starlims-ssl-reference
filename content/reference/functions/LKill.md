---
title: "LKill"
summary: "Deletes a public variable from the current SSL session by name and returns an empty string."
id: ssl.function.lkill
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LKill

Deletes a public variable from the current SSL session by name and returns an empty string.

`LKill()` removes the named entry from the public-variable store for the current runtime session. If a public variable with that name exists, it is deleted. If no public variable with that name exists, the call does nothing. In either case, the function returns an empty string.

`LKill()` affects public variables only. It does not remove local variables or caller-scope variables that happen to use the same name. Public-variable names are matched case-insensitively.

## When to use

- When you no longer need a public variable created with [`CreatePublic`](CreatePublic.md).
- When you want to clear shared session state before starting a new workflow step.
- When you need to remove a runtime-named public variable after temporary use.

## Syntax

```ssl
LKill(sVarName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sVarName` | [string](../types/string.md) | yes | — | Name of the public variable to remove. |

## Returns

**[string](../types/string.md)** — Always returns `""`.

## Best practices

!!! success "Do"
    - Use `LKill()` for cleanup of public variables that were created dynamically for the current session.
    - Keep the public-variable name in a string variable when the name is determined at runtime.
    - Use [`IsDefined`](IsDefined.md) if later logic needs to confirm the public variable is gone.

!!! failure "Don't"
    - Use `LKill()` as a substitute for clearing a local variable. It only removes public variables.
    - Assume a missing public variable is an error condition. `LKill()` simply does nothing when the name is not present.
    - Rely on undocumented input handling for invalid arguments. Pass a valid public-variable name string.

## Caveats

- Removing a public variable can change later code paths that expect the shared value to still exist.

## Examples

### Remove one public variable by runtime name

Create a public variable, confirm it exists, remove it, then confirm it no longer resolves.

```ssl
:PROCEDURE DemoLKillBasic;
    :DECLARE sVarName, bBefore, bAfter;

    sVarName := "sSharedStatus";
    CreatePublic(sVarName, "Queued");

    bBefore := IsDefined(sVarName);

    LKill(sVarName);

    bAfter := IsDefined(sVarName);

    UsrMes("Defined before delete: " + LimsString(bBefore));
    UsrMes("Defined after delete: " + LimsString(bAfter));

    :RETURN bAfter;
:ENDPROC;

/* Usage;
DoProc("DemoLKillBasic");
```

`UsrMes` displays:

```text
Defined before delete: True
Defined after delete: False
```

### Reset a shared public value before recreating it

Remove an old public value so the next step can create the shared variable again with a clean state.

```ssl
:PROCEDURE DemoLKillReset;
    :DECLARE sVarName, vValue;

    sVarName := "nSharedCount";
    CreatePublic(sVarName, 5);

    vValue := GetByName(sVarName);
    UsrMes("Old value: " + LimsString(vValue));

    LKill(sVarName);

    :IF !IsDefined(sVarName);
        CreatePublic(sVarName, 1);
    :ENDIF;

    vValue := GetByName(sVarName);
    UsrMes("Reset value: " + LimsString(vValue));

    :RETURN vValue;
:ENDPROC;

/* Usage;
DoProc("DemoLKillReset");
```

`UsrMes` displays:

```text
Old value: 5
Reset value: 1
```

### Clean up a set of runtime-created public variables

Track multiple public-variable names in an array and remove each one during a shared cleanup step.

```ssl
:PROCEDURE DemoLKillBatchCleanup;
    :DECLARE aVarNames, nIndex, sVarName, bAllRemoved;

    aVarNames := {"sFilterStatus", "sFilterOwner", "dFilterDate"};

    CreatePublic(aVarNames[1], "Active");
    CreatePublic(aVarNames[2], "jsmith");
    CreatePublic(aVarNames[3], Today());

    :FOR nIndex := 1 :TO ALen(aVarNames);
        sVarName := aVarNames[nIndex];

        LKill(sVarName);
    :NEXT;

    bAllRemoved := .T.;

    :FOR nIndex := 1 :TO ALen(aVarNames);
        sVarName := aVarNames[nIndex];

        :IF IsDefined(sVarName);
            bAllRemoved := .F.;
            :EXITFOR;
        :ENDIF;
    :NEXT;

    UsrMes("All shared filters removed: " + LimsString(bAllRemoved));

    :RETURN bAllRemoved;
:ENDPROC;

/* Usage;
DoProc("DemoLKillBatchCleanup");
```

[`UsrMes`](UsrMes.md) displays:

```text
All shared filters removed: True
```

## Related

- [`CreateLocal`](CreateLocal.md)
- [`CreatePublic`](CreatePublic.md)
- [`GetByName`](GetByName.md)
- [`IsDefined`](IsDefined.md)
- [`SetByName`](SetByName.md)
- [`string`](../types/string.md)
