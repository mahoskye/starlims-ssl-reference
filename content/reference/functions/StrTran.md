---
title: "StrTran"
summary: "Replaces all occurrences of a specified substring with another substring in a source string."
id: ssl.function.strtran
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# StrTran

Replaces all occurrences of a specified substring with another substring in a source string.

Returns a new string in which every non-overlapping occurrence of `searchFor` inside `source` is replaced with `replaceWith`.

Matching is case-sensitive. If `replaceWith` is omitted or [`NIL`](../literals/nil.md), `StrTran()` uses an empty string, so matching text is removed. If `searchFor` is not found in `source`, the original string is returned unchanged. If `source` or `searchFor` is [`NIL`](../literals/nil.md), the function raises an error.

## When to use

- When you need to replace every exact-case occurrence of a fixed substring.
- When you want to remove a known character or token by replacing it with `""`.
- When letter case matters and [`Replace`](Replace.md) would be too broad.

## Syntax

```ssl
StrTran(source, searchFor, replaceWith)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `source` | [string](../types/string.md) | yes | — | Source string where the search is performed. |
| `searchFor` | [string](../types/string.md) | yes | — | Literal substring to find. |
| `replaceWith` | [string](../types/string.md) | no | `""` | Replacement text. If omitted, `StrTran()` uses an empty string. |

## Returns

**[string](../types/string.md)** — New string containing the replacement result.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `source` is [`NIL`](../literals/nil.md). | `Argument source cannot be null.` |
| `searchFor` is [`NIL`](../literals/nil.md). | `Argument searchFor cannot be null.` |

## Best practices

!!! success "Do"
    - Validate that `source` and `searchFor` are not [`NIL`](../literals/nil.md) before calling.
    - Use `StrTran()` when you need exact case-sensitive matching.
    - Pass `""` when you want to remove all occurrences of the search substring.
    - Use [`Replace`](Replace.md) instead when you want case-insensitive matching.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `source` or `searchFor`; `StrTran()` raises an error.
    - Use `StrTran()` when you expect case-insensitive matching.
    - Use it for pattern or wildcard replacement; it only matches literal substrings.

## Caveats

- Replacements are non-overlapping. Each match is processed once in the original left-to-right scan.
- The raw source does not define a special `searchFor = ""` behavior. Avoid empty search strings.

## Examples

### Remove all dashes from a phone number

Demonstrate how to remove a repeated formatting character from a string.

```ssl
:PROCEDURE CleanPhoneNumber;
	:DECLARE sPhoneWithDashes, sPhoneClean;

	sPhoneWithDashes := "555-123-4567";
	sPhoneClean := StrTran(sPhoneWithDashes, "-", "");

	UsrMes("Original: " + sPhoneWithDashes);
	UsrMes("Cleaned: " + sPhoneClean);

	:RETURN sPhoneClean;
:ENDPROC;

/* Usage;
DoProc("CleanPhoneNumber");
```

### Replace a status code token without changing other casing

Demonstrate that `StrTran()` only replaces exact-case matches. `"OPEN"` is left alone because the match is case-sensitive; `"Open"` inside `"Opened"` is replaced as well because the search finds every occurrence.

```ssl
:PROCEDURE NormalizeStatusLine;
	:DECLARE sStatusLine, sNormalized;

	sStatusLine := "Open OPEN Opened";
	sNormalized := StrTran(sStatusLine, "Open", "Closed");

	UsrMes("Before: " + sStatusLine);
	UsrMes("After: " + sNormalized);
:ENDPROC;

/* Usage;
DoProc("NormalizeStatusLine");
```

### Apply several exact replacements to a template

Build a final message by applying several literal, case-sensitive substitutions.

```ssl
:PROCEDURE BuildSampleMessage;
	:DECLARE sTemplate, sMessage;

	sTemplate := "Sample {id} moved to {status} by {user}";

	sMessage := StrTran(sTemplate, "{id}", "S-1025");
	sMessage := StrTran(sMessage, "{status}", "Released");
	sMessage := StrTran(sMessage, "{user}", MYUSERNAME);

	UsrMes(sMessage); /* Displays the final message with the current user name;
:ENDPROC;

/* Usage;
DoProc("BuildSampleMessage");
```

## Related

- [`At`](At.md)
- [`Replace`](Replace.md)
- [`string`](../types/string.md)
