---
title: "SDMS"
summary: "Interacts with an external SDMS server to download documents, download Unified XML templates, create an SDMSDocUploader, and generate password hashes for SDMS authentication."
id: ssl.class.sdms
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SDMS

Interacts with an external SDMS server to download documents, download Unified XML templates, create an [`SDMSDocUploader`](SDMSDocUploader.md), and generate password hashes for SDMS authentication.

## When to use

- When you need to download an SDMS document to a local file path from SSL.
- When you need the original file, Unified XML, or a new revision of a document.
- When you need to download a Unified XML template by template ID or template name.
- When you need to create an [`SDMSDocUploader`](SDMSDocUploader.md) for upload workflows.
- When you need to generate HTTP or SOAP password hashes from a hexadecimal password value.

## Constructors

### `SDMS{}`

Creates an instance without loading connection settings.

### `SDMS{oCredentials}`

Creates an instance and reads connection settings from `oCredentials`.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `oCredentials` | [object](../types/object.md) | yes | Object that supplies the SDMS connection properties used by the class. |

Expected properties on `oCredentials`:

| Property | Type | Description |
|---|---|---|
| `SdmsUrl` | [string](../types/string.md) | Base SDMS URL. A trailing [`/`](../operators/divide.md) is added automatically if it is missing. |
| `SdmsUserName` | [string](../types/string.md) | User name sent with download requests. |
| `HttpPassHash` | [string](../types/string.md) | HTTP password hash sent with download requests. |
| `SdmsSiteId` | [number](../types/number.md) | Active site ID sent with download requests. |
| `SdmsSessionId` | [string](../types/string.md) | Session ID sent with requests when available. |

## Properties

| Name | Type | Access | Description |
|---|---|---|---|
| `ErrorMessage` | [string](../types/string.md) | read-only | Error text from the most recent failed download, check-out, or template download request. |
| `IsSessionExpired` | [boolean](../types/boolean.md) | read-only | Indicates whether the most recent download, check-out, or template download failed because the SDMS session expired. |
| `SessionId` | [string](../types/string.md) | read-write | Session ID to send with requests when it is not empty. |

## Methods

| Method | Returns | Description |
|---|---|---|
| `CheckOutDocument(sDocId, sDestinationPath)` | [boolean](../types/boolean.md) | Downloads the `NewRevision` version of a document to `sDestinationPath`. |
| `CreateDocUploader(oCredentials)` | [`SDMSDocUploader`](SDMSDocUploader.md) | Creates an [`SDMSDocUploader`](SDMSDocUploader.md) using the supplied credentials object. |
| `CreateUnifiedXmlDOM()` | [object](../types/object.md) | Creates and returns a Unified XML DOM object. |
| `DownloadDocument(sDocId, sDocType, sDownloadTo)` | none | Deprecated. Always raises an exception. |
| `DownloadDocument2(sDocId, sDocType, sDestinationPath)` | [boolean](../types/boolean.md) | Downloads the specified document type to `sDestinationPath`. |
| `DownloadOriginalDocument(sDocId, sDownloadTo)` | none | Deprecated. Always raises an exception. |
| `DownloadOriginalDocument2(sDocId, sDestinationPath)` | [boolean](../types/boolean.md) | Downloads the original document by calling `DownloadDocument2(sDocId, "ORG", sDestinationPath)`. |
| `DownloadUnifiedXmlDocument(sDocId, sDownloadTo)` | none | Deprecated. Always raises an exception. |
| `DownloadUnifiedXmlDocument2(sDocId, sDestinationPath)` | [boolean](../types/boolean.md) | Downloads the Unified XML version by calling `DownloadDocument2(sDocId, "UXML", sDestinationPath)`. |
| `DownloadUnifiedXmlTemplate(sTemplateId, sDestinationPath)` | [boolean](../types/boolean.md) | Downloads a Unified XML template by numeric template ID or by template name. |
| `GetHttpPassHash(sDictPass)` | [string](../types/string.md) | Converts a hexadecimal password string into the URL-encoded HTTP hash used by SDMS requests. |
| `GetSoapPassHash(sDictPass)` | [string](../types/string.md) | Converts a hexadecimal password string into the Base64 SOAP hash used by SDMS requests. |
| `SetSDMSConnection(sUrl, sUserName, sPass, bPassIsHashed)` | none | Deprecated. Always raises an exception. |
| `UploadDocument(sFullFilePath, sClientFileName, sFileType, aKeylist)` | [string](../types/string.md) | Deprecated. Always raises an exception before returning a value. |

## Exceptions

| Trigger | Exception message |
|---|---|
| Any call to `SetSDMSConnection`. | `Method is deprecated, please do not use anymore.` |
| Any call to `DownloadDocument`. | `Method is deprecated, please do not use anymore.` |
| Any call to `DownloadOriginalDocument`. | `Method is deprecated, please do not use anymore.` |
| Any call to `DownloadUnifiedXmlDocument`. | `Method is deprecated, please do not use anymore.` |
| Any call to `UploadDocument`. | `Method is deprecated, please do not use anymore.` |
| `DownloadUnifiedXmlTemplate` is called with `sTemplateId` as [`NIL`](../literals/nil.md). | `Argument sTemplateId cannot be null.` |
| `DownloadUnifiedXmlTemplate` is called with `sDestinationPath` as [`NIL`](../literals/nil.md). | `Argument sDestinationPath cannot be null.` |

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Construct `SDMS` with a credentials object when you plan to download files.
    - Use `DownloadOriginalDocument2`, `DownloadUnifiedXmlDocument2`, or `CheckOutDocument` when one of those fixed document types matches your intent.
    - Check the boolean return value and `ErrorMessage` after each download, check-out, or template download request.
    - Check `IsSessionExpired` after a failed request so you can distinguish session expiry from other download failures.
    - Pass a numeric string for `sTemplateId` when you want to address a template by ID, or pass the template name when you want name-based lookup.

!!! failure "Don't"
    - Use deprecated methods such as `DownloadDocument`, `DownloadOriginalDocument`, `DownloadUnifiedXmlDocument`, `SetSDMSConnection`, or `UploadDocument`, because they always raise their deprecation exception.
    - Rely on `SDMS{}` alone for download operations, because the class only loads its URL, user name, password hash, site ID, and initial session ID when you construct it with a credentials object.
    - Assume a failed request means the session expired, because `IsSessionExpired` is the flag that distinguishes session-expiry failures from other download errors.
    - Pass [`NIL`](../literals/nil.md) for `sTemplateId` or `sDestinationPath` to `DownloadUnifiedXmlTemplate`, because the method raises explicit argument exceptions for those values.
    - Ignore the exact meaning of `sDestinationPath`, because the download methods write to the path you provide rather than choosing a file name for you.

## Caveats

- `GetHttpPassHash` and `GetSoapPassHash` expect a hexadecimal password string.
- Failed download requests populate `ErrorMessage` with a message starting with `Unable to download document file from SDMS:`. A successful request clears `ErrorMessage`.
- `DownloadUnifiedXmlTemplate` treats a numeric `sTemplateId` as a template ID; any other string is sent as a template name.
- `IsSessionExpired` is reset to [`.F.`](../literals/false.md) before a successful response is returned. When a failed download reports `Please relogin. You session may be expired.`, `IsSessionExpired` is set to [`.T.`](../literals/true.md).

## Examples

### Download the original document

Constructs an `SDMS` instance with explicit credentials, then calls `DownloadOriginalDocument2` to write the document file to a local path. The `ErrorMessage` property describes the failure when the return value is [`.F.`](../literals/false.md).

```ssl
:PROCEDURE DownloadOriginalFromSdms;
	:DECLARE oCredentials, oSdms, sDocId, sFilePath, bDownloaded;

	oCredentials := CreateUdObject();
	oCredentials:SetProperty("SdmsUrl", "https://sdms.example.com");
	oCredentials:SetProperty("SdmsUserName", "lab_user");
	oCredentials:SetProperty("HttpPassHash", "encoded-http-pass-hash");
	oCredentials:SetProperty("SdmsSiteId", 101);
	oCredentials:SetProperty("SdmsSessionId", "session-token");

	oSdms := SDMS{oCredentials};
	sDocId := "DOC-2024-00142";
	sFilePath := "C:/Temp/doc-2024-00142.pdf";

	bDownloaded := oSdms:DownloadOriginalDocument2(sDocId, sFilePath);

	:IF bDownloaded;
		UsrMes("Downloaded " + sDocId + " to " + sFilePath);
	:ELSE;
		UsrMes("Download failed: " + oSdms:ErrorMessage);
		/* Displays on failure: download failed message;
	:ENDIF;
:ENDPROC;

DoProc("DownloadOriginalFromSdms");
```

### Download a Unified XML template and detect session expiry

Downloads a template by numeric ID, then checks `IsSessionExpired` on failure to distinguish a session timeout from other download errors.

```ssl
:PROCEDURE DownloadUxmlTemplate;
	:DECLARE oCredentials, oSdms, sTemplateId, sFilePath, bDownloaded;

	oCredentials := CreateUdObject();
	oCredentials:SetProperty("SdmsUrl", "https://sdms.example.com");
	oCredentials:SetProperty("SdmsUserName", "lab_user");
	oCredentials:SetProperty("HttpPassHash", "encoded-http-pass-hash");
	oCredentials:SetProperty("SdmsSiteId", 101);
	oCredentials:SetProperty("SdmsSessionId", "session-token");

	oSdms := SDMS{oCredentials};
	sTemplateId := "1250";
	sFilePath := "C:/Temp/template-1250.xml";

	bDownloaded := oSdms:DownloadUnifiedXmlTemplate(sTemplateId, sFilePath);

	:IF bDownloaded;
		UsrMes("Template downloaded to " + sFilePath);
	:ELSE;
		:IF oSdms:IsSessionExpired;
			UsrMes("Template download failed because the session expired");
		:ELSE;
			UsrMes("Template download failed: " + oSdms:ErrorMessage);
			/* Displays on failure: template download failed message;
		:ENDIF;
	:ENDIF;
:ENDPROC;

DoProc("DownloadUxmlTemplate");
```

## Related

- [`SDMSDocUploader`](SDMSDocUploader.md)
- [`object`](../types/object.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
- [`number`](../types/number.md)
