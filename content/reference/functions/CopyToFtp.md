---
title: "CopyToFtp"
summary: "Appends the same text content to one or more files on an FTP or SFTP server."
id: ssl.function.copytoftp
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# CopyToFtp

Appends the same text content to one or more files on an FTP or SFTP server.

`CopyToFtp` sends the same `sFileContents` value to every file name in `aRemoteFileNames`. In both FTP and SFTP mode, existing remote files are appended to rather than replaced. If `sFileContents` is omitted or [`NIL`](../literals/nil.md), the function uses an empty string.

The function returns [`.T.`](../literals/true.md) only when every requested upload succeeds. It stops on the first failed write and returns [`.F.`](../literals/false.md). The `sProxy` parameter is not usable: passing a non-empty value raises an argument error, so pass [`NIL`](../literals/nil.md) or omit it.

## When to use

- When the same generated text must be appended to several remote files in one call.
- When you need a single API that can target FTP or SFTP based on `bIsSFTP`.
- When a no-op success for an empty file list is acceptable in the calling flow.

## Syntax

```ssl
CopyToFtp(
    sServerNameOrIP,
    sRemoteDirectory,
    aRemoteFileNames,
    [sFileContents],
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
| `sServerNameOrIP` | [string](../types/string.md) | yes | — | Name or IP address of the FTP server |
| `sRemoteDirectory` | [string](../types/string.md) | yes | — | Remote folder path. In SFTP mode, an empty value causes each `aRemoteFileNames` entry to be used as the full remote path. |
| `aRemoteFileNames` | [array](../types/array.md) | yes | — | Array of remote file names. The function uploads the same content to each entry. [`NIL`](../literals/nil.md) is not allowed, but an empty array is accepted and returns success without uploading anything. |
| `sFileContents` | [string](../types/string.md) | no | `""` | Text to append to each remote file. [`NIL`](../literals/nil.md) is treated as an empty string. |
| `sUserName` | [string](../types/string.md) | yes | — | User name passed to the FTP or SFTP login step. |
| `sPassword` | [string](../types/string.md) | yes | — | Password used for FTP login. In SFTP mode, it is used for password login when `sPrivateKeyFilePath` is empty, or as the private-key passphrase when `sPrivateKeyFilePath` is provided. |
| `nPort` | [number](../types/number.md) | no | `21` | Port number. Omitted, [`NIL`](../literals/nil.md), or non-positive values fall back to `21`. |
| `sProxy` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Must be omitted, [`NIL`](../literals/nil.md), or empty. Any non-empty value raises an argument error. |
| `bIsSFTP` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | When [`.T.`](../literals/true.md), the call uses the SFTP implementation instead of the FTP implementation. |
| `sPrivateKeyFilePath` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | SFTP-only private key path. When provided, the SFTP branch attempts private-key authentication. Ignored in FTP mode. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when all requested uploads succeed; [`.F.`](../literals/false.md) when any upload fails. An empty `aRemoteFileNames` array returns [`.T.`](../literals/true.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sServerNameOrIP` is [`NIL`](../literals/nil.md) or empty on the FTP path. | `FTP server name or IP cannot be missing.` |
| `sServerNameOrIP` is [`NIL`](../literals/nil.md) or empty on the SFTP path. | `SFTP server name or IP cannot be missing.` |
| `aRemoteFileNames` is [`NIL`](../literals/nil.md). | `Array of remote file names cannot be null.` |
| Any element in `aRemoteFileNames` is [`NIL`](../literals/nil.md) or empty. | `Array of remote file names cannot contain null or empty elements.` |
| `sProxy` is non-empty. | `The proxy parameter cannot be used. The system will automatically use the proxy specified by Internet Explorer > Local Area Network settings.` |

## Best practices

!!! success "Do"
    - Validate that every entry in `aRemoteFileNames` is a non-empty string before calling.
    - Check the boolean return value and handle the first failed upload explicitly.
    - Use `bIsSFTP` and `sPrivateKeyFilePath` when the target system requires SFTP.
    - Treat this as an append operation and choose file names and content accordingly.

!!! failure "Don't"
    - Pass `sProxy` values. Any non-empty value raises an argument error.
    - Assume the function replaces existing files. It appends content instead.
    - Pass arrays with null or empty file names. Those values raise argument errors.
    - Assume later files were attempted after a failure. The function returns on the first failed write.

## Caveats

- Existing remote files are appended to, not truncated or replaced.
- `aRemoteFileNames := {}` is accepted and returns [`.T.`](../literals/true.md) without uploading anything.
- Validation is limited to the server name, proxy value, and file-name array contents. Other connection, authentication, or path problems surface during the upload attempt.
- The default port fallback is `21` in both FTP and SFTP mode, so pass `22` explicitly for `nPort` when the SFTP server expects it.

## Examples

### Append one report line to one remote file

Appends a single CSV line to a remote file on an FTP server using the minimum required arguments.

```ssl
:PROCEDURE UploadReportLine;
    :DECLARE sServer, sRemoteDir, sUserName, sPassword, sContent;
    :DECLARE aFileNames, bResult;

    sServer := "ftp.reports.lab.example.com";
    sRemoteDir := "/shared/reports";
    sUserName := "report_uploader";
    sPassword := "demo-password";

    aFileNames := {"weekly_summary.csv"};
    sContent := "S001,Passed" + Chr(13) + Chr(10);

    bResult := CopyToFtp(sServer, sRemoteDir, aFileNames, sContent, sUserName, sPassword);

    :IF bResult;
        UsrMes("Report line appended successfully");
    :ELSE;
        UsrMes("Upload failed");
    :ENDIF;

    :RETURN bResult;
:ENDPROC;

/* Usage;
DoProc("UploadReportLine");
```

### Append the same content to multiple SFTP files

Sends the same manifest text to three remote files in one SFTP call, using a private key and port 22.

```ssl
:PROCEDURE AppendManifestToSftpFiles;
    :DECLARE sServer, sRemoteDir, sUserName, sPassword, sManifest;
    :DECLARE sPrivateKeyPath;
    :DECLARE aRemoteFiles, bSuccess;

    sServer := "sftp.example.com";
    sRemoteDir := "/incoming/manifests";
    sUserName := "lims_feed";
    sPassword := "demo-passphrase";
    sPrivateKeyPath := "C:/keys/partner_feed.ppk";
    sManifest := "batch=20260418" + Chr(13) + Chr(10)
		         + "status=ready" + Chr(13) + Chr(10);

    aRemoteFiles := {"manifest_a.txt", "manifest_b.txt", "manifest_c.txt"};

    bSuccess := CopyToFtp(
        sServer,
        sRemoteDir,
        aRemoteFiles,
        sManifest,
        sUserName,
        sPassword,
        22,
        NIL,
        .T.,
        sPrivateKeyPath
    );

    :RETURN bSuccess;
:ENDPROC;

/* Usage;
DoProc("AppendManifestToSftpFiles");
```

### Stop processing when the batch upload fails

Checks the return value after uploading three date-stamped files and stops the workflow with an error message if any upload fails.

```ssl
:PROCEDURE PublishNightlyFeed;
    :DECLARE sServer, sRemoteDir, sUserName, sPassword, sExportDate;
    :DECLARE sPayload;
    :DECLARE aRemoteFiles;
    :DECLARE bUploaded;

    sServer := "ftp.partnerlab.com";
    sRemoteDir := "/incoming/daily";
    sUserName := "nightly_feed";
    sPassword := "demo-password";
    sExportDate := DToS(Today());

    aRemoteFiles := {
        "orders_" + sExportDate + ".txt",
        "results_" + sExportDate + ".txt",
        "manifest_" + sExportDate + ".txt"
    };

    sPayload := "export_date=" + sExportDate + Chr(13) + Chr(10);

    bUploaded := CopyToFtp(
        sServer,
        sRemoteDir,
        aRemoteFiles,
        sPayload,
        sUserName,
        sPassword,
        21,
        NIL,
        .F.
    );

    :IF .NOT. bUploaded;
        UsrMes("Nightly feed upload failed");
        :RETURN .F.;
    :ENDIF;

    UsrMes("Nightly feed upload completed");

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("PublishNightlyFeed");
```

## Related

- [`WriteToFtp`](WriteToFtp.md)
- [`SendToFtp`](SendToFtp.md)
- [`GetFromFtp`](GetFromFtp.md)
- [`boolean`](../types/boolean.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
