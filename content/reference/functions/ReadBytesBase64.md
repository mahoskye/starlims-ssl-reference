---
title: "ReadBytesBase64"
summary: "Reads a file from disk and returns its contents as a base64-encoded string."
id: ssl.function.readbytesbase64
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ReadBytesBase64

Reads a file from disk and returns its contents as a base64-encoded string.

`ReadBytesBase64` takes a file path, loads the file bytes into memory, and returns those bytes encoded as a base64 string. Use it when you need to move binary file content through places that only accept strings, such as database fields, message payloads, or integration objects. If you need to recreate the original file later, pair it with [`WriteBytesBase64`](WriteBytesBase64.md).

## When to use

- When you need to persist file content in a text-only field.
- When an integration expects attachments or documents as base64 strings.
- When you need a reversible file export format that can later be written back with [`WriteBytesBase64`](WriteBytesBase64.md).

## Syntax

```ssl
ReadBytesBase64(sFileName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sFileName` | [string](../types/string.md) | yes | — | Path to the file to read and encode. |

## Returns

**[string](../types/string.md)** — The file contents encoded as base64.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sFileName` is [`NIL`](../literals/nil.md) or empty. | `Value cannot be null.` |
| The path is outside the configured whitelist folders. | `Access to folder/file <path> is denied. If system needs access to this folder/file please ask the System Administrator to add the item to WhitelistFolders setting in the configuration file.` |

## Best practices

!!! success "Do"
    - Validate the file path before calling the function.
    - Wrap the call in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when file access can fail at runtime.
    - Use this function when you need a string-safe representation of binary file data.

!!! failure "Don't"
    - Pass an empty file path.
    - Assume every location is readable when whitelist restrictions are configured.
    - Use it for very large files unless loading the full file into memory is acceptable.

## Caveats

- The function reads the full file into memory before returning the base64 value.
- The return value is the encoded file content only. It does not include file name, MIME type, or other metadata.
- If the file cannot be opened, the underlying file I/O error is raised.
- If whitelist folders are not configured, the whitelist check does not block
  access.

## Examples

### Read a file and measure the encoded payload

Read a file into a base64 string and report the payload length.

```ssl
:DECLARE sFileName, sBase64Data;

sFileName := "C:\Exports\label.png";
sBase64Data := ReadBytesBase64(sFileName);

:IF Empty(sBase64Data);
	ErrorMes("No data was read from " + sFileName);
:ELSE;
	UsrMes("Base64 length: " + LimsString(Len(sBase64Data)));
:ENDIF;
```

### Store a PDF as base64 in a table

Read a PDF file, then save the encoded content with a positional-parameter SQL update.

```ssl
:PROCEDURE StorePdfBase64;
	:PARAMETERS sPdfPath, sSampleID;
	:DEFAULT sPdfPath, "C:\Exports\sample_document.pdf";
	:DEFAULT sSampleID, "S000123";
	:DECLARE sPdfBase64, sSQL, bUpdated;

	sPdfBase64 := ReadBytesBase64(sPdfPath);

	sSQL :=
		"
	    UPDATE sample_table SET
	        pdf_content_base64 = ?
	    WHERE sample_id = ?
	";

	bUpdated := RunSQL(sSQL,, {sPdfBase64, sSampleID});

	:IF bUpdated;
		UsrMes("Stored encoded PDF for sample " + sSampleID);
	:ELSE;
		ErrorMes("Database update failed for sample " + sSampleID);
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("StorePdfBase64");
```

### Build attachment payload objects with error handling

Process a list of files, encode each one, and return an array of payload objects that can be passed to another integration layer.

```ssl
:PROCEDURE BuildAttachmentPayloads;
	:PARAMETERS aFileNames;
	:DECLARE aPayloads, nIndex, sFileName, sBase64Data, oPayload, oErr;

	aPayloads := {};

	:FOR nIndex := 1 :TO ALen(aFileNames);
		sFileName := aFileNames[nIndex];

		:TRY;
			sBase64Data := ReadBytesBase64(sFileName);

			oPayload := CreateUdObject();
			oPayload:fileName := sFileName;
			oPayload:contentBase64 := sBase64Data;

			AAdd(aPayloads, oPayload);
		:CATCH;
			oErr := GetLastSSLError();
			UsrMes("Skipped file " + sFileName + ": " + oErr:Description);
			/* Displays on failure: skipped file error;
		:ENDTRY;
	:NEXT;

	:RETURN aPayloads;
:ENDPROC;

/* Usage;
DoProc("BuildAttachmentPayloads", {{"C:\Exports\label.png"}});
```

## Related

- [`WriteBytesBase64`](WriteBytesBase64.md)
- [`string`](../types/string.md)
