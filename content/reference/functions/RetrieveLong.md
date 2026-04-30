---
title: "RetrieveLong"
summary: "Retrieves a value from one database column and writes it to a file when the selected value is returned as binary data."
id: ssl.function.retrievelong
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# RetrieveLong

Retrieves a value from one database column and writes it to a file when the selected value is returned as binary data.

`RetrieveLong` builds a query in the form `SELECT <sColumnName> FROM <sTableName> WHERE <sWhereCondition>` and reads the first scalar value that query returns. If the value is a byte array, the function writes those bytes to `sOutputFilePath` and returns [`.T.`](../literals/true.md). If the query returns no row, returns `NULL`, or returns a non-binary value, the function deletes `sOutputFilePath` if it exists and still returns [`.T.`](../literals/true.md). It does not have a [`.F.`](../literals/false.md) return path. If an error occurs while checking file permissions, querying the database, or writing the file, the function deletes any existing output file and raises an exception instead.

## When to use

- When you need to export binary data such as a BLOB or stored attachment to a file.
- When you want a simple one-call way to fetch one column value for one row and persist it as a file.
- When you can supply a precise `sWhereCondition` that identifies the row you want to read.

## Syntax

```ssl
RetrieveLong([sConnectionName], sTableName, sColumnName, sWhereCondition, sOutputFilePath, [bIsCompressed])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sConnectionName` | [string](../types/string.md) | no | default connection | Database connection name. When omitted, the default connection is used. |
| `sTableName` | [string](../types/string.md) | yes | — | Table to query. |
| `sColumnName` | [string](../types/string.md) | yes | — | Column to select from that table. |
| `sWhereCondition` | [string](../types/string.md) | yes | — | SQL condition appended after `WHERE` to identify the row to read. |
| `sOutputFilePath` | [string](../types/string.md) | yes | — | Path of the file to create or overwrite. |
| `bIsCompressed` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Reserved flag. Passing [`.T.`](../literals/true.md) raises an exception because compression is not implemented. |

## Returns

**[boolean](../types/boolean.md)** — Returns [`.T.`](../literals/true.md) on every non-exception path. This includes the case where no file is ultimately written because the query returned no row, `NULL`, or a non-binary value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `bIsCompressed` is [`.T.`](../literals/true.md). | `Not implemented yet.` |
| `sTableName`, `sColumnName`, `sWhereCondition`, or `sOutputFilePath` is [`NIL`](../literals/nil.md). | `Function parameters are incorrect.` |
| The connection name is unknown. | `The provider name: <sConnectionName> not found.` |
| The database collection is unavailable. | `The internal database collection is null` |
| The output path is outside the configured whitelist. | `Access to folder/file <path> is denied. If system needs access to this folder/file please ask the System Administrator to add the item to WhitelistFolders setting in the configuration file.` |
| The database call or file write fails (any existing output file is deleted first). | The original error message is re-raised as a data access exception. |

## Best practices

!!! success "Do"
    - Use a restrictive `sWhereCondition` so the query clearly targets the row you expect.
    - Wrap the call in `:TRY / :CATCH` when the database, file path, or permissions may fail.
    - Verify the output file after the call with `FileSupport(..., "EXISTS")` or `FileSupport(..., "SIZE")` because [`.T.`](../literals/true.md) does not guarantee bytes were written.
    - Leave `bIsCompressed` omitted or pass [`.F.`](../literals/false.md).

!!! failure "Don't"
    - Treat a [`.T.`](../literals/true.md) return value as proof that a file was written.
    - Pass [`.T.`](../literals/true.md) for `bIsCompressed`; that path always raises `Not implemented yet.`
    - Use a broad `sWhereCondition` when the file must come from one specific row.
    - Assume text values are written successfully; the function only writes the result when it is returned as binary data.

## Caveats

- The function concatenates `sTableName`, `sColumnName`, and `sWhereCondition` directly into the SQL statement. Build those inputs carefully.

## Examples

### Export one PDF attachment and verify the file was written

Fetch a single BLOB column, write it to disk, and confirm the file was actually created since [`.T.`](../literals/true.md) alone does not guarantee bytes were written.

```ssl
:PROCEDURE ExportAttachmentPdf;
    :DECLARE sConnectionName, sTableName, sColumnName, sWhereCondition;
    :DECLARE sOutputFilePath, oErr, nBytes;

    sConnectionName := "LIMS";
    sTableName := "attachments";
    sColumnName := "pdf_blob";
    sWhereCondition := "attachmentid = 'ATT12345'";
    sOutputFilePath := "C:\STARLIMS\Exports\ATT12345.pdf";

    :TRY;
        RetrieveLong(
            sConnectionName,
            sTableName,
            sColumnName,
            sWhereCondition,
            sOutputFilePath,
            .F.
        );

        :IF FileSupport(sOutputFilePath, "EXISTS");
            nBytes := FileSupport(sOutputFilePath, "SIZE");
            UsrMes(
                "Exported attachment to " + sOutputFilePath +
                " (" + LimsString(nBytes) + " bytes)"
            );
            /* Displays on success: exported attachment with byte count;
        :ELSE;
            UsrMes("No binary data was written for attachment ATT12345");
        :ENDIF;
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("RetrieveLong failed: " + oErr:Description);
        /* Displays on failure: RetrieveLong failed;
    :ENDTRY;
:ENDPROC;
```

Run with:

```ssl
DoProc("ExportAttachmentPdf");
```

### Batch-export approved report files

Query for a list of IDs and export each matching BLOB to a separate file, tracking how many were written versus skipped.

```ssl
:PROCEDURE ExportApprovedReports;
    :DECLARE aReportIds, nIndex, sConnectionName, sTableName, sColumnName;
    :DECLARE sReportId, sWhereCondition, sOutputFilePath;
    :DECLARE nWritten, nSkipped, oErr;

    sConnectionName := "LIMS";
    sTableName := "report_archive";
    sColumnName := "report_blob";
    nWritten := 0;
    nSkipped := 0;

    aReportIds := SQLExecute("SELECT report_id FROM report_archive WHERE status = 'APPROVED'");

    :IF Empty(aReportIds);
        UsrMes("No approved reports were found");
        :RETURN;
    :ENDIF;

    :FOR nIndex := 1 :TO ALen(aReportIds);
        sReportId := LimsString(aReportIds[nIndex, 1]);
        sWhereCondition := "report_id = '" + sReportId + "'";
        sOutputFilePath := "C:\STARLIMS\Exports\" + sReportId + ".pdf";

        :TRY;
            RetrieveLong(
                sConnectionName,
                sTableName,
                sColumnName,
                sWhereCondition,
                sOutputFilePath,
                .F.
            );

            :IF FileSupport(sOutputFilePath, "EXISTS") .AND. FileSupport(sOutputFilePath, "SIZE") > 0;
                nWritten += 1;
            :ELSE;
                nSkipped += 1;
            :ENDIF;
        :CATCH;
            oErr := GetLastSSLError();
            ErrorMes("Failed to export report " + sReportId + ": " + oErr:Description);
            /* Displays on failure: failed to export report;
        :ENDTRY;
    :NEXT;

    UsrMes(
        "Report export complete. Written: " + LimsString(nWritten) +
        ", skipped: " + LimsString(nSkipped)
    );
    /* Displays: report export summary;
:ENDPROC;
```

Run with:

```ssl
DoProc("ExportApprovedReports");
```

## Related

- [`UpdLong`](UpdLong.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
