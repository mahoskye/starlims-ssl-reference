---
title: "LFromHex"
summary: "Converts a hexadecimal string to a string by reading the input in two-character chunks and decoding each chunk as a byte."
id: ssl.function.lfromhex
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LFromHex

Converts a hexadecimal string to a string by reading the input in two-character chunks and decoding each chunk as a byte.

`LFromHex` returns an empty string for empty input. If the input length is odd, the final character is still decoded as a single hexadecimal digit. If the argument is [`NIL`](../literals/nil.md), the function raises an error.

## When to use

- When a value is stored or transmitted as hexadecimal text and you need the
  decoded string.
- When you are round-tripping values with [`LToHex`](LToHex.md).
- When you want to validate external input with [`IsHex`](IsHex.md) before decoding it.

## Syntax

```ssl
LFromHex(sSource)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSource` | [string](../types/string.md) | yes | — | Hexadecimal text to decode |

## Returns

**[string](../types/string.md)** — The decoded string.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSource` is [`NIL`](../literals/nil.md). | `Argument sSource cannot be null.` |

## Best practices

!!! success "Do"
    - Validate external input with [`IsHex`](IsHex.md) before calling `LFromHex`.
    - Use [`LToHex`](LToHex.md) and `LFromHex` together when you need a simple round-trip conversion.
    - Treat [`NIL`](../literals/nil.md) as an error case and handle it before decoding.

!!! failure "Don't"
    - Assume external input is valid hexadecimal text. Invalid content can fail during decoding.
    - Pass [`NIL`](../literals/nil.md) to `LFromHex`. The function raises an exception for [`NIL`](../literals/nil.md) input.
    - Use `LFromHex` when you need a numeric conversion. Use [`LHex2Dec`](LHex2Dec.md) for hexadecimal-to-decimal conversion.

## Examples

### Decode a simple hex string

Call `LFromHex` with a known-valid hex string to recover the original text. The input `"48656C6C6F"` decodes byte-by-byte to `"Hello"`.

```ssl
:PROCEDURE DecodeHexMessage;
	:DECLARE sHexInput, sDecodedText;

	sHexInput := "48656C6C6F";
	sDecodedText := LFromHex(sHexInput);

	UsrMes("Decoded text: " + sDecodedText);
:ENDPROC;

/* Usage;
DoProc("DecodeHexMessage");
```

[`UsrMes`](UsrMes.md) displays:

```
Decoded text: Hello
```

### Validate incoming values before decoding

Use [`IsHex`](IsHex.md) to filter a batch before calling `LFromHex`, so only well-formed hex strings are decoded. Three of the four inputs are valid (`"XYZ123"` is rejected), yielding 3 decoded values and 1 skipped.

```ssl
:PROCEDURE DecodeHexBatch;
	:DECLARE aInput, aDecoded, aInvalid, sHex, sDecoded, sMessage, nIndex;

	aInput := {"48656C6C6F", "4D61686F", "XYZ123", "414243"};
	aDecoded := {};
	aInvalid := {};

	:FOR nIndex := 1 :TO ALen(aInput);
		sHex := aInput[nIndex];

		:IF IsHex(sHex);
			sDecoded := LFromHex(sHex);
			AAdd(aDecoded, sDecoded);
		:ELSE;
			AAdd(aInvalid, sHex);
		:ENDIF;
	:NEXT;

	sMessage := "Decoded values: " + LimsString(ALen(aDecoded));
	UsrMes(sMessage);
	/* Displays decoded count;

	:IF ALen(aInvalid) > 0;
		UsrMes("Skipped invalid hex values: " + LimsString(ALen(aInvalid)));
		/* Displays skipped invalid count;
	:ENDIF;

	:RETURN aDecoded;
:ENDPROC;

/* Usage;
DoProc("DecodeHexBatch");
```

### Round-trip text through hex encoding and decoding

Encode with [`LToHex`](LToHex.md) and immediately decode with `LFromHex` to confirm the full round-trip restores the original value. Because `"Batch-1042"` encodes and decodes correctly, the success branch fires.

```ssl
:PROCEDURE VerifyHexRoundTrip;
	:DECLARE sOriginalText, sHexValue, sDecodedText;

	sOriginalText := "Batch-1042";
	sHexValue := LToHex(sOriginalText);
	sDecodedText := LFromHex(sHexValue);

	:IF sDecodedText == sOriginalText;
		UsrMes("Round-trip decode succeeded");
	:ELSE;
		ErrorMes("Round-trip decode failed");
	:ENDIF;

	:RETURN sDecodedText == sOriginalText;
:ENDPROC;

/* Usage;
DoProc("VerifyHexRoundTrip");
```

## Related

- [`IsHex`](IsHex.md)
- [`LHex2Dec`](LHex2Dec.md)
- [`LToHex`](LToHex.md)
- [`string`](../types/string.md)
