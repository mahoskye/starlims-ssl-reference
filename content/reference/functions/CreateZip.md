---
title: "CreateZip"
summary: "Creates a ZIP archive from a source directory."
id: ssl.function.createzip
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CreateZip

Creates a ZIP archive from a source directory.

`CreateZip` creates a ZIP file at `sZipFileName` from the contents of
`sSourceDirectory`. By default it recurses into subdirectories, includes empty directories, and replaces any existing ZIP file at the target path. You can limit which files are added with a filter expression and protect the archive with a password.

## When to use

- When you need to package a folder for export, backup, or transfer.
- When you need one ZIP file that includes subfolders automatically.
- When you need to include only files that match a filter expression.
- When you need to create a password-protected archive.

## Syntax

```ssl
CreateZip(sZipFileName, sSourceDirectory, [bRecurse], [sFileFilter], [sPassword])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sZipFileName` | [string](../types/string.md) | yes | — | Full path and file name for the ZIP file to create. |
| `sSourceDirectory` | [string](../types/string.md) | yes | — | Directory whose contents will be added to the archive. |
| `bRecurse` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | When [`.T.`](../literals/true.md), includes matching files from subdirectories. When [`.F.`](../literals/false.md), scans only the top level of `sSourceDirectory`. |
| `sFileFilter` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Case-insensitive regular-expression filter applied to each file's full path while scanning. You can combine include and exclude expressions with `;`. When omitted, all files are eligible. |
| `sPassword` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Password applied to the ZIP archive when supplied. |

## Returns

**NIL** — `CreateZip` performs its work by creating the archive and does not return a result value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sZipFileName` is [`NIL`](../literals/nil.md). | `Null argument passed to CreateZip()` |
| `sSourceDirectory` is [`NIL`](../literals/nil.md). | `Null argument passed to CreateZip()` |

Other file-system, ZIP creation, and invalid filter-expression errors propagate from the underlying ZIP and file APIs.

## Best practices

!!! success "Do"
    - Validate the source directory and destination path before calling `CreateZip`.
    - Omit optional arguments you do not need instead of passing placeholder values.
    - Use a filter expression when you only need a subset of files.
    - Wrap archive creation in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the path, permissions, or filter may fail at runtime.

!!! failure "Don't"
    - Assume an existing destination ZIP file is preserved. `CreateZip` opens the target path for creation.
    - Use shell-style wildcard examples such as `*.pdf`. `sFileFilter` uses case-insensitive regular expressions against full file paths.
    - Turn on recursion when you only need top-level files.
    - Use [`ErrorMes`](ErrorMes.md) for routine success reporting. Reserve it for failures that must be logged.

## Caveats

- If `sFileFilter` matches no files, the ZIP can still be created with only directory entries or no file entries.

## Examples

### Archive a folder with default recursion

Archives a folder and all of its subfolders into a single ZIP file using the default recursive behavior.

```ssl
:PROCEDURE ArchiveReportsFolder;
    :DECLARE sZipFile, sSourceDir;

    sSourceDir := "C:\Reports\Q4Data";
    sZipFile := "C:\Archives\Q4DataBackup.zip";

    CreateZip(sZipFile, sSourceDir);

    UsrMes("Archive created: " + sZipFile);
:ENDPROC;

/*
Usage:
DoProc("ArchiveReportsFolder")
;
```

[`UsrMes`](UsrMes.md) displays:

```
Archive created: C:\Archives\Q4DataBackup.zip
```

### Archive only top-level PDF files

Disables recursion and passes a regular-expression filter so only files whose full path ends in `.pdf` are included.

```ssl
:PROCEDURE ArchiveTopLevelPdfFiles;
    :DECLARE sSourceDir, sZipFile, sFileFilter;

    sSourceDir := "C:\STARLIMS\Laboratory\Reports";
    sZipFile := "C:\Archives\CurrentReports.zip";
    sFileFilter := "\.pdf$";

    CreateZip(sZipFile, sSourceDir, .F., sFileFilter);

    UsrMes("PDF archive created: " + sZipFile);
:ENDPROC;

/*
Usage:
DoProc("ArchiveTopLevelPdfFiles")
;
```

[`UsrMes`](UsrMes.md) displays:

```
PDF archive created: C:\Archives\CurrentReports.zip
```

### Create a password-protected export

Creates a password-protected archive while skipping the optional `sFileFilter` argument, and catches any errors that arise from file-system or ZIP processing problems.

```ssl
:PROCEDURE CreateSecureExport;
    :DECLARE sZipPath, sSourceDir, sPassword, oErr;

    sSourceDir := "C:\Temp\SecureData";
    sZipPath := "C:\SecureExports\SecureData.zip";
    sPassword := "ExportOnly2026";

    :TRY;
        CreateZip(sZipPath, sSourceDir, .T.,, sPassword);
        UsrMes("Secure export created: " + sZipPath);

    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("Secure export failed: " + oErr:Description);
        /* Displays on failure: Secure export failed;
    :ENDTRY;
:ENDPROC;

/*
Usage:
DoProc("CreateSecureExport")
;
```

## Related

- [`ExtractZip`](ExtractZip.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
