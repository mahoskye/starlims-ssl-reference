---
title: "MimeDecode"
summary: "Decodes MIME-encoded data to its plain string representation."
id: ssl.function.mimedecode
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# MimeDecode

Decodes MIME-encoded data to its plain string representation.

`MimeDecode` decodes strings produced by the matching [`MimeEncode`](MimeEncode.md) function. The decoder only acts on strings that begin with the proprietary signature [`MimeEncode`](MimeEncode.md) emits; generic base64 or quoted-printable content from external sources is **not** recognized and is returned unchanged. If the input is a valid wrapped string, the original plain text is returned. If [`NIL`](../literals/nil.md) or a value of the wrong type is passed, it raises an error indicating that a string is required. When an empty string is provided, it returns an empty string without error. Use this function strictly for round-tripping data that was previously encoded with [`MimeEncode`](MimeEncode.md) in this same SSL environment; for arbitrary base64 or quoted-printable input, use a dedicated codec.

## When to use

- When decoding strings that were previously encoded with [`MimeEncode`](MimeEncode.md) in the same SSL environment.
- When reading SSL data from database fields or external payloads where [`MimeEncode`](MimeEncode.md) was used for storage or transmission.

## Syntax

```ssl
MimeDecode(sValue)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sValue` | [string](../types/string.md) | yes | — | The MIME-encoded string to decode. Must be a non-null string; passing any other type raises an exception. |

## Returns

**[string](../types/string.md)** — The decoded string when `sValue` begins with the SSL MIME signature. Returns `sValue` unchanged when it does not start with the signature. Returns `""` when `sValue` is an empty string.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sValue` is [`NIL`](../literals/nil.md) or not a string. | `The argument for MimeDecode must be a string. Current value: <value>` |

## Best practices

!!! success "Do"
    - Validate that the input value is a string before calling the function.
    - Use [`MimeEncode`](MimeEncode.md) to produce values that `MimeDecode` can decode; do not pass arbitrary base64 or externally encoded strings.
    - Wrap calls in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) when `sValue` may arrive from an uncontrolled source.

!!! failure "Don't"
    - Pass data structures, numbers, or [`NIL`](../literals/nil.md) as input. Only string values are accepted; other types raise an exception.
    - Assume that a non-empty return value means the string was decoded. If `sValue` was not encoded with [`MimeEncode`](MimeEncode.md), it is returned unchanged without error.

## Caveats

- Strings that do not begin with the SSL MIME signature are returned unchanged without raising an error. There is no indication in the return value whether decoding occurred.
- The encoding format is proprietary to STARLIMS and is not compatible with general-purpose base64 or MIME libraries.

## Examples

### Decode a previously encoded value

Encode a string with [`MimeEncode`](MimeEncode.md), then recover the original text with `MimeDecode`.

```ssl
:PROCEDURE DecodeEncodedText;
    :DECLARE sOriginal, sEncoded, sDecoded;

    sOriginal := "Q1 Summary: Sales up 12%; Margin stable";
    sEncoded := MimeEncode(sOriginal);
    sDecoded := MimeDecode(sEncoded);

    UsrMes("Decoded: " + sDecoded);
:ENDPROC;

/* Usage;
DoProc("DecodeEncodedText");
```

[`UsrMes`](UsrMes.md) displays:

```
Decoded: Q1 Summary: Sales up 12%; Margin stable
```

### Decode a batch of encoded values with error handling

Process an array of MIME-encoded strings, accumulate failures, and return a summary object.

```ssl
:PROCEDURE ProcessMimeBatch;
    :DECLARE sMimeInput, sDecoded, sErrorMsg, oBatchResult;
    :DECLARE aBatch, aErrors;
    :DECLARE nIndex, nProcessed, nFailed;

    nProcessed := 0;
    nFailed := 0;
    aErrors := {};
    aBatch := {};
    AAdd(aBatch, MimeEncode("Sample record 1"));
    AAdd(aBatch, MimeEncode("Sample record 2"));
    AAdd(aBatch, MimeEncode("Sample record 3"));

    :FOR nIndex := 1 :TO ALen(aBatch);
        sMimeInput := aBatch[nIndex];
        :TRY;
            sDecoded := MimeDecode(sMimeInput);
            nProcessed := nProcessed + 1;
        :CATCH;
            nFailed := nFailed + 1;
            sErrorMsg := "Record " + LimsString(nIndex) + " failed: " + GetLastSSLError():Description;
            AAdd(aErrors, sErrorMsg);
        :ENDTRY;
    :NEXT;

    oBatchResult := CreateUdObject();
    oBatchResult:Processed := nProcessed;
    oBatchResult:Failed := nFailed;
    oBatchResult:Errors := aErrors;

    :IF ALen(aErrors) > 0;
        UsrMes("Batch completed with " + LimsString(nFailed) + " error(s)"); /* Displays failure summary;
    :ELSE;
        UsrMes("Batch completed: " + LimsString(nProcessed) + " records decoded"); /* Displays success summary;
    :ENDIF;

    :RETURN oBatchResult;
:ENDPROC;

/* Usage;
DoProc("ProcessMimeBatch");
```

## Related

- [`MimeEncode`](MimeEncode.md)
- [`string`](../types/string.md)
