---
title: "DocExportDocument"
summary: "Exports a specified document to a chosen format and returns the result as a string."
id: ssl.function.docexportdocument
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocExportDocument

Exports a specified document to a chosen format and returns the result as a string.

`DocExportDocument` exports a Documentum document and returns the exported content as a string. It supports both `DocExportDocument(sDocumentId)` and `DocExportDocument(sDocumentId, sFormat)`. The function validates only `sDocumentId` before attempting the Documentum call: passing [`NIL`](../literals/nil.md) raises an argument error.

The underlying Documentum call returns an empty string when it does not produce an export result. When you need to know whether that empty string came from a Documentum failure, check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after the call.

## When to use

- When you need the exported document content in a string value for downstream processing.
- When your workflow needs to export a known document ID in either the default format or an explicitly requested format.
- When you want to detect Documentum export failures with [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) after the call.
- When you are already working inside an initialized Documentum session.

## Syntax

```ssl
DocExportDocument(sDocumentId, [sFormat])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sDocumentId` | [string](../types/string.md) | yes | — | Document identifier to export. |
| `sFormat` | [string](../types/string.md) | no | omitted | Export format to request. When omitted, the one-argument overload is used. |

## Returns

**[string](../types/string.md)** — The exported document content when the Documentum export succeeds.
`""` when the underlying Documentum call returns no value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDocumentId` is [`NIL`](../literals/nil.md). | `sDocumentId argument cannot be null` |

## Best practices

!!! success "Do"
    - Validate that `sDocumentId` is populated before calling the function.
    - Initialize the Documentum interface and log in before exporting.
    - Pass `sFormat` explicitly when downstream code expects a specific export type.
    - Check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after an empty-string result.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sDocumentId`; that raises an argument error instead of
      returning `""`.
    - Call the function before the Documentum interface is initialized.
    - Assume `""` means the document was simply empty; inspect the Documentum failure state before deciding how to handle the result.
    - Rely on the default format when a specific `sFormat` is part of your contract with another system.

## Caveats

- Only [`NIL`](../literals/nil.md) is rejected for `sDocumentId`. Blank strings are passed through to the Documentum layer.
- The accepted format strings are not documented here. Use only formats supported by your Documentum configuration.

## Examples

### Export with an explicit format

Logs in, requests a PDF export for a specific document ID, checks [`DocCommandFailed`](DocCommandFailed.md) on an empty result, and returns the export data string on success.

```ssl
:PROCEDURE ExportDocumentAsPdf;
	:DECLARE sDocBase, sUser, sPassword, sDocumentId, sExportData;

	sDocBase := "ProductionDB";
	sUser := "doc_user";
	sPassword := "doc_password";
	sDocumentId := "0900000180001234";

	DocInitDocumentumInterface();

	:TRY;
		:IF .NOT. DocLoginToDocumentum(sDocBase, sUser, sPassword);
			ErrorMes("Documentum login failed: " + DocGetErrorMessage());
			:RETURN "";
		:ENDIF;

		sExportData := DocExportDocument(sDocumentId, "PDF");

		:IF DocCommandFailed();
			ErrorMes("Document export failed: " + DocGetErrorMessage());
			:RETURN "";
		:ENDIF;

		UsrMes("Document exported successfully: " + sDocumentId);

		:RETURN sExportData;
	:FINALLY;
		DocEndDocumentumInterface();
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ExportDocumentAsPdf");
```

### Export using the default format

Exports a document without specifying a format, demonstrating the single-argument call form, and checks [`DocCommandFailed`](DocCommandFailed.md) on the return to detect backend failures.

```ssl
:PROCEDURE ExportDocumentDefaultFormat;
	:PARAMETERS sDocumentId;
	:DECLARE sDocBase, sUser, sPassword, sExportData;

	sDocBase := "ProductionDB";
	sUser := "doc_user";
	sPassword := "doc_password";

	DocInitDocumentumInterface();

	:TRY;
		:IF .NOT. DocLoginToDocumentum(sDocBase, sUser, sPassword);
			ErrorMes("Documentum login failed: " + DocGetErrorMessage());
			:RETURN "";
		:ENDIF;

		sExportData := DocExportDocument(sDocumentId);

		:IF DocCommandFailed();
			ErrorMes("Default export failed: " + DocGetErrorMessage());
			:RETURN "";
		:ENDIF;

		UsrMes("Default-format export completed for: " + sDocumentId);

		:RETURN sExportData;
	:FINALLY;
		DocEndDocumentumInterface();
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ExportDocumentDefaultFormat", {"0900000180001234"});
```

### Batch export with per-document failure checks

Iterates a list of document IDs, exports each as PDF, and collects a result row per document that includes a success flag and either the export data or the error message.

```ssl
:PROCEDURE BatchExportDocuments;
	:DECLARE sDocBase, sUser, sPassword, aDocumentIds, aExports, nIndex;
	:DECLARE sDocumentId, sExportData, sErrorMsg;

	sDocBase := "ProductionDB";
	sUser := "doc_user";
	sPassword := "doc_password";
	aDocumentIds := {"0900000180001234", "0900000180001235", "0900000180001236"};
	aExports := {};

	DocInitDocumentumInterface();

	:TRY;
		:IF .NOT. DocLoginToDocumentum(sDocBase, sUser, sPassword);
			ErrorMes("Documentum login failed: " + DocGetErrorMessage());
			:RETURN {};
		:ENDIF;

		:FOR nIndex := 1 :TO ALen(aDocumentIds);
			sDocumentId := aDocumentIds[nIndex];
			sExportData := DocExportDocument(sDocumentId, "PDF");

			:IF DocCommandFailed();
				sErrorMsg := DocGetErrorMessage();
				AAdd(aExports, {sDocumentId, .F., sErrorMsg, ""});
			:ELSE;
				AAdd(aExports, {sDocumentId, .T., "", sExportData});
			:ENDIF;
		:NEXT;

		:RETURN aExports;
	:FINALLY;
		DocEndDocumentumInterface();
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("BatchExportDocuments");
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocEndDocumentumInterface`](DocEndDocumentumInterface.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`DocLoginToDocumentum`](DocLoginToDocumentum.md)
- [`string`](../types/string.md)
