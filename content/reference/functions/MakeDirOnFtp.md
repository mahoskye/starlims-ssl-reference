---
title: "MakeDirOnFtp"
summary: "Creates a remote directory by using FTP, or by using SFTP when bIsSFTP is .T.."
id: ssl.function.makedironftp
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# MakeDirOnFtp

Creates a remote directory by using FTP, or by using SFTP when `bIsSFTP` is [`.T.`](../literals/true.md).

On the FTP path, `MakeDirOnFtp` sends an FTP `MKD` request for the target directory and returns [`.T.`](../literals/true.md) only when the server reports that the path was created. On the SFTP path, it connects and logs in first, then attempts to create the directory and returns [`.T.`](../literals/true.md) when the SFTP library reports success.

Missing `sServerNameOrIP`, missing `sRemoteDirectory`, and a non-empty `sProxy` raise an error instead of returning [`.F.`](../literals/false.md). On the SFTP path, connection, login, and private-key setup happen before the function reaches its boolean return path, so those failures can also raise.

## When to use

- When you need to create a remote working folder before uploading files.
- When one script must support either FTP or SFTP with the same call shape.
- When you want a simple [`.T.`](../literals/true.md) or [`.F.`](../literals/false.md) result for the directory-creation request itself.

## Syntax

```ssl
MakeDirOnFtp(
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
| `sRemoteDirectory` | [string](../types/string.md) | yes | — | Remote directory path to create. |
| `sUserName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | User name passed to the FTP or SFTP login operation. |
| `sPassword` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | FTP password, or SFTP password or private-key passphrase. |
| `nPort` | [number](../types/number.md) | no | `21` | Server port. If omitted or less than or equal to `0`, the implementation uses `21` on both the FTP and SFTP paths. |
| `sProxy` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Must be omitted, [`NIL`](../literals/nil.md), or an empty string. A non-empty value raises an error. |
| `bIsSFTP` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Set to [`.T.`](../literals/true.md) to use the SFTP implementation. Omit it or pass [`NIL`](../literals/nil.md)/[`.F.`](../literals/false.md) to use FTP. |
| `sPrivateKeyFilePath` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Optional private key file for SFTP authentication. Ignored on the FTP path. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the remote directory creation call succeeds; [`.F.`](../literals/false.md) when the FTP request fails (handled as a `WebException` on the FTP path) or when the directory-creation call fails after a successful connect and login (SFTP path).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sServerNameOrIP` is [`NIL`](../literals/nil.md) or empty (FTP path). | `FTP server name or IP cannot be missing.` |
| `sServerNameOrIP` is [`NIL`](../literals/nil.md) or empty (SFTP path). | `SFTP server name or IP cannot be missing.` |
| `sRemoteDirectory` is [`NIL`](../literals/nil.md) or empty. | `Remote folder name cannot be missing.` |
| `sProxy` is a non-empty string. | `The proxy parameter cannot be used. The system will automatically use the proxy specified by Internet Explorer > Local Area Network settings.` |

## Best practices

!!! success "Do"
    - Pass `bIsSFTP` explicitly as [`.T.`](../literals/true.md) when the target server requires SFTP.
    - Pass `nPort` explicitly for SFTP servers that listen on `22`, because this API falls back to `21` when `nPort` is omitted or non-positive.
    - Leave `sProxy` empty and rely on the system proxy configuration.
    - Wrap SFTP calls in [`:TRY`](../keywords/TRY.md) and [`:CATCH`](../keywords/CATCH.md) when connection, login, or private-key setup failures must be handled separately from a [`.F.`](../literals/false.md) return.
    - Treat `sPassword` as the private-key passphrase when you also pass `sPrivateKeyFilePath` on the SFTP path.

!!! failure "Don't"
    - Assume SFTP automatically switches to port `22`. This function uses `21` unless you pass another `nPort`.
    - Pass a manual proxy string expecting the function to use it. A non-empty `sProxy` argument raises an error.
    - Assume every failure comes back as [`.F.`](../literals/false.md). On the SFTP path, some setup
      failures can raise before the boolean result is reached.
    - Document or code around a separate `MakeDirOnSftp` call when this API is already the supported entry point for both modes.

## Caveats

- On the SFTP path, supplying `sPrivateKeyFilePath` switches authentication to key-based login.

## Examples

### Create a folder on an FTP server

Create a remote folder by using the default FTP path and check the result.

```ssl
:PROCEDURE EnsureUploadFolder;
	:DECLARE sServer, sRemoteDir, sUserName, sPassword, bCreated;

	sServer := "ftp.example.com";
	sRemoteDir := "/uploads/incoming";
	sUserName := "ftp_user";
	sPassword := "secret";

	bCreated := MakeDirOnFtp(sServer, sRemoteDir, sUserName, sPassword);

	:IF bCreated;
		UsrMes("Remote folder created: " + sRemoteDir);
	:ELSE;
		UsrMes("Remote folder could not be created: " + sRemoteDir);
	:ENDIF;

	:RETURN bCreated;
:ENDPROC;

/* Usage;
DoProc("EnsureUploadFolder");
```

### Create a folder on an SFTP server with a private key

Use the SFTP path, pass the port explicitly, and handle setup failures separately.

```ssl
:PROCEDURE EnsurePartnerDropFolder;
	:DECLARE sServer, sRemoteDir, sUserName, sPassphrase, sKeyPath;
	:DECLARE bCreated, oErr;

	sServer := "sftp.example.com";
	sRemoteDir := "/drop/partner_1042";
	sUserName := "integration_user";
	sPassphrase := "key-passphrase";
	sKeyPath := "/keys/integration_user.ppk";

	:TRY;
		bCreated := MakeDirOnFtp(
			sServer,
			sRemoteDir,
			sUserName,
			sPassphrase,
			22,,
			.T.,
			sKeyPath
		);

	:CATCH;
		oErr := GetLastSSLError();
		UsrMes("SFTP setup failed: " + oErr:Description);
		/* Displays on failure: setup error details;
		:RETURN .F.;
	:ENDTRY;

	:IF bCreated;
		UsrMes("Partner drop folder created: " + sRemoteDir);
		:RETURN .T.;
	:ENDIF;

	UsrMes("Partner drop folder was not created: " + sRemoteDir);

	:RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("EnsurePartnerDropFolder");
```

### Create several remote folders and collect failures

Create a set of partner folders, keep processing after ordinary [`.F.`](../literals/false.md) results, and also capture raised setup failures.

```ssl
:PROCEDURE EnsurePartnerFolders;
	:DECLARE sServer, sUserName, sPassword;
	:DECLARE aRemoteDirs, aFailures;
	:DECLARE nIndex, bCreated;
	:DECLARE oErr;

	sServer := "ftp.example.com";
	sUserName := "batch_user";
	sPassword := "secret";
	aRemoteDirs := {
		"/partners/acme/incoming",
		"/partners/bright/incoming",
		"/partners/cedar/incoming"
	};
	aFailures := {};

	:FOR nIndex := 1 :TO ALen(aRemoteDirs);
		:TRY;
			bCreated := MakeDirOnFtp(
				sServer,
				aRemoteDirs[nIndex],
				sUserName,
				sPassword
			);

			:IF .NOT. bCreated;
				AAdd(aFailures, aRemoteDirs[nIndex]);
			:ENDIF;

		:CATCH;
			oErr := GetLastSSLError();
			AAdd(aFailures, aRemoteDirs[nIndex] + " (" + oErr:Description + ")");
		:ENDTRY;
	:NEXT;

	:IF ALen(aFailures) == 0;
		UsrMes("All partner folders are ready.");
		:RETURN .T.;
	:ENDIF;

	UsrMes("Some partner folders could not be created.");

	:FOR nIndex := 1 :TO ALen(aFailures);
		UsrMes(aFailures[nIndex]);
		/* Displays one failure entry per line;
	:NEXT;

	:RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("EnsurePartnerFolders");
```

## Related

- [`CheckOnFtp`](CheckOnFtp.md)
- [`DeleteDirOnFtp`](DeleteDirOnFtp.md)
- [`GetDirFromFtp`](GetDirFromFtp.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
