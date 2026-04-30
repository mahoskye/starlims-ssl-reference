---
title: "DeleteFromFtp"
summary: "Deletes a remote file through FTP, or through SFTP when bIsSFTP is .T.."
id: ssl.function.deletefromftp
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DeleteFromFtp

Deletes a remote file through FTP, or through SFTP when `bIsSFTP` is [`.T.`](../literals/true.md).

On the FTP path, the function sends a delete request for the target path and returns [`.T.`](../literals/true.md) only when the server reports a successful file action. FTP request failures are logged and returned as [`.F.`](../literals/false.md).

When `bIsSFTP` is [`.T.`](../literals/true.md), the function uses the SFTP path instead. It connects with the supplied credentials, optionally loads `sPrivateKeyFilePath`, and then deletes the target file. Delete failures that happen after a successful connect and login are logged and returned as [`.F.`](../literals/false.md), but connection setup, login, and private-key loading can still raise before the function reaches its [`.F.`](../literals/false.md) return path.

## When to use

- When a workflow must remove a file from a partner FTP or SFTP drop after successful processing.
- When you want a simple logic result that tells you whether the delete request completed.
- When the same script needs to support both FTP and SFTP by switching `bIsSFTP`.

## Syntax

```ssl
DeleteFromFtp(
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
| `sRemoteDirectory` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Remote directory used with `sRemoteFileName` to build the target path. When omitted on the SFTP path, the function deletes `sRemoteFileName` as given. |
| `sRemoteFileName` | [string](../types/string.md) | yes | — | Remote file name to delete. |
| `sUserName` | [string](../types/string.md) | yes | — | User name passed to the FTP or SFTP login operation. |
| `sPassword` | [string](../types/string.md) | yes | — | Password for normal login. When `sPrivateKeyFilePath` is supplied on the SFTP path, this value is used as the private-key passphrase. |
| `nPort` | [number](../types/number.md) | no | `21` | Server port. If omitted, or if a non-positive value is supplied, the function uses `21`. |
| `sProxy` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Must be left empty. Supplying a non-empty value raises an error. |
| `bIsSFTP` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Set to [`.T.`](../literals/true.md) to use the SFTP implementation. Omitted or [`NIL`](../literals/nil.md) keeps the FTP implementation. |
| `sPrivateKeyFilePath` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Optional private key file for SFTP authentication. Ignored on the FTP path. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the target file is deleted successfully; [`.F.`](../literals/false.md) when the delete request fails. On the SFTP path, [`.F.`](../literals/false.md) is returned only when the delete fails after a successful connect and login — earlier SFTP failures can raise instead.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sServerNameOrIP` is empty in FTP mode. | `FTP server name or IP cannot be missing.` |
| `sServerNameOrIP` is empty in SFTP mode. | `SFTP server name or IP cannot be missing.` |
| `sRemoteFileName` is empty. | `Remote file name cannot be missing.` |
| `sProxy` is a non-empty string. | `The proxy parameter cannot be used. The system will automatically use the proxy specified by Internet Explorer > Local Area Network settings.` |

## Best practices

!!! success "Do"
    - Set `bIsSFTP` explicitly to [`.T.`](../literals/true.md) only when the target server really expects SFTP.
    - Leave `sProxy` empty and rely on the system proxy configuration.
    - Check the boolean return value and handle [`.F.`](../literals/false.md) as an unsuccessful delete.
    - Use [`CheckOnFtp`](CheckOnFtp.md) first when a missing file is a normal workflow case rather than an error condition.

!!! failure "Don't"
    - Assume the function auto-detects SFTP. It uses the SFTP path only when `bIsSFTP` is [`.T.`](../literals/true.md).
    - Pass a manual proxy value. Any non-empty `sProxy` argument raises an error.
    - Assume the SFTP path converts all failures to [`.F.`](../literals/false.md). Connection, login, and key-loading failures can still raise.
    - Ignore the result of the delete call when later workflow steps depend on the file being gone.

## Caveats

- `sRemoteDirectory` is not validated by this function. On the FTP path it is concatenated as `sRemoteDirectory + "/" + sRemoteFileName`; on the SFTP path an empty `sRemoteDirectory` uses `sRemoteFileName` directly.

## Examples

### Delete a processed file from an FTP drop

Removes one known file from an FTP server after a workflow step finishes and displays whether the delete succeeded.

```ssl
:PROCEDURE RemoveProcessedReport;
    :DECLARE sServer, sRemoteDir, sFileName, sUser, sPassword, bDeleted;

    sServer := "ftp.reports.example.com";
    sRemoteDir := "/processed";
    sFileName := "report_20260418.pdf";
    sUser := "report_user";
    sPassword := "SecurePass123";

    bDeleted := DeleteFromFtp(
        sServer,
        sRemoteDir,
        sFileName,
        sUser,
        sPassword
    );

    :IF bDeleted;
        UsrMes("Processed report removed from the FTP drop.");
    :ELSE;
        UsrMes("Processed report could not be removed.");
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("RemoveProcessedReport");
```

### Delete from an SFTP location with a private key

Uses the SFTP path with key-based authentication and catches connection setup failures separately from the [`.F.`](../literals/false.md) return for server-side delete rejections.

```ssl
:PROCEDURE RemovePartnerPayload;
    :DECLARE sServer, sRemoteDir, sFileName, sUser, sPassphrase;
    :DECLARE nPort, sKeyFile, bDeleted, oErr;

    sServer := "sftp.partner.example.com";
    sRemoteDir := "/outbound/archive";
    sFileName := "payload_20260418.json";
    sUser := "integration_user";
    sPassphrase := "KeyPassphrase123";
    nPort := 22;
    sKeyFile := "/etc/ssl/partner_delete_key.ppk";

    :TRY;
        bDeleted := DeleteFromFtp(
            sServer,
            sRemoteDir,
            sFileName,
            sUser,
            sPassphrase,
            nPort,,
            .T.,
            sKeyFile
        );

        :IF bDeleted;
            UsrMes("Partner payload removed from SFTP.");
        :ELSE;
            UsrMes("Partner payload was not removed from SFTP.");
        :ENDIF;
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("SFTP setup failed: " + oErr:Description);
        /* Displays on setup error: SFTP setup failed;
        :RETURN .F.;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("RemovePartnerPayload");
```

### Clean up a batch and report any files that remain

Iterates a list of expected files, deletes those that exist on the FTP server, and reports any that could not be removed.

```ssl
:PROCEDURE CleanupBatchDrop;
    :DECLARE sServer, sRemoteDir, sUser, sPassword;
    :DECLARE aFiles, aRemaining, nIndex, bDeleted;

    sServer := "ftp.batch.example.com";
    sRemoteDir := "/outgoing/batch";
    sUser := "batch_user";
    sPassword := "BatchPass123";
    aFiles := {
        "orders_20260418.csv",
        "tests_20260418.csv",
        "results_20260418.csv"
    };
    aRemaining := {};

    :FOR nIndex := 1 :TO ALen(aFiles);
        :IF CheckOnFtp(sServer, sRemoteDir, aFiles[nIndex], sUser, sPassword);
            bDeleted := DeleteFromFtp(
                sServer,
                sRemoteDir,
                aFiles[nIndex],
                sUser,
                sPassword
            );

            :IF .NOT. bDeleted;
                AAdd(aRemaining, aFiles[nIndex]);
            :ENDIF;
        :ENDIF;
    :NEXT;

    :IF ALen(aRemaining) == 0;
        UsrMes("Batch cleanup completed.");
        :RETURN .T.;
    :ENDIF;

    UsrMes("Some files were not removed from the batch drop.");

    :FOR nIndex := 1 :TO ALen(aRemaining);
        UsrMes("Remaining file: " + aRemaining[nIndex]);
        /* Displays one remaining filename per line;
    :NEXT;

    :RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("CleanupBatchDrop");
```

## Related

- [`CheckOnFtp`](CheckOnFtp.md)
- [`DeleteDirOnFtp`](DeleteDirOnFtp.md)
- [`GetFromFtp`](GetFromFtp.md)
- [`MoveInFtp`](MoveInFtp.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
