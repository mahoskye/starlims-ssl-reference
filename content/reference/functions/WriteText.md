---
title: "WriteText"
summary: "Writes string content to a file."
id: ssl.function.writetext
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# WriteText

Writes string content to a file.

`WriteText` creates a new file or writes over an existing one by default. When `sAppend` is set to `"Y"` or `"y"`, it appends the new text to the end of the file instead. If you omit `sEncoding`, the function writes using `UTF8`.

The target path must not be empty, and the runtime must allow access to the target folder or file. The `vConfirmRequired` argument is accepted for compatibility but is not used by the function's behavior.

## When to use

- Save generated text, logs, exports, or reports to disk.
- Overwrite an existing text file with fresh output.
- Append new text to an existing file without reading it first.
- Write text using a specific encoding when an integration requires it.

## Syntax

```ssl
WriteText(sFileName, sCharsToWrite, [vConfirmRequired], [sAppend], [sEncoding])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sFileName` | [string](../types/string.md) | yes | — | Full path of the file to write. The path cannot be empty. |
| `sCharsToWrite` | [string](../types/string.md) | yes | — | Text content to write to the file. |
| `vConfirmRequired` | any | no | [`NIL`](../literals/nil.md) | Reserved parameter. It is accepted by the function but does not affect the write operation. |
| `sAppend` | [string](../types/string.md) | no | `"N"` | Append mode flag. Use `"Y"` or `"y"` to append, or `"N"` or `"n"` to overwrite. Any other value raises an error. |
| `sEncoding` | [string](../types/string.md) | no | `"UTF8"` | Encoding name for the output text. Common values include `"UTF8"`, `"ASCII"`, `"UNICODE"`, `"UTF32"`, `"UTF7"`, `"DEFAULT"`, and `"BIGENDIANUNICODE"`. |

## Returns

**[string](../types/string.md)** — Always returns an empty string.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sFileName` is [`NIL`](../literals/nil.md) or empty. | `Argument sFileName cannot be null or empty.` |
| `sAppend` is not one of those four values. | `Only 'Y', 'y', 'N', and 'n' are accepted values!` |
| `sEncoding` is not a string. | `Argument: <sEncoding> must be of type string.` |
| The target path is outside the allowed whitelist. | `Access to folder/file <sFileName> is denied.\nIf system needs access to this folder/file please ask the System Administrator to add the item to WhitelistFolders setting in the configuration file.` |

## Best practices

!!! success "Do"
    - Use an explicit full path so the output location is predictable.
    - Pass `"Y"` only when you intentionally want to preserve existing content.
    - Specify `sEncoding` explicitly when another system expects a particular text format.
    - Wrap writes in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the file operation is important to the workflow.

!!! failure "Don't"
    - Pass any `sAppend` value other than `"Y"`, `"y"`, `"N"`, or `"n"` because the function raises an error instead of silently defaulting.
    - Assume `vConfirmRequired` prompts the user or changes overwrite behavior because the function ignores it.
    - Write to arbitrary folders without confirming the runtime allows that location.

## Caveats

- Append mode creates the file if it does not already exist.
- `sEncoding` is only validated as a string; an unsupported encoding name can still fail when the runtime resolves it.

## Examples

### Overwrite a small text file

Write a short message to a file, replacing any previous content.

```ssl
:PROCEDURE SaveRunNote;
    :DECLARE sFileName;

    sFileName := GetAppWorkPathFolder() + "run-note.txt";

    WriteText(sFileName, "Run started successfully");
    UsrMes("Saved run note to: " + sFileName);
    /* Displays saved file path;
:ENDPROC;

/* Usage;
DoProc("SaveRunNote");
```

### Append log lines to an existing file

Build a timestamped log entry and append it so earlier entries remain in place. The fourth argument `"Y"` enables append mode; `vConfirmRequired` is skipped with `,,`.

```ssl
:PROCEDURE AppendAuditLine;
    :DECLARE sLogFile, sEntry, sStamp;

    sLogFile := GetLogsFolder() + "integration-audit.log";
    sStamp := DToC(Today()) + " " + Time();
    sEntry := sStamp + "|Batch export completed" + Chr(13) + Chr(10);

    WriteText(sLogFile, sEntry,, "Y");
:ENDPROC;

/* Usage;
DoProc("AppendAuditLine");
```

### Write an encoded export file with error handling

Create a multi-line export in a specific encoding and report any write failure. Specifying `"ASCII"` ensures the output is readable by systems that do not support multi-byte encodings.

```ssl
:PROCEDURE WriteLegacyExport;
    :DECLARE sFileName, sContent, oErr;

    sFileName := GetAppWorkPathFolder() + "legacy-export.txt";
    sContent := "RECORD_ID,NAME,VALUE" + Chr(13) + Chr(10);
    sContent += "001,SampleA,100" + Chr(13) + Chr(10);
    sContent += "002,SampleB,200" + Chr(13) + Chr(10);

    :TRY;
        WriteText(sFileName, sContent,, "N", "ASCII");
        UsrMes("Legacy export created: " + sFileName);
        /* Displays created file path;
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("WriteText failed: " + oErr:Description);
        /* Displays write failure details;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("WriteLegacyExport");
```

## Related

- [`CombineFiles`](CombineFiles.md)
- [`GetAppWorkPathFolder`](GetAppWorkPathFolder.md)
- [`GetLogsFolder`](GetLogsFolder.md)
- [`ReadText`](ReadText.md)
- [`string`](../types/string.md)
