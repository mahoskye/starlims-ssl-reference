---
title: "Directory"
summary: "Retrieves filesystem entries that match a path or wildcard pattern, with optional filtering for directories, hidden entries, and system entries."
id: ssl.function.directory
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Directory

Retrieves filesystem entries that match a path or wildcard pattern, with optional filtering for directories, hidden entries, and system entries.

`Directory` returns an array of rows. Each row contains the entry name, size, last modified value, a formatted last modified time string, and an attribute string. By default, the function returns visible non-system files only. Directories are only included when `sAttributes` contains uppercase `D`, hidden entries are only included when it contains uppercase `H`, and system entries are only included when it contains uppercase `S`. Read-only (`R`) and archive (`A`) can appear in the returned attribute string, but they are not used as filter switches.

If `sFilePattern` is an existing directory path, the function lists entries in that directory using [`*`](../operators/multiply.md) as the pattern. If you pass an empty string, the listing logic falls back to the current working directory, but the path is still checked against the folder whitelist first. If the target directory does not exist, or the listing fails for a non-permission reason, the function returns an empty array.

## When to use

- When you need file metadata, not just names.
- When you need to include directories, hidden entries, or system entries explicitly.
- When you need one call that returns name, size, timestamp information, and attribute letters together.

## Syntax

```ssl
Directory(sFilePattern, [sAttributes])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sFilePattern` | [string](../types/string.md) | yes | — | Path and wildcard pattern to list, such as `"C:\\Reports\\*.txt"`. If it points to an existing directory, `Directory` lists that directory with the [`*`](../operators/multiply.md) pattern. If you pass an empty string, the listing logic uses the current working directory after the whitelist check passes. |
| `sAttributes` | [string](../types/string.md) | no | `""` | Attribute filter string. Uppercase `D` includes directories, uppercase `H` includes hidden entries, and uppercase `S` includes system entries. Other characters are ignored for filtering. |

## Returns

**[array](../types/array.md)** — Array of entry rows.

Each row contains these values:

| Position | Type | Description |
|----------|------|-------------|
| `1` | [string](../types/string.md) | Entry name only, not the full path |
| `2` | [number](../types/number.md) | Size in bytes. Directory entries return `0`. |
| `3` | [date](../types/date.md) | Last modified date/time value |
| `4` | [string](../types/string.md) | Last modified time formatted as `HH:MM:SS` |
| `5` | [string](../types/string.md) | Attribute letters for the entry, such as `D`, `H`, `S`, `R`, and `A` |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| The target path is outside the allowed whitelist. `{path}` is replaced with the actual path value. | `Access to folder/file {path} is denied.<LF>If system needs access to this folder/file please ask the System Administrator to add the item to WhitelistFolders setting in the configuration file.` |

## Best practices

!!! success "Do"
    - Pass an explicit directory and pattern so the listing scope is clear.
    - Check for an empty result because missing matches and non-permission listing failures both return an empty array.
    - Read the returned attribute string from column 5 when you need to distinguish files from directories or inspect `R` and `A`.

!!! failure "Don't"
    - Assume `R` or `A` in `sAttributes` will filter the result set. They appear in returned metadata, but they are not filter switches.
    - Assume directories are included by default. Add `D` when you want directory rows returned.
    - Treat an empty result as proof that the directory is accessible and has no matching items. It can also mean the directory does not exist or the listing failed for another non-whitelist reason.

## Caveats

- Non-whitelist access raises an exception; other listing failures return an empty array.

## Examples

### List visible text files

Lists all visible `.txt` files in a folder and displays each file name from the returned array.

```ssl
:PROCEDURE ShowTextFiles;
    :DECLARE sPattern, aEntries, nIndex, sName;

    sPattern := "C:\Reports\*.txt";
    aEntries := Directory(sPattern);

    :IF ALen(aEntries) == 0;
        UsrMes("No text files found.");
        :RETURN aEntries;
    :ENDIF;

    :FOR nIndex := 1 :TO ALen(aEntries);
        sName := aEntries[nIndex, 1];
        UsrMes("File: " + sName);
        /* Displays one line per matching file;
    :NEXT;

    :RETURN aEntries;
:ENDPROC;

/* Usage;
DoProc("ShowTextFiles");
```

### Include hidden entries and directories

Retrieves hidden entries and directories by passing `"DH"` as the attribute filter, then identifies directories by checking column 5 of each returned row.

```ssl
:PROCEDURE AuditHiddenEntries;
    :DECLARE sFolder, aEntries, nIndex, sName, sAttrs, sKind;

    sFolder := "C:\Temp";
    aEntries := Directory(sFolder, "DH");

    :IF ALen(aEntries) == 0;
        UsrMes("No matching entries found.");
        :RETURN aEntries;
    :ENDIF;

    :FOR nIndex := 1 :TO ALen(aEntries);
        sName := aEntries[nIndex, 1];
        sAttrs := aEntries[nIndex, 5];
        sKind := "File";

        :IF At("D", sAttrs) > 0;
            sKind := "Directory";
        :ENDIF;

        UsrMes(sKind + ": " + sName + " (" + sAttrs + ")");
        /* Displays one line per matching entry;
    :NEXT;

    :RETURN aEntries;
:ENDPROC;

/* Usage;
DoProc("AuditHiddenEntries");
```

### Handle denied access and inspect metadata

Guards against whitelist access denial by wrapping the call in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md), then displays the name, size, and attribute string for each returned entry.

```ssl
:PROCEDURE InspectImportDrop;
    :DECLARE sPattern, aEntries, oErr, nIndex, sName, nSize, sAttrs;

    sPattern := "C:\SecureDrop\*.*";

    :TRY;
        aEntries := Directory(sPattern);

        :IF ALen(aEntries) == 0;
            UsrMes("No files found in the import drop.");
            :RETURN .T.;
        :ENDIF;

        :FOR nIndex := 1 :TO ALen(aEntries);
            sName := aEntries[nIndex, 1];
            nSize := aEntries[nIndex, 2];
            sAttrs := aEntries[nIndex, 5];

            UsrMes(sName + " | Size: " + LimsString(nSize)
					+ " | Attr: " + sAttrs);
            /* Displays one line per returned entry;
        :NEXT;

    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("Directory access failed: " + oErr:Description);
        /* Displays on failure: directory access failed;
        :RETURN .F.;
    :ENDTRY;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("InspectImportDrop");
```

## Related

- [`DosSupport`](DosSupport.md)
- [`FileSupport`](FileSupport.md)
- [`LDir`](LDir.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
