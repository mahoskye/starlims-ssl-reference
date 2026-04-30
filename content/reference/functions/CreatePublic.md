---
title: "CreatePublic"
summary: "Creates or overwrites a public variable by name."
id: ssl.function.createpublic
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CreatePublic

Creates or overwrites a public variable by name.

`CreatePublic` creates a public variable when it does not already exist, then writes the supplied value into it. `sVarName` must be a string. If `vVarValue` is omitted, the public variable is initialized to an empty string. The function returns the supplied `vVarValue`; when the second argument is omitted, the public variable still stores `""`, but the call itself returns no value. Use `CreatePublic` when the variable name is only known at runtime and the value must be available outside the current local scope.

## When to use

- When you need to create a public variable whose name is decided at runtime.
- When multiple parts of the current SSL session need to share the same value.
- When you need to overwrite an existing public variable with a new value.

## Syntax

```ssl
CreatePublic(sVarName, [vVarValue])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sVarName` | [string](../types/string.md) | yes | — | Name of the public variable to create or overwrite |
| `vVarValue` | any | no | `""` | Value to store in the public variable. If omitted, the public variable is initialized to an empty string |

## Returns

**any** — The supplied `vVarValue`. If `vVarValue` is omitted, the public variable is created with `""`, and the call returns no value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sVarName` is [`NIL`](../literals/nil.md). | `Argument sVarName cannot be null.` |
| `sVarName` is not a string. | `Argument sVarName must be a string.` |

## Best practices

!!! success "Do"
    - Use `CreatePublic` only when the value must be shared outside the current local scope.
    - Use descriptive names so the public variable's purpose is obvious where it is read later.
    - Omit `vVarValue` only when an empty string is the value you actually want stored.

!!! failure "Don't"
    - Pass a number, array, object, or other non-string value as `sVarName`.
    - Use `CreatePublic` for temporary procedure-local state. Use [`CreateLocal`](CreateLocal.md) instead.
    - Assume omitting `vVarValue` makes the function return an empty string. It initializes the public variable to `""`, but the call itself does not return that value.

## Caveats

- Public-variable names are resolved case-insensitively.
- A local variable with the same name still takes precedence when code resolves that name.

## Examples

### Create a public status value by runtime name

Creates a public variable using a name stored in another variable, then reads it back using [`GetByName`](GetByName.md) to confirm the stored value.

```ssl
:PROCEDURE DemoCreatePublicBasic;
	:DECLARE sVarName, sValue;

	sVarName := "sSharedStatus";
	CreatePublic(sVarName, "Queued");
	sValue := GetByName(sVarName);

	UsrMes("Public value: " + LimsString(sValue));
	:RETURN sValue;
:ENDPROC;

/* Usage;
DoProc("DemoCreatePublicBasic");
```

[`UsrMes`](UsrMes.md) displays:

```
Public value: Queued
```

### Initialize a public variable to an empty string

Calls `CreatePublic` without a second argument so the new variable is initialized to an empty string, then checks whether the variable is empty.

```ssl
:PROCEDURE DemoCreatePublicDefault;
	:DECLARE sVarName, sValue;

	sVarName := "sSharedNote";
	CreatePublic(sVarName);
	sValue := GetByName(sVarName);

	:IF Empty(sValue);
		UsrMes("The public variable starts as an empty string.");
	:ENDIF;

	:RETURN sValue;
:ENDPROC;

/* Usage;
DoProc("DemoCreatePublicDefault");
```

[`UsrMes`](UsrMes.md) displays:

```
The public variable starts as an empty string.
```

### Overwrite a shared public value across procedure calls

Two helper procedures initialize and increment a shared public variable by name. The caller reads the current value after each step to show the progression.

```ssl
:PROCEDURE DemoCreatePublicScope;
	:DECLARE sVarName, nValue;

	sVarName := "nSharedCount";
	DoProc("InitializeSharedCount", {sVarName});
	nValue := GetByName(sVarName);
	UsrMes("Initial public value: " + LimsString(nValue));

	DoProc("IncrementSharedCount", {sVarName});
	nValue := GetByName(sVarName);
	UsrMes("Updated public value: " + LimsString(nValue));

	:RETURN nValue;
:ENDPROC;


:PROCEDURE InitializeSharedCount;
	:PARAMETERS sVarName;

	CreatePublic(sVarName, 1);
	:RETURN GetByName(sVarName);
:ENDPROC;


:PROCEDURE IncrementSharedCount;
	:PARAMETERS sVarName;
	:DECLARE nCurrentValue;

	nCurrentValue := GetByName(sVarName);
	CreatePublic(sVarName, nCurrentValue + 1);
	:RETURN GetByName(sVarName);
:ENDPROC;

/* Usage;
DoProc("DemoCreatePublicScope");
```

[`UsrMes`](UsrMes.md) displays:

```
Initial public value: 1
Updated public value: 2
```

## Related

- [`CreateLocal`](CreateLocal.md)
- [`GetByName`](GetByName.md)
- [`IsDefined`](IsDefined.md)
- [`LKill`](LKill.md)
- [`SetByName`](SetByName.md)
- [`string`](../types/string.md)
