---
title: "Decompress"
summary: "Decompresses compressed text and returns the restored string."
id: ssl.function.decompress
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Decompress

Decompresses compressed text and returns the restored string.

`Decompress` accepts a non-empty string in `sSource`. When `bFromFile` is omitted or is anything other than [`.T.`](../literals/true.md), `sSource` is treated as an in-memory base64 string containing GZip-compressed bytes. When `bFromFile` is [`.T.`](../literals/true.md), `sSource` is treated as a file path and the function reads the compressed bytes from that file. In both cases, the decompressed bytes are decoded as UTF-8 and returned as a string. Use [`Compress`](Compress.md) to produce compatible input values.

## When to use

- When another step gives you a compressed in-memory string and you need the original text back.
- When you previously called `Compress(sSource, .T.)` and need to restore the text from the generated file path.
- When you need to round-trip text through compression for storage, transfer, or temporary file handling.

## Syntax

```ssl
Decompress(sSource, [bFromFile])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSource` | [string](../types/string.md) | yes | — | Base64-encoded GZip-compressed content, or a file path when `bFromFile` is [`.T.`](../literals/true.md). Must be a non-empty string. |
| `bFromFile` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | When [`.T.`](../literals/true.md), reads compressed bytes from the file path in `sSource`. Any other value behaves like the default in-memory mode. |

## Returns

**[string](../types/string.md)** — The decompressed UTF-8 text.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSource` is [`NIL`](../literals/nil.md). | `Argument 'sSource' cannot be null.` |
| `sSource` is empty or not a string value. | `Argument 'sSource' must be a non-empty string.` |

## Best practices

!!! success "Do"
    - Pass a real non-empty string in `sSource`.
    - Use `Decompress(sValue)` for in-memory values returned by `Compress(sText)`.
    - Use `Decompress(sPath, .T.)` only when `sSource` is a file path to compressed output.

!!! failure "Don't"
    - Pass an empty string or a non-string value as `sSource`.
    - Set `bFromFile` to [`.T.`](../literals/true.md) when `sSource` contains in-memory compressed data.
    - Assume the input is plain text. `Decompress` expects compressed content and will fail if the input is not valid for this function.

## Caveats

- Only the explicit `sSource` validation errors above are guaranteed by the public contract.
- Other runtime failures depend on the supplied content and environment, such as unreadable file paths, invalid base64 input, or compressed data that cannot be decompressed.

## Examples

### Restore text from an in-memory compressed value

Compresses a string to memory with [`Compress`](Compress.md), then restores the original text with `Decompress` and displays the result.

```ssl
:PROCEDURE RestoreCompressedText;
    :DECLARE sOriginal, sCompressed, sRestored;

    sOriginal := "Batch 24018|Status=Released|Reviewer=jsmith";
    sCompressed := Compress(sOriginal);

    sRestored := Decompress(sCompressed);

    UsrMes("Restored text: " + sRestored);

    :RETURN sRestored;
:ENDPROC;

/* Usage;
DoProc("RestoreCompressedText");
```

[`UsrMes`](UsrMes.md) displays:

```text
Restored text: Batch 24018|Status=Released|Reviewer=jsmith
```

### Read compressed content from a generated file path

Compresses a multi-line string to a temporary file using [`Compress`](Compress.md), then reads and restores it with `Decompress(sCompressedPath, .T.)`, verifying the round-trip result.

```ssl
:PROCEDURE RestoreCompressedFile;
    :DECLARE sPayload, sCompressedPath, sRestored;

    sPayload := "Order=4711" + Chr(13) + Chr(10);
    sPayload := sPayload + "Sample=S-000245" + Chr(13) + Chr(10);
    sPayload := sPayload + "Status=Logged" + Chr(13) + Chr(10);
    sPayload := sPayload + "Reviewer=jsmith";

    sCompressedPath := Compress(sPayload, .T.);

    sRestored := Decompress(sCompressedPath, .T.);

    :IF sRestored == sPayload;
        UsrMes("Restored file payload from: " + sCompressedPath);
        /* Displays restored file path on success;
    :ELSE;
        ErrorMes("Restored file content did not match the original text");
    :ENDIF;

    :RETURN sRestored;
:ENDPROC;

/* Usage;
DoProc("RestoreCompressedFile");
```

### Restore a mixed batch of in-memory and file-based values

Iterates over a mixed batch of compressed payloads, some stored in memory and some as file paths, and restores each using the appropriate `Decompress` call.

```ssl
:PROCEDURE RestoreMixedCompressedBatch;
    :DECLARE aInputs, aFromFile, aRestored;
    :DECLARE sPayload, sInput, sRestored;
    :DECLARE nIndex;

    aInputs := {};
    aFromFile := {};
    aRestored := {};

    sPayload := "Short payload for API transfer";
    AAdd(aInputs, Compress(sPayload));
    AAdd(aFromFile, .F.);

    sPayload := "Long payload " + Replicate("ABC123", 40);
    AAdd(aInputs, Compress(sPayload, .T.));
    AAdd(aFromFile, .T.);

    sPayload := "Audit payload " + Replicate("ZX", 80);
    AAdd(aInputs, Compress(sPayload));
    AAdd(aFromFile, .F.);

    :FOR nIndex := 1 :TO ALen(aInputs);
        sInput := aInputs[nIndex];

        :IF aFromFile[nIndex];
            sRestored := Decompress(sInput, .T.);
        :ELSE;
            sRestored := Decompress(sInput);
        :ENDIF;

        AAdd(aRestored, sRestored);
        UsrMes("Restored payload " + LimsString(nIndex));
        /* Displays each restored payload number;
    :NEXT;

    :RETURN aRestored;
:ENDPROC;

/* Usage;
DoProc("RestoreMixedCompressedBatch");
```

## Related

- [`Compress`](Compress.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
