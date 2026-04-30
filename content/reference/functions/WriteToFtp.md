---
title: "WriteToFtp"
summary: "Appends text to a remote file over FTP or SFTP."
id: ssl.function.writetoftp
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# WriteToFtp

Appends text to a remote file over FTP or SFTP.

`WriteToFtp` writes the supplied text to the end of a remote file. If the target file does not already exist, the function creates it and writes the text starting at offset 0. When `bIsSFTP` is [`.T.`](../literals/true.md), the call uses the SFTP implementation; otherwise it uses FTP. If `sFileContents` is [`NIL`](../literals/nil.md), the function treats it as an empty string.

For FTP, the transfer request uses append semantics. For SFTP, the function looks up the current remote file size and writes starting at that offset. In both modes, the function preserves existing file contents instead of replacing them.

## When to use

- When you need to append log, audit, or export text to a remote file.
- When the target may not exist yet and creating it on first write is acceptable.
- When you need one function that can target either FTP or SFTP.
- When SFTP key-based login is required and you have a private key file path.

## Syntax

```ssl
WriteToFtp(sServerNameOrIP, sRemoteDirectory, sRemoteFileName, sFileContents, sUserName, sPassword, [nPort], [sProxy], [bIsSFTP], [sPrivateKeyFilePath])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sServerNameOrIP` | [string](../types/string.md) | yes | — | Remote server name or IP address. Empty values throw an error. |
| `sRemoteDirectory` | [string](../types/string.md) | yes | — | Remote directory path. Pass an empty string to address `sRemoteFileName` without prepending a directory. |
| `sRemoteFileName` | [string](../types/string.md) | yes | — | Remote file name to append to. Empty values throw an error. |
| `sFileContents` | [string](../types/string.md) | yes | — | Text to append. [`NIL`](../literals/nil.md) is converted to an empty string before writing. |
| `sUserName` | [string](../types/string.md) | yes | — | User name used for FTP or SFTP login. |
| `sPassword` | [string](../types/string.md) | yes | — | Password for FTP login. In SFTP key-based mode, this value is used as the private-key passphrase. |
| `nPort` | [number](../types/number.md) | no | `21` | Network port. Omitted, [`NIL`](../literals/nil.md), or non-positive values are normalized to `21`. |
| `sProxy` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Proxy setting. Non-empty values throw an error; omit it to use the system proxy configuration. |
| `bIsSFTP` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | When [`.T.`](../literals/true.md), the function uses SFTP instead of FTP. |
| `sPrivateKeyFilePath` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | SFTP-only private key path. If omitted, SFTP logs in with `sUserName` and `sPassword`. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the write completes successfully; [`.F.`](../literals/false.md) when the transfer operation reaches the FTP or SFTP write step and that step fails with a handled web exception.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sServerNameOrIP` is empty and FTP mode is active. | `FTP server name or IP cannot be missing.` |
| `sServerNameOrIP` is empty and SFTP mode is active. | `SFTP server name or IP cannot be missing.` |
| `sRemoteFileName` is empty. | `Remote file name cannot be missing.` |
| `sProxy` is non-empty. | `The proxy parameter cannot be used. The system will automatically use the proxy specified by Internet Explorer > Local Area Network settings.` |

## Best practices

!!! success "Do"
    - Use this function when append behavior is the intended outcome.
    - Pass `""` for `sRemoteDirectory` when the target file should be addressed directly.
    - Specify `nPort` explicitly for SFTP so the call does not fall back to `21`.
    - Omit trailing optional arguments when you do not need them.

!!! failure "Don't"
    - Expect the function to overwrite or truncate the remote file. It appends.
    - Pass a non-empty `sProxy` value. The function rejects it.
    - Assume every failure returns [`.F.`](../literals/false.md). Validation and some setup failures can still throw.
    - Use the SFTP default port implicitly unless `21` is actually correct for your server.

## Caveats

- In SFTP mode, connection and login happen before the guarded write block, so some setup failures can raise an error instead of returning [`.F.`](../literals/false.md).
- In FTP mode, the request URI is built before the guarded transfer block, so invalid URI construction failures are not part of the [`.F.`](../literals/false.md) return path.

## Examples

### Append a log entry to an FTP file

Append one line of text to a log file on an FTP server using the default port.

```ssl
:PROCEDURE AppendExportLog;
    :DECLARE sServerNameOrIP, sRemoteDirectory, sRemoteFileName, sFileContents;
    :DECLARE sUserName, sPassword, bWrote;

    sServerNameOrIP := "ftp.reports.example.com";
    sRemoteDirectory := "/exports";
    sRemoteFileName := "daily.log";
    sUserName := "report_user";
    sPassword := "secret";
    sFileContents := "Export completed on " + DToC(Today()) + Chr(13) + Chr(10);

    bWrote := WriteToFtp(
        sServerNameOrIP,
        sRemoteDirectory,
        sRemoteFileName,
        sFileContents,
        sUserName,
        sPassword
    );

    :IF bWrote;
        UsrMes("Export log updated.");
    :ELSE;
        UsrMes("Export log update failed.");
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("AppendExportLog");
```

### Append to an SFTP file with a private key

Append a status line over SFTP with an explicit port and key-based login.

```ssl
:PROCEDURE AppendNightlyAudit;
    :DECLARE sServerNameOrIP, sRemoteDirectory, sRemoteFileName, sFileContents;
    :DECLARE sUserName, sPassword, sPrivateKeyFilePath;
    :DECLARE nPort, bWrote;

    sServerNameOrIP := "sftp.example.com";
    sRemoteDirectory := "/logs/nightly";
    sRemoteFileName := "backup_audit.log";
    sUserName := "backup_service";
    sPassword := "key-passphrase";
    sPrivateKeyFilePath := "/keys/backup_service.ppk";
    nPort := 22;

    sFileContents := DToC(Today()) + " nightly backup completed" + Chr(10);

    bWrote := WriteToFtp(
        sServerNameOrIP,
        sRemoteDirectory,
        sRemoteFileName,
        sFileContents,
        sUserName,
        sPassword,
        nPort,,
        .T.,
        sPrivateKeyFilePath
    );

    :IF .NOT. bWrote;
        UsrMes("Nightly audit append failed.");
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("AppendNightlyAudit");
```

### Append to multiple SFTP targets with error tracking

Loop through several SFTP targets, collect transfer failures, and also handle thrown setup errors.

```ssl
:PROCEDURE AppendBatchAudit;
    :DECLARE aTargets, sFileContents, sFailureLog;
    :DECLARE sServerNameOrIP, sRemoteDirectory, sRemoteFileName;
    :DECLARE sUserName, sPassword, sPrivateKeyFilePath;
    :DECLARE nPort, nIndex, nFailures, bWrote, oError;

    aTargets := {
        {"sftp-a.example.com", "/logs", "batch.log", "svc_a", "alpha", "/keys/a.ppk", 22},
        {"sftp-b.example.com", "/logs", "batch.log", "svc_b", "beta", "/keys/b.ppk", 22}
    };
    sFileContents := "Batch completed on " + DToC(Today()) + Chr(10);
    sFailureLog := "";
    nFailures := 0;

    :FOR nIndex := 1 :TO ALen(aTargets);
        sServerNameOrIP := aTargets[nIndex, 1];
        sRemoteDirectory := aTargets[nIndex, 2];
        sRemoteFileName := aTargets[nIndex, 3];
        sUserName := aTargets[nIndex, 4];
        sPassword := aTargets[nIndex, 5];
        sPrivateKeyFilePath := aTargets[nIndex, 6];
        nPort := aTargets[nIndex, 7];

        :TRY;
            bWrote := WriteToFtp(
                sServerNameOrIP,
                sRemoteDirectory,
                sRemoteFileName,
                sFileContents,
                sUserName,
                sPassword,
                nPort,,
                .T.,
                sPrivateKeyFilePath
            );

            :IF .NOT. bWrote;
                nFailures += 1;
                sFailureLog += sServerNameOrIP + " returned .F." + Chr(10);
            :ENDIF;
        :CATCH;
            nFailures += 1;
            oError := GetLastSSLError();
            sFailureLog += sServerNameOrIP + ": " + oError:Description + Chr(10);
        :ENDTRY;
    :NEXT;

    :IF nFailures > 0;
        UsrMes(sFailureLog);
        /* Displays failure details;
    :ENDIF;

    :RETURN nFailures == 0;
:ENDPROC;

/* Usage;
DoProc("AppendBatchAudit");
```

## Related

- [`ReadFromFtp`](ReadFromFtp.md)
- [`SendToFtp`](SendToFtp.md)
- [`boolean`](../types/boolean.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
