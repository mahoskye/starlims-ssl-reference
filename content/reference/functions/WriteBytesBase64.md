---
title: "WriteBytesBase64"
summary: "Writes a base64-encoded value to disk as binary file content."
id: ssl.function.writebytesbase64
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# WriteBytesBase64

Writes a base64-encoded value to disk as binary file content.

`WriteBytesBase64` decodes the supplied base64 string and writes the resulting bytes to `sFileName`. The target file is created if it does not exist and overwritten if it already exists. On success, the function returns an empty string.

Use it when an integration, export process, or stored value provides file content as base64 and you need to reconstruct the original binary file.

## When to use

- When an external system sends file content as base64 and SSL must save it as a file.
- When restoring content that was previously captured with [`ReadBytesBase64`](ReadBytesBase64.md).
- When you need a single call that both decodes the base64 string and writes the file.

## Syntax

```ssl
WriteBytesBase64(sFileName, sBase64Data)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sFileName` | [string](../types/string.md) | yes | — | Path of the file to create or overwrite |
| `sBase64Data` | [string](../types/string.md) | yes | — | Base64 text to decode and write as file bytes |

## Returns

**[string](../types/string.md)** — Always returns an empty string when the write succeeds.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| The target path is outside the allowed whitelist. | `Access to folder/file <sFileName> is denied.\nIf system needs access to this folder/file please ask the System Administrator to add the item to WhitelistFolders setting in the configuration file.` |
| `sFileName` is [`NIL`](../literals/nil.md) or empty and the whitelist check does not fail first. | `File name cannot be missing.` |
| `sBase64Data` is not valid base64. The write does not start. | A .NET `FormatException` |
| The write operation raises a file-system error, such as a missing parent folder or insufficient write permissions. | File-system exceptions propagate from the write operation. |

## Best practices

!!! success "Do"
    - Pass a fully qualified file path that points to an approved writable location.
    - Ensure the parent folder already exists before calling the function.
    - Wrap the call in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the write is part of a larger workflow.

!!! failure "Don't"
    - Assume the function creates missing folders for you.
    - Treat the return value as a status message or saved path. A successful call returns `""`.
    - Pass unchecked external base64 data directly into a critical file path without validation.

## Caveats

- An empty `sBase64Data` value is valid base64 and writes a zero-byte file.

## Examples

### Save a base64 image to disk

This example writes a known base64 string to a file and reports success after the call completes.

```ssl
:PROCEDURE SaveLogoImage;
	:DECLARE sFileName, sBase64Data;

	sFileName := "C:\\STARLIMS\\Exports\\logo.png";
	sBase64Data :=
		"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8DwHwAFBQIAX8jx0gRAAAAABJRU5ErkJggg==";

	WriteBytesBase64(sFileName, sBase64Data);

	UsrMes("File written to " + sFileName);
:ENDPROC;
```

Call it with `DoProc("SaveLogoImage")`.

[`UsrMes`](UsrMes.md) displays:

```
File written to C:\STARLIMS\Exports\logo.png
```

### Write binary content and verify it round-trips

Write the file, then read it back with [`ReadBytesBase64`](ReadBytesBase64.md) to confirm the stored content matches the original payload. Both the verification and any file-system failure are handled inside a single [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md).

```ssl
:PROCEDURE SaveAndVerifyDocument;
	:DECLARE sFileName, sBase64Data, sSavedBase64, oErr;

	sFileName := "C:\\STARLIMS\\Exports\\payload.bin";
	sBase64Data := "AAECAwQ=";

	:TRY;
		WriteBytesBase64(sFileName, sBase64Data);

		sSavedBase64 := ReadBytesBase64(sFileName);

		:IF sSavedBase64 == sBase64Data;
			UsrMes("Document written and verified");
		:ELSE;
			ErrorMes("Document verification failed after write");
		:ENDIF;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("Failed to write file: " + oErr:Description);
		/* Displays on failure: write failed;
	:ENDTRY;
:ENDPROC;
```

Call it with `DoProc("SaveAndVerifyDocument")`.

## Related

- [`ReadBytesBase64`](ReadBytesBase64.md)
- [`string`](../types/string.md)
