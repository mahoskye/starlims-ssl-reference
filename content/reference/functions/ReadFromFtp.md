---
title: "ReadFromFtp"
summary: "Retrieves a remote file as a string by using FTP, or SFTP when bIsSFTP is .T.."
id: ssl.function.readfromftp
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ReadFromFtp

Retrieves a remote file as a string by using FTP, or SFTP when `bIsSFTP` is [`.T.`](../literals/true.md).

`ReadFromFtp` reads the contents of a remote file into memory and returns them as a string. By default it uses FTP. If `bIsSFTP` is [`.T.`](../literals/true.md), it uses SFTP instead, and `sPrivateKeyFilePath` can be used for key-based login. The function throws immediately when `sServerNameOrIP` or `sRemoteFileName` is empty, and it also throws if `sProxy` is provided with a non-empty value.

For FTP, omitted or non-positive `nMaxSize` falls back to `64000`, and the read stops after that many bytes. For the current SFTP implementation, `nMaxSize` is validated the same way but not enforced during the actual file read, so the full remote file is returned. Transfer failures caught during the read return an empty string and log an error message.

## When to use

- When you need the contents of a remote text file directly in SSL without first saving it locally.
- When the same workflow must support FTP and optionally switch to SFTP.
- When you want to cap FTP reads with `nMaxSize` to avoid bringing large files into memory.
- When you need SFTP key-based authentication by passing `bIsSFTP` as [`.T.`](../literals/true.md) and supplying `sPrivateKeyFilePath`.

## Syntax

```ssl
ReadFromFtp(sServerNameOrIP, [sRemoteDirectory], sRemoteFileName, [nMaxSize], [sUserName], [sPassword], [nPort], [sProxy], [bIsSFTP], [sPrivateKeyFilePath])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sServerNameOrIP` | [string](../types/string.md) | yes | — | FTP or SFTP server name or IP address. Empty values raise an exception. |
| `sRemoteDirectory` | [string](../types/string.md) | no | `""` | Remote folder that contains the file. |
| `sRemoteFileName` | [string](../types/string.md) | yes | — | File name to read. Empty values raise an exception. |
| `nMaxSize` | [number](../types/number.md) | no | `64000` when omitted or `<= 0` | Maximum bytes to read on the FTP path. On the current SFTP path, the full file is still read. |
| `sUserName` | [string](../types/string.md) | no | `""` | User name passed to the FTP or SFTP login routine. |
| `sPassword` | [string](../types/string.md) | no | `""` | Password passed to the login routine. When `sPrivateKeyFilePath` is used for SFTP, this value is used as the private-key passphrase. |
| `nPort` | [number](../types/number.md) | no | `21` when omitted or `<= 0` | Network port for the connection. |
| `sProxy` | [string](../types/string.md) | no | `""` | Must be omitted or empty. Any non-empty value raises an exception. |
| `bIsSFTP` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Pass [`.T.`](../literals/true.md) to use SFTP instead of FTP. |
| `sPrivateKeyFilePath` | [string](../types/string.md) | no | `""` | Private key file for SFTP authentication. Ignored on the FTP path. |

## Returns

**[string](../types/string.md)** — The remote file contents; an empty string when the FTP or SFTP read operation fails with a handled transfer error.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sServerNameOrIP` is empty on the FTP path. | `FTP server name or IP cannot be missing.` |
| `sServerNameOrIP` is empty on the SFTP path. | `SFTP server name or IP cannot be missing.` |
| `sRemoteFileName` is empty. | `Remote file name cannot be missing.` |
| `sProxy` is non-empty. | `The proxy parameter cannot be used. The system will automatically use the proxy specified by Internet Explorer > Local Area Network settings.` |

## Best practices

!!! success "Do"
    - Check for an empty return value before processing the file contents.
    - Pass an explicit `nMaxSize` for FTP reads when the remote file size is uncertain.
    - Set `bIsSFTP` to [`.T.`](../literals/true.md) and use `sPrivateKeyFilePath` when the integration requires SFTP with key-based authentication.

!!! failure "Don't"
    - Assume the function chooses SFTP automatically. It uses FTP unless `bIsSFTP` is [`.T.`](../literals/true.md).
    - Rely on `nMaxSize` to limit the SFTP branch. The full file is read regardless of this argument.
    - Pass a non-empty `sProxy` value. The function throws before attempting the transfer.

## Caveats

- `sRemoteDirectory` is not validated as required. If you do not need a folder path, pass an empty string.
- SFTP connection, login, or private-key setup occurs before the SFTP read is wrapped in its transfer-error handler, so some SFTP failures may raise an exception instead of returning `""`.
- The function returns text. Binary files can produce unreadable content.

## Examples

### Read a small FTP status file

Retrieve a short status file and stop if nothing was returned.

```ssl
:PROCEDURE ReadStatusFile;
	:DECLARE sServer, sRemoteDir, sFileName, sUser, sPassword;
	:DECLARE sFileContent, sStatus;

	sServer := "instrumentftp.lab.local";
	sRemoteDir := "/exports/status";
	sFileName := "status.txt";
	sUser := "instrument_reader";
	sPassword := "read_only_pass";

	sFileContent := ReadFromFtp(
		sServer,
		sRemoteDir,
		sFileName,
		1024,
		sUser,
		sPassword
	);

	:IF Empty(sFileContent);
		UsrMes("No status file was returned.");
		:RETURN .F.;
	:ENDIF;

	sStatus := Upper(AllTrim(Left(sFileContent, 10)));

	InfoMes("Retrieved FTP status: " + sStatus);
	/* Displays status prefix;

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ReadStatusFile");
```

### Limit an FTP read before parsing a header row

Use `nMaxSize` to limit an FTP read, then extract just the first line for lightweight validation.

```ssl
:PROCEDURE ReadTransferHeader;
	:DECLARE sServer, sRemoteDir, sFileName, sUser, sPassword;
	:DECLARE sFileContent, sHeaderLine;
	:DECLARE nMaxSize, nLineEnd;

	sServer := "ftp.analytical-lab.com";
	sRemoteDir := "/logs/transfers";
	sFileName := "transfer_log_2024.txt";
	sUser := "lab_reader";
	sPassword := "P@ssw0rd";
	nMaxSize := 32768;

	sFileContent := ReadFromFtp(
		sServer,
		sRemoteDir,
		sFileName,
		nMaxSize,
		sUser,
		sPassword
	);

	:IF Empty(sFileContent);
		UsrMes("The transfer log could not be read.");
		:RETURN "";
	:ENDIF;

	nLineEnd := At(Chr(10), sFileContent);

	:IF nLineEnd > 0;
		sHeaderLine := Left(sFileContent, nLineEnd - 1);
	:ELSE;
		sHeaderLine := sFileContent;
	:ENDIF;

	:RETURN AllTrim(sHeaderLine);
:ENDPROC;

/* Usage;
DoProc("ReadTransferHeader");
```

### Read from SFTP with a private key

Switch to the SFTP branch, use a private key, and handle setup or transfer failures.

```ssl
:PROCEDURE GetPartnerManifest;
	:DECLARE sServer, sRemoteDir, sFileName, sUser;
	:DECLARE sKeyPassphrase, sPrivateKey, sContent;
	:DECLARE nPort, oErr;

	sServer := "sftp.partner.example.com";
	sRemoteDir := "/inbound/manifests";
	sFileName := "shipment_manifest.txt";
	sUser := "startransfer";
	sKeyPassphrase := "key_passphrase";
	sPrivateKey := "/secure/keys/partner_sftp_key.pem";
	nPort := 22;

	:TRY;
		sContent := ReadFromFtp(
			sServer,
			sRemoteDir,
			sFileName,
			64000,
			sUser,
			sKeyPassphrase,
			nPort,
			,
			.T.,
			sPrivateKey
		);

		:IF Empty(sContent);
			ErrorMes("The partner manifest could not be read from SFTP.");
			:RETURN "";
		:ENDIF;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("SFTP read failed: " + oErr:Description);
		/* Displays on failure: SFTP read failed;
		:RETURN "";
	:ENDTRY;

	:RETURN sContent;
:ENDPROC;

/* Usage;
DoProc("GetPartnerManifest");
```

## Related

- [`GetDirFromFtp`](GetDirFromFtp.md)
- [`string`](../types/string.md)
