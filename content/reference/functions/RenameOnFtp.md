---
title: "RenameOnFtp"
summary: "Renames a remote file on an FTP server, or on an SFTP server when bIsSFTP is .T.."
id: ssl.function.renameonftp
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# RenameOnFtp

Renames a remote file on an FTP server, or on an SFTP server when `bIsSFTP` is [`.T.`](../literals/true.md).

`RenameOnFtp` renames a file within the same remote directory. On both the FTP and SFTP paths, the implementation delegates to the corresponding move helper with the same source and target directory and a different target file name.

The function validates `sServerNameOrIP`, `sFileNameOld`, `sFileNameNew`, and `sProxy` before attempting the rename. It also rejects renames where the trimmed new and old file names are the same ignoring case. If those validations pass, the function returns [`.T.`](../literals/true.md) only when the underlying move completes. Otherwise, it returns [`.F.`](../literals/false.md).

On the SFTP path, connection, login, and private-key setup happen inside helper calls before the function reaches its normal [`.F.`](../literals/false.md) return path, so some SFTP failures can still raise instead of returning [`.F.`](../literals/false.md).

## When to use

- When a workflow needs to rename a file already present on an FTP or SFTP server.
- When a downstream integration expects a processed or archived file name in the same remote folder.
- When you want one API that can target either FTP or SFTP based on `bIsSFTP`.

## Syntax

```ssl
RenameOnFtp(sServerNameOrIP, [sRemoteDirectory], sFileNameOld, sFileNameNew, [sUserName], [sPassword], [nPort], [sProxy], [bIsSFTP], [sPrivateKeyFilePath])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sServerNameOrIP` | [string](../types/string.md) | yes | — | Remote server name or IP address. |
| `sRemoteDirectory` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Remote directory that contains the file. The same directory is used for both the source and target path. |
| `sFileNameOld` | [string](../types/string.md) | yes | — | Existing remote file name to rename. |
| `sFileNameNew` | [string](../types/string.md) | yes | — | New remote file name to apply in the same directory. |
| `sUserName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | User name passed to the FTP or SFTP login step. |
| `sPassword` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Password for password-based login. On the SFTP path, this value is also used as the private-key passphrase when `sPrivateKeyFilePath` is supplied. |
| `nPort` | [number](../types/number.md) | no | `21` | Server port. If omitted or non-positive, the implementation uses `21`, even on the SFTP path. |
| `sProxy` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Must be left empty. Supplying a non-empty value raises an error. |
| `bIsSFTP` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Set to [`.T.`](../literals/true.md) to use the SFTP implementation. Omitted or [`NIL`](../literals/nil.md) keeps the FTP implementation. |
| `sPrivateKeyFilePath` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Optional private key file for SFTP authentication. Ignored on the FTP path. |

## Returns

**[boolean](../types/boolean.md)** - [`.T.`](../literals/true.md) when the rename completes; [`.F.`](../literals/false.md) when the underlying FTP or SFTP move helper cannot complete the rename.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sServerNameOrIP` is empty on the FTP path. | `FTP server name or IP cannot be missing.` |
| `sServerNameOrIP` is empty on the SFTP path. | `SFTP server name or IP cannot be missing.` |
| `sFileNameOld` is empty. | `Old file name cannot be null or empty.` |
| `sFileNameNew` is empty. | `New file name cannot be null or empty.` |
| The trimmed names match ignoring case. | `New file name cannot be the same as old file name.` |
| `sProxy` is non-empty. | `The proxy parameter cannot be used. The system will automatically use the proxy specified by Internet Explorer > Local Area Network settings.` |

## Best practices

!!! success "Do"
    - Pass distinct old and new file names after normalizing any workflow-specific spacing or casing.
    - Leave `sProxy` empty and rely on the system proxy configuration.
    - Set `bIsSFTP` explicitly to [`.T.`](../literals/true.md) only when the target server really expects SFTP.
    - Wrap SFTP renames in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) when connection or authentication failures should be handled gracefully.
    - Verify the target file after a business-critical rename when the workflow needs confirmation beyond the boolean result.

!!! failure "Don't"
    - Assume the function can move a file to a different folder. It renames within the same `sRemoteDirectory` only.
    - Pass a manual proxy value. Any non-empty `sProxy` argument raises an error.
    - Assume the SFTP path converts every failure to [`.F.`](../literals/false.md). Early connection, login, or key-loading failures can still raise.
    - Reuse the same file name with only casing or surrounding spaces changed. The function rejects that as the same name.

## Caveats

- Rename is performed as a move within the same directory, so a failed operation can occur after partial progress has already been made.

## Examples

### Rename a processed file in an FTP inbox

Rename one file in place after a workflow step completes.

```ssl
:PROCEDURE RenameProcessedFile;
    :DECLARE sServer, sRemoteDir, sOldName, sNewName, sUser, sPassword;
    :DECLARE bRenamed;

    sServer := "ftp.lab.example.com";
    sRemoteDir := "/incoming/results";
    sOldName := "batch_1027.tmp";
    sNewName := "batch_1027.ready";
    sUser := "labupload";
    sPassword := "SecurePass123";

    bRenamed := RenameOnFtp(
        sServer,
        sRemoteDir,
        sOldName,
        sNewName,
        sUser,
        sPassword
    );

    :IF bRenamed;
        /* Displays the old and new file names;
        UsrMes("Renamed " + sOldName + " to " + sNewName);
    :ELSE;
        /* Displays the source file name on failure;
        ErrorMes("Could not rename " + sOldName);
    :ENDIF;

    :RETURN bRenamed;
:ENDPROC;

/* Usage;
DoProc("RenameProcessedFile");
```

### Check for the original file before renaming

Verify the source file exists before attempting the rename and handle a normal failure result separately.

```ssl
:PROCEDURE ArchivePartnerDrop;
    :DECLARE sServer, sRemoteDir, sOldName, sNewName, sUser, sPassword;
    :DECLARE bExists, bRenamed;

    sServer := "ftp.partner.example.com";
    sRemoteDir := "/dropzone/outbound";
    sOldName := "shipment_20260419.csv";
    sNewName := "shipment_20260419.archived.csv";
    sUser := "partneruser";
    sPassword := "PartnerPass456";

    bExists := CheckOnFtp(
        sServer,
        sRemoteDir,
        sOldName,
        sUser,
        sPassword
    );

    :IF .NOT. bExists;
        UsrMes("Source file is not available for rename.");
        :RETURN .F.;
    :ENDIF;

    bRenamed := RenameOnFtp(
        sServer,
        sRemoteDir,
        sOldName,
        sNewName,
        sUser,
        sPassword
    );

    :IF .NOT. bRenamed;
        /* Displays the file name when the rename fails;
        ErrorMes("Rename failed for " + sOldName);
        :RETURN .F.;
    :ENDIF;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ArchivePartnerDrop");
```

### Rename over SFTP with key-based authentication and verify the result

Use the SFTP path, handle raised connection or authentication errors, and then confirm the renamed file exists.

```ssl
:PROCEDURE PromoteInstrumentFile;
    :DECLARE sServer, sRemoteDir, sOldName, sNewName, sUser, sPassphrase;
    :DECLARE sPrivateKey, oErr;
    :DECLARE nPort;
    :DECLARE bIsSFTP, bRenamed, bVerified;

    sServer := "sftp.instrument.example.com";
    sRemoteDir := "/runs/completed";
    sOldName := "run_20260419_01.pending";
    sNewName := "run_20260419_01.ready";
    sUser := "instrumentbot";
    sPassphrase := "KeyPassphrase789";
    sPrivateKey := "/etc/ssl/keys/instrumentbot.ppk";
    nPort := 22;
    bIsSFTP := .T.;

    :TRY;
        bRenamed := RenameOnFtp(
            sServer,
            sRemoteDir,
            sOldName,
            sNewName,
            sUser,
            sPassphrase,
            nPort,, bIsSFTP,
            sPrivateKey
        );

    :CATCH;
        oErr := GetLastSSLError();
        /* Displays the SFTP client failure;
        ErrorMes("SFTP rename failed: " + oErr:Description);
        :RETURN .F.;
    :ENDTRY;

    :IF .NOT. bRenamed;
        ErrorMes("Remote rename did not complete.");
        :RETURN .F.;
    :ENDIF;

    bVerified := CheckOnFtp(
        sServer,
        sRemoteDir,
        sNewName,
        sUser,
        sPassphrase,
        nPort,, bIsSFTP,
        sPrivateKey
    );

    :IF .NOT. bVerified;
        ErrorMes("Rename succeeded but the new file name could not be verified.");
        :RETURN .F.;
    :ENDIF;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("PromoteInstrumentFile");
```

## Related

- [`CheckOnFtp`](CheckOnFtp.md)
- [`MoveInFtp`](MoveInFtp.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
