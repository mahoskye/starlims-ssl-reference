---
title: "string"
summary: "Represents SSL text values, including string literals, comparisons, indexing, and JSON serialization."
id: ssl.type.string
element_type: type
doc_status: published
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

Strings are 1-based for indexing. `sValue[1]` returns the first character as a single-character string. [`Empty`](../functions/Empty.md) treats `""` and strings that become empty after trimming spaces, tabs, carriage returns, or line feeds as empty. [`ToJson`](../functions/ToJson.md)`(sValue)` returns the text as a quoted JSON string.

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

Strings have no SSL-defined `:` members. Calls such as `sValue:IsEmpty()`, `sValue:ToJson()`, `sValue:Index(1)` and `sValue:clone()` raise `Run-time error: Invalid method: …`, and `sValue:value` raises `Invalid property: value`. Work with strings through the operators above and the string functions instead:

| Task | Use |
|---|---|
| Test for blank or whitespace-only text | [`Empty`](../functions/Empty.md) |
| Count characters | [`Len`](../functions/Len.md) |
| Read one character | `sValue[nPos]` (see [Indexing](#indexing)) |
| Take part of the text | [`SubStr`](../functions/SubStr.md), [`Left`](../functions/Left.md), [`Right`](../functions/Right.md) |
| Find text | [`At`](../functions/At.md), or [`$`](../operators/dollar.md) for a yes/no check |
| Change case or trim | [`Upper`](../functions/Upper.md), [`Lower`](../functions/Lower.md), [`AllTrim`](../functions/AllTrim.md) |
| Replace text | [`Replace`](../functions/Replace.md) (case-insensitive), [`StrTran`](../functions/StrTran.md) (case-sensitive) |
| Serialize to JSON | [`ToJson`](../functions/ToJson.md) |
| Compare order | [`<`](../operators/less-than.md), [`>`](../operators/greater-than.md), or `sValue:CompareTo(sOther)`, a .NET member; see below |

## Calling .NET `String` methods

Public methods and properties of .NET's `System.String` can be called on a `string` value with the `:` method-call syntax, such as `sValue:Trim()` or `sValue:Length`. For example, `"abc":CompareTo("abd")` returns `-1`, and `sValue:Clone()` returns the same text. Member names are case-sensitive: `sValue:ToUpper()` and `sValue:Clone()` work, but `sValue:toupper()` and `sValue:clone()` raise `Invalid method: …`, and `sValue:length` raises `Invalid property: length` (see [Member names and case](../../guides/native-members.md#member-names-and-case)). Not every member form is reachable: `sValue:Split(",")` raises `Invalid method: Split`, so verify a member before relying on it. Static methods such as `String.Format` and `String.Join` are reachable through the same syntax; for a static call the receiver is only used to locate the type.

This passthrough is an interop convenience, not part of the SSL language surface. The members are not declared in SSL and do not appear in editor autocomplete. Prefer SSL-native string functions ([`Replace`](../functions/Replace.md), [`Upper`](../functions/Upper.md), [`Lower`](../functions/Lower.md), [`SubStr`](../functions/SubStr.md), and similar) for portability, and reserve direct .NET calls for behavior the SSL library does not cover. See [Native Members on SSL Values](../../guides/native-members.md) for the members verified on STARLIMS v11 and how to check others.

### Example: calling `String.Format` through a string value

Uses .NET's static `String.Format` to build a formatted message. The receiver `sName` only directs the runtime to `System.String`; the formatted output comes entirely from the arguments.

```ssl
:PROCEDURE BuildGreeting;
	:DECLARE sName, sMessage;

	sName := "Hello";
	sMessage := sName:Format("{0} world", sName);

	UsrMes(sMessage);

	:RETURN sMessage;
:ENDPROC;

/* Usage;
DoProc("BuildGreeting");
```

[`UsrMes`](../functions/UsrMes.md) logs:

```text
Hello world
```

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
    - Use [`Empty`](../functions/Empty.md) when a value may be blank or whitespace-only.
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

[`UsrMes`](../functions/UsrMes.md) logs:

```text
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

Normalizes whitespace-only input to a fallback string, then serializes the result with [`ToJson`](../functions/ToJson.md). [`Empty`](../functions/Empty.md) treats `"   "` as empty.

```ssl
:PROCEDURE BuildCommentPayload;
	:DECLARE sComment, sJson;

	sComment := "   ";

	:IF Empty(sComment);
		sComment := "No comment provided";
	:ENDIF;

	sJson := ToJson(sComment);

	UsrMes(sJson);

	:RETURN sJson;
:ENDPROC;

/* Usage;
DoProc("BuildCommentPayload");
```

[`UsrMes`](../functions/UsrMes.md) logs:

```text
"No comment provided"
```

## Caveats

- A `:` member call on a string reaches a .NET `String` member (e.g. `sValue:EndsWith("suffix")`). A member that doesn't exist, or doesn't accept the arguments given, raises an error such as `Run-time error: Invalid method: Split`. Check a member before relying on it; see [Native Members](../../guides/native-members.md).

## Related elements

- [`LimsString`](../functions/LimsString.md)
- [`Val`](../functions/Val.md)
- [`Empty`](../functions/Empty.md)
- [`array`](array.md)
- [`boolean`](boolean.md)
- [`object`](object.md)
- [`nil`](../literals/nil.md)
