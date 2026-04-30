---
title: "GetLogsFolder"
summary: "Returns the configured user log folder path with a trailing backslash."
id: ssl.function.getlogsfolder
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetLogsFolder

Returns the configured user log folder path with a trailing backslash.

`GetLogsFolder` returns `AppConfig.Instance.UserLogFolder + "\\"` as a string. The function takes no parameters, performs no validation, and does not check whether the folder exists or is writable. The returned value always ends with a trailing backslash.

## When to use

- When you need the configured log folder path instead of hard-coding one.
- When building a full log-file path by appending a file name.
- When diagnostic or maintenance code needs to inspect files in the log folder.

## Syntax

```ssl
GetLogsFolder()
```

## Parameters

This function takes no parameters.

## Returns

**[string](../types/string.md)** — The configured user log folder path, always with a trailing backslash.

## Best practices

!!! success "Do"
    - Use the returned path as the base folder for log-file reads and writes.
    - Append file names directly, because the returned path already ends with a backslash.
    - Verify folder availability separately when your code depends on the directory existing.

!!! failure "Don't"
    - Append another backslash before adding the file name.
    - Assume the folder exists just because the function returned a string.
    - Use this function as a general application-folder lookup.

## Caveats

- If the configured folder value is empty, the return value is just `\`.
- Any later file-system failure happens in the code that uses the returned path, not in `GetLogsFolder` itself.

## Examples

### Build a log-file path

Use the returned folder path directly when constructing a full file name.

```ssl
:PROCEDURE ShowLogFilePath;
	:DECLARE sLogsFolder, sLogFilePath;

	sLogsFolder := GetLogsFolder();
	sLogFilePath := sLogsFolder + "session.log";

	UsrMes("Log file path: " + sLogFilePath);

	:RETURN sLogFilePath;
:ENDPROC;

/* Usage;
DoProc("ShowLogFilePath");
```

[`UsrMes`](UsrMes.md) displays:

```
Log file path: C:\Logs\session.log
```

### List log files from the configured folder

Use the returned folder path with [`Directory`](Directory.md) to count existing log files.

```ssl
:PROCEDURE CountLogFiles;
	:DECLARE sLogsFolder, aFiles, nCount;

	sLogsFolder := GetLogsFolder();
	aFiles := Directory(sLogsFolder + "*.log");
	nCount := ALen(aFiles);

	UsrMes("Log files found: " + LimsString(nCount));

	:RETURN nCount;
:ENDPROC;

/* Usage;
DoProc("CountLogFiles");
```

[`UsrMes`](UsrMes.md) displays:

```
Log files found: 3
```

### Guard file writes with an explicit path check

Checks whether the returned folder is just `\` (unconfigured) before calling [`WriteText`](WriteText.md), making it easy to distinguish a configuration problem from a file-system error.

```ssl
:PROCEDURE WriteRunMarker;
	:DECLARE sLogsFolder, sMarkerPath;

	sLogsFolder := GetLogsFolder();

	:IF sLogsFolder == "\\";
		ErrorMes("User log folder is not configured");
		:RETURN .F.;
	:ENDIF;

	sMarkerPath := sLogsFolder + "run-marker.txt";
	WriteText(sMarkerPath, "Run started", .F.);

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("WriteRunMarker");
```

## Related

- [`GetAppBaseFolder`](GetAppBaseFolder.md)
- [`GetAppWorkPathFolder`](GetAppWorkPathFolder.md)
- [`GetWebFolder`](GetWebFolder.md)
- [`string`](../types/string.md)
