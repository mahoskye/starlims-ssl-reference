---
title: "LTrim"
summary: "Removes leading whitespace from a string."
id: ssl.function.ltrim
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LTrim

Removes leading whitespace from a string.

`LTrim` removes leading whitespace characters and leaves the rest of the string unchanged. Trailing whitespace is preserved. If `sSource` is an empty string or contains only whitespace, the function returns an empty string. Passing [`NIL`](../literals/nil.md) raises an error.

Use `LTrim` when you need left-side trimming only. Use [`AllTrim`](AllTrim.md) when both ends should be trimmed, or [`Trim`](Trim.md) when only trailing whitespace should be removed.

## When to use

- When imported or typed values may contain accidental leading spaces.
- When left padding should be removed without changing trailing spaces.
- When whitespace-only input should be treated as empty by later checks.

## Syntax

```ssl
LTrim(sSource)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSource` | [string](../types/string.md) | yes | — | String to trim from the left side. |

## Returns

**[string](../types/string.md)** — `sSource` with all leading whitespace removed. Returns an empty string when `sSource` is `""` or contains only whitespace. Trailing whitespace is preserved.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSource` is [`NIL`](../literals/nil.md). | `Argument sSource cannot be null.` |

## Best practices

!!! success "Do"
    - Use `LTrim` when only the left side of the string should change.
    - Check the result with [`Empty`](Empty.md) after trimming when the input may be blank or whitespace-only.
    - Use [`AllTrim`](AllTrim.md) instead when you need to remove padding from both ends.

!!! failure "Don't"
    - Use `LTrim` when trailing whitespace also matters — it only trims the start of the string.
    - Assume whitespace-only input will produce a non-empty string safe to concatenate without checking first.
    - Pass [`NIL`](../literals/nil.md) expecting a silent empty result — the function raises an error.

## Caveats

- Tabs, line breaks, and other leading whitespace characters are trimmed along with spaces.

## Examples

### Remove leading spaces from a sample code

Trim accidental leading spaces from a code value before display. The brackets in the output confirm that no leading spaces remain and that trailing content is unchanged.

```ssl
:PROCEDURE NormalizeSampleCode;
	:DECLARE sRawCode, sCleanCode;

	sRawCode := "   QC-1042";
	sCleanCode := LTrim(sRawCode);

	UsrMes("[" + sCleanCode + "]");
:ENDPROC;

/* Usage;
DoProc("NormalizeSampleCode");
```

[`UsrMes`](UsrMes.md) displays:

```text
[QC-1042]
```

### Filter blank rows from an imported list after trimming

Trim leading spaces from each entry in the raw list, then skip any entry that becomes empty after trimming. The result contains only `{"S-1001", "S-1002", "S-1003"}` — the whitespace-only entry is excluded.

```ssl
:PROCEDURE CollectSampleIds;
	:DECLARE aRawIds, aSampleIds, nIndex, sSampleId;

	aRawIds := {"   S-1001", "      ", " S-1002", "S-1003"};
	aSampleIds := {};

	:FOR nIndex := 1 :TO ALen(aRawIds);
		sSampleId := LTrim(aRawIds[nIndex]);

		:IF Empty(sSampleId);
			:LOOP;
		:ENDIF;

		AAdd(aSampleIds, sSampleId);
	:NEXT;

	:RETURN aSampleIds;
:ENDPROC;

/* Usage;
DoProc("CollectSampleIds");
```

## Related

- [`AllTrim`](AllTrim.md)
- [`LLower`](LLower.md)
- [`Lower`](Lower.md)
- [`Trim`](Trim.md)
- [`Upper`](Upper.md)
- [`string`](../types/string.md)
