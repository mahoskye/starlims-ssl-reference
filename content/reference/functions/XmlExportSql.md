---
title: "XmlExportSql"
summary: "Runs a SQL query, writes the result set to an XML file, and returns an empty string on success or an error message on failure."
id: ssl.function.xmlexportsql
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# XmlExportSql

Runs a SQL query, writes the result set to an XML file, and returns an empty string on success or an error message on failure.

`XmlExportSql` executes the supplied SQL against the requested database, writes the results to the file path you provide, and returns a status string rather than the XML content itself. If `sDb` is omitted or passed as [`NIL`](../literals/nil.md), the function uses `"DATABASE"`. If `sSql` or `sFile` is [`NIL`](../literals/nil.md), the function raises an argument error before attempting the export.

When the export fails during execution or file writing, the function catches the failure and returns a formatted error string that includes the SQL text, file name, database name, and error message.

## When to use

- When you need to export SQL query results directly to an XML file instead of keeping them in memory for integration, data transfer, or reporting.
- When you need a simple success-or-error return value instead of working with a dataset in memory.
- When you must choose the database for the query dynamically via the sDb parameter without changing your connection logic.

## Syntax

```ssl
XmlExportSql(sSql, sFile, [sDb], [aSqlParams], [sTable])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSql` | [string](../types/string.md) | yes | — | SQL statement to execute against the database |
| `sFile` | [string](../types/string.md) | yes | — | Full path and file name for the XML output file |
| `sDb` | [string](../types/string.md) | no | `"DATABASE"` when [`NIL`](../literals/nil.md) | Database name to execute the query against |
| `aSqlParams` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Accepted in the signature but has no effect on the export |
| `sTable` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Accepted in the signature but has no effect on the export |

## Returns

**[string](../types/string.md)** — Empty string on success, or a multi-line error message string if the operation fails.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSql` is [`NIL`](../literals/nil.md). | `Sql parameter cannot be null.` |
| `sFile` is [`NIL`](../literals/nil.md). | `File name parameter cannot be null.` |

## Best practices

!!! success "Do"
    - Check that the returned string is empty before treating the export as successful.
    - Pass `sDb` explicitly when the target database matters; only rely on the default when that is intentional.
    - Use a writable file path and make sure the destination folder exists before exporting.
    - Use [`GetDataSet`](GetDataSet.md) or [`GetDataSetXMLFromSelect`](GetDataSetXMLFromSelect.md) instead when you need the XML or rows in memory rather than on disk.

!!! failure "Don't"
    - Assume the export succeeded just because no SSL exception was raised; runtime failures are returned as text.
    - Expect this function to return XML content; it only writes to disk and returns status.
    - Rely on `aSqlParams` or `sTable` to change the export behavior; those arguments have no effect.
    - Pass [`NIL`](../literals/nil.md) for required arguments such as `sSql` or `sFile`; those cases raise argument errors.

## Caveats

- Large result sets produce large XML files and may impact disk space and performance.

## Examples

### Export results to an XML file and check status

Run a query and write the results to a file. The empty-string return value signals success; a non-empty return value contains the error details.

```ssl
:PROCEDURE ExportSampleResultsToXml;
    :DECLARE sSql, sFile, sResult;

    sSql :=
        "
        SELECT sample_id, sample_name, status
        FROM sample
        WHERE status = 'A'
    ";
    sFile := "C:\temp\sample_data.xml";

    sResult := XmlExportSql(sSql, sFile);

    :IF Empty(sResult);
        UsrMes("XML export completed: " + sFile);
    :ELSE;
        ErrorMes(sResult);  /* Displays on failure: export error details;
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("ExportSampleResultsToXml");
```

### Export to a specific database with error handling

Target a named database and wrap the call in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) to distinguish between argument errors (which throw) and runtime failures (which return an error string). Checking the return value before the [`:ENDTRY`](../keywords/ENDTRY.md) handles the runtime case.

```ssl
:PROCEDURE ExportSamplesForArchive;
    :PARAMETERS sOutputFile;
    :DECLARE sSql, sDb, sResult, oErr;

    sDb := "LIMBDATA";
    sSql :=
        "
        SELECT sample_id, sample_name, status, received_date
        FROM sample
        WHERE status = 'A'
        ORDER BY sample_id
    ";

    :TRY;
        sResult := XmlExportSql(sSql, sOutputFile, sDb);

        :IF Empty(sResult);
            UsrMes("Archive export completed: " + sOutputFile);
            :RETURN .T.;
        :ENDIF;

        ErrorMes(sResult);  /* Displays on failure: export error details;
        :RETURN .F.;
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes(oErr:Description);  /* Displays on failure: argument error details;
        :RETURN .F.;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ExportSamplesForArchive", {"C:\temp\archive.xml"});
```

## Related

- [`GetDataSet`](GetDataSet.md)
- [`GetDataSetXMLFromSelect`](GetDataSetXMLFromSelect.md)
- [`string`](../types/string.md)
