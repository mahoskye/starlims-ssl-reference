---
title: "Replace"
summary: "Replaces all occurrences of a specified substring within a string with another substring and returns the resulting string."
id: ssl.function.replace
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Replace

Replaces all occurrences of a specified substring within a string with another substring and returns the resulting string.

Returns a new string in which every non-overlapping occurrence of `searchFor` inside `source` is replaced by `replaceWith`.

Matching is **case-insensitive**. A search for `"abc"` matches `"abc"`, `"ABC"`, `"aBc"`, and other case variants. If any argument (`source`, `searchFor`, or `replaceWith`) is [`NIL`](../literals/nil.md), an error is raised. If `searchFor` is empty, the function returns `source` unchanged.

## When to use

- When you need to replace all instances of a particular separator in a delimited string (such as changing commas to pipes).
- When standardizing input by replacing variant substrings, such as converting all hyphens to underscores in identifiers.
- When you need to normalize text without caring about the original casing of the matched substring.
- When you want a simpler alternative to manual loop-based replacement logic.

## Syntax

```ssl
Replace(source, searchFor, replaceWith)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `source` | [string](../types/string.md) | yes | — | Source string where the search will be performed. |
| `searchFor` | [string](../types/string.md) | yes | — | Substring to search for. |
| `replaceWith` | [string](../types/string.md) | yes | — | Substring to replace occurrences with. |

## Returns

**[string](../types/string.md)** — New string containing the result of the replacement operation.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `source` is [`NIL`](../literals/nil.md). | `Argument source cannot be null.` |
| `searchFor` is [`NIL`](../literals/nil.md). | `Argument searchFor cannot be null.` |
| `replaceWith` is [`NIL`](../literals/nil.md). | `Argument replaceWith cannot be null.` |

## Best practices

!!! success "Do"
    - Validate that `source`, `searchFor`, and `replaceWith` are not null before calling.
    - Use `Replace()` when you want every case variant of the same substring replaced.
    - Use [`StrTran()`](StrTran.md) instead when you need exact case-sensitive matching.
    - Use `Replace()` when you want all matches replaced, not just the first one.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for any argument. `Replace()` raises an error for [`NIL`](../literals/nil.md) inputs.
    - Use `Replace()` when letter case must be part of the match criteria.
    - Expect only the first occurrence to change. `Replace()` replaces all matches.
    - Expect an empty `searchFor` to insert text between characters. It returns the source unchanged.

## Caveats

- `replaceWith` is inserted exactly as provided; the original match casing is not preserved.

## Examples

### Replace spaces with underscores in a filename

Show how to make a filename safe for use in code by replacing all spaces with underscores.

```ssl
:PROCEDURE MakeFilenameSafe;
    :DECLARE sOriginalName, sSafeName;

    sOriginalName := "Sample Report Q1 2024";
    sSafeName := Replace(sOriginalName, " ", "_");

    UsrMes("Original: " + sOriginalName);
    UsrMes("Safe name: " + sSafeName);
:ENDPROC;

/* Usage;
DoProc("MakeFilenameSafe");
```

### Replace a token regardless of its casing

Show that `Replace()` matches the search text without regard to letter case.

```ssl
:PROCEDURE NormalizeStatusText;
    :DECLARE sStatusLine, sNormalized;

    sStatusLine := "Pending, PENDING, pending";
    sNormalized := Replace(sStatusLine, "pending", "Ready");

    UsrMes("Before: " + sStatusLine);
    UsrMes("After: " + sNormalized);
:ENDPROC;

/* Usage;
DoProc("NormalizeStatusText");
```

### Apply several replacements to a template

Build a final message by applying several case-insensitive replacements in sequence.

```ssl
:PROCEDURE BuildAlertMessage;
    :DECLARE sTemplate, sMessage;

    sTemplate := "sample {id} failed on {DATE}";

    sMessage := Replace(sTemplate, "{id}", "S-10025");
    sMessage := Replace(sMessage, "{date}", "2026-04-19");
    sMessage := Replace(sMessage, "failed", "requires review");

    UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("BuildAlertMessage");
```

[`UsrMes`](UsrMes.md) displays:

```text
sample S-10025 requires review on 2026-04-19
```

## Related

- [`At`](At.md)
- [`StrTran`](StrTran.md)
- [`string`](../types/string.md)
