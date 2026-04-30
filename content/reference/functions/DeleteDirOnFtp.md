---
title: "DeleteDirOnFtp"
summary: "Deletes a remote directory over FTP or SFTP."
id: ssl.function.deletedironftp
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DeleteDirOnFtp

Deletes a remote directory over FTP or SFTP.

Use `DeleteDirOnFtp` to remove a remote folder by path. When `bIsSFTP` is [`.T.`](../literals/true.md), the call uses SFTP; otherwise it uses FTP. If `nPort` is omitted or less than or equal to `0`, the function uses `21` in both modes. The function returns [`.T.`](../literals/true.md) when the server accepts the directory removal request. It returns [`.F.`](../literals/false.md) when the delete request itself fails, such as when the directory does not exist, is not empty, or the server refuses the operation. Missing server or directory values, and a non-empty `sProxy`, raise an error instead of returning [`.F.`](../literals/false.md). In SFTP mode, connection, login, and private key setup happen before the delete call, so those failures can raise before any boolean result is returned.

## When to use

- When you need to remove an empty working folder after a remote process finishes.
- When the same script must support either FTP or SFTP with one call shape.
- When you want a simple success or failure result for the delete request.

## Syntax

```ssl
DeleteDirOnFtp(
    sServerNameOrIP,
    sRemoteDirectory,
    [sUserName],
    [sPassword],
    [nPort],
    [sProxy],
    [bIsSFTP],
    [sPrivateKeyFilePath]
)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sServerNameOrIP` | [string](../types/string.md) | yes | — | Remote server host name or IP address. |
| `sRemoteDirectory` | [string](../types/string.md) | yes | — | Remote directory path to remove. |
| `sUserName` | [string](../types/string.md) | no | — | User name for the remote server login. |
| `sPassword` | [string](../types/string.md) | no | — | FTP password, or SFTP password or private-key passphrase. |
| `nPort` | [number](../types/number.md) | no | `21` | Port used for the connection. Values less than or equal to `0` are treated as `21`. |
| `sProxy` | [string](../types/string.md) | no | blank | Must be omitted or blank. A non-empty value raises an error. |
| `bIsSFTP` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Set to [`.T.`](../literals/true.md) to use SFTP. Omit it or pass [`.F.`](../literals/false.md) to use FTP. |
| `sPrivateKeyFilePath` | [string](../types/string.md) | no | blank | In SFTP mode, when provided, the function loads this key file and uses `sPassword` as the key passphrase. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the remote directory is deleted successfully; [`.F.`](../literals/false.md) when the server rejects the delete request.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sServerNameOrIP` is empty in FTP mode. | `FTP server name or IP cannot be missing.` |
| `sServerNameOrIP` is empty in SFTP mode. | `SFTP server name or IP cannot be missing.` |
| `sRemoteDirectory` is empty. | `Remote folder name cannot be missing.` |
| `sProxy` is a non-empty string. | `The proxy parameter cannot be used. The system will automatically use the proxy specified by Internet Explorer > Local Area Network settings.` |

## Best practices

!!! success "Do"
    - Delete only directories you expect to be empty.
    - Wrap SFTP calls in [`:TRY`](../keywords/TRY.md) and [`:CATCH`](../keywords/CATCH.md) when connection or key-loading failures must be handled separately from a [`.F.`](../literals/false.md) return.
    - Leave `sProxy` blank and let the platform use its configured proxy settings.
    - Pass `bIsSFTP` and `sPrivateKeyFilePath` explicitly when the target server requires SFTP key authentication.

!!! failure "Don't"
    - Assume the function uses port `22` for SFTP automatically. This API defaults `nPort` to `21` unless you pass another value.
    - Assume every failure comes back as [`.F.`](../literals/false.md). Input validation errors, and some SFTP setup failures, can raise instead.
    - Pass a proxy string expecting the function to use it. A non-empty `sProxy` value is rejected.
    - Use [`ErrorMes`](ErrorMes.md) for ordinary retry or status messages. Reserve it for failures that must always be logged.

## Caveats

- The function does not remove directory contents first. If the server refuses to delete a non-empty directory, the call returns [`.F.`](../literals/false.md).

## Examples

### Delete an empty FTP archive folder

Removes a completed archive folder from an FTP server and displays whether the delete succeeded or was rejected.

```ssl
:PROCEDURE RemoveArchiveFolder;
    :DECLARE sServer, sRemoteDir, sUserName, sPassword, bDeleted;

    sServer := "ftp.example.com";
    sRemoteDir := "/archive/2026-04-18";
    sUserName := "archive_user";
    sPassword := "secret";

    bDeleted := DeleteDirOnFtp(sServer, sRemoteDir, sUserName, sPassword);

    :IF bDeleted;
        UsrMes("Archive folder removed: " + sRemoteDir);
        /* Displays the removed folder path;
    :ELSE;
        UsrMes("Archive folder could not be removed: " + sRemoteDir);
        /* Displays the folder that could not be removed;
    :ENDIF;

    :RETURN bDeleted;
:ENDPROC;

/* Usage;
DoProc("RemoveArchiveFolder");
```

### Delete an SFTP folder with a private key

Uses SFTP key authentication to delete a drop folder, handling connection setup failures separately from the [`.F.`](../literals/false.md) return for server-side rejections.

```ssl
:PROCEDURE RemoveSftpDropFolder;
    :DECLARE sServer, sRemoteDir, sUserName, sKeyPass, sKeyPath;
    :DECLARE bDeleted, oErr;

    sServer := "sftp.example.com";
    sRemoteDir := "/drop/offloaded_batch";
    sUserName := "integration_user";
    sKeyPass := "key-passphrase";
    sKeyPath := "/keys/integration_user.ppk";

    :TRY;
        bDeleted := DeleteDirOnFtp(
            sServer,
            sRemoteDir,
            sUserName,
            sKeyPass,
            22,,
            .T.,
            sKeyPath
        );

        :IF bDeleted;
            UsrMes("SFTP folder removed: " + sRemoteDir);
            /* Displays the removed SFTP folder path;
        :ELSE;
            UsrMes("SFTP folder could not be removed: " + sRemoteDir);
            /* Displays the rejected SFTP folder path;
        :ENDIF;

    :CATCH;
        oErr := GetLastSSLError();
        UsrMes("SFTP setup failed: " + oErr:Description);
        /* Displays the setup failure details;
        :RETURN .F.;
    :ENDTRY;

    :RETURN bDeleted;
:ENDPROC;

/* Usage;
DoProc("RemoveSftpDropFolder");
```

### Verify the folder is empty before deleting it

Verifies the remote folder is empty with [`GetDirFromFtp`](GetDirFromFtp.md) before calling `DeleteDirOnFtp`, avoiding server rejection for non-empty directories.

```ssl
:PROCEDURE RemoveProcessedBatchFolder;
    :DECLARE sServer, sRemoteDir, sUserName, sPassword;
    :DECLARE aEntries, bDeleted, oErr;

    sServer := "ftp.example.com";
    sRemoteDir := "/processing/batch_1042";
    sUserName := "batch_user";
    sPassword := "secret";

    :TRY;
        aEntries := GetDirFromFtp(sServer, sRemoteDir, "*", sUserName, sPassword);

        :IF aEntries == NIL;
            UsrMes("Could not verify the remote folder contents.");
            :RETURN .F.;
        :ENDIF;

        :IF ALen(aEntries) > 0;
            UsrMes(
                "Remote folder is not empty. Leaving it in place: "
                + sRemoteDir
            );
            /* Displays the non-empty folder path;
            :RETURN .F.;
        :ENDIF;

        bDeleted := DeleteDirOnFtp(sServer, sRemoteDir, sUserName, sPassword);

        :IF .NOT. bDeleted;
            UsrMes("Remote folder delete failed: " + sRemoteDir);
            /* Displays the folder that failed to delete;
            :RETURN .F.;
        :ENDIF;

    :CATCH;
        oErr := GetLastSSLError();
        UsrMes("Remote folder cleanup failed: " + oErr:Description);
        /* Displays the cleanup failure details;
        :RETURN .F.;
    :ENDTRY;

    UsrMes("Remote folder cleanup complete: " + sRemoteDir);
    /* Displays the cleaned folder path;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("RemoveProcessedBatchFolder");
```

## Related

- [`DeleteFromFtp`](DeleteFromFtp.md)
- [`GetDirFromFtp`](GetDirFromFtp.md)
- [`MakeDirOnFtp`](MakeDirOnFtp.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
