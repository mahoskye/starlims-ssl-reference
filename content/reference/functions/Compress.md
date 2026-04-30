---
title: "Compress"
summary: "Compresses a non-empty string and returns the compressed result as either a base64 string or a generated file path."
id: ssl.function.compress
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Compress

Compresses a non-empty string and returns the compressed result as either a base64 string or a generated file path.

`Compress` accepts a non-empty string in `sSource`. When `bToFile` is omitted or is anything other than [`.T.`](../literals/true.md), it returns the compressed bytes as a base64-encoded string. When `bToFile` is [`.T.`](../literals/true.md), it writes the compressed bytes to a generated file in the application work `Temp` folder and returns the full path to that file. The input text is encoded as UTF-8 before compression. Use [`Decompress`](Decompress.md) to restore the original text.

## When to use

- When you need an in-memory compressed string for storage, transfer, or later
  round-trip decompression.
- When another step in the workflow needs a temporary compressed file instead of
  an in-memory value.
- When you want to reduce the size of repetitive text before passing it between
  SSL procedures or integrations.

## Syntax

```ssl
Compress(sSource, [bToFile])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSource` | [string](../types/string.md) | yes | — | Text to compress. Must be a non-empty string. |
| `bToFile` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | When [`.T.`](../literals/true.md), writes the compressed bytes to a generated file in the application work `Temp` folder and returns that file path. Any other value behaves like the default in-memory mode. |

## Returns

**[string](../types/string.md)** — A base64-encoded compressed string when `bToFile` is omitted or is not [`.T.`](../literals/true.md); the full path to the generated compressed file when `bToFile` is [`.T.`](../literals/true.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSource` is [`NIL`](../literals/nil.md). | `Argument 'sSource' cannot be null.` |
| `sSource` is empty or not a string value. | `Argument 'sSource' must be a non-empty string.` |

## Best practices

!!! success "Do"
    - Pass a real non-empty string in `sSource`.
    - Use the default in-memory result when you want to store or transmit compressed text without creating a file.
    - Pass the returned value to [`Decompress`](Decompress.md) to restore the original text. For file output, use `Decompress(sPath, .T.)`.

!!! failure "Don't"
    - Pass an empty string or a non-string value as `sSource`.
    - Assume the return value is a file path unless you called `Compress(sSource, .T.)`.
    - Treat the returned value as ready-to-read plain text. It is compressed output and must be decompressed before use.

## Caveats

- File output is created under the application work `Temp` folder with a generated name.
- The generated file name uses a `.zip` extension even though the content is produced by GZip compression.
- This function documents only the explicit argument-validation errors shown above. Other runtime failures, such as file-write problems when `bToFile` is [`.T.`](../literals/true.md), depend on the environment.

## Examples

### Compress text in memory

Compresses a multi-line report string and displays both the original and compressed lengths to show the size reduction.

```ssl
:PROCEDURE CompressReportText;
    :DECLARE sReport, sCompressed;
    :DECLARE nOriginalLen, nCompressedLen;

    sReport := "Batch 24018" + Chr(13) + Chr(10);
    sReport := sReport + "Status=Released" + Chr(13) + Chr(10);
    sReport := sReport + "Reviewer=jsmith" + Chr(13) + Chr(10);
    sReport := sReport + "Comment=Ready for archive";

    nOriginalLen := Len(sReport);

    sCompressed := Compress(sReport);
    nCompressedLen := Len(sCompressed);

    UsrMes("Original length: " + LimsString(nOriginalLen));
    UsrMes("Compressed length: " + LimsString(nCompressedLen));

    :RETURN sCompressed;
:ENDPROC;

/* Usage;
DoProc("CompressReportText");
```

[`UsrMes`](UsrMes.md) displays:

```
Original length: 72
Compressed length: [value less than 72]
```

### Write compressed output to a temporary file

Passes `bToFile := .T.` to write compressed bytes to a generated temp file, then decompresses it to verify the round-trip is lossless.

```ssl
:PROCEDURE CreateCompressedPayloadFile;
    :DECLARE sPayload, sZipPath, sRestored;

    sPayload := "Order=4711" + Chr(13) + Chr(10);
    sPayload := sPayload + "Sample=S-000245" + Chr(13) + Chr(10);
    sPayload := sPayload + "Status=Logged" + Chr(13) + Chr(10);
    sPayload := sPayload + "Reviewer=jsmith";

    sZipPath := Compress(sPayload, .T.);

    sRestored := Decompress(sZipPath, .T.);

    :IF sRestored == sPayload;
        UsrMes("Compressed file created: " + sZipPath);
    :ELSE;
        ErrorMes("Compressed file verification failed");
    :ENDIF;

    :RETURN sZipPath;
:ENDPROC;

/* Usage;
DoProc("CreateCompressedPayloadFile");
```

[`UsrMes`](UsrMes.md) displays:

```
Compressed file created: [Temp path].zip
```

### Batch process payloads and verify mixed output modes

Selects in-memory or file output per payload based on length, then verifies each result by decompressing and comparing back to the original.

```ssl
:PROCEDURE PrepareCompressedExports;
    :DECLARE aPayloads, aResults;
    :DECLARE sPayload, sCompressed, sMode, sRestored;
    :DECLARE oResult;
    :DECLARE nIndex;

    aPayloads := {
        "Short payload for API transfer",
        "Long payload " + Replicate("ABC123", 40),
        "Audit payload " + Replicate("ZX", 80)
    };

    aResults := {};

    :FOR nIndex := 1 :TO ALen(aPayloads);
        sPayload := aPayloads[nIndex];

        :IF Len(sPayload) > 100;
            sCompressed := Compress(sPayload, .T.);
            sMode := "FILE";
        :ELSE;
            sCompressed := Compress(sPayload);
            sMode := "MEMORY";
        :ENDIF;

        :IF sMode == "FILE";
            sRestored := Decompress(sCompressed, .T.);
        :ELSE;
            sRestored := Decompress(sCompressed);
        :ENDIF;

        oResult := CreateUdObject();
        oResult:mode := sMode;
        oResult:value := sCompressed;
        oResult:matchesSource := sRestored == sPayload;

        AAdd(aResults, oResult);

        UsrMes("Payload " + LimsString(nIndex)
	            + " stored as " + sMode);
    :NEXT;

    :RETURN aResults;
:ENDPROC;

/* Usage;
DoProc("PrepareCompressedExports");
```

[`UsrMes`](UsrMes.md) displays one line per payload:

```
Payload 1 stored as MEMORY
Payload 2 stored as FILE
Payload 3 stored as FILE
```

## Related

- [`Decompress`](Decompress.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
