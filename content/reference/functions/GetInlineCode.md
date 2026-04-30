---
title: "GetInlineCode"
summary: "Retrieves a named inline code block as a string."
id: ssl.function.getinlinecode
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetInlineCode

Retrieves a named inline code block as a string.

`GetInlineCode` looks up an inline code block created with [`:BEGININLINECODE`](../keywords/BEGININLINECODE.md) and returns its text. If you pass `aVariables`, the function replaces those variable names in the returned code with their current values before returning the string. The lookup is case-insensitive.

## When to use

- When you need the text of a previously defined inline code block.
- When you want to inject current variable values into inline code before passing the result to [`ExecUdf`](ExecUdf.md) or another dynamic execution path.
- When you need inline code retrieval rather than region text retrieval.

## Syntax

```ssl
GetInlineCode(sValue, [aVariables])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sValue` | [string](../types/string.md) | yes | — | Name of the inline code block to retrieve. |
| `aVariables` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Array of variable names to substitute with their current values in the returned code. |

## Returns

**[string](../types/string.md)** — The inline code text for the named block. Returns an empty string when no inline code blocks are defined in the current execution context. Returns the code unchanged when `aVariables` is omitted or [`NIL`](../literals/nil.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| Inline code blocks are defined but the named block is not among them. | `<name> not in scope.` |
| A name in `aVariables` is not defined in the current scope. | `Variable [<variable_name>] is undefined!` |

## Best practices

!!! success "Do"
    - Use `GetInlineCode` when you need the stored inline code text, with or
      without variable substitution.
    - Pass only the variable names that must be resolved into the returned code.
    - Delete temporary inline code with [`DeleteInlineCode`](DeleteInlineCode.md) when you are finished with it.

!!! failure "Don't"
    - Assume a missing inline code block returns an empty string in all cases. That only happens when no inline code blocks are currently defined.
    - Pass variable names that are not defined in the current scope.
    - Use `GetInlineCode` when you need region text from [`:REGION`](../keywords/REGION.md); use [`GetRegion`](GetRegion.md) or [`GetRegionEx`](GetRegionEx.md) for that case.

## Caveats

- `GetInlineCode` retrieves code text; it does not execute that code.

## Examples

### Retrieve and execute inline code

Retrieves a named inline code block as a string, then executes it with [`ExecUdf`](ExecUdf.md); cleans up the inline code after use with [`DeleteInlineCode`](DeleteInlineCode.md).

```ssl
:PROCEDURE RunGreeting;
	:DECLARE sCode, sMessage;

	:BEGININLINECODE "GreetingTemplate";
		:RETURN "Hello from inline code";
	:ENDINLINECODE;

	sCode := GetInlineCode("GreetingTemplate");
	sMessage := ExecUdf(sCode, {}, .F.);

	DeleteInlineCode("GreetingTemplate");

	UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("RunGreeting");
```

[`UsrMes`](UsrMes.md) displays:

```
Hello from inline code
```

### Substitute current variable values before execution

Passes variable names in `aVariables` so the function embeds their current values into the code text before returning it; the substituted code is then executed by [`ExecUdf`](ExecUdf.md).

```ssl
:PROCEDURE BuildStatusMessage;
	:DECLARE sStatus, nCount, sCode, sMessage;

	sStatus := "Complete";
	nCount := 12;

	:BEGININLINECODE "StatusTemplate";
		:RETURN "Status: " + sStatus + " Count: " + LimsString(nCount);
	:ENDINLINECODE;

	sCode := GetInlineCode("StatusTemplate", {"sStatus", "nCount"});
	sMessage := ExecUdf(sCode, {}, .F.);

	DeleteInlineCode("StatusTemplate");

	UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("BuildStatusMessage");
```

[`UsrMes`](UsrMes.md) displays:

```
Status: Complete Count: 12
```

## Related

- [`DeleteInlineCode`](DeleteInlineCode.md)
- [`ExecUdf`](ExecUdf.md)
- [`GetRegion`](GetRegion.md)
- [`GetRegionEx`](GetRegionEx.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
