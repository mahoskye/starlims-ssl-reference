---
title: "CombineFiles"
summary: "Concatenates multiple files into one output file on disk."
id: ssl.function.combinefiles
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CombineFiles

Concatenates multiple files into one output file on disk.

`CombineFiles` reads each path in `aFileNames` in array order and copies its raw bytes into a newly created output file at `sOutFile`. It returns an empty string on success. Use it when you need one physical output file rather than combined content in memory.

The output file is created with create-new semantics. If a file already exists at `sOutFile`, the call fails instead of overwriting it. The function also enforces the configured file-access whitelist for the output path and for every source file it reads.

## When to use

- When you need to merge several text or data files into a single file stored on disk.
- When preparing a batch of files for downstream use that expects one combined file.
- When the order of the source files must be preserved in the output.

## Syntax

```ssl
CombineFiles(aFileNames, sOutFile);
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aFileNames` | [array](../types/array.md) | yes | — | Array of source file paths to copy into the output file in array order |
| `sOutFile` | [string](../types/string.md) | yes | — | Destination file path for the combined output |

## Returns

**[string](../types/string.md)** — An empty string on success.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `aFileNames` is [`NIL`](../literals/nil.md). | Raises a null-argument error for `aFileNames`. |
| `sOutFile` is [`NIL`](../literals/nil.md). | Raises a null-argument error for `sOutFile`. |
| The whitelist configuration denies access to a source or output path. | `Access to folder/file {path} is denied. If system needs access to this folder/file please ask the System Administrator to add the item to WhitelistFolders setting in the configuration file.` |
| `sOutFile` already exists, because the output file is opened in create-new mode. | Raises a file-creation error. |
| A source file cannot be opened for reading. | Raises an I/O error. |

## Best practices

!!! success "Do"
    - Verify that all input files exist and are readable before calling this function.
    - Choose an output path that does not already exist, or remove the old file first.
    - Pass the source files in the exact order you want them copied into the result.
    - Use this function when you need one combined file on disk rather than a combined string in memory.
    - Treat the operation as byte-for-byte concatenation with no separators added between files.

!!! failure "Don't"
    - Assume inaccessible source files will be skipped. The call stops when it cannot open one of the files.
    - Expect `CombineFiles` to overwrite an existing output file. It creates a new file and fails if the target already exists.
    - Use this function when you need separators, headers, encoding changes, or other content transformations between files.
    - Assume the function rolls back a partially written output file after a later source-file failure.

## Caveats

- If `aFileNames` is empty, the function still creates an empty output file.
- The function concatenates raw file contents in order. It does not insert line breaks, separators, or metadata between files.
- If a later source file fails after earlier files were already copied, the output file is not automatically removed or rolled back.
- The return value is always an empty string on success; verify the output file separately if you need to confirm contents or size.

## Examples

### Combine three logs into a single result file

Combines three known log files in array order into a single output file and confirms success by checking that the return value is an empty string.

```ssl
:PROCEDURE CombineLogFiles;
    :DECLARE aLogFiles, sOutFile, sResult;

    aLogFiles := {
        "C:/Logs/application.log",
        "C:/Logs/system.log",
        "C:/Logs/error.log"
    };

    sOutFile := "C:/Logs/combined.log";

    sResult := CombineFiles(aLogFiles, sOutFile);

    :IF Empty(sResult);
        UsrMes("Created " + sOutFile);
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("CombineLogFiles");
```

### Batch merge several data output files for downstream import

Checks each source file for existence first, then merges only the files that are present into one combined output.

```ssl
:PROCEDURE MergeLabImportFiles;
    :DECLARE aSourceFiles, aValidFiles, sOutputFile, sFile;
    :DECLARE nIndex, nCount;

    aSourceFiles := {
        "C:/Data/LabA_export.csv",
        "C:/Data/LabB_export.csv",
        "C:/Data/LabC_export.csv"
    };

    aValidFiles := {};

    :FOR nIndex := 1 :TO ALen(aSourceFiles);
        sFile := aSourceFiles[nIndex];

        :IF FileSupport(sFile, "EXISTS");
            AAdd(aValidFiles, sFile);
        :ENDIF;
    :NEXT;

    :IF ALen(aValidFiles) > 0;
        sOutputFile := "C:/Data/Merged_lab_results.csv";

        CombineFiles(aValidFiles, sOutputFile);

        nCount := ALen(aValidFiles);
        UsrMes("Merged " + LimsString(nCount)
	            + " files into " + sOutputFile);
        /* Displays merged file count and output path;
    :ELSE;
        UsrMes("No source files were available to combine");
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("MergeLabImportFiles");
```

### Create a manifest and handle failures explicitly

Merges the source files in a [`:TRY`](../keywords/TRY.md) block, writes a separate manifest file on success, and reports the error message if the combine fails.

```ssl
:PROCEDURE MergeFilesWithManifest;
    :PARAMETERS aFileNames, sOutFile;

    :DECLARE bSuccess, oErr, sManifestFile, sManifest;

    bSuccess := .F.;

    :TRY;
        CombineFiles(aFileNames, sOutFile);

        sManifestFile := sOutFile + ".manifest";
        sManifest := "Combined "
		            + LimsString(ALen(aFileNames))
		            + " files into "
		            + sOutFile;

        WriteText(sManifestFile, sManifest, "N", "N");

        bSuccess := .T.;
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("CombineFiles failed: " + oErr:Description);
        /* Displays combine failure details;
    :ENDTRY;

    :RETURN bSuccess;
:ENDPROC;

/* Usage;
DoProc("MergeFilesWithManifest", {
	    {"C:/Data/part1.csv", "C:/Data/part2.csv"},
	    "C:/Data/combined.csv"
});
```

## Related

- [`ReadText`](ReadText.md)
- [`WriteText`](WriteText.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
