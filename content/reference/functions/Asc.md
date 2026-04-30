---
title: "Asc"
summary: "Return the character code of the first character in a string."
id: ssl.function.asc
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Asc

Return the character code of the first character in a string.

Asc returns the numeric code for the first character of `sSource`. Characters after the first one are ignored.

Pass a non-empty string. If `sSource` is [`NIL`](../literals/nil.md), Asc raises an error, and an empty string does not provide a first character to evaluate.

Use Asc when you need numeric character comparisons or when working with code values that pair naturally with [`Chr`](Chr.md).

## When to use

- When you need the numeric code for a single character.
- When parsing input based on character ranges such as digits or letters.
- When converting between characters and numeric codes with [`Chr`](Chr.md).

## Syntax

```ssl
Asc(sSource)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSource` | [string](../types/string.md) | yes | — | Source string whose first character is evaluated. Pass a non-empty string. |

## Returns

**[number](../types/number.md)** — Numeric code of the first character in `sSource`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSource` is [`NIL`](../literals/nil.md). | `Argument sSource cannot be null.` |

## Best practices

!!! success "Do"
    - Pass a string that is known to contain at least one character.
    - Use Asc for single-character checks such as digit or letter tests.
    - Pair Asc with [`Chr`](Chr.md) when converting between codes and characters.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md). Asc raises an error for a null argument.
    - Pass an empty string. Asc requires a first character to read.
    - Expect Asc to evaluate the whole string. It only uses the first character.
    - Use Asc when direct string comparison is clearer than code-based logic.

## Examples

### Check whether a character is uppercase

Reads the code for `"M"` and tests whether it falls in the uppercase ASCII range (65–90).

```ssl
:PROCEDURE ValidateUppercaseLetter;
	:DECLARE sUserInput, nCode;

	sUserInput := "M";
	nCode := Asc(sUserInput);

	:IF nCode >= 65 .AND. nCode <= 90;
		UsrMes("Uppercase letter detected.");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("ValidateUppercaseLetter");
```

[`UsrMes`](UsrMes.md) displays:

```text
Uppercase letter detected.
```

### Convert each character in a string to its code

Iterates each character in `"ABC"` with [`SubStr`](SubStr.md), calls `Asc` on each one-character slice, and joins the codes into a comma-separated string.

```ssl
:PROCEDURE ConvertForExternalExport;
	:DECLARE sInput, nIndex, sOutput;

	sInput := "ABC";
	sOutput := "";

	:FOR nIndex := 1 :TO Len(sInput);
		:IF nIndex > 1;
			sOutput := sOutput + ",";
		:ENDIF;
		sOutput := sOutput + LimsString(Asc(SubStr(sInput, nIndex, 1)));
	:NEXT;

	UsrMes(sOutput);
:ENDPROC;

/* Usage;
DoProc("ConvertForExternalExport");
```

[`UsrMes`](UsrMes.md) displays:

```text
65,66,67
```

## Related

- [`Chr`](Chr.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
