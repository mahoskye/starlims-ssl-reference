---
title: "DocImportDocument"
summary: "Imports a document into Documentum and returns the underlying import result as a string."
id: ssl.function.docimportdocument
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocImportDocument

Imports a document into Documentum and returns the underlying import result as a string.

`DocImportDocument` sends the source file path and destination path to the Documentum import operation. You can also supply a document name, document type, application code, and ACL name when that metadata should be part of the import.

Only `sDocFile` and `sDestinationPath` are null-validated by this function. When `sDocName`, `sDocType`, `sAppCode`, or `sAclName` are omitted, the call forwards them as omitted values to the Documentum import operation.

The function runs inside the current Documentum interface context. When the underlying import operation throws, the Documentum helper records the failure in that context and this function returns `""`.

## When to use

- When you need to import a local file into a Documentum repository location.
- When the import should include optional metadata such as type, application code, or ACL.
- When you want to check import failures with [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md).

## Syntax

```ssl
DocImportDocument(
    sDocFile,
    sDestinationPath,
    [sDocName],
    [sDocType],
    [sAppCode],
    [sAclName]
)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sDocFile` | [string](../types/string.md) | yes | — | Source file path to import |
| `sDestinationPath` | [string](../types/string.md) | yes | — | Destination path in Documentum |
| `sDocName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Document name passed to the import operation |
| `sDocType` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Document type passed to the import operation |
| `sAppCode` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Application code passed to the import operation |
| `sAclName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | ACL name passed to the import operation |

## Returns

**[string](../types/string.md)** — The string returned by the underlying Documentum import call. Returns `""` when the import operation fails and records an exception in the current Documentum context.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDocFile` is [`NIL`](../literals/nil.md). | `sDocFile argument cannot be null` |
| `sDestinationPath` is [`NIL`](../literals/nil.md). | `sDestinationPath argument cannot be null` |

## Best practices

!!! success "Do"
    - Initialize the Documentum interface before importing, and end it when the workflow is complete.
    - Check [`DocCommandFailed`](DocCommandFailed.md) immediately after the import when failure handling matters.
    - Capture [`DocGetErrorMessage`](DocGetErrorMessage.md) before another Documentum call can overwrite the current failure state.
    - Supply `sDocName`, `sDocType`, `sAppCode`, and `sAclName` only when your workflow needs those values.

!!! failure "Don't"
    - Call this function before [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md) has created the current Documentum context.
    - Rely on the returned string alone to detect failure when your workflow needs certainty.
    - Pass [`NIL`](../literals/nil.md) for `sDocFile` or `sDestinationPath`; those arguments raise immediate SSL exceptions.
    - Wait until later in the workflow to inspect [`DocCommandFailed`](DocCommandFailed.md) or [`DocGetErrorMessage`](DocGetErrorMessage.md).

## Caveats

- The exact content or format of the success string is not defined here.
- The Documentum helper clears the current failure state before the import runs. If the import throws, it stores that exception and the function returns `""`.

## Examples

### Import with only the required arguments

Imports a single file using only the two required arguments, then checks [`DocCommandFailed`](DocCommandFailed.md) to detect a failed import, using [`:TRY`](../keywords/TRY.md)/[`:FINALLY`](../keywords/FINALLY.md) to ensure the Documentum interface is always cleaned up.

```ssl
:PROCEDURE ImportDocumentBasic;
    :DECLARE sDocFile, sDestinationPath, sImportResult;

    sDocFile := "C:\\Docs\\Result.pdf";
    sDestinationPath := "/Standard/Reports/2026";

    DocInitDocumentumInterface();

    :TRY;
        :IF .NOT. DocLoginToDocumentum("Repository1", "analyst", "secret");
            ErrorMes("Login failed: " + DocGetErrorMessage());
            :RETURN "";
        :ENDIF;

        sImportResult := DocImportDocument(sDocFile, sDestinationPath);

        :IF DocCommandFailed();
            ErrorMes("Import failed: " + DocGetErrorMessage());
            :RETURN "";
        :ENDIF;

        UsrMes("Import completed: " + sImportResult);
        :RETURN sImportResult;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ImportDocumentBasic");
```

### Import with metadata and ACL

Imports a typed document with all six metadata fields, showing how to supply name, type, application code, and ACL alongside the required source and destination paths.

```ssl
:PROCEDURE ImportTypedDocument;
    :DECLARE sDocFile, sDestinationPath, sDocName, sDocType;
    :DECLARE sAppCode, sAclName, sImportResult;

    sDocFile := "C:\\Docs\\BatchRelease.pdf";
    sDestinationPath := "/Quality/BatchRelease/2026";
    sDocName := "BatchRelease-2026-04-18";
    sDocType := "BatchRelease";
    sAppCode := "QC";
    sAclName := "QC_REVIEWERS";

    DocInitDocumentumInterface();

    :TRY;
        :IF .NOT. DocLoginToDocumentum("Repository1", "analyst", "secret");
            ErrorMes("Login failed: " + DocGetErrorMessage());
            :RETURN "";
        :ENDIF;

        sImportResult := DocImportDocument(
            sDocFile,
            sDestinationPath,
            sDocName,
            sDocType,
            sAppCode,
            sAclName
        );

        :IF DocCommandFailed();
            ErrorMes("Import failed: " + DocGetErrorMessage());
            :RETURN "";
        :ENDIF;

        UsrMes("Typed import completed: " + sImportResult);
        :RETURN sImportResult;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ImportTypedDocument");
```

### Import several files and capture per-file failures

Iterates a list of three documents and imports each one, collecting per-file failure messages using [`AAdd`](AAdd.md) and reporting any failures after the loop completes.

```ssl
:PROCEDURE ImportDocumentBatch;
    :DECLARE aImports, aFailures, aRow;
    :DECLARE sImportResult, sMessage;
    :DECLARE nIndex;

    aImports := {
        {
            "C:\\Docs\\COA-001.pdf",
            "/Quality/COA/2026",
            "COA-001",
            "COA",
            "QC",
            "QC_REVIEWERS"
        },
        {
            "C:\\Docs\\COA-002.pdf",
            "/Quality/COA/2026",
            "COA-002",
            "COA",
            "QC",
            "QC_REVIEWERS"
        },
        {
            "C:\\Docs\\COA-003.pdf",
            "/Quality/COA/2026",
            "COA-003",
            "COA",
            "QC",
            "QC_REVIEWERS"
        }
    };
    aFailures := {};

    DocInitDocumentumInterface();

    :TRY;
        :IF .NOT. DocLoginToDocumentum("Repository1", "analyst", "secret");
            ErrorMes("Login failed: " + DocGetErrorMessage());
            :RETURN {};
        :ENDIF;

        :FOR nIndex := 1 :TO ALen(aImports);
            aRow := aImports[nIndex];

            sImportResult := DocImportDocument(
                aRow[1],
                aRow[2],
                aRow[3],
                aRow[4],
                aRow[5],
                aRow[6]
            );

            :IF DocCommandFailed();
                sMessage := aRow[1] + ": " + DocGetErrorMessage();
                AAdd(aFailures, sMessage);
            :ELSE;
                UsrMes("Imported " + aRow[1] + ": " + sImportResult);
                /* Displays per success: Imported file path and result;
            :ENDIF;
        :NEXT;

        :IF ALen(aFailures) > 0;
            ErrorMes("One or more imports failed");
        :ENDIF;

        :RETURN aFailures;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ImportDocumentBatch");
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocEndDocumentumInterface`](DocEndDocumentumInterface.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`DocLoginToDocumentum`](DocLoginToDocumentum.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
