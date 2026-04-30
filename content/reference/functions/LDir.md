---
title: "LDir"
summary: "Retrieves an array of file and directory names matching a specified pattern and optional attribute filter."
id: ssl.function.ldir
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LDir

Retrieves an array of file and directory names matching a specified pattern and optional attribute filter.

Enumerates filesystem entries and returns only their names. `LDir` is the name-only companion to [`Directory`](Directory.md): it performs the same lookup, then returns just the first column from each matching row rather than the full metadata record.

`sFilePattern` accepts either an existing directory path or a directory-plus-pattern string such as `C:\Reports\*.txt`. When the value is an existing directory, `LDir` lists every visible regular file in that directory by default. When the value includes a wildcard pattern, `LDir` uses the parent path as the directory and the last segment as the pattern. The function returns names only, not full paths.

The optional `sAttributes` argument does not switch `LDir` into an exclusive mode. Instead, it expands what can be included in the results: `D` includes directories, `H` includes hidden entries, and `S` includes system entries. Without `sAttributes`, `LDir` returns visible non-system files only. If the target directory does not exist or the lookup fails for a normal filesystem reason, the result is an empty array. Access to non-whitelisted paths still raises an explicit security error.

## When to use

- When scanning a folder for files or directories matching a naming pattern such as all ".csv" files for data imports.
- When building UIs, scripts, or automations that need to present the user with a filtered file/directory list.
- When automating batch file operations and only entry names are needed (not file details).
- When validating the presence of required files in an expected directory before further processing.
- When scripting folder cleanup, backup, or migration tasks based on extension or file type attributes.

## Syntax

```ssl
LDir(sFilePattern, [sAttributes])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sFilePattern` | [string](../types/string.md) | yes | — | Existing directory path or directory-plus-pattern string to enumerate. Pass an explicit path such as `C:\Reports\*.txt` or `C:\Reports`. [`NIL`](../literals/nil.md) or an omitted first argument raises an error instead of falling back automatically. An empty string can fall back to the current working directory, but relying on that is fragile and may still fail permission checks. |
| `sAttributes` | [string](../types/string.md) | no | `""` | Inclusion flags for entry types that are excluded by default. `D` includes directories, `H` includes hidden entries, and `S` includes system entries. Other characters are ignored. Omitting `sAttributes` returns visible non-system files only. |

## Returns

**[array](../types/array.md)** — Array of entry names that match the requested path/pattern. The values are names only, not full paths or metadata.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sFilePattern` is [`NIL`](../literals/nil.md) or omitted. | `Second parameter cannot be null.` |
| The specified path is not in the allowed folders. | `Access to folder/file {folderOrFile} is denied. If system needs access to this folder/file please ask the System Administrator to add the item to WhitelistFolders setting in the configuration file.` |

## Best practices

!!! success "Do"
    - Supply a fully qualified directory or directory-plus-pattern such as `C:\\reports\\*.pdf` so the lookup target is explicit.
    - Use `D`, `H`, and `S` only when you intentionally want to include directories, hidden entries, or system entries.
    - Handle empty arrays defensively, as no matches found is not an error.
    - Use [`Directory`](Directory.md) when you need size, date, time, or attribute metadata instead of just names.

!!! failure "Don't"
    - Omit `sFilePattern` or pass [`NIL`](../literals/nil.md) expecting a safe default. `LDir` reaches [`DosSupport`](DosSupport.md), which treats a missing first argument as an error.
    - Treat `D`, `H`, or `S` as exclusive filters such as "directories only" or "hidden only". They add those entry types to the normal visible-file results.
    - Write downstream logic that assumes LDir always returns results. Filters or missing files yield empty arrays and must be handled gracefully.
    - Try to derive file size, timestamps, attributes, or full paths from `LDir` results. The function only returns names.

## Caveats

- `LDir` returns only names. If you need paths or metadata, call [`Directory`](Directory.md) instead.
- An empty result means either no entries matched or the lookup failed for a normal filesystem reason such as a missing directory.
- Unsupported attribute characters are ignored.
- `D`, `H`, and `S` include additional entry types; they do not remove regular visible files from the result.

## Examples

### List text files in a specific folder

Retrieve the names of all `.txt` files in an explicit folder.

```ssl
:PROCEDURE ListTextFiles;
    :DECLARE sFolder, aFiles, sFile, nIndex, nCount;

    sFolder := "C:\Reports";
    aFiles := LDir(sFolder + "\*.txt");
    nCount := ALen(aFiles);

    UsrMes(
        "Found " + LimsString(nCount) + " text files in " + sFolder
    );
    /* Displays file count for the selected folder;

    :FOR nIndex := 1 :TO nCount;
        sFile := aFiles[nIndex];
        UsrMes(sFile);
        /* Displays one matching file name per iteration;
    :NEXT;

    :RETURN aFiles;
:ENDPROC;

/* Usage;
DoProc("ListTextFiles");
;
```

### Include subfolders in the results

Include directory names as well as regular files when scanning a staging folder.

```ssl
:PROCEDURE ListStagingEntries;
    :DECLARE sFolder, aEntries, sName, nIndex;

    sFolder := "C:\Imports\Staging";
    aEntries := LDir(sFolder, "D");

    :FOR nIndex := 1 :TO ALen(aEntries);
        sName := aEntries[nIndex];
        UsrMes(sName);
        /* Displays one file or folder name per iteration;
    :NEXT;

    :RETURN aEntries;
:ENDPROC;

/* Usage;
DoProc("ListStagingEntries");
;
```

### Verify mandatory files before import

Verify that the expected import package is present before continuing.

```ssl
:PROCEDURE ValidateImportFiles;
    :PARAMETERS sImportFolder;
    :DEFAULT sImportFolder, "C:\Imports";
    :DECLARE aCsvFiles, aJsonFiles, aCtlFiles, aMissing;
    :DECLARE bIsValid, sMessage, oResult;

    bIsValid := .T.;
    aMissing := {};

    aCsvFiles := LDir(sImportFolder + "\*.csv");
    aJsonFiles := LDir(sImportFolder + "\*.json");
    aCtlFiles := LDir(sImportFolder + "\*.ctl");

    :IF ALen(aCsvFiles) == 0;
        bIsValid := .F.;
        AAdd(aMissing, "CSV");
    :ENDIF;

    :IF ALen(aJsonFiles) == 0;
        bIsValid := .F.;
        AAdd(aMissing, "JSON");
    :ENDIF;

    :IF ALen(aCtlFiles) == 0;
        bIsValid := .F.;
        AAdd(aMissing, "CTL");
    :ENDIF;

    :IF !bIsValid;
        sMessage := "Import validation failed. Missing required file types: " + BuildString(aMissing,,, ", ");

        ErrorMes(sMessage);
        /* Displays import validation failure details;

        oResult := CreateUdObject({
            {"Valid", .F.},
            {"Missing", aMissing}
        });
    :ELSE;
        sMessage := "Import validation passed. Found ";
        sMessage := sMessage + LimsString(ALen(aCsvFiles));
        sMessage := sMessage + " CSV and ";
        sMessage := sMessage + LimsString(ALen(aJsonFiles));
        sMessage := sMessage + " JSON files, plus ";
        sMessage := sMessage + LimsString(ALen(aCtlFiles));
        sMessage := sMessage + " CTL files.";

        InfoMes(sMessage);
        /* Displays import validation success details;

        oResult := CreateUdObject({
            {"Valid", .T.},
            {"CsvCount", ALen(aCsvFiles)},
            {"JsonCount", ALen(aJsonFiles)},
            {"CtlCount", ALen(aCtlFiles)}
        });
    :ENDIF;

    :RETURN oResult;
:ENDPROC;

/* Usage;
DoProc("ValidateImportFiles");
;
```

## Related

- [`Directory`](Directory.md)
- [`DosSupport`](DosSupport.md)
- [`FileSupport`](FileSupport.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
