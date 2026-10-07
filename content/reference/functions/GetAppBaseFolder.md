---
title: "GetAppBaseFolder"
summary: "Returns the application's base folder path as a string for use in file and configuration operations."
id: ssl.function.getappbasefolder
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [12]
---

# GetAppBaseFolder

Returns the application's base folder path as a string for use in file and configuration operations.

`GetAppBaseFolder` returns the root directory path configured for the current application context. It takes no arguments and always returns the same value within a given run. The returned path ends with a backslash, so append a relative folder or file name directly instead of adding another separator.

## When to use

- When you need a reliable reference to the root directory for your application's files or settings.
- When dynamically building absolute paths for file access, configuration storage, or file system operations.
- When writing utilities or scripts that depend on a static base directory instead of hardcoded paths.
- When integrating with other system utilities that require knowledge of the main application folder.

## Syntax

```ssl
GetAppBaseFolder()
```

## Parameters

This function takes no parameters.

## Returns

**[string](../types/string.md)** — The base folder path configured for the application context, ending with a backslash.

## Best practices

!!! success "Do"
    - Always verify that the returned path is not empty before using it for critical file system operations.
    - Use this function for the root folder only; use related functions for specialized directories like logs or web content.
    - Cache the result if called repeatedly within the same context.

!!! failure "Don't"
    - Assume the path is always correctly set in configuration. Configuration errors or missing entries can result in empty or wrong paths, causing downstream failures.
    - Rely on it as a catch-all for every folder. Specialized functions return more accurate paths for their domain and improve code clarity.
    - Call the function on every file operation if the folder is not expected to change. Reduces redundant configuration reads and potential performance impact.

## Caveats

- This function does not check if the returned folder actually exists on disk; using an invalid path will result in errors later.

## Examples

### Build a path for file uploads under the application root

Use the application's base folder to store user-uploaded files.

```ssl
:PROCEDURE SetupUserUploadFolder;
	:DECLARE sAppBasePath, sUploadFolder, sFullPath;

	sAppBasePath := GetAppBaseFolder();
	sUploadFolder := "UserUploads";
	sFullPath := sAppBasePath + sUploadFolder;

	UsrMes("Upload folder path: " + sFullPath);

	:RETURN sFullPath;
:ENDPROC;

/* Usage;
DoProc("SetupUserUploadFolder");
```

[`UsrMes`](UsrMes.md) logs the full path, where `<app-folder>` stands for the application base folder in your environment:

```text
Upload folder path: <app-folder>\UserUploads
```

### Build a dynamic path to read a configuration file

Combine the application base folder with relative paths to read configuration files.

```ssl
:PROCEDURE ReadConfigFile;
	:DECLARE sBaseFolder, sConfigRelative, sFullPath, sContent;

	sBaseFolder := GetAppBaseFolder();
	sConfigRelative := "config\application.cfg";
	sFullPath := sBaseFolder + sConfigRelative;

	:IF !FileSupport(sFullPath, "CHECK");
		ErrorMes("Configuration file not found at: " + sFullPath);

		:RETURN "";
	:ENDIF;

	sContent := ReadText(sFullPath);
	UsrMes("Configuration loaded from: " + sFullPath);

	:RETURN sContent;
:ENDPROC;

/* Usage;
DoProc("ReadConfigFile");
```

## Related

- [`GetAppWorkPathFolder`](GetAppWorkPathFolder.md)
- [`GetLogsFolder`](GetLogsFolder.md)
- [`GetWebFolder`](GetWebFolder.md)
- [`string`](../types/string.md)
