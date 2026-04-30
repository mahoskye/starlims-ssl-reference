---
title: "CreateLocal"
summary: "Creates or overwrites a local variable in the current scope by name."
id: ssl.function.createlocal
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CreateLocal

Creates or overwrites a local variable in the current scope by name.

`CreateLocal` creates or updates a local variable in the current local scope using a runtime-supplied name. `sVarName` must be a string. `vVarValue` is optional; when you omit it, the local variable is initialized to an empty string. If a local with the same name already exists in the current scope, `CreateLocal` overwrites that local value. The function returns the supplied `vVarValue` unchanged; when the second argument is omitted, the local still stores `""`, but the call itself returns no value. Use `CreateLocal` when the variable name is decided at runtime and the value should remain local instead of becoming public.

## When to use

- When you need to create a local variable whose name is only known at runtime.
- When you want to keep temporary state local to the current procedure call instead of creating a public variable.
- When separate procedure calls need their own local variables even if they reuse the same name.

## Syntax

```ssl
CreateLocal(sVarName, [vVarValue])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sVarName` | [string](../types/string.md) | yes | — | Name of the local variable to create or overwrite |
| `vVarValue` | any | no | `""` | Value to store in the local variable. If omitted, the local variable is initialized to an empty string |

## Returns

**any** — Returns the supplied `vVarValue`. If `vVarValue` is omitted, the local variable is still created with `""`, and the call returns no value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sVarName` is [`NIL`](../literals/nil.md). | `Argument sVarName cannot be null.` |
| `sVarName` is not a string. | `Argument sVarName must be a string.` |

## Best practices

!!! success "Do"
    - Use `CreateLocal` when the variable name must be built at runtime.
    - Use descriptive names so the runtime-created local is easy to identify when reading it later with [`GetByName`](GetByName.md).
    - Omit `vVarValue` only when an empty string is the value you actually want stored.

!!! failure "Don't"
    - Pass a number, array, object, or [`NIL`](../literals/nil.md) as `sVarName`.
    - Use `CreateLocal` for values that must be shared outside the current local scope. Use [`CreatePublic`](CreatePublic.md) for that.
    - Assume omitting `vVarValue` makes the function return an empty string. It initializes the local to `""`, but the call itself does not return that value.

## Caveats

- Local-variable names are resolved case-insensitively.

## Examples

### Create a runtime-named local variable

Creates a local variable using a name stored in another variable, then reads it back using [`GetByName`](GetByName.md) to confirm the stored value.

```ssl
:PROCEDURE DemoCreateLocalBasic;
	:DECLARE sVarName, sValue;

	sVarName := "sStatus";
	CreateLocal(sVarName, "Queued");
	sValue := GetByName(sVarName);

	UsrMes("Local value: " + LimsString(sValue));
	:RETURN sValue;
:ENDPROC;

/* Usage;
DoProc("DemoCreateLocalBasic");
```

[`UsrMes`](UsrMes.md) displays:

```text
Local value: Queued
```

### Initialize a local to an empty string

Calls `CreateLocal` without a second argument so the new variable is initialized to an empty string, then checks whether the variable is empty.

```ssl
:PROCEDURE DemoCreateLocalDefault;
	:DECLARE sVarName, sValue;

	sVarName := "sOptionalNote";
	CreateLocal(sVarName);
	sValue := GetByName(sVarName);

	:IF Empty(sValue);
		UsrMes("The local starts as an empty string.");
	:ENDIF;

	:RETURN sValue;
:ENDPROC;

/* Usage;
DoProc("DemoCreateLocalDefault");
```

[`UsrMes`](UsrMes.md) displays:

```text
The local starts as an empty string.
```

### Shadow the same local name in a nested call

Two procedures each create a local variable with the same name. The inner procedure's call does not affect the outer scope, so the outer value is unchanged before and after calling the inner procedure.

```ssl
:PROCEDURE DemoCreateLocalOuter;
	:DECLARE sOuterValue;

	CreateLocal("sScopeName", "outer");
	sOuterValue := GetByName("sScopeName");
	UsrMes("Outer before nested call: " + sOuterValue);

	DoProc("DemoCreateLocalInner");

	sOuterValue := GetByName("sScopeName");
	UsrMes("Outer after nested call: " + sOuterValue);
	:RETURN sOuterValue;
:ENDPROC;

:PROCEDURE DemoCreateLocalInner;
	:DECLARE sInnerValue;

	CreateLocal("sScopeName", "inner");
	sInnerValue := GetByName("sScopeName");
	UsrMes("Inner value: " + sInnerValue);
	:RETURN sInnerValue;
:ENDPROC;

/* Usage;
DoProc("DemoCreateLocalOuter");
```

[`UsrMes`](UsrMes.md) displays:

```text
Outer before nested call: outer
Inner value: inner
Outer after nested call: outer
```

## Related

- [`CreatePublic`](CreatePublic.md)
- [`GetByName`](GetByName.md)
- [`IsDefined`](IsDefined.md)
- [`SetByName`](SetByName.md)
- [`string`](../types/string.md)
