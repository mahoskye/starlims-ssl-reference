---
title: "DosSupport"
summary: "Executes operating system-level file and directory commands."
id: ssl.function.dossupport
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DosSupport

Executes operating system-level file and directory commands.

`DosSupport` dispatches a small set of command strings such as `DIR`, `MD`, `CD`, `RD`, `ENV`, `WORK`, `WORKDIR`, `CURRENTDRIVE`, and `ISDIR`. Depending on the command, it returns a directory listing, a string value, or a success flag.

Some commands change process state. In particular, `CD` updates the current working directory used by later calls, and `MD` and `RD` modify the file system.

## When to use

- When automating multiple file system operations in workflow logic where command-driven, shell-like control is preferred.
- When initializing or validating environment state by interacting with directories or environment variables in an abstracted, platform-independent way.
- When mimicking or scripting DOS-style file commands inside SSL without writing multiple function calls for each operation.
- When access, modification, or inspection of directory structure is required in a batch or user-driven application process.

## Syntax

```ssl
DosSupport(sCmd, [sPrm], [vDbg])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCmd` | [string](../types/string.md) | yes | — | Command name. Supported values are `DIR`, `MD`, `CD`, `RD`, `ENV`, `WORK`, `WORKDIR`, `CURRENTDRIVE`, `ISDIR`, and `""`. Matching is case-insensitive after trimming. |
| `sPrm` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Path, file pattern, directory name, or environment variable name, depending on `sCmd`. It may be omitted only for `WORK`, `WORKDIR`, and `CURRENTDRIVE`. |
| `vDbg` | any | no | [`NIL`](../literals/nil.md) | Command-specific third argument. For `DIR`, it is an optional attribute filter. For `MD`, `CD`, and `RD`, a boolean [`.T.`](../literals/true.md) causes failures to be logged with [`UsrMes`](UsrMes.md). Other commands ignore it. |

## Returns

**any** — The return type depends on the command.

| Command | Return type | Behavior |
|---------|-------------|----------|
| `ENV` | [string](../types/string.md) | Returns the environment variable value, or `""` when it is missing or cannot be read. |
| `DIR` | [array](../types/array.md) | Returns an array of rows. Each row contains `{name, size, lastWriteDateTime, lastWriteTimeText, attributes}`. If the directory does not exist or enumeration fails, the result is an empty array. |
| `MD` | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the directory is created and [`.F.`](../literals/false.md) when creation fails. |
| `CD` | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the current working directory is changed and [`.F.`](../literals/false.md) when the change fails. |
| `RD` | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the call succeeds. If the target directory does not exist, it still returns [`.T.`](../literals/true.md). It returns [`.F.`](../literals/false.md) only when deletion raises an error. |
| `ISDIR` | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when `sPrm` names an existing directory, otherwise [`.F.`](../literals/false.md). |
| `WORK`, `WORKDIR` | [string](../types/string.md) | Returns the current working directory. |
| `CURRENTDRIVE` | [string](../types/string.md) | Returns the current drive letter when the working directory uses a drive-rooted path such as `C:\...`; otherwise returns `""`. |
| `""` | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md). |

For `DIR`, `vDbg` can be a string or numeric attribute filter. The filter affects whether directory, hidden, and system entries are included:

- Include `D` to include directories.
- Include `H` to include hidden entries.
- Include `S` to include system entries.
- Without those flags, those entry types are excluded from the result.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sCmd` is [`NIL`](../literals/nil.md). | `Command parameter cannot be null` |
| `sPrm` is [`NIL`](../literals/nil.md) for commands other than `WORK`, `WORKDIR`, and `CURRENTDRIVE`. | `Second parameter cannot be null` |
| `sCmd` is not a supported command. | `Unknown option - {command}` |
| `DIR`, `MD`, `CD`, `RD`, or `ISDIR` targets a non-whitelisted path. | `Access to folder/file {path} is denied` |

## Best practices

!!! success "Do"
    - Use `WORK` or `WORKDIR` to read the current directory instead of trying to infer it from `CD`.
    - Check the boolean result from `MD`, `CD`, and `RD` before continuing with later file operations.
    - Use explicit `DIR` attribute filters when you need directories, hidden items, or system items in the result.

!!! failure "Don't"
    - Treat the third argument (`vDbg`) as a universal debug message. Only `MD`, `CD`, and `RD` use a boolean debug flag, while `DIR` uses that position for attribute filtering.
    - Assume `RD` returning [`.T.`](../literals/true.md) means a directory was actually removed. It also returns [`.T.`](../literals/true.md) when the target does not exist.
    - Call path-based commands against locations outside the configured whitelist.

## Caveats

- Passing [`NIL`](../literals/nil.md) for `sPrm` raises an exception for most commands, even when an empty string would be acceptable.
- `DIR` returns raw row arrays, not objects.

## Examples

### List files in a user-upload directory

Retrieve a directory listing and read the file name from the first column of each returned row.

```ssl
:PROCEDURE ListUploadFiles;
    :DECLARE sUploadPath, aDirRows, nIndex, sFileName;

    sUploadPath := "C:\STARLIMS\Uploads";

    aDirRows := DosSupport("DIR", sUploadPath);

    UsrMes("Files in upload directory: " + LimsString(ALen(aDirRows)));

    :FOR nIndex := 1 :TO ALen(aDirRows);
        sFileName := aDirRows[nIndex, 1];
        UsrMes(LimsString(nIndex) + ": " + LimsString(sFileName));
        /* Displays one line per file;
    :NEXT;
:ENDPROC;

/* Usage;
DoProc("ListUploadFiles");
```

### Change the working directory for a file import operation

Capture the original working directory, switch to a target folder, then restore it.

```ssl
:PROCEDURE ChangeDirectoryForImport;
    :DECLARE sOriginalDir, sTargetDir, sCurrentDir, bChanged;

    sOriginalDir := DosSupport("WORK");
    sTargetDir := "C:\Data\Imports";

    bChanged := DosSupport("CD", sTargetDir, .T.);
    :IF !bChanged;
        ErrorMes("Failed to change directory to: " + sTargetDir);
        /* Displays on failure;
        :RETURN .F.;
    :ENDIF;

    sCurrentDir := DosSupport("WORKDIR");
    UsrMes("Current import directory: " + sCurrentDir);

    DosSupport("CD", sOriginalDir, .T.);

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ChangeDirectoryForImport");
```

## Related

- [`Directory`](Directory.md)
- [`FileSupport`](FileSupport.md)
- [`LDir`](LDir.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
- [`array`](../types/array.md)
