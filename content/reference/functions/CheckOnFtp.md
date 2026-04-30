---
title: "CheckOnFtp"
summary: "Checks whether a remote file exists on an FTP server, or on an SFTP server when bIsSFTP is .T.."
id: ssl.function.checkonftp
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CheckOnFtp

Checks whether a remote file exists on an FTP server, or on an SFTP server when `bIsSFTP` is [`.T.`](../literals/true.md).

On the FTP path, the function sends a file-size request for the target path and returns [`.T.`](../literals/true.md) when the server responds successfully.

On the SFTP path, the function connects first, logs in with either the supplied password or the private key from `sPrivateKeyFilePath`, and then checks the target path. The existence check itself returns [`.T.`](../literals/true.md) or [`.F.`](../literals/false.md), but connection, login, and private-key setup happen before that check and can raise an error.

## When to use

- When you need a quick yes/no check before downloading, renaming, or deleting a remote file.
- When a workflow should continue only after a partner or instrument has placed a file on an FTP or SFTP server.
- When you need to verify several expected files before starting a batch step.

## Syntax

```ssl
CheckOnFtp(
    sServerNameOrIP,
    [sRemoteDirectory],
    sRemoteFileName,
    sUserName,
    sPassword,
    [nPort],
    [sProxy],
    [bIsSFTP],
    [sPrivateKeyFilePath]
)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sServerNameOrIP` | [string](../types/string.md) | yes | — | Remote server name or IP address. |
| `sRemoteDirectory` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Remote directory combined with `sRemoteFileName` to build the lookup path. On SFTP, an empty directory checks `sRemoteFileName` directly. |
| `sRemoteFileName` | [string](../types/string.md) | yes | — | Remote file name to check. |
| `sUserName` | [string](../types/string.md) | yes | — | User name passed to the FTP or SFTP login operation. |
| `sPassword` | [string](../types/string.md) | yes | — | Password for password-based login. When `sPrivateKeyFilePath` is supplied on the SFTP path, this value is used as the private-key passphrase. |
| `nPort` | [number](../types/number.md) | no | `21` | Server port. If omitted or non-positive, the implementation uses `21`. |
| `sProxy` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Must be left empty. Supplying a non-empty value raises an error. |
| `bIsSFTP` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Set to [`.T.`](../literals/true.md) to use the SFTP implementation. Omitted or [`NIL`](../literals/nil.md) keeps the FTP implementation. |
| `sPrivateKeyFilePath` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Optional private key file for SFTP authentication. Ignored on the FTP path. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the remote file exists and the check succeeds; [`.F.`](../literals/false.md) when the file is not found or the check fails.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sServerNameOrIP` is missing on the FTP path. | `FTP server name or IP cannot be missing.` |
| `sServerNameOrIP` is missing on the SFTP path. | `SFTP server name or IP cannot be missing.` |
| `sRemoteFileName` is missing on the FTP or SFTP path. | `Remote file name cannot be missing.` |
| `sProxy` is non-empty. | `The proxy parameter cannot be used. The system will automatically use the proxy specified by Internet Explorer > Local Area Network settings.` |

## Best practices

!!! success "Do"
    - Set `bIsSFTP` explicitly to [`.T.`](../literals/true.md) only when the target server really expects SFTP.
    - Leave `sProxy` empty and rely on the system proxy configuration.
    - Use `sPrivateKeyFilePath` only for SFTP servers that require key-based authentication.
    - Wrap SFTP checks in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) when connection or login failures should be handled gracefully.
    - Treat a [`.F.`](../literals/false.md) result as "the check did not confirm the file exists" rather than as proof of one specific failure mode.

!!! failure "Don't"
    - Assume the function auto-detects SFTP. It uses the SFTP path only when `bIsSFTP` is [`.T.`](../literals/true.md).
    - Pass a manual proxy value. Any non-empty `sProxy` argument raises an error.
    - Assume the SFTP path converts all failures to [`.F.`](../literals/false.md). Connection, login, and key-loading failures can raise instead.
    - Use `CheckOnFtp` as a transfer API when you actually need [`CopyToFtp`](CopyToFtp.md), [`GetFromFtp`](GetFromFtp.md), [`DeleteFromFtp`](DeleteFromFtp.md), or [`RenameOnFtp`](RenameOnFtp.md).

## Caveats

- `bIsSFTP` is not auto-detected. Omit it or pass [`NIL`](../literals/nil.md)/[`.F.`](../literals/false.md) for FTP, and pass [`.T.`](../literals/true.md) for SFTP.
- The FTP and SFTP paths do not fail in exactly the same way. SFTP connection, login, and private-key setup happen before the existence check, so those failures can raise rather than return [`.F.`](../literals/false.md). On the FTP path, a failed size request returns [`.F.`](../literals/false.md) and logs the error.
- FTP and SFTP build the remote path slightly differently when `sRemoteDirectory` is empty. The SFTP path checks `sRemoteFileName` directly, while the FTP path still builds a slash-prefixed file path.

## Examples

### Check whether a single FTP file is ready

Uses the default FTP path to check a daily report file and displays a message depending on whether the file is found.

```ssl
:PROCEDURE VerifyReportFile;
    :DECLARE sServer, sRemoteDir, sFileName, sUser, sPassword, bFileExists;

    sServer := "ftp.reports.example.com";
    sRemoteDir := "/daily_reports";
    sFileName := "Q4_Report_2026.pdf";
    sUser := "report_reader";
    sPassword := "SecurePass123";

    bFileExists := CheckOnFtp(
        sServer,
        sRemoteDir,
        sFileName,
        sUser,
        sPassword
    );

    :IF bFileExists;
        UsrMes("Report file is available.");
    :ELSE;
        UsrMes("Report file is not available yet.");
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("VerifyReportFile");
```

### Check an SFTP drop with a private key

Connects to a partner SFTP server using a private key and handles connection or login failures explicitly in a [`:CATCH`](../keywords/CATCH.md) block, since SFTP setup errors raise rather than return [`.F.`](../literals/false.md).

```ssl
:PROCEDURE CheckPartnerDrop;
    :DECLARE sServer, sRemoteDir, sFileName, sUser, sPassphrase;
    :DECLARE nPort, sProxy, sPrivateKey;
    :DECLARE bIsSFTP, bFileExists;
    :DECLARE oError;

    sServer := "sftp.partner.example.com";
    sRemoteDir := "/incoming/data";
    sFileName := "analysis_data.csv";
    sUser := "automation_user";
    sPassphrase := "KeyPassphrase123";
    nPort := 22;
    sProxy := NIL;
    bIsSFTP := .T.;
    sPrivateKey := "/etc/ssh/automation_key.ppk";

    :TRY;
        bFileExists := CheckOnFtp(
            sServer,
            sRemoteDir,
            sFileName,
            sUser,
            sPassphrase,
            nPort,
            sProxy,
            bIsSFTP,
            sPrivateKey
        );
    :CATCH;
        oError := GetLastSSLError();
        ErrorMes("SFTP availability check failed: " + oError:Description);
        /* Displays on failure: SFTP availability check failed;
        :RETURN .F.;
    :ENDTRY;

    :IF bFileExists;
        UsrMes("Partner file is ready for download.");
        :RETURN .T.;
    :ELSE;
        UsrMes("Partner file is not available yet.");
        :RETURN .F.;
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("CheckPartnerDrop");
```

### Verify a full batch before starting processing

Checks three expected files on an FTP server, collects any missing filenames, and reports them before stopping the batch if any are absent.

```ssl
:PROCEDURE VerifyBatchFiles;
    :DECLARE sServer, sRemoteDir, sUser, sPassword;
    :DECLARE aExpectedFiles, aMissingFiles;
    :DECLARE nIndex, bAllPresent;

    sServer := "ftp.batch.example.com";
    sRemoteDir := "/incoming/batch";
    sUser := "batch_reader";
    sPassword := "BatchPass123";

    aExpectedFiles := {
        "orders_20260418.csv",
        "tests_20260418.csv",
        "results_20260418.csv"
    };
    aMissingFiles := {};
    bAllPresent := .T.;

    :FOR nIndex := 1 :TO ALen(aExpectedFiles);
        :IF .NOT. CheckOnFtp(
            sServer,
            sRemoteDir,
            aExpectedFiles[nIndex],
            sUser,
            sPassword
        );
            AAdd(aMissingFiles, aExpectedFiles[nIndex]);
            bAllPresent := .F.;
        :ENDIF;
    :NEXT;

    :IF bAllPresent;
        UsrMes("All expected batch files are present.");
        :RETURN .T.;
    :ENDIF;

    UsrMes("One or more expected batch files are missing.");

    :FOR nIndex := 1 :TO ALen(aMissingFiles);
        UsrMes("Missing file: " + aMissingFiles[nIndex]);
        /* Displays one missing filename per line;
    :NEXT;

    :RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("VerifyBatchFiles");
```

## Related

- [`CopyToFtp`](CopyToFtp.md)
- [`DeleteFromFtp`](DeleteFromFtp.md)
- [`GetFromFtp`](GetFromFtp.md)
- [`ReadFromFtp`](ReadFromFtp.md)
- [`RenameOnFtp`](RenameOnFtp.md)
- [`WriteToFtp`](WriteToFtp.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
