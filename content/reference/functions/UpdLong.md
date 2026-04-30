---
title: "UpdLong"
summary: "Updates a large field value in a database table from the contents of a file, using search criteria for row selection."
id: ssl.function.updlong
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# UpdLong

Updates a large field value in a database table from the contents of a file, using search criteria for row selection.

`UpdLong` reads all bytes from `sInputFilePath`, builds an `UPDATE <sTableName> SET <sColumnName> = ... WHERE <sWhereCondition>` statement, and writes those bytes to the target column. It returns [`.T.`](../literals/true.md) when the update affects at least one row. It does not have a normal [`.F.`](../literals/false.md) path. If the file cannot be accessed, the update fails, or the `WHERE` clause updates zero rows, the function raises an exception instead. Passing [`.T.`](../literals/true.md) for `bIsCompressed` also raises an exception because compression is not implemented.

## When to use

- When updating a large binary or text field (BLOB, CLOB) in a database using the contents of a file.
- When automating the process of storing digital assets (such as documents or images) within a database table.
- When an SSL workflow requires an exact overwrite of one row identified by a precise `sWhereCondition`.
- When integrating file-based imports into a STARLIMS script without writing the database update manually.

## Syntax

```ssl
UpdLong([sConnectionName], sTableName, sColumnName, sWhereCondition, sInputFilePath, [bIsCompressed])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sConnectionName` | [string](../types/string.md) | no | default connection when [`NIL`](../literals/nil.md) | Database connection name. When omitted or passed as [`NIL`](../literals/nil.md), SSL uses the default connection. |
| `sTableName` | [string](../types/string.md) | yes | — | Database table name containing the column. |
| `sColumnName` | [string](../types/string.md) | yes | — | Name of the column where the long value should be stored. |
| `sWhereCondition` | [string](../types/string.md) | yes | — | SQL WHERE clause used to identify the target row. |
| `sInputFilePath` | [string](../types/string.md) | yes | — | Path to the input file containing the long data to update. |
| `bIsCompressed` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Reserved flag. Passing [`.T.`](../literals/true.md) raises an exception because compression is not implemented. |

## Returns

**[boolean](../types/boolean.md)** — Returns [`.T.`](../literals/true.md) when the update completes and affects at least one row. `UpdLong` does not return [`.F.`](../literals/false.md) on failure; error cases raise an exception instead.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `bIsCompressed` is [`.T.`](../literals/true.md). | `(bIsCompressed = TRUE) - not implemented yet.` |
| `sTableName`, `sColumnName`, `sWhereCondition`, or `sInputFilePath` is [`NIL`](../literals/nil.md). | `Function parameters are incorrect.` |
| The input path is not allowed by whitelist settings. | `Access to folder/file <sInputFilePath> is denied.` |
| The input file does not exist. | `File <sInputFilePath> cannot be found.` |
| The file cannot be read. | `Error reading the file <sInputFilePath>.` |
| No rows match the `sWhereCondition`. | `Error updating long value\nNo rows were updated - maybe the WHERE clause evaluated to False: <sWhereCondition>` |
| The database update fails for another reason. | `Error updating long value\n<database error>` |

## Best practices

!!! success "Do"
    - Use a restrictive `sWhereCondition` so the update targets the row you expect.
    - Wrap the call in `:TRY / :CATCH` when the file path, permissions, or update may fail.
    - Leave `bIsCompressed` omitted or pass [`.F.`](../literals/false.md).
    - Verify the source file before calling `UpdLong`, especially in import workflows.

!!! failure "Don't"
    - Treat `UpdLong` as returning [`.F.`](../literals/false.md) for recoverable failures; those paths raise exceptions.
    - Pass [`.T.`](../literals/true.md) for `bIsCompressed`; that path always raises `not implemented yet`.
    - Use a broad or uncertain `sWhereCondition` when zero updated rows should be treated as an error.
    - Pass unchecked file paths; whitelist and file-read failures stop the call before the update runs.

## Caveats

- `UpdLong` concatenates `sTableName`, `sColumnName`, and `sWhereCondition` directly into the generated SQL statement. Build those values carefully.
- The file-permission check runs before the file-exists check. A disallowed path fails before `UpdLong` checks whether the file is present.
- When zero rows are affected, the exception message distinguishes this from a database error by including the `sWhereCondition` value.
- `bIsCompressed` is accepted only for signature compatibility. [`.T.`](../literals/true.md) is not supported.

## Examples

### Store a scanned document in a sample table

Upload a single file to the `DOCUMENT_FILE` column of a specific sample row. Wrap the call in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) because `UpdLong` raises an exception for any failure rather than returning [`.F.`](../literals/false.md).

```ssl
:PROCEDURE UploadScannedDocument;
    :DECLARE sConnectionName, sTableName, sColumnName, sWhereCondition;
    :DECLARE sFilePath, oErr;

    sConnectionName := "LIMS";
    sTableName := "SAMPLE";
    sColumnName := "DOCUMENT_FILE";
    sWhereCondition := "SAMPLE_ID = 'SAM-2024-001'";
    sFilePath := "C:\Documents\ScannedFiles\report.pdf";

    :TRY;
        UpdLong(sConnectionName, sTableName, sColumnName, sWhereCondition, sFilePath);
        UsrMes("Document uploaded successfully");
    :CATCH;
        oErr := GetLastSSLError();
        /* Displays on failure: UpdLong failed with the SSL error description;
        ErrorMes("UpdLong failed: " + oErr:Description);
    :ENDTRY;
:ENDPROC;

/*
Usage:
DoProc("UploadScannedDocument")
;
```

### Bulk update asset images with per-item error handling

Iterate over a list of asset IDs and upload a matching image file for each one. Each iteration is wrapped independently so a failure on one asset does not abort the rest of the batch.

```ssl
:PROCEDURE BulkUpdateAssetImages;
    :DECLARE sConnectionName, sTableName, sColumnName, sWhereCond, sFilePath, sAssetTag;
    :DECLARE aAssetIds, aImageFiles, nIndex, nUpdated, nFailed;
    :DECLARE oErr, sErrorMsg;

    sConnectionName := "LIMS";
    sTableName := "assets";
    sColumnName := "image_data";
    nUpdated := 0;
    nFailed := 0;

    aAssetIds := {"ASSY-2024-001", "ASSY-2024-002", "ASSY-2024-003"};
    aImageFiles := {
        "C:\Images\assy2024001.png",
        "C:\Images\assy2024002.png",
        "C:\Images\assy2024003.png"
    };

    :FOR nIndex := 1 :TO ALen(aAssetIds);
        sAssetTag := aAssetIds[nIndex];
        sFilePath := aImageFiles[nIndex];
        sWhereCond := "asset_tag = '" + LimsString(sAssetTag) + "'";

        :TRY;
            UpdLong(sConnectionName, sTableName, sColumnName, sWhereCond, sFilePath);
            nUpdated := nUpdated + 1;
            /* Displays the updated asset tag on success;
            UsrMes("Updated image for asset: " + sAssetTag);
        :CATCH;
            oErr := GetLastSSLError();
            sErrorMsg := "Error updating asset " + sAssetTag + ": " + oErr:Description;
            /* Displays the asset tag and SSL error description on failure;
            ErrorMes(sErrorMsg);
            nFailed := nFailed + 1;
        :ENDTRY;
    :NEXT;

    /* Displays final updated and failed counts;
    UsrMes("Bulk update complete. Updated: " + LimsString(nUpdated) + ", Failed: " + LimsString(nFailed));

    :RETURN nUpdated;
:ENDPROC;

/*
Usage:
DoProc("BulkUpdateAssetImages")
;
```

### Update inside a transaction with temp file cleanup

Copy an external file to a local temp path, update the long column inside a transaction, and use [`:FINALLY`](../keywords/FINALLY.md) to delete the temp file whether the operation succeeds or fails.

```ssl
:PROCEDURE ImportExternalFileToLongColumn;
    :DECLARE sConnectionName, sTableName, sColumnName;
    :DECLARE sWhereCond, sInputPath, sExternalPath;
    :DECLARE bInTrans;
    :DECLARE oErr, sLogMsg;

    sConnectionName := "LIMS";
    sTableName := "SAMPLE_ANALYSIS";
    sColumnName := "RESULT_FILE";
    sWhereCond := "ANALYSIS_ID = 'A-2024-00421'";
    bInTrans := .F.;

    sExternalPath := "\\external-system\transfer\assay_results.dat";
    sInputPath := GetAppWorkPathFolder() + "temp_incoming.dat";

    :TRY;
        BeginLimsTransaction(sConnectionName, "SERIALIZABLE");
        bInTrans := .T.;

        :IF FileSupport(sExternalPath, "EXISTS");
            FileSupport(sExternalPath, "COPYTOFILE", sInputPath);
        :ELSE;
            RaiseError("External file not found at " + sExternalPath);
        :ENDIF;

        UpdLong(sConnectionName, sTableName, sColumnName, sWhereCond, sInputPath);

        EndLimsTransaction(sConnectionName, .T.);
        bInTrans := .F.;
        sLogMsg := "Long column updated successfully for " + sWhereCond;
        UsrMes(sLogMsg);
    :CATCH;
        :IF bInTrans;
            EndLimsTransaction(sConnectionName, .F.);
            bInTrans := .F.;
        :ENDIF;

        oErr := GetLastSSLError();
        /* Displays on failure: Import failed with the SSL error description;
        ErrorMes("Import failed: " + oErr:Description);

        :RETURN .F.;
    :FINALLY;
        :IF !Empty(sInputPath) .AND. FileSupport(sInputPath, "EXISTS");
            FileSupport(sInputPath, "DELETE");
        :ENDIF;
    :ENDTRY;

    :RETURN .T.;
:ENDPROC;

/*
Usage:
DoProc("ImportExternalFileToLongColumn")
;
```

## Related

- [`RetrieveLong`](RetrieveLong.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
