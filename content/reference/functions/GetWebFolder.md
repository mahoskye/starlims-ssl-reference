---
title: "GetWebFolder"
summary: "Returns the current web folder path as a string."
id: ssl.function.getwebfolder
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# GetWebFolder

Returns the current web folder path as a string.

`GetWebFolder` takes no parameters and returns the web folder path exposed by the current application context. The returned path ends with a backslash. The function does not validate the path or check whether the folder exists.

## When to use

- When you need the configured web-root path instead of hard-coding one.
- When building paths for files that should live under the application's web folder.
- When you need to distinguish the web folder from the work folder or log folder.

## Syntax

```ssl
GetWebFolder()
```

## Parameters

This function takes no parameters.

## Returns

**[string](../types/string.md)** — The current web folder path, ending with a backslash.

## Best practices

!!! success "Do"
    - Use `GetWebFolder` when you need the configured web-root path rather than a hard-coded location.
    - Verify the returned value before using it in later file operations.
    - Append relative paths directly, because the returned path already ends with a backslash.

!!! failure "Don't"
    - Hard-code the web folder path in scripts.
    - Assume the returned folder exists or is writable just because the function returned a string.
    - Use `GetWebFolder` for work or log storage when [`GetAppWorkPathFolder`](GetAppWorkPathFolder.md) or [`GetLogsFolder`](GetLogsFolder.md) is the better match.

## Caveats

- The returned path already ends with a backslash, so adding another separator before a relative path produces a doubled backslash.

## Examples

### Show the configured web folder

Retrieve the current web folder path and display it.

```ssl
:PROCEDURE ShowWebFolder;
	:DECLARE sWebFolder;

	sWebFolder := GetWebFolder();

	:IF Empty(sWebFolder);
		ErrorMes("GetWebFolder", "Web folder is not available");
		:RETURN "";
	:ENDIF;

	UsrMes("Web folder", sWebFolder);

	:RETURN sWebFolder;
:ENDPROC;

/* Usage;
DoProc("ShowWebFolder");
```

### Build a file path under the web folder

Check the returned folder value, then append a relative asset path. The folder already ends with a backslash, so no separator is added.

```ssl
:PROCEDURE GetAssetPath;
	:DECLARE sWebFolder, sAssetPath;

	sWebFolder := GetWebFolder();

	:IF Empty(sWebFolder);
		ErrorMes("GetWebFolder", "Web folder is not available");
		:RETURN "";
	:ENDIF;

	sAssetPath := sWebFolder + "assets\report_template.html";

	:RETURN sAssetPath;
:ENDPROC;

/* Usage;
DoProc("GetAssetPath");
```

### Choose the correct root for published output

Compare the web folder with other folder helpers so published output goes under the web root and not under the work or log folders.

```ssl
:PROCEDURE ResolvePublishedOutputPath;
	:DECLARE sWebFolder, sWorkFolder, sLogsFolder, sOutputPath;

	sWebFolder := GetWebFolder();
	sWorkFolder := GetAppWorkPathFolder();
	sLogsFolder := GetLogsFolder();

	:IF Empty(sWebFolder);
		ErrorMes("GetWebFolder", "Web folder is not available");
		:RETURN "";
	:ENDIF;

	:IF sWebFolder == sWorkFolder .OR. sWebFolder == sLogsFolder;
		UsrMes("Configuration", "Review folder configuration before publishing files");
	:ENDIF;

	sOutputPath := sWebFolder + "downloads\daily-report.txt";

	:RETURN sOutputPath;
:ENDPROC;

/* Usage;
DoProc("ResolvePublishedOutputPath");
```

## Related

- [`GetAppBaseFolder`](GetAppBaseFolder.md)
- [`GetAppWorkPathFolder`](GetAppWorkPathFolder.md)
- [`GetLogsFolder`](GetLogsFolder.md)
- [`string`](../types/string.md)
