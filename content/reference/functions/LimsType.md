---
title: "LimsType"
summary: "Returns the single-character SSL type code for a variable name or expression."
id: ssl.function.limstype
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LimsType

Returns the single-character SSL type code for a variable name or expression.

`LimsType` accepts a string that is either a bare variable name or an SSL expression. For a bare identifier, it looks up the variable directly. For any other string, it evaluates `:RETURN <string>;` in the current scope and inspects the result.

If the variable is undeclared or the expression results in an undeclared variable, the function returns `"U"`. The literal expression `LimsType("NIL")` also returns `"U"`, but naming a variable that holds [`NIL`](../literals/nil.md), such as an omitted [`:PARAMETERS`](../keywords/PARAMETERS.md) argument, raises an error instead. If evaluation fails with a runtime error other than an undeclared variable, it returns `"UE"`.

## When to use

- When you need to check the runtime type of a variable before type-specific logic.
- When input arrives as a string (variable name or expression) and you need to confirm its type.
- When building dynamic dispatch that must handle undeclared or unknown values.

## Syntax

```ssl
LimsType(sParam)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sParam` | [string](../types/string.md) | yes | — | Variable name or SSL expression to inspect. |

## Returns

**[string](../types/string.md)** — A single-character type code based on what `sParam` evaluates to.

| Return value | Meaning |
| --- | --- |
| `C` | String |
| `N` | Number |
| `A` | Array |
| `D` | Date |
| `L` | Boolean |
| `B` | Expando |
| `O` | Object or .NET object |
| `U` | Undeclared variable, or the literal expression `"NIL"` |
| `UE` | Evaluation error |
| `UI` | Unrecognized type |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sParam` is [`NIL`](../literals/nil.md). | `Null argument.` |
| `sParam` is not a string. | `The argument for function LimsType must be a string.` |
| `sParam` names a variable that holds [`NIL`](../literals/nil.md), including an omitted [`:PARAMETERS`](../keywords/PARAMETERS.md) argument. | `Object reference not set to an instance of an object.` |

## Best practices

!!! success "Do"
    - Pass a variable name as a string (e.g. `LimsType("sMyVar")`) when you want the type of a local variable.
    - Check for `"U"`, `"UI"`, and `"UE"` explicitly — they are normal return values, not exceptions.
    - Use [`LimsTypeEx`](LimsTypeEx.md) instead when you already have the value and do not need to reference it by name.

!!! failure "Don't"
    - Pass the value itself rather than a string. `LimsType` requires a string argument.
    - Assume evaluation of an expression is side-effect-free. The function executes the expression to obtain a result.
    - Pass non-string types (numbers, arrays, objects) as the argument — they raise an error.
    - Read `"U"` as "this parameter was not passed". An omitted parameter holds [`NIL`](../literals/nil.md), and `LimsType` raises for a variable that holds [`NIL`](../literals/nil.md).

## Caveats

- Evaluating expressions may have side effects if the expression calls functions or modifies state.
- The function executes code to resolve the value; avoid passing untrusted input.
- Naming a variable that holds [`NIL`](../literals/nil.md) raises an error rather than returning `"U"`. When a variable may hold [`NIL`](../literals/nil.md), check for it first with `LimsTypeEx(vValue) == "NIL"`, or use [`LimsTypeEx`](LimsTypeEx.md) instead, which accepts [`NIL`](../literals/nil.md).

## Examples

### Check the type of a local variable by name

Pass the variable name as a string literal. `LimsType("sSampleId")` looks up `sSampleId` in the current scope and returns `"C"` because the variable holds a string value.

```ssl
:PROCEDURE CheckVariableType;
	:DECLARE sSampleId, sTypeCode;

	sSampleId := "SMP-2024-001";
	sTypeCode := LimsType("sSampleId");

	UsrMes("Type of sSampleId: " + sTypeCode);
:ENDPROC;

/* Usage;
DoProc("CheckVariableType");
```

[`UsrMes`](UsrMes.md) logs:

```text
Type of sSampleId: C
```

### Validate an optional parameter before use

Check whether an optional parameter was passed and has the expected type. An omitted parameter holds [`NIL`](../literals/nil.md), and `LimsType` raises for a variable that holds [`NIL`](../literals/nil.md), so the procedure checks for [`NIL`](../literals/nil.md) with [`LimsTypeEx`](LimsTypeEx.md) first. Only then does `LimsType("vInput")` inspect the parameter by name.

```ssl
:PROCEDURE ProcessInput;
	:PARAMETERS vInput;
	:DECLARE sTypeCode;

	:IF LimsTypeEx(vInput) == "NIL";
		UsrMes("No input provided, skipping");
		:RETURN .F.;
	:ENDIF;

	sTypeCode := LimsType("vInput");

	:IF sTypeCode != "C";
		UsrMes("Expected string but got: " + sTypeCode);
		:RETURN .F.;
	:ENDIF;

	UsrMes("Processing: " + vInput);
	/* Logs provided input;
	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ProcessInput", {"SMP-2024-001"});
```

## Related

- [`LimsTypeEx`](LimsTypeEx.md)
- [`string`](../types/string.md)
