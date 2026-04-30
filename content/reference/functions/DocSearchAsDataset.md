---
title: "DocSearchAsDataset"
summary: "Searches Documentum and returns the matches as dataset XML."
id: ssl.function.docsearchasdataset
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocSearchAsDataset

Searches Documentum and returns the matches as dataset XML.

`DocSearchAsDataset` builds a Documentum search over the requested object type and returns the result as a serialized dataset string. When omitted, `sObjectType` defaults to `"dm_document"`, `bAllVersions` defaults to [`.F.`](../literals/false.md), and `nResultSetSize` defaults to `-1`. A non-blank `sContains` value adds a full-text `SEARCH DOCUMENT CONTAINS` clause, a non-blank `sStartLocation` adds `FOLDER('<path>', DESCEND)`, and a non-blank `sWhere` value is appended as an additional filter. If the search returns no rows, the function returns an empty string.

## When to use

- When you need Documentum search results in dataset XML form for later processing or transport.
- When you want to combine a content search term with folder scoping or an additional DQL filter.
- When you need to search object types other than the default `dm_document`.
- When you need to include all versions or cap the returned row count.

## Syntax

```ssl
DocSearchAsDataset([sContains], [sStartLocation], [sObjectType], [sWhere], [bAllVersions], [nResultSetSize])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sContains` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Full-text search text. Blank or omitted values skip the `SEARCH DOCUMENT CONTAINS` clause. |
| `sStartLocation` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Folder path used as `FOLDER('<path>', DESCEND)`. Blank or omitted values do not add folder scoping. |
| `sObjectType` | [string](../types/string.md) | no | `"dm_document"` | Documentum object type to query. |
| `sWhere` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Additional DQL filter text appended to the generated `WHERE` clause. |
| `bAllVersions` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | When [`.T.`](../literals/true.md), searches all versions of the selected object type. |
| `nResultSetSize` | [number](../types/number.md) | no | `-1` | Maximum number of rows requested. A value greater than `0` applies a top-N limit. |

## Returns

**[string](../types/string.md)** — XML for a dataset with schema information.

When rows are returned, the dataset contains these columns:

| Column | Description |
|--------|-------------|
| `r_object_id` | Documentum object ID |
| `object_name` | Object name |
| `r_object_type` | Object type |
| `title` | Title |
| `subject` | Subject |
| `a_content_type` | Content type |
| `r_version_label` | Version label |

If no rows are returned, the function returns `""`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| The underlying query object cannot be obtained. | `Couldn't obtain query` |
| The underlying Documentum search raises repository or DQL execution errors. | Repository or DQL execution errors can also propagate from the underlying Documentum search. |

## Best practices

!!! success "Do"
    - Pass only the filters you need so the generated search stays narrow and predictable.
    - Check for an empty string before trying to parse or forward the returned dataset XML.
    - Keep `sWhere` as a valid DQL condition fragment that can follow `WHERE` or `AND`.
    - Set `nResultSetSize` when the caller only needs a bounded result set.

!!! failure "Don't"
    - Treat the return value as an array. The function returns dataset XML, not row data.
    - Pass an arbitrary free-form query in `sWhere`. The function already builds the `SELECT` and `FROM` portions.
    - Leave every filter open for routine searches in large repositories when a folder, type, or result cap is known.

## Caveats

- Omitting every filter searches the default object type without folder scoping.
- `sWhere` is appended directly to the generated filter logic, so invalid DQL can fail at runtime.
- The return value is XML with schema, so parse it with a dataset-aware workflow before treating it as tabular data.

## Examples

### Search a folder and return the dataset XML

Fetches documents containing `"Approved"` from a specific folder path and returns the raw dataset XML, using [`Empty`](Empty.md) to guard against a no-match result.

```ssl
:PROCEDURE FindApprovedDocsInFolder;
    :DECLARE sResultsXml, sContains, sStartLocation;

    sContains := "Approved";
    sStartLocation := "/Documents/Quality/Approved";

    sResultsXml := DocSearchAsDataset(sContains, sStartLocation);

    :IF Empty(sResultsXml);
        UsrMes("No matching documents found");
        :RETURN "";
    :ENDIF;

    UsrMes("Search returned dataset XML");

    :RETURN sResultsXml;
:ENDPROC;

/* Usage;
DoProc("FindApprovedDocsInFolder");
```

### Parse the dataset XML into rows

Searches for revised documents under a configurable path with a result cap, parses the returned dataset XML into a table, and lists each document name and version label.

```ssl
:PROCEDURE BuildRevisedDocReport;
    :PARAMETERS sSectionPath, nMaxResults;
    :DEFAULT sSectionPath, "/Documents/Quality";
    :DEFAULT nMaxResults, 25;
    :DECLARE sResultsXml, sWhere, oTable, aRows, nIndex;

    sWhere := "subject = 'Revision'";

    sResultsXml := DocSearchAsDataset(
        "revised",
        sSectionPath,
        "dm_document",
        sWhere,
        .F.,
        nMaxResults
    );

    :IF Empty(sResultsXml);
        UsrMes("No revised documents found");
        :RETURN 0;
    :ENDIF;

    /* Load the first table from the returned dataset XML;
    oTable := CDataTable{};
    oTable:FromXml(sResultsXml);
    aRows := oTable:ToArray();

    :FOR nIndex := 1 :TO ALen(aRows);
        UsrMes(
            "Document: " + LimsString(aRows[nIndex, 2])
            + ", Version: " + LimsString(aRows[nIndex, 7])
        );  /* Displays each row with document name and version;
    :NEXT;

    :RETURN ALen(aRows);
:ENDPROC;

/* Usage;
DoProc("BuildRevisedDocReport");
```

### Build a version-aware review queue

Searches all PDF versions of documents matching `"method"` under a controlled-docs path and collects their object IDs into an array for downstream processing.

```ssl
:PROCEDURE BuildReviewQueue;
    :DECLARE sResultsXml, sWhere, oTable, aRows, aObjectIds, nIndex;

    sWhere := "a_content_type = 'pdf'";

    sResultsXml := DocSearchAsDataset(
        "method",
        "/ControlledDocs",
        "dm_document",
        sWhere,
        .T.,
        100
    );

    :IF Empty(sResultsXml);
        :RETURN {};
    :ENDIF;

    oTable := CDataTable{};
    oTable:FromXml(sResultsXml);
    aRows := oTable:ToArray();
    aObjectIds := {};

    :FOR nIndex := 1 :TO ALen(aRows);
        AAdd(aObjectIds, aRows[nIndex, 1]);
    :NEXT;

    :RETURN aObjectIds;
:ENDPROC;

/* Usage;
DoProc("BuildReviewQueue");
```

## Related

- [`DocSearchFullText`](DocSearchFullText.md)
- [`DocSearchUsingDql`](DocSearchUsingDql.md)
- [`CDataTable`](../classes/CDataTable.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
- [`number`](../types/number.md)
