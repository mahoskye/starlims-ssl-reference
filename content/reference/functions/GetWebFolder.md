---
title: "GetWebFolder"
summary: "Returns the current web folder path as a string."
id: ssl.function.getwebfolder
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetWebFolder

Returns the current web folder path as a string.

`GetWebFolder` takes no parameters and returns the web folder path exposed by the current application context. The function does not validate the path, check whether the folder exists, or normalize the returned string for you.

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

**[string](../types/string.md)** — The current web folder path.

## Best practices

!!! success "Do"
    - Use `GetWebFolder` when you need the configured web-root path rather than a hard-coded location.
    - Verify the returned value before using it in later file operations.
    - Normalize path separators in your own code if you need to append relative paths safely.

!!! failure "Don't"
    - Hard-code the web folder path in scripts.
    - Assume the returned folder exists or is writable just because the function returned a string.
    - Use `GetWebFolder` for work or log storage when [`GetAppWorkPathFolder`](GetAppWorkPathFolder.md) or [`GetLogsFolder`](GetLogsFolder.md) is the better match.

## Caveats

- Any separator handling or path normalization must be done by the caller.

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
```

Call it with `DoProc("ShowWebFolder")`.

### Build a file path under the web folder

Check the returned folder value, add a separator only when needed, and then append a relative asset path.

```ssl
:PROCEDURE GetAssetPath;
	:DECLARE sWebFolder, sLastChar, sSeparator, sAssetPath;

	sWebFolder := GetWebFolder();

	:IF Empty(sWebFolder);
		ErrorMes("GetWebFolder", "Web folder is not available");
		:RETURN "";
	:ENDIF;

	sLastChar := sWebFolder[Len(sWebFolder)];
	sSeparator := "";

	:IF !(sLastChar $ "/\\");
		sSeparator := "\\";
	:ENDIF;

	sAssetPath := sWebFolder + sSeparator + "assets\\report_template.html";

	:RETURN sAssetPath;
:ENDPROC;
```

Call it with `DoProc("GetAssetPath")`.

### Choose the correct root for published output

Compare the web folder with other folder helpers so published output goes under the web root and not under the work or log folders.

```ssl
:PROCEDURE ResolvePublishedOutputPath;
	:DECLARE sWebFolder, sWorkFolder, sLogsFolder, sLastChar;
	:DECLARE sSeparator, sOutputPath;

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

	sLastChar := sWebFolder[Len(sWebFolder)];
	sSeparator := "";

	:IF !(sLastChar $ "/\\");
		sSeparator := "\\";
	:ENDIF;

	sOutputPath := sWebFolder + sSeparator + "downloads\\daily-report.txt";

	:RETURN sOutputPath;
:ENDPROC;
```

Call it with `DoProc("ResolvePublishedOutputPath")`.

## Related

- [`GetAppBaseFolder`](GetAppBaseFolder.md)
- [`GetAppWorkPathFolder`](GetAppWorkPathFolder.md)
- [`GetLogsFolder`](GetLogsFolder.md)
- [`string`](../types/string.md)
