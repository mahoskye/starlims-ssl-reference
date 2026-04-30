---
title: "GetDirFromFtp"
summary: "Lists directory entries from an FTP server, or from an SFTP server when bIsSFTP is .T.."
id: ssl.function.getdirfromftp
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetDirFromFtp

Lists directory entries from an FTP server, or from an SFTP server when `bIsSFTP` is [`.T.`](../literals/true.md).

On the FTP path, the function sends an FTP `LIST` request for `sRemoteDirectory/sFilePattern`, defaults `sFilePattern` to [`*`](../operators/multiply.md) when it is empty, and returns the parsed listing. On the SFTP path, it ignores `bUsePassive`, connects with either password or private-key authentication, and lists the directory directly. A successful call returns an array of entry rows. Each row contains `{name, size, date, time, attributes}`, where `attributes` is `"A"` for a file or `"D"` for a directory.

## When to use

- When you need to inspect a remote drop folder before downloading or moving
  files.
- When you want one API that can list either FTP or SFTP locations.
- When an FTP workflow needs server-side wildcard filtering through `sFilePattern`.
- When an SFTP workflow should enumerate a directory and then apply its own
  filtering in SSL.

## Syntax

```ssl
GetDirFromFtp(sServerNameOrIP, [sRemoteDirectory], [sFilePattern], [sUserName], [sPassword], [nPort], [sProxy], [bUsePassive], [bIsSFTP], [sPrivateKeyFilePath])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sServerNameOrIP` | [string](../types/string.md) | yes | — | Remote server name or IP address. |
| `sRemoteDirectory` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Remote directory to list. The value is passed directly to the FTP or SFTP implementation. |
| `sFilePattern` | [string](../types/string.md) | no | `"*"` on FTP | Wildcard pattern appended to the FTP request path. On the SFTP path, this must be omitted, [`NIL`](../literals/nil.md), or an empty string. |
| `sUserName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | User name used for login. |
| `sPassword` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Password for FTP login. On the SFTP path, this is also used as the private-key passphrase when `sPrivateKeyFilePath` is supplied. |
| `nPort` | [number](../types/number.md) | no | `21` | Server port. If omitted or non-positive, the implementation uses `21`. |
| `sProxy` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Must be left empty. Supplying a non-empty value raises an error. |
| `bUsePassive` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | FTP passive mode flag. Ignored on the SFTP path. |
| `bIsSFTP` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Set to [`.T.`](../literals/true.md) to use the SFTP implementation. Omitted or [`NIL`](../literals/nil.md) keeps the FTP implementation. |
| `sPrivateKeyFilePath` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Optional private key file for SFTP authentication. Ignored on the FTP path. |

## Returns

**[array](../types/array.md)** — Array of directory-entry rows on success; [`NIL`](../literals/nil.md) when the listing request fails.

Each row is a 5-element positional array:

| Position | Value |
|----------|-------|
| `1` | Entry name |
| `2` | Entry size |
| `3` | Entry date |
| `4` | Entry time text |
| `5` | Entry attribute: `"A"` for a file or `"D"` for a directory |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sServerNameOrIP` is [`NIL`](../literals/nil.md) or empty on the FTP path. | `FTP server name or IP cannot be missing.` |
| `sServerNameOrIP` is [`NIL`](../literals/nil.md) or empty on the SFTP path. | `SFTP server name or IP cannot be missing.` |
| `sProxy` is non-empty. | `The proxy parameter cannot be used. The system will automatically use the proxy specified by Internet Explorer > Local Area Network settings.` |
| `sFilePattern` is non-empty on the SFTP path. | `The file pattern cannot be used.` |

## Best practices

!!! success "Do"
    - Pass `bIsSFTP` explicitly when you intend to use the SFTP path.
    - Leave `sProxy` empty and rely on the system proxy configuration.
    - Use `sFilePattern` for FTP filtering, but pass [`NIL`](../literals/nil.md) or `""` for SFTP.
    - Check for [`NIL`](../literals/nil.md) before iterating the returned array.
    - Read column positions consistently, for example `aEntry[1]` for the name
      and `aEntry[5]` for the file-or-directory flag.

!!! failure "Don't"
    - Assume `sFilePattern` works on both protocols. A non-empty value is
      valid only on the FTP path.
    - Pass a manual proxy value. Any non-empty `sProxy` argument raises an
      error.
    - Assume SFTP failures always become [`NIL`](../literals/nil.md). Connection and login
      failures can raise before the function returns.
    - Guess the entry layout. The returned rows are positional arrays, not
      named objects.

## Caveats

- The implementation falls back to port `21` when `nPort` is omitted or less
  than or equal to zero, even on the SFTP path.
- On the FTP path, unparseable listing text causes a user message and a [`NIL`](../literals/nil.md)
  return.
- SFTP connection, login, or private-key setup failures occur before the [`NIL`](../literals/nil.md)
  return path, so those errors can propagate as exceptions rather than returning [`NIL`](../literals/nil.md).
- The returned array shape is the same on both paths, but the date and time
  values come from each protocol's listing data.

## Examples

### List all entries from an FTP folder

Use the FTP path with the default wildcard to inspect a drop folder.

```ssl
:PROCEDURE ListFtpDrop;
    :DECLARE sServer, sRemoteDir, sPattern, sUser, sPassword;
    :DECLARE aEntries, aEntry;
    :DECLARE nIndex;

    sServer := "ftp.example.com";
    sRemoteDir := "/incoming";
    sPattern := "*";
    sUser := "batch_reader";
    sPassword := "BatchPass123";

    aEntries := GetDirFromFtp(
        sServer,
        sRemoteDir,
        sPattern,
        sUser,
        sPassword
    );

    :IF aEntries == NIL;
        ErrorMes("Could not retrieve the FTP listing.");
        :RETURN .F.;
    :ENDIF;

    :FOR nIndex := 1 :TO ALen(aEntries);
        aEntry := aEntries[nIndex];
        /* Displays each entry name and type;
        UsrMes(aEntry[1] + " (" + aEntry[5] + ")");
    :NEXT;

    :RETURN .T.;
:ENDPROC;
```

Call with `DoProc("ListFtpDrop");`.

### List an SFTP folder with private-key authentication

Use the SFTP path, keep `sFilePattern` empty, and handle connection or login errors explicitly.

```ssl
:PROCEDURE ListPartnerSftpDrop;
    :DECLARE sServer, sRemoteDir, sUser, sPassphrase, sProxy, sPrivateKey;
    :DECLARE sFilePattern;
    :DECLARE nPort;
    :DECLARE bIsSFTP, bUsePassive;
    :DECLARE aEntries, aEntry, oErr;
    :DECLARE nIndex;

    sServer := "sftp.partner.example.com";
    sRemoteDir := "/outbound/results";
    sUser := "partner_user";
    sPassphrase := "KeyPassphrase123";
    sProxy := NIL;
    sPrivateKey := "/secure/keys/partner_key.ppk";
    sFilePattern := "";
    nPort := 22;
    bIsSFTP := .T.;
    bUsePassive := .T.;

    :TRY;
        aEntries := GetDirFromFtp(
            sServer,
            sRemoteDir,
            sFilePattern,
            sUser,
            sPassphrase,
            nPort,
            sProxy,
            bUsePassive,
            bIsSFTP,
            sPrivateKey
        );

    :CATCH;
        oErr := GetLastSSLError();
        /* Displays on failure with error details;
        ErrorMes("SFTP listing failed: " + oErr:Description);
        :RETURN .F.;
    :ENDTRY;

    :IF aEntries == NIL;
        ErrorMes("The SFTP server returned no listing.");
        :RETURN .F.;
    :ENDIF;

    :FOR nIndex := 1 :TO ALen(aEntries);
        aEntry := aEntries[nIndex];
        /* Displays each entry name and size;
        UsrMes(aEntry[1] + " size=" + LimsString(aEntry[2]));
    :NEXT;

    :RETURN .T.;
:ENDPROC;
```

Call with `DoProc("ListPartnerSftpDrop");`.

### Split the returned rows into files and directories

Inspect the entry layout and branch on the attributes column so later logic can process files and folders differently.

```ssl
:PROCEDURE ClassifyRemoteEntries;
    :DECLARE sServer, sRemoteDir, sPattern, sUser, sPassword;
    :DECLARE aEntries, aEntry, aFiles, aDirectories;
    :DECLARE nIndex;

    sServer := "ftp.example.com";
    sRemoteDir := "/release";
    sPattern := "*";
    sUser := "release_reader";
    sPassword := "ReleasePass123";

    aEntries := GetDirFromFtp(
        sServer,
        sRemoteDir,
        sPattern,
        sUser,
        sPassword,
        21,
        NIL,
        .T.
    );

    :IF aEntries == NIL;
        ErrorMes("Remote listing failed.");
        :RETURN NIL;
    :ENDIF;

    aFiles := {};
    aDirectories := {};

    :FOR nIndex := 1 :TO ALen(aEntries);
        aEntry := aEntries[nIndex];

        :IF aEntry[5] == "D";
            AAdd(aDirectories, aEntry[1]);
        :ELSE;
            AAdd(aFiles, aEntry[1]);
        :ENDIF;
    :NEXT;

    /* Displays the file count;
    UsrMes("Files found: " + LimsString(ALen(aFiles)));
    /* Displays the directory count;
    UsrMes("Directories found: " + LimsString(ALen(aDirectories)));

    :RETURN {aFiles, aDirectories};
:ENDPROC;
```

Call with `DoProc("ClassifyRemoteEntries");`.

## Related

- [`CheckOnFtp`](CheckOnFtp.md)
- [`GetFromFtp`](GetFromFtp.md)
- [`ReadFromFtp`](ReadFromFtp.md)
- [`SendToFtp`](SendToFtp.md)
- [`DeleteFromFtp`](DeleteFromFtp.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
- [`number`](../types/number.md)
