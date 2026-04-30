---
title: "SSLRegex"
summary: "Matches SSL strings against a stored regular expression pattern."
id: ssl.class.sslregex
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SSLRegex

Matches SSL strings against a stored regular expression pattern.

`SSLRegex` lets you create a reusable pattern and test whether an input string contains a match. You can create it with the default case-sensitive behavior, or pass a second argument to ignore case.

`IsMatch` searches the input string and returns [`.T.`](../literals/true.md) when the pattern matches any portion of the text. If you pass a starting position, SSL uses a 1-based character index. Values above the string length start at the end of the string and return [`.F.`](../literals/false.md) unless the pattern can match there.

## When to use

- When you need to validate a value such as a sample ID, batch number, or code.
- When simple string functions are not enough for the matching rule.
- When you want to reuse the same pattern against multiple input values.

## Constructors

### `SSLRegex{sPattern}`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sPattern` | [string](../types/string.md) | yes | Regular expression pattern to store |

### `SSLRegex{sPattern, bCaseSensitive}`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sPattern` | [string](../types/string.md) | yes | Regular expression pattern to store |
| `bCaseSensitive` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) for case-sensitive matching, [`.F.`](../literals/false.md) for case-insensitive matching |

**Raises:**
- `Argument sPattern cannot be null.`
- An invalid regular expression pattern raises a runtime error when the object is created.

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `CaseSensitive` | [boolean](../types/boolean.md) | read-only | Reports the value exposed by the class for case sensitivity |

`CaseSensitive` returns [`.F.`](../literals/false.md) for the one-argument constructor and for `SSLRegex{pattern, .F.}`. It also returns [`.F.`](../literals/false.md) when you explicitly pass [`.T.`](../literals/true.md), so do not rely on this property to confirm whether matching is case-sensitive.

## Methods

| Name | Returns | Description |
|------|---------|-------------|
| `IsMatch` | [boolean](../types/boolean.md) | Returns whether the stored pattern matches the input string |

### `IsMatch`

Tests the stored pattern against an input string.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sInput` | [string](../types/string.md) | yes | String to search |
| `nStartAt` | [number](../types/number.md) | no | 1-based character position where matching begins |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) if the pattern matches; otherwise [`.F.`](../literals/false.md).

**Raises:**
- `Argument sInput cannot be null.`
- `Argument nStartAt must refer to a location within the string.`

If `nStartAt` contains a fractional value, SSL rounds it to the nearest whole number away from zero before matching. Values less than or equal to `0` raise the `nStartAt` error. Values greater than the input length are accepted and start matching at the end of the string.

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Reuse one `SSLRegex` instance when you need the same pattern for multiple values.
    - Pass [`.F.`](../literals/false.md) explicitly when matching should ignore letter case.
    - Use a 1-based `nStartAt` only when you intentionally want to skip earlier characters.

!!! failure "Don't"
    - Pass an empty or invalid pattern unless you want the regex engine's behavior exactly as written. Invalid patterns fail at object creation.
    - Rely on the default constructor when case-insensitive matching is required. Use `SSLRegex{sPattern, .F.}` so the behavior is explicit.
    - Pass `0` or a negative `nStartAt`. Those values raise a runtime error instead of returning [`.F.`](../literals/false.md).

## Caveats

- Passing `nStartAt` beyond the end of the string does not raise an error; matching starts at the end of the input.

## Examples

### Validate a sample identifier

Creates a case-sensitive regex for the format `LAB-` followed by exactly five digits, then tests a sample ID and reports whether it matches.

```ssl
:PROCEDURE ValidateSampleIdFormat;
	:DECLARE oRegex, sSampleID, bIsValid;

	sSampleID := "LAB-12345";
	oRegex := SSLRegex{"^LAB-[0-9]{5}$"};

	bIsValid := oRegex:IsMatch(sSampleID);

	:IF bIsValid;
		UsrMes("Sample ID format is valid");
	:ELSE;
		UsrMes("Sample ID format is not valid");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("ValidateSampleIdFormat");
```

### Ignore case when checking a result code

Constructs a case-insensitive regex for `pass` by passing [`.F.`](../literals/false.md) as the second argument, then confirms the pattern matches mixed-case text.

```ssl
:PROCEDURE FindPassingResultText;
	:DECLARE oRegex, sResultText, bMatched;

	sResultText := "Final status: PaSs";
	oRegex := SSLRegex{"pass", .F.};

	bMatched := oRegex:IsMatch(sResultText);

	:IF bMatched;
		UsrMes("A passing result was found in the text");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("FindPassingResultText");
```

`UsrMes` displays:

```text
A passing result was found in the text
```

### Start matching from a specific position

Passes a 1-based `nStartAt` position to skip the `Prefix Batch:` header and match only the batch number portion of the string.

```ssl
:PROCEDURE MatchBatchNumberAfterPrefix;
	:DECLARE oRegex, sText, bMatched;

	sText := "Prefix Batch:AB-1042";
	oRegex := SSLRegex{"AB-[0-9]{4}$"};

	bMatched := oRegex:IsMatch(sText, 14);

	:IF bMatched;
		UsrMes("The batch number has the expected format");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("MatchBatchNumberAfterPrefix");
```

`UsrMes` displays:

```text
The batch number has the expected format
```

## Related

- [`boolean`](../types/boolean.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
- [`object`](../types/object.md)
