---
title: "ExtractZip"
summary: "Extracts a ZIP archive into a target directory."
id: ssl.function.extractzip
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ExtractZip

Extracts a ZIP archive into a target directory.

`ExtractZip` unpacks a ZIP file to `sTargetDirectory`. You can limit extracted files with an optional filter expression and supply a password for encrypted archives. The function also creates empty directories stored in the archive, and it overwrites existing target files when names collide.

## When to use

- When you need to unpack an archive into a working folder.
- When you need to preserve directory structure, including empty directories.
- When you need to extract only files that match a filter expression.
- When you need to open a password-protected ZIP archive.

## Syntax

```ssl
ExtractZip(sZipFileName, sTargetDirectory, [sFileFilter], [sPassword])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sZipFileName` | [string](../types/string.md) | yes | — | Full path to the ZIP archive to extract. |
| `sTargetDirectory` | [string](../types/string.md) | yes | — | Directory where the archive contents will be written. |
| `sFileFilter` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Case-insensitive regular-expression filter applied to each archived file path. When omitted, all archived files are eligible for extraction. |
| `sPassword` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Password used when opening an encrypted ZIP archive. |

## Returns

**NIL** — `ExtractZip` performs its work by writing files and directories and does not return a result value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sZipFileName` is [`NIL`](../literals/nil.md). | `Null argument passed to ExtractZip()`. |
| `sTargetDirectory` is [`NIL`](../literals/nil.md). | `Null argument passed to ExtractZip()`. |

## Best practices

!!! success "Do"
    - Validate the archive path and destination folder before calling `ExtractZip`.
    - Omit optional arguments you do not need instead of passing placeholder values.
    - Use a filter expression when you only need a subset of archived files.
    - Wrap extraction in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the archive, path, password, or filter may fail at runtime.

!!! failure "Don't"
    - Assume existing files in the destination are preserved. `ExtractZip` extracts with overwrite enabled.
    - Use shell-style wildcard examples such as `*.csv`. `sFileFilter` uses case-insensitive regular expressions against archived file paths.
    - Assume a file-only filter prevents empty directory creation. Empty directory entries can still be created from the archive.
    - Use [`ErrorMes`](ErrorMes.md) for routine success reporting. Reserve it for failures that must be logged.

## Caveats

- Errors from invalid paths, invalid filter expressions, ZIP processing, and decryption propagate to the caller.

## Examples

### Extract an archive with required arguments only

Extract the full archive into a working directory.

```ssl
:PROCEDURE ExtractZipBasic;
	:DECLARE sZipFile, sTargetDir;

	sZipFile := "C:\Data\archive.zip";
	sTargetDir := "C:\Data\Extracted";

	ExtractZip(sZipFile, sTargetDir);

	UsrMes("Archive extracted: " + sTargetDir);
:ENDPROC;

/* Usage;
DoProc("ExtractZipBasic");
```

[`UsrMes`](UsrMes.md) displays:

```text
Archive extracted: C:\Data\Extracted
```

### Extract only CSV files with a filter expression

Extract only archived file paths that end in `.csv`.

```ssl
:PROCEDURE ExtractCsvFiles;
	:DECLARE sArchivePath, sTargetFolder, sFileFilter;

	sArchivePath := "C:\Imports\IncomingResults.zip";
	sTargetFolder := "C:\Imports\CsvOnly";
	sFileFilter := "\.csv$";

	ExtractZip(sArchivePath, sTargetFolder, sFileFilter);

	UsrMes("CSV files extracted: " + sTargetFolder);
:ENDPROC;

/* Usage;
DoProc("ExtractCsvFiles");
```

[`UsrMes`](UsrMes.md) displays:

```text
CSV files extracted: C:\Imports\CsvOnly
```

### Extract a password-protected archive with error handling

Handle password-protected extraction and report failures from the archive, password, or destination path.

```ssl
:PROCEDURE ExtractSecureSubmission;
	:DECLARE sZipPath, sExtractDir, sFileFilter, sPassword, oErr;

	sZipPath := "C:\SecureDrop\submission.zip";
	sExtractDir := "C:\SecureDrop\Working";
	sFileFilter := "\.xml$|\.pdf$";
	sPassword := "Submission2026";

	:TRY;
		ExtractZip(sZipPath, sExtractDir, sFileFilter, sPassword);

		UsrMes("Secure archive extracted: " + sExtractDir);
		/* Displays on success: extraction confirmation;

	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("Archive extraction failed: " + oErr:Description);
		/* Displays on failure: extraction failed;
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ExtractSecureSubmission");
```

## Related

- [`CreateZip`](CreateZip.md)
- [`GetLastSSLError`](GetLastSSLError.md)
- [`string`](../types/string.md)
