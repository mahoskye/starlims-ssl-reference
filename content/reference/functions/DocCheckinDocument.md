---
title: "DocCheckinDocument"
summary: "Checks a local file into an existing Documentum document."
id: ssl.function.doccheckindocument
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocCheckinDocument

Checks a local file into an existing Documentum document.

`DocCheckinDocument` submits file content for an existing Documentum document ID and returns the checked-in object's ID as a string. The function checks out the document automatically when needed, then checks in the file using the supplied version label and flags. When optional arguments are omitted, `sVersion` defaults to `""` and both boolean flags default to [`.F.`](../literals/false.md).

This function raises direct SSL exceptions only when `sFilePath` or `sDocumentId` is [`NIL`](../literals/nil.md). Other check-in failures are not raised directly by the function call itself. Instead, the function returns an empty string, and you should inspect [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) for failure details.

If `sVersion` is empty, the check-in uses the `CURRENT` label. If `sVersion` contains text, the check-in uses `CURRENT,<sVersion>`. When both `bReplaceContent` and `bMajorVersion` are [`.T.`](../literals/true.md), `bReplaceContent` takes precedence.

## When to use

- When you need to update the content of an existing Documentum document.
- When a workflow needs to apply a specific version label during check-in.
- When you need to control whether the check-in uses replacement behavior or a major-version check-in.
- When you need the ID of the checked-in object returned by the operation.

## Syntax

```ssl
DocCheckinDocument(sFilePath, sDocumentId, [sVersion], [bReplaceContent], [bMajorVersion])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sFilePath` | [string](../types/string.md) | yes | — | Path to the local file to check in. |
| `sDocumentId` | [string](../types/string.md) | yes | — | Documentum identifier of the existing document. |
| `sVersion` | [string](../types/string.md) | no | `""` | Version label to send with the check-in. |
| `bReplaceContent` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Replaces the existing document content when true. |
| `bMajorVersion` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Marks the check-in as a major version when true. |

## Returns

**[string](../types/string.md)** — The checked-in object's ID. If the underlying check-in command fails, this function returns an empty string.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sFilePath` is [`NIL`](../literals/nil.md). | `sFilePath argument cannot be null` |
| `sDocumentId` is [`NIL`](../literals/nil.md). | `sDocumentId argument cannot be null` |

## Best practices

!!! success "Do"
    - Initialize and log in to Documentum before calling this function.
    - Check [`DocCommandFailed`](DocCommandFailed.md) immediately after the call when the result matters.
    - Use `bReplaceContent` and `bMajorVersion` only when the workflow really needs those behaviors.
    - Pass only the flags you intend to use so the check-in mode is unambiguous.

!!! failure "Don't"
    - Assume every operational failure raises an SSL exception. Most command failures are reported through the Documentum error helpers instead.
    - Treat an empty return value as a successful check-in.
    - Pass both `bReplaceContent` and `bMajorVersion` as [`.T.`](../literals/true.md) unless you specifically want replacement behavior to win.
    - Mark every check-in as content-replacing or major-version by default. Unnecessary version changes make repository history harder to manage.

## Caveats

- This function works on an existing Documentum document ID; it does not create a new document.
- Empty `sFilePath` and empty `sDocumentId` values do not raise direct exceptions. They fail through the Documentum command path, reporting `Please specify the file to checkin!` or `Please specify the document id!` respectively.
- A missing local file reports `Failed: File does not exist`; a missing Documentum object reports `Failed: Object does not exist`.
- A valid Documentum session is required, typically established with [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md) and [`DocLoginToDocumentum`](DocLoginToDocumentum.md).

## Examples

### Check in a local file using the required arguments only

Logs in to Documentum, checks in a local PDF using only the required arguments, and reports either the checked-in object ID or the command failure message.

```ssl
:PROCEDURE CheckinDocumentBasic;
    :DECLARE sDocBase, sUser, sPassword;
    :DECLARE sFilePath, sDocumentId, sCheckedInId;
    :DECLARE bLoggedIn;

    sDocBase := "QualityRepository";
    sUser := "doc_user";
    sPassword := "secret";
    sFilePath := "C:\\Docs\\QA_Report.pdf";
    sDocumentId := "DOC-2024-001";
    bLoggedIn := .F.;

    DocInitDocumentumInterface();

    :TRY;
        bLoggedIn := DocLoginToDocumentum(sDocBase, sUser, sPassword);

        :IF .NOT. bLoggedIn;
            ErrorMes("Documentum login failed: " + DocGetErrorMessage());
        :ELSE;
            sCheckedInId := DocCheckinDocument(sFilePath, sDocumentId);

            :IF DocCommandFailed();
                ErrorMes("Check-in failed: " + DocGetErrorMessage());
            :ELSE;
                UsrMes("Checked-in object ID: " + sCheckedInId);
            :ENDIF;
        :ENDIF;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("CheckinDocumentBasic");
```

### Replace document content and apply a version label

Checks in a revised document with `bReplaceContent` set to [`.T.`](../literals/true.md) and a specific version label, then reports the resulting object ID or any command failure.

```ssl
:PROCEDURE CheckinDocumentReplaceContent;
    :DECLARE sDocBase, sUser, sPassword;
    :DECLARE sFilePath, sDocumentId, sVersion, sCheckedInId;
    :DECLARE bReplaceContent, bLoggedIn;

    sDocBase := "QualityRepository";
    sUser := "doc_user";
    sPassword := "secret";
    sFilePath := "C:\\Docs\\Spec_Report_v2.docx";
    sDocumentId := "DOC-2024-0042";
    sVersion := "2.1";
    bReplaceContent := .T.;
    bLoggedIn := .F.;

    DocInitDocumentumInterface();

    :TRY;
        bLoggedIn := DocLoginToDocumentum(sDocBase, sUser, sPassword);

        :IF .NOT. bLoggedIn;
            ErrorMes("Documentum login failed: " + DocGetErrorMessage());
        :ELSE;
            sCheckedInId := DocCheckinDocument(
                sFilePath,
                sDocumentId,
                sVersion,
                bReplaceContent
            );

            :IF DocCommandFailed();
                ErrorMes("Replacement check-in failed: " + DocGetErrorMessage());
            :ELSE;
                UsrMes("Replacement check-in object ID: " + sCheckedInId);
            :ENDIF;
        :ENDIF;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("CheckinDocumentReplaceContent");
```

### Perform a major-version check-in and capture the result or error

Checks in a document with `bMajorVersion` set to [`.T.`](../literals/true.md) and a version label string, captures any Documentum error message, and displays the outcome.

```ssl
:PROCEDURE CheckinDocumentMajorRevision;
    :DECLARE sDocBase, sUser, sPassword;
    :DECLARE sFilePath, sDocumentId, sVersion, sCheckedInId, sErrMsg;
    :DECLARE bReplaceContent, bMajorVersion, bLoggedIn;

    sDocBase := "QualityRepository";
    sUser := "doc_user";
    sPassword := "secret";
    sFilePath := "C:\\Docs\\QCP-2024-001.pdf";
    sDocumentId := "DOC-2024-00042";
    sVersion := "3.0";
    bReplaceContent := .F.;
    bMajorVersion := .T.;
    bLoggedIn := .F.;
    sErrMsg := "";

    DocInitDocumentumInterface();

    :TRY;
        bLoggedIn := DocLoginToDocumentum(sDocBase, sUser, sPassword);

        :IF .NOT. bLoggedIn;
            ErrorMes("Documentum login failed: " + DocGetErrorMessage());
        :ELSE;
            sCheckedInId := DocCheckinDocument(
                sFilePath,
                sDocumentId,
                sVersion,
                bReplaceContent,
                bMajorVersion
            );

            :IF DocCommandFailed();
                sErrMsg := DocGetErrorMessage();
                ErrorMes("Major revision check-in failed: " + sErrMsg);
            :ELSE;
                UsrMes("Major revision object ID: " + sCheckedInId);
            :ENDIF;
        :ENDIF;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("CheckinDocumentMajorRevision");
```

## Related

- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`DocLoginToDocumentum`](DocLoginToDocumentum.md)
- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocEndDocumentumInterface`](DocEndDocumentumInterface.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
