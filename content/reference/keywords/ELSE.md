---
title: "ELSE"
summary: "Directs control to an alternate set of statements when the preceding IF condition is false."
id: ssl.keyword.else
element_type: keyword
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ELSE

Directs control to an alternate set of statements when the preceding IF condition is false.

`ELSE` is the optional alternate branch of an [`:IF`](IF.md) ... [`:ENDIF`](ENDIF.md) block. When the [`:IF`](IF.md) condition evaluates to false, execution continues in the `:ELSE` branch. When the [`:IF`](IF.md) condition evaluates to true, the `:ELSE` branch is skipped.

`:ELSE` does not take parameters or an expression. It is only valid between the statements for [`:IF`](IF.md) and the closing [`:ENDIF`](ENDIF.md), so it cannot be used as a standalone statement or repeated within the same conditional block.

## Behavior

Use `:ELSE;` after the true branch statements of an [`:IF`](IF.md) block and before [`:ENDIF;`](ENDIF.md). The `:ELSE` branch is optional, but when present it defines the statements that run only when the [`:IF`](IF.md) condition is false.

## When to use

- When you need the program to perform one operation if a condition is true, and a different operation if it is false.
- When you want to ensure there is always a fall-back action if the main condition is not met.

## Syntax

```ssl
:ELSE;
```

Within a full conditional block:

```ssl
:IF bCondition;
    /* Statements for the true branch;
:ELSE;
    /* Statements for the false branch;
:ENDIF;
```

## Keyword group

**Group:** Control Flow
**Role:** separator

## Best practices

!!! success "Do"
    - Use `:ELSE` to clearly define mutually exclusive logic paths.
    - Always keep `:ELSE` branches as minimal as necessary.

!!! failure "Don't"
    - Nest [`:IF`](IF.md) blocks in the `:ELSE` section when simple two-way branching is sufficient. Clarity is improved and branching logic stays concise.
    - Place unrelated logic within `:ELSE` just to re-use the block. Each branch should address one logical alternative for easier understanding and maintenance.

## Caveats

- Keywords in SSL are case-sensitive and must be written in uppercase.

## Examples

### Handling alternate workflow when validation fails

`:ELSE` executes when the [`:IF`](IF.md) condition is not met. With `sStatus` set to `"REJECTED"`, the condition is false and the `:ELSE` branch runs.

```ssl
:PROCEDURE ValidateSampleStatus;
	:DECLARE sStatus, sResult;

	sStatus := "REJECTED";

	:IF sStatus == "APPROVED";
		sResult := "Sample passed validation";
	:ELSE;
		sResult := "Sample failed validation and requires review";
	:ENDIF;

	UsrMes(sResult);

	:RETURN sResult;
:ENDPROC;

/* Usage;
DoProc("ValidateSampleStatus");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Sample failed validation and requires review
```

### Ensuring default values when data is missing

Use `:ELSE` to apply a fallback value when a lookup yields no result. If [`LSearch`](../functions/LSearch.md) returns empty for the given ID, `sStatus` is set to `sDefaultStatus` instead.

```ssl
:PROCEDURE GetSampleStatus;
	:PARAMETERS sSampleID;
	:DECLARE sStatus, sDefaultStatus, sResult;

	sDefaultStatus := "PENDING";

	sResult := LSearch("
	    SELECT status
	    FROM samples
	    WHERE sample_id = ?
	", "",, {sSampleID});

	:IF !Empty(sResult);
		sStatus := sResult;
	:ELSE;
		sStatus := sDefaultStatus;
	:ENDIF;

	:RETURN sStatus;
:ENDPROC;

/* Usage;
DoProc("GetSampleStatus", {"S-001"});
```

## Related

- [`IF`](IF.md)
- [`ENDIF`](ENDIF.md)
