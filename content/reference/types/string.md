---
title: "string"
summary: "Represents SSL text values, including string literals, comparisons, indexing, and JSON serialization."
id: ssl.type.string
element_type: type
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# string

## What it is

Represents SSL text values, including string literals, comparisons, indexing,
and JSON serialization.

The `string` type stores text exactly as text. You can create string values with double-quoted, single-quoted, or bracketed literals such as `"text"`, `'text'`, and `[text]`.

Strings support concatenation with [`+`](../operators/plus.md), trimmed concatenation with [`-`](../operators/minus.md), containment checks with [`$`](../operators/dollar.md), exact equality with [`==`](../operators/strict-equals.md), and prefix-style equality with [`=`](../operators/equals.md). For strings, `sLeft = sRight` returns [`.T.`](../literals/true.md) when the right operand is empty, exactly equal to the left operand, or a prefix of the left operand.

Strings are 1-based for indexing. `sValue[1]` returns the first character as a single-character string. [`Empty`](../functions/Empty.md) treats null string values, `""`, and strings that become empty after trimming spaces, tabs, carriage returns, or line feeds as empty. [`ToJson()`](../functions/ToJson.md) returns JSON string text for non-null values and `null` for null strings.

## Creating values

String values are created with any of three literal forms.

```ssl
sDouble := "text value";
sSingle := 'text value';
sBracketed := [text value];
```

| Attribute | Value |
|---|---|
| Runtime type | `STRING` |
| Literal syntax | `"text"`, `'text'`, `[text]` |
| Empty value | `""` |

## Operators

| Operator | Symbol | Returns | Behavior |
|---|---|---|---|
| [`plus`](../operators/plus.md) | [`+`](../operators/plus.md) | `string` | Concatenates two string values. |
| [`minus`](../operators/minus.md) | [`-`](../operators/minus.md) | `string` | Trims trailing spaces from the left operand, then concatenates the right operand. |
| [`dollar`](../operators/dollar.md) | [`$`](../operators/dollar.md) | [`boolean`](boolean.md) | Returns [`.T.`](../literals/true.md) when the left string is found anywhere inside the right string. |
| [`equals`](../operators/equals.md) | [`=`](../operators/equals.md) | [`boolean`](boolean.md) | Returns [`.T.`](../literals/true.md) when the right string is empty, exactly equal to the left string, or a prefix of the left string. |
| [`strict-equals`](../operators/strict-equals.md) | [`==`](../operators/strict-equals.md) | [`boolean`](boolean.md) | Returns [`.T.`](../literals/true.md) only when both strings are exactly equal. |
| [`less-than`](../operators/less-than.md) | [`<`](../operators/less-than.md) | [`boolean`](boolean.md) | Lexicographic comparison against another string. |
| [`greater-than`](../operators/greater-than.md) | [`>`](../operators/greater-than.md) | [`boolean`](boolean.md) | Lexicographic comparison against another string. |
| [`less-than-or-equal`](../operators/less-than-or-equal.md) | [`<=`](../operators/less-than-or-equal.md) | [`boolean`](boolean.md) | Lexicographic less-than-or-equal comparison against another string. |
| [`greater-than-or-equal`](../operators/greater-than-or-equal.md) | [`>=`](../operators/greater-than-or-equal.md) | [`boolean`](boolean.md) | Lexicographic greater-than-or-equal comparison against another string. |

## Members

| Member | Kind | Parameters | Returns | Description |
|---|---|---|---|---|
| `value` | Property | — | `string` | Returns the stored text value. |
| `clone()` | Method | none | `string` | Returns a copy of the string. |
| `IsEmpty()` | Method | none | [`boolean`](boolean.md) | Returns [`.T.`](../literals/true.md) when the value is null, empty, or only whitespace made of spaces, tabs, carriage returns, or line feeds. |
| [`ToJson()`](../functions/ToJson.md) | Method | none | `string` | Returns JSON string text, or `null` when the string value is null. |
| `CompareTo(sOther)` | Method | `sOther` (`string`) | [`number`](number.md) | Returns a negative number, `0`, or a positive number based on lexical ordering. |
| `Index(nPos)` | Method | `nPos` ([`number`](number.md)) | `string` | Returns the character at the specified 1-based position. In SSL code this is normally used through `sValue[nPos]`. |

## Indexing

| Attribute | Value |
|---|---|
| Supported | `true` |
| Base | `1` |
| Read behavior | Returns a single-character string at the specified 1-based position |
| Assignment | Not supported |

Index expressions must resolve to an integer value. Values below `1` or above the string length raise a runtime error.

## Notes for daily SSL work

!!! success "Do"
    - Use [`==`](../operators/strict-equals.md) when you need exact string equality.
    - Use [`=`](../operators/equals.md) only when you intentionally want prefix behavior.
    - Use `IsEmpty()` when a value may be blank or whitespace-only.
    - Remember that `sValue[1]` is the first character, not `sValue[0]`.

!!! failure "Don't"
    - Assume only double quotes are valid string literals. SSL also accepts single-quoted and bracketed string literals.
    - Use [`=`](../operators/equals.md) when you mean exact equality. It can return [`.T.`](../literals/true.md) for prefixes such as `"LOGGED" = "LOG"`.
    - Assume [`$`](../operators/dollar.md) reads left-to-right like many other contains APIs. In SSL, the left operand is the text being searched for inside the right operand.
    - Treat strings like arrays you can modify in place by index. String index assignment is not supported.

## Examples

### Reading a character by 1-based position

Reads the first character of `"STARLIMS"` using 1-based indexing. `sWord[1]` returns `"S"`.

```ssl
:PROCEDURE GetFirstLetter;
	:DECLARE sWord, sFirstLetter;

	sWord := "STARLIMS";
	sFirstLetter := sWord[1];

	UsrMes("First letter: " + sFirstLetter);

	:RETURN sFirstLetter;
:ENDPROC;

/* Usage;
DoProc("GetFirstLetter");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
First letter: S
```

### Prefix match versus exact match

Shows that [`=`](../operators/equals.md) returns [`.T.`](../literals/true.md) for a prefix (`"LOG"` is a prefix of `"LOGGED"`) while [`==`](../operators/strict-equals.md) requires the full string.

```ssl
:PROCEDURE CompareStatuses;
	:DECLARE sValue, sPrefix, sExact;

	sValue := "LOGGED";
	sPrefix := "LOG";
	sExact := "LOGGED";

	:IF sValue = sPrefix;
		UsrMes("Prefix match succeeded");
	:ENDIF;

	:IF sValue == sPrefix;
		UsrMes("This line does not run");
	:ELSE;
		UsrMes("Exact match failed for LOG");
	:ENDIF;

	:IF sValue == sExact;
		UsrMes("Exact match succeeded for LOGGED");
	:ENDIF;

	:RETURN;
:ENDPROC;

/* Usage;
DoProc("CompareStatuses");
```

### Checking blank input and serializing to JSON

Normalizes whitespace-only input to a fallback string, then serializes the result as JSON. `IsEmpty()` treats `"   "` as empty.

```ssl
:PROCEDURE BuildCommentPayload;
	:DECLARE sComment, sJson;

	sComment := "   ";

	:IF sComment:IsEmpty();
		sComment := "No comment provided";
	:ENDIF;

	sJson := sComment:ToJson();

	UsrMes(sJson);

	:RETURN sJson;
:ENDPROC;

/* Usage;
DoProc("BuildCommentPayload");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
"No comment provided"
```

## Related elements

- [`LimsString`](../functions/LimsString.md)
- [`Val`](../functions/Val.md)
- [`Empty`](../functions/Empty.md)
- [`array`](array.md)
- [`boolean`](boolean.md)
- [`object`](object.md)
- [`nil`](../literals/nil.md)
