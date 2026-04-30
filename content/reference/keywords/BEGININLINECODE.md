---
title: "BEGININLINECODE"
summary: "Starts a named inline SSL code block that is stored for later retrieval with GetInlineCode."
id: ssl.keyword.begininlinecode
element_type: keyword
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# BEGININLINECODE

Starts a named inline SSL code block that is stored for later retrieval with [`GetInlineCode`](../functions/GetInlineCode.md).

`:BEGININLINECODE` opens a named block of SSL source and continues until [`:ENDINLINECODE`](ENDINLINECODE.md). The block name is required and is later used to retrieve or delete the stored code. The inline body must be valid SSL, so syntax errors inside the block still fail compilation.

## Behavior

`:BEGININLINECODE` can appear where a statement is allowed. The block body is captured until [`:ENDINLINECODE`](ENDINLINECODE.md) and stored under the supplied name.

Unlike [`:REGION`](REGION.md), the inline body is validated as executable SSL. Use this form when you want a named block of executable SSL code that can be retrieved later as text.

## When to use

- When you want to store a reusable snippet of SSL code in the current script.
- When you plan to retrieve that snippet later with [`GetInlineCode`](../functions/GetInlineCode.md).
- When you need a named block whose text can be reused with different local variable substitutions.

## Syntax

```ssl
:BEGININLINECODE BlockName;
    /* Inline SSL code here;
:ENDINLINECODE;
```

You can also quote the block name:

```ssl
:BEGININLINECODE "BlockName";
    /* Inline SSL code here;
:ENDINLINECODE;
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `BlockName` | Identifier or quoted identifier | Yes | Name of the inline code block used by [`GetInlineCode`](../functions/GetInlineCode.md) and [`DeleteInlineCode`](../functions/DeleteInlineCode.md). |

## Keyword group

**Group:** Organization
**Role:** opener

## Best practices

!!! success "Do"
    - Use a clear block name that matches how the code will be retrieved.
    - Keep the inline body valid SSL so the script compiles cleanly.
    - Delete temporary inline code with [`DeleteInlineCode`](../functions/DeleteInlineCode.md) after use when the block is no longer needed.

!!! failure "Don't"
    - Treat the block name as a language name; it is a lookup name, not a host-language selector.
    - Use `:BEGININLINECODE` for unvalidated free-form text. Use [`REGION`](REGION.md) when you need stored text that is not validated as executable SSL.
    - Omit [`:ENDINLINECODE`](ENDINLINECODE.md) or the required block name; the script will not compile.

## Caveats

- [`GetInlineCode`](../functions/GetInlineCode.md) raises a runtime error if the named block is not in scope.
- [`DeleteInlineCode`](../functions/DeleteInlineCode.md) raises a runtime error if the named block is not in scope.

## Examples

### Store and run a simple inline block

Define a named inline block, retrieve it with [`GetInlineCode`](../functions/GetInlineCode.md), execute it with [`ExecUdf`](../functions/ExecUdf.md), and then remove it with [`DeleteInlineCode`](../functions/DeleteInlineCode.md).

```ssl
:PROCEDURE RunGreeting;
	:DECLARE sCode, sResult;

	:BEGININLINECODE GreetingBlock;
		:RETURN "Hello from inline code";
	:ENDINLINECODE;

	sCode := GetInlineCode("GreetingBlock");
	sResult := ExecUdf(sCode, {}, .F.);

	DeleteInlineCode("GreetingBlock");
	UsrMes(sResult);
:ENDPROC;

/* Usage;
DoProc("RunGreeting");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Hello from inline code
```

### Substitute local variables before execution

Pass local variable names to [`GetInlineCode`](../functions/GetInlineCode.md) so the returned code uses the current values of those variables. Here `sStatus` and `nCount` are substituted before [`ExecUdf`](../functions/ExecUdf.md) executes the tailored snippet.

```ssl
:PROCEDURE BuildStatusMessage;
	:DECLARE sCode, sResult, sStatus, nCount;

	sStatus := "Logged";
	nCount := 3;

	:BEGININLINECODE StatusMessage;
		:RETURN "Status: " + sStatus + ", Count: " + LimsString(nCount);
	:ENDINLINECODE;

	sCode := GetInlineCode("StatusMessage", {"sStatus", "nCount"});
	sResult := ExecUdf(sCode, {}, .F.);

	DeleteInlineCode("StatusMessage");
	UsrMes(sResult);
:ENDPROC;

/* Usage;
DoProc("BuildStatusMessage");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Status: Logged, Count: 3
```

### Choose between multiple named blocks

Store more than one inline block and select which one to execute by name. With `sAction` set to `"LOG"`, the matching block is retrieved and executed.

```ssl
:PROCEDURE RunAction;
	:PARAMETERS sAction;
	:DECLARE sCode, sResult;

	sCode := "";

	:BEGININLINECODE LogAction;
		:RETURN "Action logged";
	:ENDINLINECODE;

	:BEGININLINECODE RetryAction;
		:RETURN "Action retried";
	:ENDINLINECODE;

	:BEGINCASE;
	:CASE Upper(sAction) == "LOG";
		sCode := GetInlineCode("LogAction");
		:EXITCASE;
	:CASE Upper(sAction) == "RETRY";
		sCode := GetInlineCode("RetryAction");
		:EXITCASE;
	:OTHERWISE;
		sResult := "Unknown action";
		:EXITCASE;
	:ENDCASE;

	:IF Empty(sCode);
		DeleteInlineCode("LogAction");
		DeleteInlineCode("RetryAction");

		:RETURN sResult;
	:ENDIF;

	sResult := ExecUdf(sCode, {}, .F.);

	DeleteInlineCode("LogAction");
	DeleteInlineCode("RetryAction");

	:RETURN sResult;
:ENDPROC;

/* Usage;
DoProc("RunAction", {"LOG"});
```

## Related

- [`ENDINLINECODE`](ENDINLINECODE.md)
- [`GetInlineCode`](../functions/GetInlineCode.md)
- [`DeleteInlineCode`](../functions/DeleteInlineCode.md)
- [`REGION`](REGION.md)
