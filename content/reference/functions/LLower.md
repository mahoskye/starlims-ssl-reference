---
title: "LLower"
summary: "Converts all characters in a string to their lowercase equivalents."
id: ssl.function.llower
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LLower

Converts all characters in a string to their lowercase equivalents.

`LLower` returns the input string converted to lowercase using the current culture. Use it when you need stable case normalization before exact comparisons, validation, or storage. If `sSource` is an empty string, the result is also empty. If `sSource` is [`NIL`](../literals/nil.md), the function raises an error.

## When to use

- When normalizing user input for case-insensitive comparison or storage.
- When you need consistent lowercase formatting for values such as usernames or codes.
- When preparing string data before exact comparisons with [`==`](../operators/strict-equals.md).
- When matching values that may arrive with inconsistent casing.

## Syntax

```ssl
LLower(sSource)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSource` | [string](../types/string.md) | yes | — | The string to convert to lowercase. |

## Returns

**[string](../types/string.md)** — The lowercase form of `sSource`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSource` is [`NIL`](../literals/nil.md). | `Argument sSource cannot be null.` |

## Best practices

!!! success "Do"
    - Normalize both values before an exact string comparison when case should not matter.
    - Combine `LLower` with [`AllTrim`](AllTrim.md) when input may contain extra spaces.
    - Use [`Lower`](Lower.md) and `LLower` interchangeably — both produce identical output.

!!! failure "Don't"
    - Assume `LLower` handles [`NIL`](../literals/nil.md) input silently. It raises an error instead.
    - Expect `LLower` to trim or remove whitespace. It changes case only.
    - Compare unnormalized mixed-case strings directly when the match should be case-insensitive.

## Caveats

- Case conversion depends on the current culture, so some characters can lowercase differently in different locales.

## Examples

### Compare a user-provided login to a stored username

Lowercase both values before comparing so that `"JSmith"` matches `"jsmith"` regardless of how the user typed the name.

```ssl
:PROCEDURE ValidateLogin;
	:DECLARE sUserInput, sStoredUsername, sInputLower, sStoredLower, bMatch;

	sUserInput := "JSmith";
	sStoredUsername := "jsmith";

	sInputLower := LLower(sUserInput);
	sStoredLower := LLower(sStoredUsername);

	bMatch := sInputLower == sStoredLower;

	UsrMes("Names match: " + LimsString(bMatch));

	:RETURN bMatch;
:ENDPROC;

/* Usage;
DoProc("ValidateLogin");
```

[`UsrMes`](UsrMes.md) displays:

```text
Names match: True
```

### Validate a status code regardless of input casing

Trim and lowercase the incoming status before checking it against a fixed list, so that `"Active"`, `"ACTIVE"`, and `"active"` all pass. Values not in the list are rejected by using the original unmodified input in the message.

```ssl
:PROCEDURE ValidateSampleStatus;
	:PARAMETERS sStatusCode;
	:DECLARE sNormalizedStatus, aValidStatuses, bIsValid;

	sNormalizedStatus := LLower(AllTrim(sStatusCode));
	aValidStatuses := {"active", "pending", "closed"};

	bIsValid := AScan(aValidStatuses, sNormalizedStatus) > 0;

	:IF bIsValid;
		UsrMes("Status accepted: " + sNormalizedStatus);
	:ELSE;
		UsrMes("Invalid status: " + sStatusCode);
	:ENDIF;

	:RETURN bIsValid;
:ENDPROC;

/* Usage;
DoProc("ValidateSampleStatus", {"Active"});
```

### Normalize a batch of codes to lowercase

Trim whitespace and lowercase all entries in an array in a single loop, producing `{"abc-01", "def-02", "ghi-03"}` from the raw input so it is ready for storage or comparison.

```ssl
:PROCEDURE NormalizeCodes;
	:DECLARE aRawCodes, aNormalizedCodes, nIndex;

	aRawCodes := {" AbC-01 ", "def-02", "GHI-03 "};
	aNormalizedCodes := {};

	:FOR nIndex := 1 :TO ALen(aRawCodes);
		AAdd(aNormalizedCodes, LLower(AllTrim(aRawCodes[nIndex])));
	:NEXT;

	:RETURN aNormalizedCodes;
:ENDPROC;

/* Usage;
DoProc("NormalizeCodes");
```

## Related

- [`AllTrim`](AllTrim.md)
- [`LTrim`](LTrim.md)
- [`Lower`](Lower.md)
- [`Trim`](Trim.md)
- [`Upper`](Upper.md)
- [`string`](../types/string.md)
