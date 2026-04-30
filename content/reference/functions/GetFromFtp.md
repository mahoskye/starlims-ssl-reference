---
title: "GetFromFtp"
summary: "Downloads a file from an FTP or SFTP server to a local file."
id: ssl.function.getfromftp
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetFromFtp

Downloads a file from an FTP or SFTP server to a local file.

`GetFromFtp` retrieves a remote file by using plain FTP by default or SFTP when `bIsSFTP` is [`.T.`](../literals/true.md). If `sLocalFileName` is empty, the function uses `sRemoteFileName` as the local file name. It returns [`.T.`](../literals/true.md) when the transfer completes successfully and [`.F.`](../literals/false.md) when the transfer or local write fails.

For SFTP, supplying `sPrivateKeyFilePath` switches authentication to private-key login. When no key path is supplied, SFTP uses the `sUserName` and `sPassword` parameters for login.

## When to use

- When you need to download a file from a partner FTP server into a local path.
- When the same integration must support either FTP or SFTP from one call site.
- When you want a simple success/failure result instead of processing a stream directly.

## Syntax

```ssl
GetFromFtp(sServerNameOrIP, [sRemoteDirectory], sRemoteFileName, [sLocalFileName], [sUserName], [sPassword], [nPort], [sProxy], [bIsSFTP], [sPrivateKeyFilePath])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sServerNameOrIP` | [string](../types/string.md) | yes | — | FTP or SFTP server host name or IP address. |
| `sRemoteDirectory` | [string](../types/string.md) | no | — | Remote folder that contains the file. Pass an empty string when the file is in the server's default or root location. |
| `sRemoteFileName` | [string](../types/string.md) | yes | — | Remote file name to download. |
| `sLocalFileName` | [string](../types/string.md) | no | `sRemoteFileName` | Local path and file name to create. If empty, the function uses `sRemoteFileName`. |
| `sUserName` | [string](../types/string.md) | no | — | User name for FTP or SFTP login. |
| `sPassword` | [string](../types/string.md) | no | — | Password for FTP login or password-based SFTP login. When `sPrivateKeyFilePath` is supplied for SFTP, this value is used as the private-key passphrase. |
| `nPort` | [number](../types/number.md) | no | `21` | Server port. Values less than or equal to 0 are reset to `21`. |
| `sProxy` | [string](../types/string.md) | no | — | Must be omitted or empty. A non-empty proxy value raises an exception. |
| `bIsSFTP` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Set to [`.T.`](../literals/true.md) to use SFTP instead of FTP. |
| `sPrivateKeyFilePath` | [string](../types/string.md) | no | — | SFTP private key file path. Used only when `bIsSFTP` is [`.T.`](../literals/true.md). |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the file is downloaded successfully; [`.F.`](../literals/false.md) when the transfer fails or the local file cannot be created or written.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sServerNameOrIP` is [`NIL`](../literals/nil.md) or empty on the FTP path. | `FTP server name or IP cannot be missing.` |
| `sServerNameOrIP` is [`NIL`](../literals/nil.md) or empty on the SFTP path. | `SFTP server name or IP cannot be missing.` |
| `sRemoteFileName` is [`NIL`](../literals/nil.md) or empty. | `Remote file name cannot be missing.` |
| `sProxy` is non-empty. | `The proxy parameter cannot be used. The system will automatically use the proxy specified by Internet Explorer > Local Area Network settings.` |

## Best practices

!!! success "Do"
    - Check the boolean return value before using the downloaded file.
    - Use `GetLastSSLError():Description` after a [`.F.`](../literals/false.md) result when an SSL error object is available and you need more detail about a failed transfer.
    - Set `bIsSFTP` to [`.T.`](../literals/true.md) for secure transfers, and provide `sPrivateKeyFilePath` when the server requires key-based authentication.

!!! failure "Don't"
    - Pass a non-empty `sProxy` value. The function rejects it immediately.
    - Assume SFTP defaults to port `22`; if the server expects `22`, pass `nPort` explicitly.
    - Rely on the function to keep a partially downloaded local file for retry or inspection after a failed FTP transfer; the FTP path deletes the incomplete local file.

## Caveats

- In the FTP path, a failed transfer deletes the incomplete local file before the function returns [`.F.`](../literals/false.md).
- In the SFTP path, the source does not provide the same explicit partial-file cleanup behavior.

## Examples

### Download a file from an FTP server

Downloads a file from a named FTP directory to an explicit local path and reports success or failure.

```ssl
:PROCEDURE DownloadPartnerFile;
    :DECLARE sServer, sRemoteDir, sRemoteFile, sLocalFile, sUser, sPassword;
    :DECLARE bDownloaded;

    sServer := "ftp.partner.example.com";
    sRemoteDir := "/public/data";
    sRemoteFile := "daily_rates.csv";
    sLocalFile := "C:\\WorkflowData\\daily_rates.csv";
    sUser := "publicuser";
    sPassword := "public";

    bDownloaded := GetFromFtp(
        sServer,
        sRemoteDir,
        sRemoteFile,
        sLocalFile,
        sUser,
        sPassword
    );

    :IF bDownloaded;
        UsrMes("Downloaded " + sRemoteFile + " to " + sLocalFile);
        /* Displays the downloaded file path;
    :ELSE;
        ErrorMes("Download failed for " + sRemoteFile);
        /* Displays the failed file name;
    :ENDIF;

    :RETURN bDownloaded;
:ENDPROC;
```

Call with `DoProc("DownloadPartnerFile");`.

### Download from SFTP with key-based authentication

Uses SFTP with a private key file for authentication, targets port 22, and reports any download failure with details from the SSL error object.

```ssl
:PROCEDURE DownloadNightlyReport;
    :DECLARE sServer, sRemoteDir, sRemoteFile, sLocalFile, sUser, sPassphrase;
    :DECLARE sKeyPath, oErr;
    :DECLARE nPort, bDownloaded;

    sServer := "sftp.partner.example.com";
    sRemoteDir := "/daily/reports";
    sRemoteFile := "daily_report.csv";
    sLocalFile := "C:\\Imports\\daily_report.csv";
    sUser := "report_service";
    sPassphrase := "key-passphrase";
    sKeyPath := "C:\\Keys\\report_service.pem";
    nPort := 22;

    bDownloaded := GetFromFtp(
        sServer,
        sRemoteDir,
        sRemoteFile,
        sLocalFile,
        sUser,
        sPassphrase,
        nPort,,
        .T.,
        sKeyPath
    );

    :IF .NOT. bDownloaded;
        oErr := GetLastSSLError();

        :IF .NOT. Empty(oErr);
            ErrorMes("SFTP download failed: " + oErr:Description);
            /* Displays the SSL error description;
        :ELSE;
            ErrorMes("SFTP download failed.");
        :ENDIF;
    :ENDIF;

    :RETURN bDownloaded;
:ENDPROC;
```

Call with `DoProc("DownloadNightlyReport");`.

### Use the remote file name as the local file name and handle validation and transfer failures

Omits the local file name so the function saves under the remote name and wraps the call in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) to distinguish argument-validation errors from transfer failures.

```ssl
:PROCEDURE FetchInboundFile;
    :DECLARE sServer, sRemoteDir, sRemoteFile, sUser, sPassword, oErr;
    :DECLARE bDownloaded;

    sServer := "sftp.partner.example.com";
    sRemoteDir := "/inbound";
    sRemoteFile := "orders.csv";
    sUser := "integration_user";
    sPassword := "secret";

    :TRY;
        bDownloaded := GetFromFtp(
            sServer,
            sRemoteDir,
            sRemoteFile,
            "",
            sUser,
            sPassword,
            22,,
            .T.
        );

        :IF .NOT. bDownloaded;
            oErr := GetLastSSLError();

            :IF .NOT. Empty(oErr);
                ErrorMes("Transfer failed: " + oErr:Description);
                /* Displays the SSL error description;
            :ELSE;
                ErrorMes("Transfer failed without an SSL error object.");
            :ENDIF;
        :ENDIF;
    :CATCH;
        oErr := GetLastSSLError();

        :IF .NOT. Empty(oErr);
            ErrorMes("Invalid call to GetFromFtp: " + oErr:Description);
            /* Displays the validation error description;
        :ELSE;
            ErrorMes("Invalid call to GetFromFtp.");
        :ENDIF;

        bDownloaded := .F.;
    :ENDTRY;

    :RETURN bDownloaded;
:ENDPROC;
```

Call with `DoProc("FetchInboundFile");`.

## Related

- [`CopyToFtp`](CopyToFtp.md)
- [`DeleteFromFtp`](DeleteFromFtp.md)
- [`GetDirFromFtp`](GetDirFromFtp.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
