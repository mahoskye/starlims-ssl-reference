---
title: "HtmlEncode"
summary: "Converts selected characters in a string to entity sequences for HTML or XML text output."
id: ssl.function.htmlencode
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# HtmlEncode

Converts selected characters in a string to entity sequences for HTML or XML text output.

`HtmlEncode` accepts one string argument. When `sData` is [`NIL`](../literals/nil.md), the function returns [`NIL`](../literals/nil.md). Otherwise it replaces the following characters and leaves all other text unchanged.

| Character | Entity sequence |
|---|---|
| [`&`](../operators/and.md) | `&amp;` |
| [`<`](../operators/less-than.md) | `&lt;` |
| [`>`](../operators/greater-than.md) | `&gt;` |
| `'` | `&apos;` |
| `"` | `&quot;` |

Use this function when text must be inserted into HTML or XML content as literal text instead of markup. Use [`HtmlDecode`](HtmlDecode.md) to reverse these specific replacements.

## When to use

- When inserting text into generated HTML or XML content and the text may contain [`<`](../operators/less-than.md), [`>`](../operators/greater-than.md), [`&`](../operators/and.md), quotes, or apostrophes.
- When building markup strings from data that should be treated as text rather than interpreted as tags or attributes.
- When you need the exact entity replacements supported by `HtmlEncode` before passing the result to another system.

## Syntax

```ssl
HtmlEncode(sData)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sData` | [string](../types/string.md) | yes | — | String to encode. [`NIL`](../literals/nil.md) is accepted and returns [`NIL`](../literals/nil.md). |

## Returns

**[string](../types/string.md)** — The encoded string with [`&`](../operators/and.md), [`<`](../operators/less-than.md), [`>`](../operators/greater-than.md), `'`, and `"` replaced by their entity sequences. Returns [`NIL`](../literals/nil.md) when `sData` is [`NIL`](../literals/nil.md).

## Best practices

!!! success "Do"
    - Encode text at the point where you insert it into HTML or XML output.
    - Keep the original unencoded value when that same data may also be needed for plain text, storage, or later editing.
    - Use [`HtmlDecode`](HtmlDecode.md) only when you specifically need to undo the five replacements performed by `HtmlEncode`.

!!! failure "Don't"
    - Encode the same value multiple times unless you intentionally want sequences like `&amp;amp;`.
    - Assume `HtmlEncode` performs general input validation or business rule checks. It only replaces five characters.
    - Assume it converts every named HTML entity or every non-ASCII character. Characters outside the five supported replacements are left as-is.

## Caveats

- An empty string returns an empty string.
- Already encoded text is encoded again. For example, `&amp;` becomes `&amp;amp;`.

## Examples

### Encode a string before inserting it into HTML

Encode user-supplied text before placing it inside a markup string, so that special characters become safe entity sequences rather than markup.

```ssl
:PROCEDURE BuildCommentMarkup;
	:DECLARE sComment, sEncodedComment, sHtml;

	sComment := "Meeting at 3pm <review> & 'coffee'";
	sEncodedComment := HtmlEncode(sComment);
	sHtml := "<p>" + sEncodedComment + "</p>";

	UsrMes(sHtml);

	:RETURN sHtml;
:ENDPROC;

/* Usage;
DoProc("BuildCommentMarkup");
```

[`UsrMes`](UsrMes.md) displays:

```
<p>Meeting at 3pm &lt;review&gt; &amp; &apos;coffee&apos;</p>
```

### Encode attribute values when building an XML element

Encode each attribute value inline while composing an XML element string, so that quotes and special characters inside values do not break the markup structure.

```ssl
:PROCEDURE BuildSampleXml;
	:DECLARE sSampleId, sStatus, sXml;

	sSampleId := "A&B<42>";
	sStatus := 'Ready "now"';
	sXml := "<sample id='" + HtmlEncode(sSampleId) + "' status='"
			+ HtmlEncode(sStatus) + "'></sample>";

	UsrMes(sXml);

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("BuildSampleXml");
```

[`UsrMes`](UsrMes.md) displays:

```
<sample id='A&amp;B&lt;42&gt;' status='Ready &quot;now&quot;'></sample>
```

### Encode a batch of values including NIL entries

Encode an array containing a mix of strings and a [`NIL`](../literals/nil.md) entry, showing that `HtmlEncode` passes [`NIL`](../literals/nil.md) through unchanged while encoding all other values. After the loop, `aEncodedNotes[1]` holds `&lt;alpha&gt;`, entry 2 remains [`NIL`](../literals/nil.md), `aEncodedNotes[3]` holds `Tom &amp; Jerry`, and `aEncodedNotes[4]` holds `She said &quot;go&quot;`. The [`UsrMes`](UsrMes.md) call confirms that the [`NIL`](../literals/nil.md) entry was preserved.

```ssl
:PROCEDURE EncodeNotes;
	:DECLARE aNotes, aEncodedNotes;
	:DECLARE nIndex, vEncoded;

	aNotes := {"<alpha>", NIL, "Tom & Jerry", 'She said "go"'};
	aEncodedNotes := {};

	:FOR nIndex := 1 :TO ALen(aNotes);
		vEncoded := HtmlEncode(aNotes[nIndex]);
		AAdd(aEncodedNotes, vEncoded);
	:NEXT;

	UsrMes(LimsString(Empty(aEncodedNotes[2])));

	:RETURN aEncodedNotes;
:ENDPROC;

/* Usage;
DoProc("EncodeNotes");
```

[`UsrMes`](UsrMes.md) displays:

```
true
```

## Related

- [`HtmlDecode`](HtmlDecode.md)
- [`string`](../types/string.md)
