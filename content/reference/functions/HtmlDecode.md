---
title: "HtmlDecode"
summary: "Converts selected HTML/XML entity sequences in a string back to literal characters."
id: ssl.function.htmldecode
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# HtmlDecode

Converts selected HTML/XML entity sequences in a string back to literal characters.

`HtmlDecode` accepts one string argument. When `sData` is [`NIL`](../literals/nil.md), the function returns [`NIL`](../literals/nil.md). Otherwise it replaces the following sequences and leaves all other text unchanged.

| Entity sequence | Decoded character |
| --- | --- |
| `&lt;` | [`<`](../operators/less-than.md) |
| `&gt;` | [`>`](../operators/greater-than.md) |
| `&apos;` | `'` |
| `&quot;` | `"` |
| `&amp;` | [`&`](../operators/and.md) |

Use this function when you need to reverse output produced by [`HtmlEncode`](HtmlEncode.md) or to make encoded text readable in a plain-text context.

## When to use

- When a value was previously passed through [`HtmlEncode`](HtmlEncode.md) and now needs to be shown as normal text.
- When external data contains encoded markup characters such as `&lt;` or `&amp;` and your script needs the literal characters.
- When you want readable text for logging, comparison, or plain-text display instead of entity sequences.

## Syntax

```ssl
HtmlDecode(sData)
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `sData` | [string](../types/string.md) | yes | — | String to decode. [`NIL`](../literals/nil.md) is accepted and returns [`NIL`](../literals/nil.md). |

## Returns

**[string](../types/string.md)** - The decoded string with supported entity sequences replaced by their literal characters. Returns [`NIL`](../literals/nil.md) when `sData` is [`NIL`](../literals/nil.md).

## Best practices

!!! success "Do"
    - Use `HtmlDecode` when you need to reverse text that was previously encoded with [`HtmlEncode`](HtmlEncode.md).
    - Check for [`NIL`](../literals/nil.md) when your calling code distinguishes between no value and an empty string.
    - Treat the decoded result as plain text unless you have separately validated it for HTML rendering.

!!! failure "Don't"
    - Assume `HtmlDecode` sanitizes content. It only converts supported entity sequences back to literal characters.
    - Assume it decodes every named HTML entity. The implementation only replaces `&lt;`, `&gt;`, `&apos;`, `&quot;`, and `&amp;`.
    - Inject decoded untrusted content into an HTML-rendering context without separate validation or sanitization.

## Caveats

- An empty string returns an empty string.

## Examples

### Decode text for plain display

Convert encoded comparison text into a readable message.

```ssl
:PROCEDURE ShowDecodedMessage;
    :DECLARE sEncodedText, sDecodedText;

    sEncodedText := "Formula requires x &lt; 100 &amp; y &gt; 0";
    sDecodedText := HtmlDecode(sEncodedText);

    UsrMes(sDecodedText);

    :RETURN sDecodedText;
:ENDPROC;

/* Usage;
DoProc("ShowDecodedMessage");
```

[`UsrMes`](UsrMes.md) displays:

```text
Formula requires x < 100 & y > 0
```

### Decode a list of encoded values

Process multiple encoded strings, showing that only the five supported entity sequences are decoded. The third entry uses `&plusmn;`, which is not a supported entity, so it is returned unchanged and [`UsrMes`](UsrMes.md) displays `Value &plusmn; limit`.

```ssl
:PROCEDURE DecodeMessages;
	:DECLARE aEncoded, aDecoded, sMessage;
	:DECLARE nIndex;

	aEncoded := {
		"Sample &lt;A&gt;",
		"Tom &amp; Jerry",
		"Value &plusmn; limit"
	};
	aDecoded := {};

	:FOR nIndex := 1 :TO ALen(aEncoded);
		sMessage := HtmlDecode(aEncoded[nIndex]);
		AAdd(aDecoded, sMessage);
	:NEXT;

	UsrMes(aDecoded[1]);
	UsrMes(aDecoded[2]);
	UsrMes(aDecoded[3]);

	:RETURN aDecoded;
:ENDPROC;

/* Usage;
DoProc("DecodeMessages");
```

[`UsrMes`](UsrMes.md) displays:

```text
Sample <A>
Tom & Jerry
Value &plusmn; limit
```

## Related

- [`HtmlEncode`](HtmlEncode.md)
- [`string`](../types/string.md)
