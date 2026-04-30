---
title: "MoveInFtp"
summary: "Moves a remote file on an FTP server, or on an SFTP server when bIsSFTP is .T.."
id: ssl.function.moveinftp
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# MoveInFtp

Moves a remote file on an FTP server, or on an SFTP server when `bIsSFTP` is [`.T.`](../literals/true.md).

Use `MoveInFtp` when you need to relocate a file to another remote directory, rename it during the move, or do both in one call. The move returns [`.T.`](../literals/true.md) only when the source file is retrieved, the target file is written, and the source file is then removed. If any of those steps fails, the function returns [`.F.`](../literals/false.md).

Only `sRemoteFileTo` has a built-in fallback: when it is empty, the function reuses `sRemoteFileFrom`. `sRemoteDirectoryTo` is passed through as provided; it does not automatically fall back to `sRemoteDirectoryFrom`.

## When to use

- When a workflow needs to archive an incoming file after processing.
- When you need to rename a remote file while moving it to a new folder.
- When the same integration must work against either FTP or SFTP, selected by `bIsSFTP`.
- When you want a simple success or failure result for a remote move step.

## Syntax

```ssl
MoveInFtp(sServerNameOrIP, [sRemoteDirectoryFrom], [sRemoteDirectoryTo], sRemoteFileFrom, [sRemoteFileTo], [sUserName], [sPassword], [nPort], [sProxy], [bIsSFTP], [sPrivateKeyFilePath])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sServerNameOrIP` | [string](../types/string.md) | yes | — | Remote server name or IP address. |
| `sRemoteDirectoryFrom` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Source directory portion of the remote path. Empty values are passed through to the underlying FTP or SFTP download step. |
| `sRemoteDirectoryTo` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Target directory portion of the remote path. Empty values are passed through as-is; this parameter does not automatically reuse `sRemoteDirectoryFrom`. |
| `sRemoteFileFrom` | [string](../types/string.md) | yes | — | Source remote file name. |
| `sRemoteFileTo` | [string](../types/string.md) | no | `sRemoteFileFrom` | Target remote file name. When omitted or empty, the source file name is reused. |
| `sUserName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | User name passed to the FTP or SFTP login operation. |
| `sPassword` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Password for password-based login. On the SFTP path, this is also used as the private-key passphrase when `sPrivateKeyFilePath` is supplied. |
| `nPort` | [number](../types/number.md) | no | `21` | Server port. If omitted or non-positive, the implementation uses `21`, even on the SFTP path. |
| `sProxy` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Must be left empty. Supplying a non-empty value raises an error. |
| `bIsSFTP` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Set to [`.T.`](../literals/true.md) to use the SFTP implementation. Omitted or [`NIL`](../literals/nil.md) keeps the FTP implementation. |
| `sPrivateKeyFilePath` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Optional private key file for SFTP authentication. Ignored on the FTP path. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the source file is retrieved, the target file is written, and the source file is removed; [`.F.`](../literals/false.md) when any of those steps fails.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sServerNameOrIP` is [`NIL`](../literals/nil.md) or empty (both FTP and SFTP paths use this message). | `FTP server name or IP cannot be missing.` |
| `sRemoteFileFrom` is [`NIL`](../literals/nil.md) or empty. | `Source remote directory name cannot be missing.` |
| `sProxy` is a non-empty string. | `The proxy parameter cannot be used. The system will automatically use the proxy specified by Internet Explorer > Local Area Network settings.` |

!!! note
    The SFTP-path error for a missing `sServerNameOrIP` says `FTP server name or IP cannot be missing.` — same as the FTP message. This appears to be a runtime quirk; the message text does not change on the SFTP path.

## Best practices

!!! success "Do"
    - Set `bIsSFTP` explicitly to [`.T.`](../literals/true.md) only when the target server really expects SFTP.
    - Pass `sRemoteFileTo` explicitly when the move should also rename the file.
    - Leave `sProxy` empty and rely on the system proxy configuration.
    - Wrap SFTP moves in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) when connection, login, or key-loading failures should be handled gracefully.
    - Verify the target file after a business-critical move when the workflow needs confirmation beyond the [`.T.`](../literals/true.md) or [`.F.`](../literals/false.md) result.

!!! failure "Don't"
    - Assume `sRemoteDirectoryTo` defaults to `sRemoteDirectoryFrom`. It does not.
    - Pass a manual proxy value. Any non-empty `sProxy` argument raises an error.
    - Assume the function is atomic. A failed move can leave the source file in place or leave the target file written without completing the overall move.
    - Assume the SFTP path converts all failures to [`.F.`](../literals/false.md). Early connection or authentication failures can still raise.

## Caveats

- FTP and SFTP do not build empty directory values the same way. On the FTP path an empty directory still produces a slash-prefixed path, while on the SFTP path an empty directory uses the file name directly.
- The function can return [`.F.`](../literals/false.md) after the target write step has already succeeded if the source delete step fails.

## Examples

### Move a lab report to a processed directory

Move a file from one FTP folder to another while keeping the same name.

```ssl
:PROCEDURE MoveLabReportToProcessed;
    :DECLARE sServer, sSourceDir, sTargetDir, sFileName, sUser, sPassword;
    :DECLARE bMoved;

    sServer := "ftp.labserver.local";
    sSourceDir := "/incoming";
    sTargetDir := "/processed";
    sFileName := "LB20240415_001.pdf";
    sUser := "labupload";
    sPassword := "SecureP@ss";

    bMoved := MoveInFtp(
        sServer,
        sSourceDir,
        sTargetDir,
        sFileName,
        sFileName,
        sUser,
        sPassword
    );

    :IF bMoved;
        UsrMes("Moved " + sFileName + " to " + sTargetDir);
    :ELSE;
        ErrorMes("Could not move " + sFileName + " to " + sTargetDir);
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("MoveLabReportToProcessed");
```

### Rename a scanned document during workflow reorganization

Move a file from one directory to another and apply a new file name in the process.

```ssl
:PROCEDURE ArchiveScannedDocument;
    :PARAMETERS sServerName, sUser, sPassword;
    :DEFAULT sServerName, "ftp.acme-lims.com";
    :DEFAULT sUser, "limsftp";
    :DEFAULT sPassword, "";
    :DECLARE sSourceDir, sArchiveDir, sOriginalFile, sNewFile, sRefNumber;
    :DECLARE bMoved;

    sSourceDir := "/incoming/scans";
    sArchiveDir := "/archived/documents";
    sOriginalFile := "scan_2024_q1_001.pdf";
    sRefNumber := "REV-2024-042";

    sNewFile := "contract_" + sRefNumber + "_signed.pdf";

    bMoved := MoveInFtp(
        sServerName,
        sSourceDir,
        sArchiveDir,
        sOriginalFile,
        sNewFile,
        sUser,
        sPassword
    );

    :IF bMoved;
        UsrMes("Archived " + sOriginalFile + " as " + sNewFile);
    :ELSE;
        ErrorMes("Could not archive " + sOriginalFile + " as " + sNewFile);
    :ENDIF;

    :RETURN bMoved;
:ENDPROC;

/* Usage;
DoProc("ArchiveScannedDocument");
```

### Retry an SFTP move and verify the destination file

Move a file over SFTP with key-based authentication, retry on failure, and then confirm the destination file exists.

```ssl
:PROCEDURE ArchiveInstrumentOutput;
    :DECLARE sServer, sUser, sPassword, sFromDir, sToDir, sFileFrom, sFileTo;
    :DECLARE sPrivateKeyFile, sMessage;
    :DECLARE nPort, nAttempt, nMaxAttempts;
    :DECLARE bIsSFTP, bMoved, bTargetExists, oErr;

    sServer := "ftp.instrument.lab.local";
    sUser := "archiver";
    sPassword := "KeyPassphrase";
    sFromDir := "/instrument/output";
    sToDir := "/archive/2024";
    sFileFrom := "sample_run_2024-04-11.csv";
    sFileTo := "sample_run_2024-04-11.csv";
    nPort := 22;
    bIsSFTP := .T.;
    sPrivateKeyFile := "/etc/ssh/keys/archiver_key";
    nMaxAttempts := 3;

    nAttempt := 1;
    bMoved := .F.;
    bTargetExists := .F.;

    :WHILE nAttempt <= nMaxAttempts
        .AND. .NOT. bMoved;
        :TRY;
            bMoved := MoveInFtp(
                sServer,
                sFromDir,
                sToDir,
                sFileFrom,
                sFileTo,
                sUser,
                sPassword,
                nPort,
                "",
                bIsSFTP,
                sPrivateKeyFile
            );

            :IF .NOT. bMoved;
                nAttempt += 1;
            :ENDIF;
        :CATCH;
            oErr := GetLastSSLError();
            sMessage := "SFTP move attempt " + LimsString(nAttempt)
                + " failed: " + oErr:Description;
            UsrMes(sMessage);  /* Displays on failure: retry message;
            nAttempt += 1;
        :ENDTRY;
    :ENDWHILE;

    :IF bMoved;
        bTargetExists := CheckOnFtp(
            sServer,
            sToDir,
            sFileTo,
            sUser,
            sPassword,
            nPort,
            "",
            bIsSFTP,
            sPrivateKeyFile
        );

        :IF bTargetExists;
            UsrMes("Moved " + sFileFrom + " to " + sToDir + "/" + sFileTo);
        :ELSE;
            ErrorMes(
                "Move returned true, but the destination file was not confirmed."
            );
        :ENDIF;
    :ELSE;
        ErrorMes(
            "Could not move " + sFileFrom + " after "
            + LimsString(nMaxAttempts) + " attempts."
        );
    :ENDIF;

    :RETURN bMoved .AND. bTargetExists;
:ENDPROC;

/* Usage;
DoProc("ArchiveInstrumentOutput");
```

## Related

- [`CheckOnFtp`](CheckOnFtp.md)
- [`CopyToFtp`](CopyToFtp.md)
- [`DeleteFromFtp`](DeleteFromFtp.md)
- [`RenameOnFtp`](RenameOnFtp.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
