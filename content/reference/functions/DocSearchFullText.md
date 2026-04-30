---
title: "DocSearchFullText"
summary: "Performs a Documentum full-text search and returns matching documents as an array."
id: ssl.function.docsearchfulltext
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocSearchFullText

Performs a Documentum full-text search and returns matching documents as an array.

`DocSearchFullText` searches `dm_document` content using the supplied search text. An optional `sStartLocation` narrows the search to a folder path and its descendants, and an optional `nResultSetSize` requests a bounded result set. The returned rows contain document metadata for each match.

## When to use

- When you need to find documents whose content matches a search term.
- When you want to scope a content search to a specific folder tree.
- When you need a quick array result instead of dataset XML.
- When you want to cap the number of returned matches for a review or pick-list workflow.

## Syntax

```ssl
DocSearchFullText(sTextToSearch, [sStartLocation], [nResultSetSize])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sTextToSearch` | [string](../types/string.md) | yes | — | Full-text search text for the Documentum document search. |
| `sStartLocation` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Folder path used to scope the search with descendants included. Blank or omitted values do not add folder scoping. |
| `nResultSetSize` | [number](../types/number.md) | no | `-1` | Maximum number of rows requested. A value greater than `0` applies a top-N limit. |

## Returns

**[array](../types/array.md)** — An array of matching documents.

Each returned row contains these columns:

| Column | Description |
|--------|-------------|
| `r_object_id` | Documentum object ID |
| `object_name` | Object name |
| `r_object_type` | Object type |
| `title` | Title |
| `subject` | Subject |

If no documents match, the function returns an empty array.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sTextToSearch` is [`NIL`](../literals/nil.md). | `sTextToSearch argument cannot be null` |
| Blank or whitespace-only search text. | Also rejected by the underlying search call. |

## Best practices

!!! success "Do"
    - Validate that `sTextToSearch` is not blank before calling the function.
    - Pass `sStartLocation` when the search should stay inside a known folder tree.
    - Set `nResultSetSize` for review queues and pick lists that only need a bounded result set.
    - Read the returned rows by documented column position so your code stays predictable.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md), `""`, or whitespace-only text as the search value.
    - Assume `nResultSetSize` paginates results. It only requests a maximum row count.
    - Search the entire repository when a folder path is already known.
    - Assume a match exists before checking `ALen(aResults)`.

## Examples

### Search for a keyword in all documents

Searches all `dm_document` content for a keyword, counts the matches, and displays the total.

```ssl
:PROCEDURE SearchPoliciesByKeyword;
    :DECLARE sSearchKeyword, aResults, nResultCount;

    sSearchKeyword := "compliance";

    aResults := DocSearchFullText(sSearchKeyword);

    nResultCount := ALen(aResults);

    UsrMes(
        "Found " + LimsString(nResultCount)
        + " documents containing " + sSearchKeyword
    );

    :RETURN aResults;
:ENDPROC;

/* Usage;
DoProc("SearchPoliciesByKeyword");
```

[`UsrMes`](UsrMes.md) displays:

```text
Found [n] documents containing compliance
```

### Search within a specific folder tree

Scopes the search to a specific folder path with a result cap, then lists each matching document name or reports no matches.

```ssl
:PROCEDURE SearchEngineeringSafetyDocs;
    :DECLARE aResults, sSearchText, sLocation, nMaxResults, nIndex, nCount, sMsg;

    sSearchText := "safety";
    sLocation := "/Documents/Engineering";
    nMaxResults := 10;

    aResults := DocSearchFullText(sSearchText, sLocation, nMaxResults);
    nCount := ALen(aResults);
    sMsg := LimsString(nCount) + " documents found in " + sLocation + " folder";

    /* Displays: count summary;
    InfoMes(sMsg);

    :IF nCount > 0;
        :FOR nIndex := 1 :TO nCount;
            /* Displays: matching document name;
            UsrMes(aResults[nIndex, 2]);
        :NEXT;
    :ELSE;
        UsrMes("No safety-related documents found in the Engineering folder");
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("SearchEngineeringSafetyDocs");
```

### Collect object IDs for a bounded review queue

Searches for documents matching a phrase under a quality folder with a 50-row cap, collects the object IDs, and displays the queue size.

```ssl
:PROCEDURE BuildComplianceReviewQueue;
    :DECLARE sSearchText, sStartLocation, nMaxResults, aResults, aObjectIds, nIndex;

    sSearchText := "retention policy";
    sStartLocation := "/Documents/Quality";
    nMaxResults := 50;

    aResults := DocSearchFullText(sSearchText, sStartLocation, nMaxResults);
    aObjectIds := {};

    :FOR nIndex := 1 :TO ALen(aResults);
        AAdd(aObjectIds, aResults[nIndex, 1]);
    :NEXT;

    UsrMes(
        "Queued " + LimsString(ALen(aObjectIds))
        + " documents for compliance review"
    );

    :RETURN aObjectIds;
:ENDPROC;

/* Usage;
DoProc("BuildComplianceReviewQueue");
```

[`UsrMes`](UsrMes.md) displays:

```text
Queued [n] documents for compliance review
```

## Related

- [`DocSearchAsDataset`](DocSearchAsDataset.md)
- [`DocSearchUsingDql`](DocSearchUsingDql.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
- [`array`](../types/array.md)
