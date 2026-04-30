---
title: "Trim"
summary: "Removes trailing whitespace from a string."
id: ssl.function.trim
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Trim

Removes trailing whitespace from a string.

`Trim` returns `sSource` with trailing whitespace removed. Leading content is left unchanged. If `sSource` is [`NIL`](../literals/nil.md), the function raises an error. If `sSource` is an empty string or becomes empty after trailing whitespace is removed, the result is an empty string.

Use `Trim` when only the right side of the string should change. Use [`LTrim`](LTrim.md) for left-side trimming, or [`AllTrim`](AllTrim.md) when you need to remove leading and trailing space characters.

## When to use

- When preparing user input for processing and you need to remove accidental spacing at the end without affecting the start of the input.
- When cleaning file or log lines that may have inconsistent trailing whitespace introduced by copy-paste or system behaviors.
- When comparing values or generating keys where trailing whitespace could create false mismatches.

## Syntax

```ssl
Trim(sSource)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSource` | [string](../types/string.md) | yes | — | String whose trailing whitespace is removed. |

## Returns

**[string](../types/string.md)** — `sSource` with trailing whitespace removed.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSource` is [`NIL`](../literals/nil.md). | `Argument sSource cannot be null.` |

## Best practices

!!! success "Do"
    - Use Trim before string comparison when trailing whitespace can vary.
    - Handle the [`NIL`](../literals/nil.md) case explicitly when input may be missing or optional.
    - Use [`AllTrim`](AllTrim.md) when both ends need cleanup, or [`LTrim`](LTrim.md) when only leading whitespace should be removed.
    - Use Trim when tabs, line breaks, or other trailing whitespace may be present at the end of imported text.

!!! failure "Don't"
    - Assume Trim removes leading whitespace. It only changes the end of the string.
    - Pass [`NIL`](../literals/nil.md) to Trim expecting an empty result. The function raises an error.
    - Use Trim when you want to remove ordinary spaces from both ends. [`AllTrim`](AllTrim.md) is the better match for that case.

## Caveats

- Trailing tabs, line breaks, and other whitespace characters are removed, not just spaces.

## Examples

### Clean up user entry before saving

Remove trailing spaces from a username before storage. The conditional check confirms that the value actually changed.

```ssl
:PROCEDURE CleanUsername;
	:DECLARE sUsername, sCleanUsername;

	sUsername := "johnsmith   ";
	sCleanUsername := Trim(sUsername);

	:IF sCleanUsername != sUsername;
		UsrMes("Username trimmed for storage: " + LimsString(Len(sCleanUsername)) + " chars");
	:ENDIF;

	:RETURN sCleanUsername;
:ENDPROC;

/* Usage;
DoProc("CleanUsername");
```

[`UsrMes`](UsrMes.md) displays:

```text
Username trimmed for storage: 9 chars
```

### Normalize log lines in a loop

Trim trailing whitespace from each element of an imported log array and collect the cleaned lines into a new array.

```ssl
:PROCEDURE NormalizeLogLines;
	:DECLARE aRawLogLines, aCleanLines, nIndex, sLine, nCount;

	aRawLogLines := {
		"2026-04-11 14:32:01  INFO     Processing request    ",
		"2026-04-11 14:32:02  DEBUG    Connection opened     ",
		"2026-04-11 14:32:03  WARN     Retry attempt 1       ",
		"2026-04-11 14:32:04  ERROR    Operation failed      "
	};

	aCleanLines := {};
	nCount := ALen(aRawLogLines);

	:FOR nIndex := 1 :TO nCount;
		sLine := Trim(aRawLogLines[nIndex]);

		AAdd(aCleanLines, sLine);
	:NEXT;

	UsrMes("Normalized " + LimsString(nCount) + " log lines");

	:RETURN aCleanLines;
:ENDPROC;

/* Usage;
DoProc("NormalizeLogLines");
```

[`UsrMes`](UsrMes.md) displays:

```text
Normalized 4 log lines
```

## Related

- [`AllTrim`](AllTrim.md)
- [`LTrim`](LTrim.md)
- [`string`](../types/string.md)
