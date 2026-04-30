---
title: "SDMSDocUploader"
summary: "Uploads files into SDMS, attaches uploads to workflow steps, and checks in document revisions."
id: ssl.class.sdmsdocuploader
element_type: class
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SDMSDocUploader

Uploads files into SDMS, attaches uploads to workflow steps, and checks in document revisions.

`SDMSDocUploader` is an SDMS-focused helper class for sending local files to SDMS and, when needed, adding workflow context to those uploads. You can create it directly with `SDMSDocUploader{}` or `SDMSDocUploader{oCredentials}`, or obtain it from `SDMS:CreateDocUploader(oCredentials)`. Most upload-oriented methods return a boolean result and populate the inherited `ErrorMessage` property when the upload fails. `DoUpload()` is the exception: it returns the resulting document ID on success or `0` on failure.

## When to use

- When you need to upload a new file into SDMS.
- When you need to attach a document to a specific workflow, stage, and action.
- When you need to attach an additional file to an existing SDMS document.
- When you need to check in a new revision of an existing SDMS document.
- When you need to upload Office templates or ELN documents through the SDMS uploader.

## Constructors

### `SDMSDocUploader{oCredentials}`

Creates an uploader and loads the SDMS URL, username, password hash, site ID, and session ID from the credentials object. Workflow IDs start in a missing state and must be set before workflow-specific calls.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `oCredentials` | [object](../types/object.md) | yes | Credentials object supplying SDMS URL, username, password hash, site ID, and session ID. |

### `SDMSDocUploader{}`

Creates an uploader without loading SDMS connection or authentication values. Workflow IDs start at `0`, so the workflow-specific missing-ID validation described below does not run automatically unless you assign your own values.

## Properties

| Name | Type | Access | Description |
|---|---|---|---|
| `FilePath` | [string](../types/string.md) | read-write | Local path of the file to upload or attach. |
| `DocName` | [string](../types/string.md) | read-write | Document name sent to SDMS. For most upload methods, if this is blank it defaults to the file name from `FilePath`. `CheckInDocument()` still requires it to be set. |
| `DocId` | [number](../types/number.md) | read-write | Target SDMS document ID. Uploads that return a document ID also update this property from the SDMS response. |
| `FileType` | [string](../types/string.md) | read-write | SDMS file type value for upload requests. If blank, most upload methods use `Default`. |
| `ProjectName` | [string](../types/string.md) | read-write | SDMS project name for upload requests. If blank, most upload methods use `DefaultProject`. |
| `WorkflowId` | [number](../types/number.md) | read-write | Workflow identifier used by workflow-specific methods. |
| `StageId` | [number](../types/number.md) | read-write | Workflow stage identifier used by workflow-specific methods. |
| `ActionId` | [number](../types/number.md) | read-write | Workflow action identifier used by workflow-specific methods. |
| `Metadata` | [array](../types/array.md) | read-write | Array of `{key, value}` pairs used only by `UploadOriginalDoc()` when `UXmlTemplate` is also set. |
| `UXmlTemplate` | [string](../types/string.md) | read-write | UXML content used only by `UploadOriginalDoc()` when `Metadata` is also set. |

## Methods

| Method | Returns | Description |
|---|---|---|
| `UploadOriginalDoc()` | [boolean](../types/boolean.md) | Uploads the file as an original SDMS document. |
| `AttachDocToWorkflow()` | [boolean](../types/boolean.md) | Uploads the file and attaches it to the configured workflow, stage, and action. |
| `CheckInDocument(sRevision, sVersionStatus)` | [boolean](../types/boolean.md) | Checks in a new revision for an existing SDMS document. |
| `AttachFileToDocument()` | [boolean](../types/boolean.md) | Attaches a file to an existing SDMS document. |
| `UploadOfficeTemplate()` | [boolean](../types/boolean.md) | Uploads the file as an Office template. |
| `UploadELNDocument()` | [boolean](../types/boolean.md) | Uploads the file as an ELN document. |
| `AddHeader(sKey, sValue)` | none | Adds a custom header to later requests made by this uploader instance. |
| `RemoveHeader(sKey)` | none | Removes a custom header from later requests made by this uploader instance. |
| `DoUpload(sFilePath, sSdmsUrl)` | [number](../types/number.md) | Performs a low-level upload and returns the document ID on success. |
| `CheckInWorkflowDocument(sRevision, sVersionStatus[, nDocEntryPoint])` | [boolean](../types/boolean.md) | Adds workflow context, then checks in a document revision. |
| `UploadNewRevisionForWorkflowDocument([sCustomMessage])` | [boolean](../types/boolean.md) | Uploads a new workflow revision with version status `newDoc`. |

### `UploadOriginalDoc`

Uploads the file as an original SDMS document.

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) on success, [`.F.`](../literals/false.md) on failure.

If both `Metadata` and `UXmlTemplate` are set and the initial upload succeeds, the uploader also sends the UXML content for the same document.

### `AttachDocToWorkflow`

Uploads the file and associates it with the configured workflow, stage, and action.

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) on success, [`.F.`](../literals/false.md) on upload failure.

**Raises:**
- `Workflow id cannot be missing. Please set it using the WorkflowId property.`
- `Stage id cannot be missing. Please set it using the StageId property.`
- `Action id cannot be missing. Please set it using the ActionId property.`

### `CheckInDocument`

Checks in a new revision for an existing SDMS document.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `sRevision` | [string](../types/string.md) | yes | Revision value to send with the check-in request. |
| `sVersionStatus` | [string](../types/string.md) | yes | Version status to send with the check-in request. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) on success, [`.F.`](../literals/false.md) if the upload request fails.

**Raises:**
- `SDMS document uploader - check in operation: file path cannot be missing.`
- `SDMS document uploader - check in operation: document ID cannot be missing.`
- `SDMS document uploader - check in operation: document name cannot be missing.`

### `AttachFileToDocument`

Attaches a file to an existing SDMS document.

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) on success, [`.F.`](../literals/false.md) on upload failure.

**Raises:**
- `SDMS document uploader - attach file to document operation: file path for attachment cannot be missing.`
- `SDMS document uploader - attach file to document operation: document ID cannot be missing.`

### `UploadOfficeTemplate`

Uploads the file as an Office template document.

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) on success, [`.F.`](../literals/false.md) on upload failure.

**Raises:**
- `SDMS document uploader - upload Office template operation: file path for document cannot be missing.`

### `UploadELNDocument`

Uploads the file as an ELN document.

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) on success, [`.F.`](../literals/false.md) on upload failure.

**Raises:**
- `SDMS document uploader - upload ELN document operation: file path for document cannot be missing.`

### `AddHeader`

Adds a custom header to this uploader instance.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `sKey` | [string](../types/string.md) | yes | Header name. |
| `sValue` | [string](../types/string.md) | yes | Header value. |

**Returns:** none — No return value.

### `RemoveHeader`

Removes a custom header from this uploader instance.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `sKey` | [string](../types/string.md) | yes | Header name to remove. |

**Returns:** none — No return value.

### `DoUpload`

Performs a low-level upload to the supplied SDMS URL.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `sFilePath` | [string](../types/string.md) | yes | Local path of the file to upload. |
| `sSdmsUrl` | [string](../types/string.md) | yes | SDMS base URL used for the upload. |

**Returns:** [number](../types/number.md) — Document ID on success, or `0` on failure.

### `CheckInWorkflowDocument`

Adds workflow context, then performs the same check-in behavior as `CheckInDocument()`.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `sRevision` | [string](../types/string.md) | yes | Revision value to send with the check-in request. |
| `sVersionStatus` | [string](../types/string.md) | yes | Version status to send with the check-in request. |
| `nDocEntryPoint` | [number](../types/number.md) | no | Workflow entry point value used as the source stage header. When [`NIL`](../literals/nil.md) or omitted, the source stage header is not added. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) on success, [`.F.`](../literals/false.md) on upload failure.

**Raises:**
- `SDMS document uploader - check in operation: workflow ID cannot be missing.`
- `SDMS document uploader - check in operation: stage ID cannot be missing.`
- `SDMS document uploader - check in operation: action ID cannot be missing.`
- Any validation error documented for `CheckInDocument()`.

### `UploadNewRevisionForWorkflowDocument`

Uploads a new workflow revision and sends version status `newDoc`.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `sCustomMessage` | [string](../types/string.md) | no | Optional custom message to include in the request. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) on success, [`.F.`](../literals/false.md) on upload failure.

**Raises:**
- `SDMS document uploader - check in operation: workflow ID cannot be missing.`
- `SDMS document uploader - check in operation: stage ID cannot be missing.`
- `SDMS document uploader - check in operation: action ID cannot be missing.`

## Inheritance

**Base class:** [`SDMS`](SDMS.md)

This class also inherits the SDMS `ErrorMessage`, `SessionId`, and `IsSessionExpired` properties.

## Best practices

!!! success "Do"
    - Use `SDMSDocUploader{oCredentials}` when the upload requires established SDMS connection and authentication values.
    - Set `FilePath` before calling any upload, attach, or check-in method that depends on the instance properties.
    - Set `DocId` and `DocName` before `CheckInDocument()` and set `DocId` before `AttachFileToDocument()`.
    - Set `WorkflowId`, `StageId`, and `ActionId` before calling workflow-specific methods.
    - Check the boolean result or returned document ID after every call and inspect `ErrorMessage` when the operation fails.
    - Set both `Metadata` and `UXmlTemplate` before `UploadOriginalDoc()` when you need the related UXML upload.

!!! failure "Don't"
    - Assume the parameterless constructor supplies SDMS connection details. It does not load them for you.
    - Rely on workflow methods to infer missing workflow IDs. Missing-ID validation is only triggered in the cases documented above, and parameterless instances can pass zero-valued workflow IDs instead.
    - Call `CheckInDocument()` without `FilePath`, `DocId`, and `DocName`. That raises validation errors before the upload starts.
    - Expect `Metadata` or `UXmlTemplate` to affect workflow attachment, revision upload, Office template upload, or ELN upload. They are only used by `UploadOriginalDoc()`.
    - Treat `DoUpload()` as a full replacement for the higher-level helpers. It uploads the file to a supplied SDMS URL, but it does not prepare the standard document or workflow context for you.

## Caveats

- `UploadOriginalDoc()`, `AttachDocToWorkflow()`, `AttachFileToDocument()`, `UploadOfficeTemplate()`, `UploadELNDocument()`, and `UploadNewRevisionForWorkflowDocument()` can auto-fill blank `DocName`, `FileType`, and `ProjectName` values.
- `CheckInDocument()` does not auto-fill `DocName`; it raises an error if `DocName` is blank.
- `AttachDocToWorkflow()` validates missing workflow IDs only when those properties are still in the missing-value state used by the credentialed constructor.
- `CheckInWorkflowDocument()` accepts [`NIL`](../literals/nil.md) for `nDocEntryPoint`; in that case it skips the source stage header.
- `DoUpload()` returns the document ID, while the higher-level helper methods return booleans.
- When `UploadOriginalDoc()` runs the UXML upload, `FilePath` is overwritten with a temporary path. Reassign `FilePath` before reusing the same uploader instance.
- Large files are uploaded automatically in multiple chunks.

## Examples

### Upload an original document

Creates a credentials object, builds an `SDMSDocUploader`, then uploads a PDF file as an original SDMS document. The `DocId` property is updated from the SDMS response on success.

```ssl
:PROCEDURE UploadOriginalSdmsDocument;
    :DECLARE oCredentials, oUploader, bUploaded;

    oCredentials := CreateUdObject({
        {"SdmsUrl", "https://sdms.example/"},
        {"SdmsUserName", "sdms_user"},
        {"HttpPassHash", "encoded-pass-hash"},
        {"SdmsSiteId", 1},
        {"SdmsSessionId", ""}
    });

    oUploader := SDMSDocUploader{oCredentials};
    oUploader:FilePath := "C:/Docs/AnalysisReport.pdf";
    oUploader:FileType := "PDF";
    oUploader:ProjectName := "Laboratory Results";

    bUploaded := oUploader:UploadOriginalDoc();

    :IF bUploaded;
        UsrMes("Uploaded document ID " + LimsString(oUploader:DocId));
    :ELSE;
        ErrorMes("Upload Failed", oUploader:ErrorMessage);
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("UploadOriginalSdmsDocument");
```

### Attach a document to a workflow step

Sets the workflow, stage, and action IDs on an `SDMSDocUploader` instance, then calls `AttachDocToWorkflow()` to upload the file and associate it with that workflow context.

```ssl
:PROCEDURE AttachDocumentToWorkflowStep;
    :DECLARE oCredentials, oUploader, bAttached;

    oCredentials := CreateUdObject({
        {"SdmsUrl", "https://sdms.example/"},
        {"SdmsUserName", "sdms_user"},
        {"HttpPassHash", "encoded-pass-hash"},
        {"SdmsSiteId", 1},
        {"SdmsSessionId", ""}
    });

    oUploader := SDMSDocUploader{oCredentials};
    oUploader:FilePath := "C:/Docs/BatchRecord.pdf";
    oUploader:DocName := "BatchRecord.pdf";
    oUploader:WorkflowId := 1205;
    oUploader:StageId := 3;
    oUploader:ActionId := 2;

    bAttached := oUploader:AttachDocToWorkflow();

    :IF bAttached;
        UsrMes("Workflow attachment completed");
    :ELSE;
        ErrorMes("Workflow Error", oUploader:ErrorMessage);
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("AttachDocumentToWorkflowStep");
```

### Check in a document revision

Sets `DocId`, `DocName`, and `FilePath` on an existing document, then calls `CheckInDocument()` inside a [`:TRY`](../keywords/TRY.md) block to handle the validation errors raised when required properties are missing.

```ssl
:PROCEDURE CheckInSdmsRevision;
    :DECLARE oCredentials, oUploader, bCheckedIn, oErr;

    oCredentials := CreateUdObject({
        {"SdmsUrl", "https://sdms.example/"},
        {"SdmsUserName", "sdms_user"},
        {"HttpPassHash", "encoded-pass-hash"},
        {"SdmsSiteId", 1},
        {"SdmsSessionId", ""}
    });

    oUploader := SDMSDocUploader{oCredentials};
    oUploader:DocId := 10045;
    oUploader:DocName := "AnalysisReport.pdf";
    oUploader:FilePath := "C:/Docs/AnalysisReport_v2.pdf";

    :TRY;
        bCheckedIn := oUploader:CheckInDocument("2.1", "RELEASED");

        :IF bCheckedIn;
            UsrMes("Revision check-in completed");
        :ELSE;
            ErrorMes("Check-in Failed", oUploader:ErrorMessage);
        :ENDIF;

    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("Check-in Error", oErr:Description);
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("CheckInSdmsRevision");
```

## Related

- [`SDMS`](SDMS.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
- [`boolean`](../types/boolean.md)
- [`object`](../types/object.md)
