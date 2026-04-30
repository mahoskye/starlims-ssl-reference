---
title: "GetFileVersion"
summary: "Retrieves the file version string for a specified file path."
id: ssl.function.getfileversion
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetFileVersion

Retrieves the file version string for a specified file path.

`GetFileVersion` accepts one string argument, `sFileName`, and returns the version string reported for that file. The surfaced SSL implementation only adds a null check for `sFileName` and then performs the file-version lookup.

## When to use

- When you need to show the version of a deployed executable or library.
- When you need to compare an installed file against an expected version.
- When you want to collect version details for diagnostics or audit output.

## Syntax

```ssl
GetFileVersion(sFileName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sFileName` | [string](../types/string.md) | yes | — | Path to the file whose version information should be retrieved. |

## Returns

**[string](../types/string.md)** — The file version string returned for `sFileName`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sFileName` is [`NIL`](../literals/nil.md). | `Argument cannot be null.` |

## Best practices

!!! success "Do"
    - Pass a real file path string, not an unset or [`NIL`](../literals/nil.md) value.
    - Wrap calls in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the path may be invalid or unavailable in the current environment.
    - Use this function for files that are expected to carry version information, such as executables and DLLs.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) as `sFileName`. The function explicitly raises an argument-null error.
    - Assume every path is safe to query without error handling when the file location is user-provided or environment-dependent.
    - Use this as a content-inspection function. It is for file version lookup, not for reading file contents.

## Caveats

- Any additional file-system or platform-specific failures depend on the runtime lookup, so handle uncertain paths defensively.

## Examples

### Display the version of a known DLL

Show the version string for a specific file and display it to the user.

```ssl
:PROCEDURE ShowDllVersion;
    :DECLARE sFileName, sVersion;

    sFileName := "C:\\Windows\\System32\\shell32.dll";
    sVersion := GetFileVersion(sFileName);

    UsrMes(sFileName + " version: " + sVersion);
:ENDPROC;

/* Usage;
DoProc("ShowDllVersion");
```

[`UsrMes`](UsrMes.md) displays:

```text
C:\Windows\System32\shell32.dll version: 6.1.7601.23537
```

### Compare a file against an expected version

Check whether a deployed file matches the version your script expects.

```ssl
:PROCEDURE CheckExpectedVersion;
    :DECLARE sFileName, sExpectedVersion, sActualVersion;

    sFileName := GetAppBaseFolder() + "starlims.exe";
    sExpectedVersion := "11.0.0.0";
    sActualVersion := GetFileVersion(sFileName);

    :IF sActualVersion == sExpectedVersion;
        UsrMes("Version check passed for " + sFileName);
        :RETURN .T.;
    :ENDIF;

    /* Displays on mismatch: version mismatch message;
    UsrMes(
        "Version mismatch for " + sFileName + ": expected "
        + sExpectedVersion + ", got " + sActualVersion
    );
    :RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("CheckExpectedVersion");
```

### Audit several files with error handling

Collect version information for multiple files and continue even if one lookup fails.

```ssl
:PROCEDURE AuditFileVersions;
    :DECLARE aFileNames, aReport, nIndex, sFileName, sVersion, oErr;

    aFileNames := {
        GetAppBaseFolder() + "starlims.exe",
        GetAppBaseFolder() + "lims.dll",
        "C:\\Windows\\System32\\shell32.dll"
    };
    aReport := {};

    :FOR nIndex := 1 :TO ALen(aFileNames);
        sFileName := aFileNames[nIndex];

        :TRY;
            sVersion := GetFileVersion(sFileName);
            AAdd(aReport, {sFileName, sVersion, "OK"});
        :CATCH;
            oErr := GetLastSSLError();
            AAdd(aReport, {sFileName, oErr:Description, "ERROR"});
        :ENDTRY;
    :NEXT;

    :RETURN aReport;
:ENDPROC;

/* Usage;
DoProc("AuditFileVersions");
```

## Related

- [`GetAppBaseFolder`](GetAppBaseFolder.md)
- [`GetSetting`](GetSetting.md)
- [`string`](../types/string.md)
