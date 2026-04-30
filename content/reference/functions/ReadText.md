---
title: "ReadText"
summary: "Retrieves text content from a file in memory, allowing partial reads and encoding selection."
id: ssl.function.readtext
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ReadText

Retrieves text content from a file in memory, allowing partial reads and encoding selection.

`ReadText` reads a text file and returns its contents as a string. You can read the whole file or request only the first `n` characters. If `nCharsToRead` is omitted, [`NIL`](../literals/nil.md), or less than or equal to zero, the function returns the full text. If `sEncoding` is omitted or [`NIL`](../literals/nil.md), the file is read as `UTF8`.

If the file is empty, the function returns an empty string. If the requested character count is longer than the file contents, the full text is returned with no error.

## When to use

- When you need the contents of one text file as a string for parsing or processing.
- When you want to preview the beginning of a file without returning the entire text.
- When you need to read a file using a specific encoding such as `ASCII`, `Unicode`, or `UTF8`.

## Syntax

```ssl
ReadText(sFileName, [nCharsToRead], [sEncoding])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sFileName` | [string](../types/string.md) | yes | — | The path to the text file to read. |
| `nCharsToRead` | [number](../types/number.md) | no | -1 | The maximum number of characters to return. If omitted, [`NIL`](../literals/nil.md), or less than or equal to zero, the function returns the full text. |
| `sEncoding` | [string](../types/string.md) | no | `"UTF8"` | The text encoding to use. If omitted or [`NIL`](../literals/nil.md), the function uses `UTF8`. |

## Returns

**[string](../types/string.md)** — The file contents, or the first `nCharsToRead` characters when a positive limit is provided.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sFileName` is [`NIL`](../literals/nil.md) or empty. | `Value cannot be null.` |
| `sEncoding` is not a string. | `Argument: <encoding> must be of type string.` |
| The path is outside the configured whitelist folders. | `Access to folder/file <path> is denied. If system needs access to this folder/file please ask the System Administrator to add the item to WhitelistFolders setting in the configuration file.` |
| The file cannot be opened or the encoding name is unsupported. | The underlying file I/O or encoding lookup raises an error. |

## Best practices

!!! success "Do"
    - Pass a full file path that exists and is allowed by the system whitelist.
    - Omit `nCharsToRead` or pass a value less than or equal to `0` when you want the full file.
    - Pass `sEncoding` explicitly when reading files that are not stored as UTF-8.
    - Use a small positive `nCharsToRead` value for previews or header reads.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) or an empty string for `sFileName`.
    - Pass a non-string value for `sEncoding`.
    - Expect `0` or negative `nCharsToRead` values to return an empty string.
    - Assume every text file is UTF-8 when the source system uses a different encoding.

## Caveats

- `ReadText` reads the file into memory before returning the final string, even when you request only part of the text.

## Examples

### Read a complete configuration file

Read a UTF-8 text file and return the full contents.

```ssl
:PROCEDURE LoadConfigSettings;
    :DECLARE sConfigPath, sConfigData;

    sConfigPath := GetAppWorkPathFolder() + "/config/app_settings.txt";
    sConfigData := ReadText(sConfigPath);

    :IF Empty(sConfigData);
        UsrMes("Configuration file is empty: " + sConfigPath);
        /* Displays when the file is empty;
    :ELSE;
        UsrMes("Loaded " + LimsString(Len(sConfigData)) + " characters");
        /* Displays the loaded character count;
    :ENDIF;

    :RETURN sConfigData;
:ENDPROC;

/* Usage;
DoProc("LoadConfigSettings");
```

### Preview a file with a non-default encoding

Read only the first part of a file and specify a non-default encoding.

```ssl
:PROCEDURE PreviewLegacyFile;
    :DECLARE sFilePath, sPreview;

    sFilePath := GetAppWorkPathFolder() + "/import/legacy_report.txt";
    sPreview := ReadText(sFilePath, 120, "ASCII");

    :IF Empty(sPreview);
        UsrMes("The file is empty");
    :ELSE;
        UsrMes(sPreview);
        /* Displays the file preview;
    :ENDIF;

    :RETURN sPreview;
:ENDPROC;

/* Usage;
DoProc("PreviewLegacyFile");
```

### Preview a large data file with error handling

Wrap the read in structured error handling so you can report file or access problems.

```ssl
:PROCEDURE LoadImportPreview;
    :DECLARE sFilePath, sHeader, nHeaderLength, oErr;

    sFilePath := GetAppWorkPathFolder() + "/import/IncomingSamples.csv";
    nHeaderLength := 1024;

    :TRY;
        sHeader := ReadText(sFilePath, nHeaderLength, "UTF8");

        :IF !Empty(sHeader);
            UsrMes(sHeader);
            /* Displays the header preview;
        :ENDIF;
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("ReadText failed: " + oErr:Description);
        /* Displays on failure;
        sHeader := "";
    :ENDTRY;

    :RETURN sHeader;
:ENDPROC;

/* Usage;
DoProc("LoadImportPreview");
```

## Related

- [`CombineFiles`](CombineFiles.md)
- [`WriteText`](WriteText.md)
- [`string`](../types/string.md)
