---
title: "AllTrim"
summary: "Remove leading and trailing space characters from a string."
id: ssl.function.alltrim
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# AllTrim

Remove leading and trailing space characters from a string.

AllTrim returns `sSource` with leading and trailing space characters removed. It trims ordinary space characters at the beginning and end of the string and leaves embedded spaces unchanged. It requires a non-[`NIL`](../literals/nil.md) string argument and raises an error when `sSource` is [`NIL`](../literals/nil.md).

Use AllTrim when unwanted padding spaces need to be removed but the text inside the string should stay unchanged.

## When to use

- When user input may include leading or trailing spaces.
- When imported codes or identifiers need to be normalized before comparison.
- When you want to clean up a value before storing or displaying it.

## Syntax

```ssl
AllTrim(sSource)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSource` | [string](../types/string.md) | yes | — | String whose leading and trailing space characters are removed. |

## Returns

**[string](../types/string.md)** — `sSource` with leading and trailing space characters removed.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSource` is [`NIL`](../literals/nil.md). | `Argument sSource cannot be null.` |

## Best practices

!!! success "Do"
    - Use AllTrim before string comparisons when surrounding spaces are not meaningful.
    - Apply AllTrim to imported IDs, codes, and keys before storing them.
    - Combine AllTrim with case normalization when matching user input.

!!! failure "Don't"
    - Expect AllTrim to handle [`NIL`](../literals/nil.md) by returning an empty string. It raises an error.
    - Expect embedded spaces to be removed. AllTrim only affects the beginning and end of the string.
    - Use AllTrim when you need to remove tabs, line breaks, or other non-space padding characters.
    - Rely on downstream code to clean stray spaces if the value matters for matching or lookup.

## Examples

### Trim a single padded value

Removes leading and trailing spaces from an input string and shows the cleaned result in brackets to confirm both sides were trimmed.

```ssl
:PROCEDURE CleanSearchInput;
    :DECLARE sRawInput, sCleanInput;

	sRawInput := "   copper sample   ";
	sCleanInput := AllTrim(sRawInput);

	UsrMes("[" + sCleanInput + "]");
:ENDPROC;

/* Usage;
DoProc("CleanSearchInput");
```

[`UsrMes`](UsrMes.md) displays:

```text
[copper sample]
```

### Clean imported codes before use

Trims each element in an array of imported codes, removing stray padding spaces while leaving embedded content untouched.

```ssl
:PROCEDURE NormalizeCodes;
	:DECLARE aCodes, aCleanCodes, nIndex;

	aCodes := {"LAB-001 ", " LAB-002", "LAB-003"};
	aCleanCodes := {};

	:FOR nIndex := 1 :TO ALen(aCodes);
		AAdd(aCleanCodes, AllTrim(aCodes[nIndex]));
	:NEXT;

	UsrMes(aCleanCodes[1]);  /* Displays: LAB-001;
	UsrMes(aCleanCodes[2]);  /* Displays: LAB-002;
:ENDPROC;

/* Usage;
DoProc("NormalizeCodes");
```

### Trim before comparison

Calls `AllTrim` inline inside the [`:IF`](../keywords/IF.md) condition so that surrounding spaces in the input do not prevent a match.

```ssl
:PROCEDURE MatchDepartment;
	:DECLARE sInput;

	sInput := "  Chemistry  ";

	:IF AllTrim(sInput) == "Chemistry";
		UsrMes("Department matched.");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("MatchDepartment");
```

[`UsrMes`](UsrMes.md) displays:

```text
Department matched.
```

## Related

- [`LTrim`](LTrim.md)
- [`Trim`](Trim.md)
- [`Upper`](Upper.md)
- [`Lower`](Lower.md)
- [`string`](../types/string.md)
