---
title: "Lower"
summary: "Converts all characters in a string to lowercase."
id: ssl.function.lower
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Lower

Converts all characters in a string to lowercase.

`Lower` returns the input string converted to lowercase by using the current culture. Use it when you want consistent lowercase normalization before comparison, validation, storage, or display. If `sSource` is an empty string, the result is also empty. If `sSource` is [`NIL`](../literals/nil.md), the function raises an error.

## When to use

- When normalizing user input before exact string comparison.
- When preparing values such as usernames, codes, or statuses for case-insensitive matching.
- When storing or displaying text in a consistent lowercase form.
- When combining case normalization with [`AllTrim`](AllTrim.md) or [`Trim`](Trim.md) for cleaner input handling.

## Syntax

```ssl
Lower(sSource)
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
    - Combine `Lower` with [`AllTrim`](AllTrim.md) when input may contain extra spaces.
    - Use `Lower` and [`LLower`](LLower.md) interchangeably only when you want the same behavior.

!!! failure "Don't"
    - Assume `Lower` handles [`NIL`](../literals/nil.md) input silently. It raises an error instead.
    - Expect `Lower` to trim or remove whitespace. It changes case only.
    - Compare mixed-case strings directly when the match should be case-insensitive.

## Caveats

- Case conversion depends on the current culture, so some characters can lowercase differently in different locales.

## Examples

### Normalize a value before exact comparison

Normalize two values before checking whether they match exactly.

```ssl
:PROCEDURE MatchUserName;
	:DECLARE sUserInput, sStoredValue, sInputLower, sStoredLower, bMatch;

	sUserInput := "JSmith";
	sStoredValue := "jsmith";

	sInputLower := Lower(sUserInput);
	sStoredLower := Lower(sStoredValue);

	bMatch := sInputLower == sStoredLower;

	UsrMes("Names match: " + LimsString(bMatch));

	:RETURN bMatch;
:ENDPROC;

/* Usage;
DoProc("MatchUserName");
```

[`UsrMes`](UsrMes.md) displays:

```text
Names match: .T.
```

### Combine trimming and lowercase normalization

Clean a user-entered status value before validating it against an allowed list.

```ssl
:PROCEDURE ValidateStatus;
	:PARAMETERS sStatusCode;
	:DECLARE sNormalizedStatus, aValidStatuses, bIsValid;

	sNormalizedStatus := Lower(AllTrim(sStatusCode));
	aValidStatuses := {"active", "pending", "closed"};

	bIsValid := AScan(aValidStatuses, sNormalizedStatus) > 0;

	:IF bIsValid;
		UsrMes("Status accepted: " + sNormalizedStatus);
		/* Displays accepted status;
	:ELSE;
		UsrMes("Invalid status: " + sStatusCode);
		/* Displays rejected status;
	:ENDIF;

	:RETURN bIsValid;
:ENDPROC;

/* Usage;
DoProc("ValidateStatus", {"Active"});
```

### Normalize a batch of incoming codes

Normalize multiple values before storing or comparing them later.

```ssl
:PROCEDURE NormalizeCodes;
	:DECLARE aRawCodes, aNormalizedCodes, nIndex;

	aRawCodes := {" AbC-01 ", "def-02", "GHI-03 "};
	aNormalizedCodes := {};

	:FOR nIndex := 1 :TO ALen(aRawCodes);
		AAdd(aNormalizedCodes, Lower(AllTrim(aRawCodes[nIndex])));
	:NEXT;

	:RETURN aNormalizedCodes;
:ENDPROC;

/* Usage;
DoProc("NormalizeCodes");
```

## Related

- [`AllTrim`](AllTrim.md)
- [`LCase`](LCase.md)
- [`LLower`](LLower.md)
- [`LTrim`](LTrim.md)
- [`Trim`](Trim.md)
- [`Upper`](Upper.md)
- [`string`](../types/string.md)
