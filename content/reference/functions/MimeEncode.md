---
title: "MimeEncode"
summary: "Encodes a string so it can be round-tripped later with MimeDecode."
id: ssl.function.mimeencode
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# MimeEncode

Encodes a string so it can be round-tripped later with [`MimeDecode`](MimeDecode.md).

`MimeEncode` accepts a single string argument and returns an encoded string.
The paired [`MimeDecode`](MimeDecode.md) function can restore the original text. If the value is [`NIL`](../literals/nil.md) or is not a string, the function raises an error.

## When to use

- When you need to store or transmit text in the encoded form expected by [`MimeDecode`](MimeDecode.md).
- When you want to preserve text exactly for later round-trip decoding in SSL.
- When you are working with product features that already exchange text through this encode/decode pair.

## Syntax

```ssl
MimeEncode(sValue)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sValue` | [string](../types/string.md) | yes | — | String to encode. |

## Returns

**[string](../types/string.md)** — Encoded string value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sValue` is [`NIL`](../literals/nil.md) or not a string. | `The argument for MimeEncode must be a string. Current value: <value>` |

## Best practices

!!! success "Do"
    - Pass only string values to `MimeEncode`.
    - Keep `MimeEncode` and [`MimeDecode`](MimeDecode.md) paired when you need round-trip behavior.
    - Store the encoded result as a string field or value, not as a structured object.

!!! failure "Don't"
    - Pass numbers, arrays, objects, or [`NIL`](../literals/nil.md); the function raises an error for non-string input.
    - Treat the output as interchangeable with arbitrary externally encoded content; this function is intended to pair with [`MimeDecode`](MimeDecode.md).
    - Encode text unless you actually need this function's encoded form for a downstream consumer or later decode step.

## Caveats

- Encoded output can only be decoded with [`MimeDecode`](MimeDecode.md); the format is not compatible with general-purpose base64 or MIME libraries.

## Examples

### Encode a string for later decoding

Encode a plain string and keep the encoded value for later use.

```ssl
:PROCEDURE EncodeNote;
	:DECLARE sNote, sEncodedNote;

	sNote := "Review complete for batch 24A";
	sEncodedNote := MimeEncode(sNote);

	UsrMes("Encoded note: " + sEncodedNote);
:ENDPROC;

/* Usage;
DoProc("EncodeNote");
```

[`UsrMes`](UsrMes.md) displays:

```text
Encoded note: <MIME-encoded string>
```

### Round-trip a value through encode and decode

Round-trip a message through `MimeEncode` and [`MimeDecode`](MimeDecode.md).

```ssl
:PROCEDURE EncodeAndDecodeComment;
	:DECLARE sComment, sEncodedComment, sDecodedComment;

	sComment := "Sample comment with special text: Batch A / shift 2";
	sEncodedComment := MimeEncode(sComment);
	sDecodedComment := MimeDecode(sEncodedComment);

	UsrMes("Original: " + sComment);
	/* Displays: original round-tripped text;
	UsrMes("Decoded: " + sDecodedComment);
	/* Displays: decoded round-tripped text;
:ENDPROC;

/* Usage;
DoProc("EncodeAndDecodeComment");
```

### Encode a batch of strings into a payload

Encode several strings before placing them into an outbound payload.

```ssl
:PROCEDURE BuildEncodedPayload;
	:DECLARE aMessages, aEncodedMessages, nIndex, sPayload;

	aMessages := {
		"Order 1001 approved",
		"Order 1002 pending review",
		"Order 1003 complete"
	};
	aEncodedMessages := {};

	:FOR nIndex := 1 :TO ALen(aMessages);
		AAdd(aEncodedMessages, MimeEncode(aMessages[nIndex]));
	:NEXT;

	sPayload := aEncodedMessages[1] + "|"
	+ aEncodedMessages[2] + "|"
	+ aEncodedMessages[3];

	UsrMes("Payload ready: " + sPayload);

	:RETURN sPayload;
:ENDPROC;

/* Usage;
DoProc("BuildEncodedPayload");
```

[`UsrMes`](UsrMes.md) displays:

```text
Payload ready: <three MIME-encoded strings joined by |>
```

## Related

- [`MimeDecode`](MimeDecode.md)
- [`string`](../types/string.md)
