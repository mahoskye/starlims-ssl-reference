---
title: "GetAppWorkPathFolder"
summary: "Returns the path to the application's working directory as a string."
id: ssl.function.getappworkpathfolder
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetAppWorkPathFolder

Returns the path to the application's working directory as a string.

`GetAppWorkPathFolder` returns the configured path to the application's working directory. It takes no arguments and always returns the same value within a given run. The path is not validated for existence or accessibility.

## When to use

- When you need a central location for storing application-generated temporary or intermediate files that should not mix with persistent data.
- When building features that require referencing the application’s own workspace directory, such as processing exports, intermediate computations, or caches.
- When deploying your application to different environments (development, test, production) and need to dynamically locate the correct working directory without hardcoding paths.
- When writing reusable modules or libraries that must interact with a safe, application-approved workspace for file operations.
- When you wish to centralize cleanup routines for files generated during processing, by referencing the dedicated work folder.

## Syntax

```ssl
GetAppWorkPathFolder()
```

## Parameters

This function takes no parameters.

## Returns

**[string](../types/string.md)** — The application work path folder configured in the system.

## Best practices

!!! success "Do"
    - Always check file system permissions before writing to the returned folder.
    - Use this function whenever you need a central, application-defined location for workspace files.

!!! failure "Don't"
    - Assume the work path folder is always accessible or exists.
    - Hardcode a path for temporary or intermediate files in your logic.

## Caveats

- The returned path may use different formats (trailing slash, drive letters) depending on operating system or configuration.

## Examples

### Write a temporary file to the work folder

Demonstrate how to use the work path folder to save a temporary export or intermediate result.

```ssl
:PROCEDURE SaveTempExport;
	:DECLARE sWorkPath, sFileName, sFilePath, nData;

	sWorkPath := GetAppWorkPathFolder();
	sFileName := "temp_export_001.txt";
	sFilePath := sWorkPath + sFileName;
	nData := 42;

	WriteText(sFilePath, LimsString(nData), .F.);

	UsrMes("Temporary export saved to: " + sFilePath);
:ENDPROC;

/* Usage;
DoProc("SaveTempExport");
```

[`UsrMes`](UsrMes.md) displays:

```
Temporary export saved to: C:\STARLIMS\Work\temp_export_001.txt
```

### Validate the work path before performing file operations

Check that the work path is non-empty and verify whether a specific file is present before acting on it.

```ssl
:PROCEDURE ValidateWorkPathForFileOps;
	:DECLARE sWorkPath, sTestFile;

	sWorkPath := GetAppWorkPathFolder();

	:IF Empty(sWorkPath);
		ErrorMes("Work path is empty - cannot proceed");
		:RETURN .F.;
	:ENDIF;

	InfoMes("Work path is: " + sWorkPath);
	/* Displays the configured work path;

	sTestFile := sWorkPath + "\config.xml";

	:IF FileSupport(sTestFile, "CHECK");
		InfoMes("Config file exists at: " + sTestFile);
		/* Displays when the config file exists;
	:ELSE;
		InfoMes("Config file not found (normal for new installs)");
	:ENDIF;

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ValidateWorkPathForFileOps");
```

## Related

- [`GetAppBaseFolder`](GetAppBaseFolder.md)
- [`GetLogsFolder`](GetLogsFolder.md)
- [`GetWebFolder`](GetWebFolder.md)
- [`string`](../types/string.md)
