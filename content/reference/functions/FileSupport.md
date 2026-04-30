---
title: "FileSupport"
summary: "Performs multiple file operations through a single request-driven interface."
id: ssl.function.filesupport
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# FileSupport

Performs multiple file operations through a single request-driven interface.

`FileSupport` works in two modes. Path-based requests operate on a file path, while handle-based requests operate on a numeric file handle returned by `CREATE` or `OPEN`. The `sEncoding` argument defaults to `"UTF8"` and is used when a file handle is created or opened.

Supported request families are `CHECK`, `SETATTR`, `GETATTR`, `CREATE`, `OPEN`, `CLOSE`, `READ`, `READBLK`, `WRITE`, `BOF`, `EOF`, `TELL`, `SEEK`, `RESIZE`, `COPY`, `DELETE`, `MOVE`, `RENAME`, `PATH`, `FOLDERNAME`, `FILENAME`, `NAME`, `EXT`, `SIZE`, `DATE`, `TIME`, and `DIR`.

The implementation matches `sRequest` by case-insensitive leading text. Use the canonical request names above to avoid accidental matches.

## When to use

- When you need low-level file-handle operations such as `OPEN`, `READ`, `WRITE`, `SEEK`, and `CLOSE`.
- When you need one API that can both inspect file metadata and perform file system actions such as `COPY`, `MOVE`, `DELETE`, and `DIR`.
- When you need path parsing helpers such as `PATH`, `FILENAME`, `NAME`, or `EXT`.
- When you need to control the text encoding used for a created or opened file handle.

## Syntax

```ssl
FileSupport(vFileIdentifier, sRequest, [vArg1], [sArg2], [sEncoding])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vFileIdentifier` | [string](../types/string.md) or [number](../types/number.md) | yes | — | Path for path-based requests, or numeric file handle for handle-based requests. `CLOSE`, `READ`, `READBLK`, `WRITE`, `BOF`, `EOF`, `TELL`, `SEEK`, and `RESIZE` expect a handle. Most other requests expect a path. |
| `sRequest` | [string](../types/string.md) | yes | — | Request name that selects the operation. Use the canonical names shown above. |
| `vArg1` | any | no | [`NIL`](../literals/nil.md) | Request-specific argument. Examples: access mode for `OPEN`, byte count for `READ`, delimiter for `READBLK`, text to write for `WRITE`, offset for `SEEK`, new size for `RESIZE`, destination path for `COPY` / `MOVE` / `RENAME`, and attribute letter for `SETATTR`. |
| `sArg2` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Secondary request-specific string. Used as the share mode for `OPEN` and the origin for `SEEK`. Other requests generally ignore it. |
| `sEncoding` | [string](../types/string.md) | no | `UTF8` | Text encoding used when `CREATE` or `OPEN` registers a file handle. |

## Returns

**any** — The return type depends on `sRequest`.

| Request | Return type | Behavior |
|---------|-------------|----------|
| `CHECK` | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the file exists, otherwise [`.F.`](../literals/false.md). |
| `SETATTR` | [string](../types/string.md) | Sets one attribute flag and returns `""`. If the file does not exist, nothing is changed and the function still returns `""`. |
| `GETATTR` | [string](../types/string.md) | Returns a compact attribute string composed from `A`, `H`, `N`, `R`, and `S` when those flags are present. |
| `CREATE` | [number](../types/number.md) | Creates the file and returns a numeric handle. |
| `OPEN` | [number](../types/number.md) | Opens an existing file and returns a numeric handle. `vArg1` selects access mode and `sArg2` selects share mode. |
| `CLOSE` | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the handle is closed and unregistered, otherwise [`.F.`](../literals/false.md). |
| `READ` | [string](../types/string.md) | Reads `vArg1` characters from the current position. If fewer characters are available, the result is padded on the right with spaces to the requested length. |
| `READBLK` | [string](../types/string.md) | Reads from the current position until `vArg1` is found. If `vArg1` is omitted, the delimiter defaults to `";"`. The delimiter is not included in the returned text. |
| `WRITE` | [number](../types/number.md) | Writes the text from `vArg1` at the current position and returns the number of characters written. |
| `BOF` | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the handle position is at or before the beginning of the file. |
| `EOF` | [boolean](../types/boolean.md) | Returns [`.T.`](../literals/true.md) when the handle position is exactly at end of file. |
| `TELL` | [number](../types/number.md) | Returns the current file position. |
| `SEEK` | [number](../types/number.md) | Moves the handle position and returns the new position. `sArg2` may begin with `TOP`, `BOTTOM`, or `RELATIVE`; omitted means `TOP`. A seek before beginning of file returns `-1`. |
| `RESIZE` | [number](../types/number.md) | Sets the file length to `vArg1` and returns the new size. |
| `COPY` | [boolean](../types/boolean.md) | Copies the source file to the destination path in `vArg1`, overwriting an existing target if present. |
| `DELETE` | [boolean](../types/boolean.md) | Deletes the file. Returns [`.F.`](../literals/false.md) when the file does not exist or deletion fails. |
| `MOVE`, `RENAME` | [boolean](../types/boolean.md) | Moves the source file to the destination path in `vArg1`. `RENAME` uses the same implementation as `MOVE`. |
| `PATH` | [string](../types/string.md) | Returns the full path for `vFileIdentifier`. |
| `FOLDERNAME` | [string](../types/string.md) | Returns the containing directory path. |
| `FILENAME` | [string](../types/string.md) | Returns the file name with extension. |
| `NAME` | [string](../types/string.md) | Returns the file name without extension. |
| `EXT` | [string](../types/string.md) | Returns the extension, including the leading period when present. |
| `SIZE` | [number](../types/number.md) | Returns the file length in bytes. |
| `DATE` | [date](../types/date.md) | Returns the file's last-write date value. |
| `TIME` | [date](../types/date.md) | Returns the file's last-write timestamp converted to UTC. |
| `DIR` | [array](../types/array.md) | Returns an array of rows. Each row contains `{name, size, lastWriteDate, lastWriteTimeText, attributes}` for visible files that match the path pattern. Hidden files are excluded. |

For `OPEN`, the observed request-specific values are:

- `vArg1`: access mode beginning with `R` for read, `W` for write, or omitted for read/write.
- `sArg2`: share mode `R`, `W`, `RW`, or `EXC`. Omitted defaults to read-share.

For `SETATTR`, only the first non-space character is used. The supported values are `A`, `H`, `N`, `R`, and `S`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `vFileIdentifier` is [`NIL`](../literals/nil.md). | `Fileidentifier is mandatory!` |
| `vFileIdentifier` is neither a string nor a number. | `Request argument does not contain a string/numeric!` |
| `sRequest` is [`NIL`](../literals/nil.md). | `Request is mandatory!` |
| `sRequest` is not a string. | `Request argument does not contain a string!` |
| `sEncoding` is provided but is not a string. | `Argument: <encoding> must be of type string.` |
| `sRequest` does not match any supported request family. | `Invalid request provided!` |
| The byte count for `READ` is negative. | `Read size expected positive or 0` |
| `CHECK`, `SETATTR`, `GETATTR`, `CREATE`, `OPEN`, `COPY`, `DELETE`, `MOVE`, `RENAME`, or `DIR` targets a path outside the configured whitelist. | `Access to folder/file {path} is denied. If system needs access to this folder/file please ask the System Administrator to add the item to WhitelistFolders setting in the configuration file.` |

## Best practices

!!! success "Do"
    - Use `CREATE` or `OPEN` first, keep the returned handle, and close it with `CLOSE` when you finish.
    - Use the canonical request names such as `"READ"`, `"WRITE"`, and `"SEEK"` even though the implementation matches by leading text.
    - Check the boolean result from `COPY`, `DELETE`, `MOVE`, `RENAME`, and `CLOSE` before assuming the operation succeeded.
    - Wrap path-based operations in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the target path may fall outside the configured whitelist.

!!! failure "Don't"
    - Pass a file path to handle-based requests such as `READ` or `WRITE`, or a handle to path-based requests such as `COPY` or `DIR`.
    - Assume `READ` returns a short string at end of file. It pads the result with spaces when fewer characters are available.
    - Treat `RENAME` as a metadata-only rename. It uses the same move logic as `MOVE` and therefore depends on a destination path.
    - Rely on non-canonical request prefixes in published code just because the implementation accepts leading-text matches.

## Caveats

- `DIR` returns files only. Unlike [`Directory`](Directory.md), it does not expose attribute filtering and does not include hidden files.
- Using the wrong argument type for a specific request can raise a runtime type error before the underlying file operation runs.

## Examples

### Create a file, write text, and close it

Use a created handle for sequential write operations.

```ssl
:PROCEDURE WriteAuditNote;
	:DECLARE sFilePath, nHandle, nWritten, bClosed;

	sFilePath := "C:\STARLIMS\Exports\audit_note.txt";
	nHandle := FileSupport(sFilePath, "CREATE");

	nWritten := FileSupport(
		nHandle,
		"WRITE",
		"Audit export started on " + DToC(Today())
	);

	bClosed := FileSupport(nHandle, "CLOSE");

	:IF !bClosed;
		ErrorMes("Failed to close audit_note.txt");
		:RETURN .F.;
	:ENDIF;

	UsrMes("Characters written: " + LimsString(nWritten));
	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("WriteAuditNote");
```

### Open an existing file and read blocks until EOF

Read a delimited text file one block at a time with a handle opened for read access.

```ssl
:PROCEDURE ReadPipeDelimitedValues;
	:DECLARE sFilePath, nHandle, sValue, aValues, bClosed;

	sFilePath := "C:\STARLIMS\Imports\values.txt";
	aValues := {};
	nHandle := FileSupport(sFilePath, "OPEN", "R", "R");

	:WHILE !FileSupport(nHandle, "EOF");
		sValue := FileSupport(nHandle, "READBLK", "|");
		AAdd(aValues, sValue);
	:ENDWHILE;

	bClosed := FileSupport(nHandle, "CLOSE");

	:IF !bClosed;
		ErrorMes("Failed to close values.txt");
		:RETURN {};
	:ENDIF;

	:RETURN aValues;
:ENDPROC;

/* Usage;
DoProc("ReadPipeDelimitedValues");
```

### Copy a file and verify the destination metadata

Combine a path-based write operation with metadata checks and error handling.

```ssl
:PROCEDURE CopyApprovedReport;
	:DECLARE sSourcePath, sDestPath, bCopied, nBytes, sFileName, oErr;

	sSourcePath := "C:\STARLIMS\Reports\approved.pdf";
	sDestPath := "C:\STARLIMS\Archive\approved.pdf";

	:TRY;
		bCopied := FileSupport(sSourcePath, "COPY", sDestPath);
		:IF !bCopied;
			ErrorMes("Copy failed for approved report");
			:RETURN .F.;
		:ENDIF;

		nBytes := FileSupport(sDestPath, "SIZE");
		sFileName := FileSupport(sDestPath, "FILENAME");

		UsrMes(
			"Copied " + sFileName + " with size " + LimsString(nBytes)
		);
		/* Displays copied file details;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("FileSupport error: " + oErr:Description);
		/* Displays on failure: FileSupport error;
		:RETURN .F.;
	:ENDTRY;

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("CopyApprovedReport");
```

## Related

- [`Directory`](Directory.md)
- [`DosSupport`](DosSupport.md)
- [`GetLastSSLError`](GetLastSSLError.md)
- [`LDir`](LDir.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
- [`boolean`](../types/boolean.md)
- [`array`](../types/array.md)
- [`date`](../types/date.md)
