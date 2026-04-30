---
title: "FtpsClient"
summary: "Transfers files and manages directories on an FTPS server."
id: ssl.class.ftpsclient
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# FtpsClient

Transfers files and manages directories on an FTPS server.

`FtpsClient` lets SSL scripts connect to an FTPS server, authenticate, secure the session, and perform common remote file operations. Use it when you need to upload or download files, list remote directories, create or remove folders, or rename and move files.

The class does not open a session automatically. Create the object, apply any proxy or TLS settings you need, call `Connect`, then `Login`, and call `Secure` when the server workflow requires upgrading the session after connection. Most file and directory methods return [`.T.`](../literals/true.md) on success and [`.F.`](../literals/false.md) on failure. `Connect`, `Disconnect`, `Login`, and `ReadFromFtps` return strings.

## When to use

- When you need to exchange files with an FTPS server from SSL code.
- When you need to create, inspect, rename, move, or delete remote files and directories.
- When the FTPS connection must use an explicit proxy or custom TLS settings.

## Constructors

### `FtpsClient{}`

Creates a new FTPS client instance.

## Methods

### `SetFtpsProxy`

Applies proxy settings before connecting.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sProxyType` | [string](../types/string.md) | yes | Proxy type name. |
| `sProxy` | [string](../types/string.md) | yes | Proxy host name or address. |
| `nPort` | [number](../types/number.md) | yes | Proxy port. |
| `sUserName` | [string](../types/string.md) | yes | Proxy user name. |
| `sPassword` | [string](../types/string.md) | yes | Proxy password. |

**Returns:** none

The proxy type string must match a supported FTPS proxy mode name.

### `SetTlsParameters`

Sets TLS options and optional certificate details for later secure operations.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sAllowedSuites` | [string](../types/string.md) | yes | Allowed cipher suite name. |
| `sCommonName` | [string](../types/string.md) | yes | Expected certificate common name. |
| `sVersion` | [string](../types/string.md) | yes | TLS version name. |
| `sCertificateLocation` | [string](../types/string.md) | yes | Certificate source location. Supported values are `Path` and `Store`. |
| `sCertificatePath` | [string](../types/string.md) | yes | Certificate file path when `sCertificateLocation` is `Path`. |
| `sCertificatePassword` | [string](../types/string.md) | yes | Certificate password when a certificate file requires one. |

**Returns:** none

`sCertificateLocation` must be `Path` or `Store`.

### `Connect`

Connects to the FTPS server.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sServerName` | [string](../types/string.md) | yes | FTPS server name or IP address. |
| `nServerPort` | [number](../types/number.md) | yes | Server port. |
| `sSecurity` | [string](../types/string.md) | no | Security mode to use during connection. When omitted or empty, the client uses the two-argument connect flow. Supported values include `Unsecure`, `Implicit`, `Secure`, `Explicit`, and `TumbleweedTunnel`. |

**Returns:** [string](../types/string.md) — Server response text from the connect operation.

### `Disconnect`

Closes the server session.

**Returns:** [string](../types/string.md) — Server response text from the disconnect operation.

### `Login`

Authenticates to the connected server.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sUserName` | [string](../types/string.md) | yes | FTPS user name. |
| `sPassword` | [string](../types/string.md) | yes | FTPS password. |
| `sAccount` | [string](../types/string.md) | yes | FTPS account value. Pass `""` when the server does not require it. |

**Returns:** [string](../types/string.md) — Server response text from the login operation.

### `Secure`

Secures the current session. If you previously called `SetTlsParameters`, those settings are applied here. Without prior TLS settings, the method secures the session with the default FTPS TLS handling.

**Returns:** none

### `CheckOnFtps`

Checks whether a remote file exists.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sRemoteDirectory` | [string](../types/string.md) | yes | Remote directory path. Pass `""` to check a file path without a directory prefix. |
| `sRemoteFileName` | [string](../types/string.md) | yes | Remote file name. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the file can be found, otherwise [`.F.`](../literals/false.md).

**Raises:**
- An error when `sRemoteFileName` is empty.

### `CopyToFtps`

Writes the same content to multiple remote files.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sRemoteDirectory` | [string](../types/string.md) | yes | Remote directory path. |
| `aRemoteFileNames` | [array](../types/array.md) | yes | Array of target file names. |
| `sFileContents` | [string](../types/string.md) | yes | Content written to each file. [`NIL`](../literals/nil.md) is treated as an empty string. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when every write succeeds, otherwise [`.F.`](../literals/false.md).

**Raises:**
- An error when `aRemoteFileNames` is [`NIL`](../literals/nil.md).
- An error when any element in `aRemoteFileNames` is empty.

### `DeleteDirOnFtps`

Deletes a remote directory.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sRemoteDirectory` | [string](../types/string.md) | yes | Remote directory path to remove. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) on success, otherwise [`.F.`](../literals/false.md).

**Raises:**
- An error when `sRemoteDirectory` is empty.

### `DeleteFromFtps`

Deletes a remote file.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sRemoteDirectory` | [string](../types/string.md) | yes | Remote directory path. Pass `""` to address the file directly. |
| `sRemoteFileName` | [string](../types/string.md) | yes | Remote file name. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) on success, otherwise [`.F.`](../literals/false.md).

**Raises:**
- An error when `sRemoteFileName` is empty.

### `GetDirFromFtps`

Returns a detailed listing for a remote directory.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sRemoteDirectory` | [string](../types/string.md) | yes | Remote directory path. |

**Returns:** [array](../types/array.md) — A 2D array where each row contains `{name, size, date, time, attributes}`. `name`, [`date`](../types/date.md), `time`, and `attributes` are strings. `size` is numeric. `attributes` is `"D"` for directories and `"A"` for files. Returns [`NIL`](../literals/nil.md) when the listing request fails.

### `GetDirNamesFromFtps`

Returns file and directory names from a remote directory.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sRemoteDirectory` | [string](../types/string.md) | yes | Remote directory path. |

**Returns:** [array](../types/array.md) — An array of entry names. Returns [`NIL`](../literals/nil.md) when the request fails.

### `GetFromFtps`

Downloads a remote file to a local file.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sRemoteDirectory` | [string](../types/string.md) | yes | Remote directory path. Pass `""` to address the file directly. |
| `sRemoteFileName` | [string](../types/string.md) | yes | Remote file name. |
| `sLocalFileName` | [string](../types/string.md) | yes | Local output file path. When empty, the remote file name is used. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) on success, otherwise [`.F.`](../literals/false.md).

**Raises:**
- An error when `sRemoteFileName` is empty.

### `MakeDirOnFtps`

Creates a remote directory.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sRemoteDirectory` | [string](../types/string.md) | yes | Remote directory path to create. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the server reports a non-empty creation result, otherwise [`.F.`](../literals/false.md).

**Raises:**
- An error when `sRemoteDirectory` is empty.

### `MoveInFtps`

Moves a file by downloading it to a temporary local file, uploading it to the target location, and deleting the original remote file.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sRemoteDirectoryFrom` | [string](../types/string.md) | yes | Source remote directory path. |
| `sRemoteDirectoryTo` | [string](../types/string.md) | yes | Destination remote directory path. |
| `sRemoteFileFrom` | [string](../types/string.md) | yes | Source remote file name. |
| `sRemoteFileTo` | [string](../types/string.md) | yes | Destination remote file name. When empty, the source file name is reused. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) on success, otherwise [`.F.`](../literals/false.md).

**Raises:**
- An error when `sRemoteFileFrom` is empty.

### `ReadFromFtps`

Reads the full contents of a remote file and returns them as a string.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sRemoteDirectory` | [string](../types/string.md) | yes | Remote directory path. Pass `""` to address the file directly. |
| `sRemoteFileName` | [string](../types/string.md) | yes | Remote file name. |
| `nMaxSize` | [number](../types/number.md) | no | Optional size argument. If omitted or less than or equal to `0`, the method uses `64000`. Note that the full file is read regardless of this value. |

**Returns:** [string](../types/string.md) — File contents, or `""` when the read fails.

**Raises:**
- An error when `sRemoteFileName` is empty.

### `RenameOnFtps`

Renames a file in a remote directory.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sRemoteDirectory` | [string](../types/string.md) | yes | Remote directory path. |
| `sFileNameOld` | [string](../types/string.md) | yes | Existing file name. |
| `sFileNameNew` | [string](../types/string.md) | yes | New file name. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) on success, otherwise [`.F.`](../literals/false.md).

**Raises:**
- An error when `sFileNameOld` is empty.
- An error when `sFileNameNew` is empty.
- An error when `sFileNameNew` matches `sFileNameOld` after trimming and case normalization.

### `SendToFtps`

Uploads a local file to the server.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sRemoteDirectory` | [string](../types/string.md) | yes | Remote directory path. Pass `""` to upload to the current remote location. |
| `sRemoteFileName` | [string](../types/string.md) | yes | Remote file name. When empty, the local file name is used. |
| `sLocalFileName` | [string](../types/string.md) | yes | Local file path to upload. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) on success, otherwise [`.F.`](../literals/false.md).

**Raises:**
- An error when `sLocalFileName` is empty.

### `WriteToFtps`

Writes string content to a remote file.

If the target file already exists, the method writes starting at the current file length, so the new content is appended rather than replacing the existing file.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sRemoteDirectory` | [string](../types/string.md) | yes | Remote directory path. Pass `""` to address the file directly. |
| `sRemoteFileName` | [string](../types/string.md) | yes | Remote file name. |
| `sFileContents` | [string](../types/string.md) | yes | Content to write. [`NIL`](../literals/nil.md) is treated as an empty string. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) on success, otherwise [`.F.`](../literals/false.md).

**Raises:**
- An error when `sRemoteFileName` is empty.

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Configure proxy and TLS settings before `Connect` so the session starts with the intended network and certificate behavior.
    - Call `Connect`, then `Login`, then `Secure` only when that matches the server workflow you need.
    - Check boolean return values after file and directory operations so your script can stop or recover cleanly.
    - Validate remote file names, directory paths, and local file paths before
      calling methods that require them.
    - Call `Disconnect` when the transfer session is complete.
    - Treat `WriteToFtps` as an append operation when the remote file already exists.

!!! failure "Don't"
    - Call file or directory methods before a successful connection and login. Those operations depend on an active authenticated session.
    - Pass empty file names, directory paths, or local file paths to methods that validate them. They can raise argument errors.
    - Assume `WriteToFtps` overwrites an existing file. The current behavior appends at the existing remote file length.
    - Rely on `ReadFromFtps(maxSize)` to enforce a hard read limit. The full file contents are read regardless of the `nMaxSize` argument.
    - Forget to disconnect. This class does not automatically close the session for you.

## Caveats

- `CheckOnFtps` checks for a file, not for directory existence.
- `CopyToFtps` writes identical content to every name in `aRemoteFileNames`.
- `GetDirFromFtps` returns rows in the shape `{name, size, date, time, attributes}`, with [`date`](../types/date.md) and `time` returned as strings.
- `GetDirNamesFromFtps` and `GetDirFromFtps` return [`NIL`](../literals/nil.md) when the server request fails.
- `ReadFromFtps` returns `""` on failure.
- `SendToFtps` uses the local file name when `sRemoteFileName` is empty.
- `GetFromFtps` uses the remote file name when `sLocalFileName` is empty.

## Examples

### Upload a local file

Establishes a full `Connect` -> `Login` -> `Secure` session in explicit TLS mode, uploads a local file with `SendToFtps`, and logs the server response from each step. [`:FINALLY`](../keywords/FINALLY.md) guarantees `Disconnect` runs even if `SendToFtps` fails.

```ssl
:PROCEDURE UploadReportToFtps;
	:DECLARE oFtps, sResult, bOk, oErr;

	oFtps := FtpsClient{};

	:TRY;
		sResult := oFtps:Connect("ftp.example.com", 21, "Explicit");
		UsrMes("Connect: " + sResult);
		/* Displays: connect response text;

		sResult := oFtps:Login("reports_user", "secure_password", "");
		UsrMes("Login: " + sResult);
		/* Displays: login response text;

		oFtps:Secure();

		bOk := oFtps:SendToFtps(
			"/data/reports",
			"weekly_report.txt",
			"C:/Temp/weekly_report.txt"
		);

		:IF bOk;
			UsrMes("Upload completed.");
		:ELSE;
			UsrMes("Upload failed.");
		:ENDIF;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("FTPS Error", oErr:Description);
		/* Displays on failure: FTPS error details;
	:FINALLY;
		sResult := oFtps:Disconnect();
		UsrMes("Disconnect: " + sResult);
		/* Displays: disconnect response text;
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("UploadReportToFtps");
```

### List a directory and verify a file

Reads a remote directory with `GetDirFromFtps`, prints each entry's name, size, date, time, and attributes, then calls `CheckOnFtps` to confirm a specific file is present. Each row of the 2D listing array is formatted as a [`|`](../operators/or.md)-delimited line.

```ssl
:PROCEDURE ReviewFtpsFolder;
	:DECLARE oFtps, aEntries, nIndex, bFound, sResult, sLine, oErr;

	oFtps := FtpsClient{};

	:TRY;
		sResult := oFtps:Connect("ftp.example.com", 21, "Explicit");
		sResult := oFtps:Login("qc_user", "secure_password", "");

		oFtps:Secure();

		aEntries := oFtps:GetDirFromFtps("/qc/archive");

		:IF Empty(aEntries);
			UsrMes("No entries returned.");
		:ELSE;
			:FOR nIndex := 1 :TO ALen(aEntries);
				sLine := aEntries[nIndex, 1] + " | ";
				sLine := sLine + LimsString(aEntries[nIndex, 2]) + " | ";
				sLine := sLine + aEntries[nIndex, 3] + " | ";
				sLine := sLine + aEntries[nIndex, 4] + " | ";
				sLine := sLine + aEntries[nIndex, 5];
				UsrMes(sLine);
				/* Displays: one directory entry;
			:NEXT;
		:ENDIF;

		bFound := oFtps:CheckOnFtps("/qc/archive", "batch_1001.csv");

		:IF bFound;
			UsrMes("batch_1001.csv is present.");
		:ELSE;
			UsrMes("batch_1001.csv was not found.");
		:ENDIF;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("FTPS Error", oErr:Description);
		/* Displays on failure: FTPS error details;
	:FINALLY;
		sResult := oFtps:Disconnect();
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ReviewFtpsFolder");
```

### Append content with custom TLS settings

Calls `SetTlsParameters` before `Connect` to specify a cipher suite, expected common name, and certificate file. Then `WriteToFtps` appends a CRLF-terminated log line to an existing remote file because `WriteToFtps` writes starting at the current file length, so the call adds to rather than replaces the log.

```ssl
:PROCEDURE AppendComplianceLog;
	:DECLARE oFtps, sContent, sResult, bOk, oErr;

	oFtps := FtpsClient{};

	oFtps:SetTlsParameters(
		"TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
		"ftp.example.com",
		"TLS12",
		"Path",
		"C:/Certificates/ComplianceFTPS.pfx",
		"CertPassword123"
	);

	:TRY;
		sResult := oFtps:Connect("ftp.example.com", 21, "Explicit");
		sResult := oFtps:Login("compliance_user", "secure_password", "");

		oFtps:Secure();

		sContent := "Batch 1001 validated" + Chr(13) + Chr(10);
		bOk := oFtps:WriteToFtps(
			"/regulated/logs",
			"compliance.log",
			sContent
		);

		:IF bOk;
			UsrMes("Log entry appended.");
		:ELSE;
			UsrMes("Log append failed.");
		:ENDIF;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("FTPS Error", oErr:Description);
		/* Displays on failure: FTPS error details;
	:FINALLY;
		sResult := oFtps:Disconnect();
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("AppendComplianceLog");
```

## Related

- [`GetLastSSLError`](../functions/GetLastSSLError.md)
- [`ClearLastSSLError`](../functions/ClearLastSSLError.md)
