---
title: "SendToFtp"
summary: "Uploads one local file to an FTP or SFTP server."
id: ssl.function.sendtoftp
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SendToFtp

Uploads one local file to an FTP or SFTP server.

`SendToFtp` sends a local file to a remote location using either FTP or SFTP. When `bIsSFTP` is [`.T.`](../literals/true.md), the call uses the SFTP branch. Otherwise it uses the FTP branch. If `sRemoteFileName` is empty, the function uses the local file name from `sLocalFileName`.

The function returns [`.T.`](../literals/true.md) when the upload completes successfully. It returns [`.F.`](../literals/false.md) for caught transfer failures such as being unable to open the local file or the upload request failing. The `sProxy` parameter is not usable in either mode: a non-empty value raises an argument error.

## When to use

- When you need to upload one existing local file to a remote FTP or SFTP location.
- When the caller needs one API that can switch between FTP and SFTP with `bIsSFTP`.
- When you want the remote file name to default from the local file path if you do not supply one.

## Syntax

```ssl
SendToFtp(sServerNameOrIP, sRemoteDirectory, [sRemoteFileName], sLocalFileName, sUserName, sPassword, [nPort], [sProxy], [bUsePassive], [bIsSFTP], [sPrivateKeyFilePath])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sServerNameOrIP` | [string](../types/string.md) | yes | — | FTP or SFTP server name or IP address. |
| `sRemoteDirectory` | [string](../types/string.md) | yes | — | Remote folder path passed to the selected backend. |
| `sRemoteFileName` | [string](../types/string.md) | no | local file name | Remote file name. If omitted, empty, or [`NIL`](../literals/nil.md), the function uses the file name portion of `sLocalFileName`. |
| `sLocalFileName` | [string](../types/string.md) | yes | — | Local file path to upload. |
| `sUserName` | [string](../types/string.md) | yes | — | User name for the FTP or SFTP login step. |
| `sPassword` | [string](../types/string.md) | yes | — | Password for FTP login. In SFTP mode, it is used for password login when `sPrivateKeyFilePath` is empty, or as the private-key passphrase when `sPrivateKeyFilePath` is provided. |
| `nPort` | [number](../types/number.md) | no | `21` | Port number. Omitted, [`NIL`](../literals/nil.md), or non-positive values fall back to `21`. Pass `22` explicitly when the SFTP server expects the standard SFTP port. |
| `sProxy` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Must be omitted, [`NIL`](../literals/nil.md), or empty. Any non-empty value raises an argument error. |
| `bUsePassive` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | FTP-only passive mode flag. It affects the FTP branch and is ignored when `bIsSFTP` is [`.T.`](../literals/true.md). |
| `bIsSFTP` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | When [`.T.`](../literals/true.md), the call uses SFTP instead of FTP. |
| `sPrivateKeyFilePath` | [string](../types/string.md) | no | — | SFTP-only private key path. When provided, the SFTP branch attempts private-key authentication. Ignored in FTP mode. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the file upload completes successfully; [`.F.`](../literals/false.md) when the selected backend catches a file-read or transfer error during the upload attempt.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sServerNameOrIP` is [`NIL`](../literals/nil.md) or empty in FTP mode. | `FTP server name or IP cannot be missing.` |
| `sServerNameOrIP` is [`NIL`](../literals/nil.md) or empty in SFTP mode. | `SFTP server name or IP cannot be missing.` |
| `sLocalFileName` is [`NIL`](../literals/nil.md) or empty. | `Local file name cannot be missing.` |
| `sProxy` is non-empty. | `The proxy parameter cannot be used. The system will automatically use the proxy specified by Internet Explorer > Local Area Network settings.` |

## Best practices

!!! success "Do"
    - Validate `sServerNameOrIP` and `sLocalFileName` before calling so argument errors are caught earlier in your workflow.
    - Pass `22` explicitly for SFTP servers that use the standard SFTP port.
    - Check the boolean result and treat [`.F.`](../literals/false.md) as a failed upload that needs user feedback, retry logic, or follow-up handling.
    - Use `sPrivateKeyFilePath` in SFTP mode when the target server requires key-based authentication.

!!! failure "Don't"
    - Pass a non-empty `sProxy` value. The function rejects it in both FTP and SFTP mode.
    - Assume `bUsePassive` affects SFTP. It is only used by the FTP branch.
    - Assume the function always keeps the original local file name on the server. An explicit `sRemoteFileName` overrides it.
    - Rely on the default port for SFTP. The default fallback is `21`, not `22`.

## Caveats

- The function does not validate `sRemoteDirectory` before delegating to the FTP or SFTP backend.

## Examples

### Upload one file to an FTP folder

Upload a local report file to a named remote file on a standard FTP server.

```ssl
:PROCEDURE UploadDailyReport;
	:DECLARE sServer, sRemoteDir, sRemoteFile, sLocalFile;
	:DECLARE sUserName, sPassword;
	:DECLARE bUploaded;

	sServer := "ftp.partner.example.com";
	sRemoteDir := "/reports/outbound";
	sRemoteFile := "daily_report.csv";
	sLocalFile := "C:/Exports/daily_report.csv";
	sUserName := "report_user";
	sPassword := "demo-password";

	bUploaded := SendToFtp(
		sServer,
		sRemoteDir,
		sRemoteFile,
		sLocalFile,
		sUserName,
		sPassword
	);

	:IF bUploaded;
		UsrMes("Daily report uploaded");
		:RETURN .T.;
	:ENDIF;

	UsrMes("Daily report upload failed");

	:RETURN .F.;
:ENDPROC;

/*
Run with DoProc("UploadDailyReport")
;
```

### Upload by SFTP and let the remote name default

Use SFTP with a private key and let the function reuse the local file name by leaving `sRemoteFileName` empty.

```ssl
:PROCEDURE UploadInstrumentResult;
	:DECLARE sServer, sRemoteDir, sLocalFile;
	:DECLARE sUserName, sPassphrase, sKeyFile;
	:DECLARE bUploaded;

	sServer := "sftp.instrument.example.com";
	sRemoteDir := "/incoming/results";
	sLocalFile := "C:/LabData/batch567/results.csv";
	sUserName := "instrument_feed";
	sPassphrase := "demo-passphrase";
	sKeyFile := "C:/Keys/instrument_feed.ppk";

	bUploaded := SendToFtp(
		sServer,
		sRemoteDir,
		"",
		sLocalFile,
		sUserName,
		sPassphrase,
		22,,
		.T.,
		.T.,
		sKeyFile
	);

	:IF .NOT. bUploaded;
		ErrorMes("Instrument result upload failed");
		:RETURN .F.;
	:ENDIF;

	UsrMes("Instrument result upload completed");

	:RETURN .T.;
:ENDPROC;

/*
Run with DoProc("UploadInstrumentResult")
;
```

### Stop a multi-file workflow on the first failed upload

Call `SendToFtp` inside a loop and stop the workflow as soon as one upload fails.

```ssl
:PROCEDURE PublishOutboundFiles;
	:DECLARE sServer, sRemoteDir, sUserName, sPassword;
	:DECLARE aUploads;
	:DECLARE nIndex, bUploaded;

	sServer := "ftp.partner.example.com";
	sRemoteDir := "/outbound";
	sUserName := "nightly_feed";
	sPassword := "demo-password";

	aUploads := {
		{"C:/Exports/orders_20260419.txt", "orders_20260419.txt"},
		{"C:/Exports/results_20260419.txt", "results_20260419.txt"},
		{"C:/Exports/manifest_20260419.txt", "manifest_20260419.txt"}
	};

	:FOR nIndex := 1 :TO ALen(aUploads);
		bUploaded := SendToFtp(
			sServer,
			sRemoteDir,
			aUploads[nIndex, 2],
			aUploads[nIndex, 1],
			sUserName,
			sPassword,
			21,,
			.T.
		);

		:IF .NOT. bUploaded;
			ErrorMes("Outbound upload failed for " + aUploads[nIndex, 2]);
			/* Displays on failure: outbound upload message;
			:RETURN .F.;
		:ENDIF;
	:NEXT;

	UsrMes("All outbound files uploaded");

	:RETURN .T.;
:ENDPROC;

/*
Run with DoProc("PublishOutboundFiles")
;
```

## Related

- [`CopyToFtp`](CopyToFtp.md)
- [`WriteToFtp`](WriteToFtp.md)
- [`GetFromFtp`](GetFromFtp.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
