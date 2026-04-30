---
title: "DocCreateFolder"
summary: "Creates a Documentum folder under a parent path and returns the string result from the create operation."
id: ssl.function.doccreatefolder
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocCreateFolder

Creates a Documentum folder under a parent path and returns the string result from the create operation.

`DocCreateFolder` takes a required parent path, a required folder name, and an optional ACL name. The surfaced SSL function raises immediately only when `sParentPath` or `sFolderName` is [`NIL`](../literals/nil.md). Otherwise it forwards the provided values to the Documentum create call and returns its string result. If that call does not produce a value, the function returns an empty string.

Treat a `""` result as a failed create attempt and check it immediately with [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md).

## When to use

- When you need to create a folder under an existing Documentum path from SSL.
- When your workflow needs the returned create result for later Documentum operations.
- When you need to supply an ACL during folder creation instead of relying on
  backend defaults.

## Syntax

```ssl
DocCreateFolder(sParentPath, sFolderName, [sAcl])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sParentPath` | [string](../types/string.md) | yes | — | Parent Documentum path passed to the create call. |
| `sFolderName` | [string](../types/string.md) | yes | — | Folder name to create under `sParentPath`. |
| `sAcl` | [string](../types/string.md) | no | omitted | Optional ACL name passed when supplied. |

## Returns

**[string](../types/string.md)** — The string returned by the Documentum folder-create call, or an empty string when that call does not return a value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sParentPath` is [`NIL`](../literals/nil.md). | `sParentPath argument cannot be null` |
| `sFolderName` is [`NIL`](../literals/nil.md). | `sFolderName argument cannot be null` |

## Best practices

!!! success "Do"
    - Validate that `sParentPath` and `sFolderName` contain usable values before calling the function.
    - Omit `sAcl` when you do not need to override the backend's default behavior.
    - Check for an empty return immediately, then inspect [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) before making another Documentum call.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sParentPath` or `sFolderName`; those inputs raise an immediate error.
    - Treat an empty returned string as a successful folder create result.
    - Delay error inspection after a failed create attempt. A later Documentum call can overwrite the stored failure state.

## Caveats

- The call is intended for use within an initialized Documentum session.
- `sParentPath` and `sFolderName` are checked only for [`NIL`](../literals/nil.md) at the SSL boundary. Other input validation depends on the backend call.
- When the create operation fails without raising a direct SSL argument error, inspect the current Documentum session with [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) before making another Documentum call.

## Examples

### Create one folder and verify the result

Creates a single folder under a known parent path and checks the Documentum failure state when the return value is empty.

```ssl
:PROCEDURE CreateCustomerCaseFolder;
    :DECLARE sParentPath, sFolderName, sCreateResult;

    sParentPath := "/Cases/CustomerCases";
    sFolderName := "CASE-2024-00142";
    sCreateResult := DocCreateFolder(sParentPath, sFolderName);

    :IF Empty(sCreateResult);
        :IF DocCommandFailed();
            ErrorMes("Folder creation failed: " + DocGetErrorMessage());
            /* Displays on command failure: folder creation failed;
        :ELSE;
            ErrorMes("Folder creation did not return a result string");
        :ENDIF;
        :RETURN "";
    :ENDIF;

    UsrMes("Folder created: " + sCreateResult);
    /* Displays: created folder path;

    :RETURN sCreateResult;
:ENDPROC;

/* Usage;
DoProc("CreateCustomerCaseFolder");
```

### Create several folders with per-folder ACL values

Iterates a list of project names, creates each folder under a shared base path with a project-specific ACL, and collects failure objects for any empty results.

```ssl
:PROCEDURE SetupProjectFolders;
    :DECLARE sBasePath, sProjectName, sAcl, sCreateResult, sFolderPath;
    :DECLARE aProjects, aFailures, oFailure, nIndex;

    sBasePath := "/Projects";
    aProjects := {"Alpha", "Beta", "Gamma"};
    aFailures := {};

    :FOR nIndex := 1 :TO ALen(aProjects);
        sProjectName := aProjects[nIndex];
        sAcl := "Project_" + sProjectName + "_ACL";
        sCreateResult := DocCreateFolder(sBasePath, sProjectName, sAcl);

        :IF Empty(sCreateResult);
            oFailure := CreateUdObject();
            oFailure:folderName := sProjectName;
            :IF DocCommandFailed();
                oFailure:errorMessage := DocGetErrorMessage();
            :ELSE;
                oFailure:errorMessage := "Folder creation returned an empty result string";
            :ENDIF;
            AAdd(aFailures, oFailure);
            :LOOP;
        :ENDIF;

        sFolderPath := sBasePath + "/" + sProjectName;
        UsrMes("Created folder: " + sFolderPath);
        /* Displays per success: created folder path;
    :NEXT;

    :IF ALen(aFailures) > 0;
        ErrorMes("Some folders were not created: " + LimsString(ALen(aFailures)));
        /* Displays when some failed: folder creation summary;
    :ENDIF;

    :RETURN aFailures;
:ENDPROC;

/* Usage;
DoProc("SetupProjectFolders");
```

### Validate inputs and handle both raised and backend failures

Guards against blank path or name inputs, wraps the call in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) to handle a raised SSL exception, and then inspects the Documentum failure state for an empty result.

```ssl
:PROCEDURE CreateDynamicFolder;
    :PARAMETERS sParentPath, sFolderName, sAcl;
    :DEFAULT sParentPath, "/TestCabinet";
    :DEFAULT sFolderName, "";
    :DEFAULT sAcl, "";
    :DECLARE oErr, sCreateResult;

    :IF Empty(sParentPath) .OR. Empty(sFolderName);
        ErrorMes("Folder path and folder name are required");
        :RETURN "";
    :ENDIF;

    :TRY;
        sCreateResult := DocCreateFolder(sParentPath, sFolderName, sAcl);
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("DocCreateFolder raised an error: " + oErr:Description);
        /* Displays when NIL is passed: DocCreateFolder raised an error;
        :RETURN "";
    :ENDTRY;

    :IF Empty(sCreateResult);
        :IF DocCommandFailed();
            ErrorMes("DocCreateFolder failed: " + DocGetErrorMessage());
            /* Displays on command failure: DocCreateFolder failed;
        :ELSE;
            ErrorMes("DocCreateFolder returned an empty result string");
        :ENDIF;
        :RETURN "";
    :ENDIF;

    UsrMes("Folder created successfully: " + sCreateResult);
    /* Displays: created folder result;

    :RETURN sCreateResult;
:ENDPROC;

/* Usage;
DoProc("CreateDynamicFolder", {"/Projects", "CASE-2024-00142", "LabACL"});
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`string`](../types/string.md)
