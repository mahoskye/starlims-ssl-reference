---
title: "ENDIF"
summary: "Terminates an :IF block, with or without an :ELSE branch."
id: ssl.keyword.endif
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ENDIF

Terminates an [`:IF`](IF.md) block, with or without an [`:ELSE`](ELSE.md) branch.

`:ENDIF` closes the conditional structure started by [`:IF`](IF.md). It appears after the [`:IF`](IF.md) body or after an optional [`:ELSE`](ELSE.md) body, and execution then continues with the next statement after the conditional block. `:ENDIF` is only valid as the closer for a matching [`:IF`](IF.md) structure and must be written as the uppercase colon-prefixed keyword `:ENDIF;`.

## When to use

- When closing any [`:IF`](IF.md) block — `:ENDIF;` is required for both the simple `:IF ... :ENDIF` form and the `:IF ... :ELSE ... :ENDIF` form.

## Syntax

```ssl
:ENDIF;
```

## Keyword group

**Group:** Control Flow
**Role:** closer

## Best practices

!!! success "Do"
    - Always pair each [`:IF`](IF.md) with a matching `:ENDIF;`, including nested conditionals.
    - Keep the [`:IF`](IF.md), optional [`:ELSE`](ELSE.md), and `:ENDIF;` visibly aligned so the full block is easy to follow.

!!! failure "Don't"
    - Omit `:ENDIF;` and rely on indentation or spacing to imply the end of the block. SSL requires an explicit closing keyword.
    - Mis-case the keyword as `:endif` or `:EndIf`. Colon-prefixed SSL keywords are case-sensitive and must be uppercase.

## Examples

### Completing a simple conditional block

`:ENDIF;` closes the [`:IF`](IF.md) block so execution continues with the next statement. With `nTemp` set to `72`, the condition is false and `sMessage` keeps its initial value.

```ssl
:PROCEDURE CheckTemperature;
	:DECLARE nTemp, sMessage;

	nTemp := 72;
	sMessage := "Temperature is normal";

	:IF nTemp > 80;
		sMessage := "Temperature exceeds limit";
	:ENDIF;

	UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("CheckTemperature");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Temperature is normal
```

### Closing an IF...ELSE block

`:ENDIF;` is the same closing keyword whether the conditional has only a true branch or both branches. With `nScore` set to `85`, the condition is false and the [`:ELSE`](ELSE.md) branch runs.

```ssl
:PROCEDURE ClassifyResult;
	:PARAMETERS nScore;
	:DECLARE sResult;

	:IF nScore >= 90;
		sResult := "Pass";
	:ELSE;
		sResult := "Review";
	:ENDIF;

	UsrMes(sResult);

	:RETURN sResult;
:ENDPROC;

/* Usage;
DoProc("ClassifyResult", {85});
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Review
```

## Related

- [`IF`](IF.md)
- [`ELSE`](ELSE.md)
