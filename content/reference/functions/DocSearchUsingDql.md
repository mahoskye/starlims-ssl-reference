---
title: "DocSearchUsingDql"
summary: "Executes a Documentum DQL query and returns the result set as a two-dimensional array."
id: ssl.function.docsearchusingdql
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocSearchUsingDql

Executes a Documentum DQL query and returns the result set as a two-dimensional array.

`DocSearchUsingDql` sends the DQL text to Documentum and converts the returned rows into SSL arrays. Each result row is an array, and the column order matches the `SELECT` list in your DQL statement. When `nResultSetSize` is greater than `0`, the runtime appends `ENABLE (RETURN_TOP n)` unless your DQL already contains `RETURN_TOP`.

If the `sDql` argument is [`NIL`](../literals/nil.md), SSL raises an exception before the Documentum call starts. Other Documentum execution failures are captured by the Documentum interface and surface as an empty array; use [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) to distinguish a failed call from a genuine no-results search.

## When to use

- When you need full control over the Documentum query instead of the fixed search shapes used by helper functions.
- When you want to choose the exact columns, filters, and sort order returned from Documentum.
- When you need a bounded result set for a review queue or picker dialog.
- When you want array results that follow the column order of your DQL `SELECT` list.

## Syntax

```ssl
DocSearchUsingDql(sDql, [nResultSetSize])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sDql` | [string](../types/string.md) | yes | — | Documentum DQL statement to execute. Passing [`NIL`](../literals/nil.md) raises an exception. |
| `nResultSetSize` | [number](../types/number.md) | no | `-1` | Maximum number of rows requested. When greater than `0`, the runtime appends `ENABLE (RETURN_TOP n)` if the DQL text does not already contain `RETURN_TOP`. |

## Returns

**[array](../types/array.md)** — A two-dimensional array of result rows. Column positions follow the order of the DQL `SELECT` list. Returns an empty array when the query returns no rows or when the Documentum call fails; use [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) to distinguish a failed call from a genuine no-results search.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDql` is [`NIL`](../literals/nil.md). | `sDql argument cannot be null` |

## Best practices

!!! success "Do"
    - Select only the columns your script actually uses so the returned row shape stays simple and predictable.
    - Check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) when `ALen(aResults) == 0` and you need to know whether the search failed.
    - Pass `nResultSetSize` for review queues, lookups, and other flows that do not need the full result set.
    - Read row values by their documented query position, such as `aResults[nIndex, 2]` for the second selected column.

!!! failure "Don't"
    - Treat each result row as an object with named properties. Each row is an array.
    - Pass [`NIL`](../literals/nil.md) for `sDql`. That raises an exception instead of returning a result.
    - Assume `nResultSetSize` paginates results. It only requests a top-N limit.
    - Assume every empty result means no documents matched. A failed Documentum call also returns an empty array.

## Caveats

- An empty string DQL value is rejected by the underlying Documentum search call. In that case SSL receives an empty array and the failure details are available through [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md).
- Call [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md) before using Documentum functions.

## Examples

### Search for document IDs and names

Queries released documents with a 10-row cap, checks for a failed call before iterating, and prints each document name.

```ssl
:PROCEDURE ListReleasedDocumentNames;
    :DECLARE sDql, aResults, nIndex;

    DocInitDocumentumInterface();

    :TRY;
        sDql := "SELECT r_object_id, object_name FROM dm_document WHERE a_status = 'Released'";
        aResults := DocSearchUsingDql(sDql, 10);

        :IF ALen(aResults) == 0 .AND. DocCommandFailed();
            /* Displays on failure: Document search failed;
            ErrorMes("Document search failed: " + DocGetErrorMessage());
            :RETURN {};
        :ENDIF;

        :FOR nIndex := 1 :TO ALen(aResults);
            /* Displays each document name;
            UsrMes(aResults[nIndex, 2]);
        :NEXT;

        :RETURN aResults;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ListReleasedDocumentNames");
```

### Select specific columns for a stable row shape

Fetches three columns from documents in a specific folder path and assembles each row into a `"name (id)"` label string for a summary array.

```ssl
:PROCEDURE BuildDocumentSummary;
    :DECLARE sDql, aResults, aSummary, nIndex;

    DocInitDocumentumInterface();

    :TRY;
        sDql := "SELECT r_object_id, object_name, title FROM dm_document "
	            + "WHERE folder('/Quality/Specs', DESCEND)";
        aResults := DocSearchUsingDql(sDql, 25);
        aSummary := {};

        :IF ALen(aResults) == 0 .AND. DocCommandFailed();
            /* Displays on failure: Unable to read document summary;
            ErrorMes("Unable to read document summary: " + DocGetErrorMessage());
            :RETURN {};
        :ENDIF;

        :FOR nIndex := 1 :TO ALen(aResults);
            AAdd(aSummary, aResults[nIndex, 2] + " (" + aResults[nIndex, 1] + ")");
        :NEXT;

        :RETURN aSummary;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("BuildDocumentSummary");
```

### Use RETURN_TOP inside the DQL to control the limit directly

Shows that when `RETURN_TOP` is already in the DQL text, `nResultSetSize` has no effect. The limit is controlled entirely by the DQL clause.

```ssl
:PROCEDURE GetRecentProtocolRows;
    :DECLARE sDql, aResults, sError;

    DocInitDocumentumInterface();

    :TRY;
        sDql := "SELECT r_object_id, object_name, subject FROM dm_document "
	            + "WHERE object_name LIKE 'Protocol%' "
	            + "ENABLE (RETURN_TOP 5)";
        aResults := DocSearchUsingDql(sDql, 50);

        :IF ALen(aResults) == 0 .AND. DocCommandFailed();
            sError := DocGetErrorMessage();
            /* Displays on failure: Protocol search failed;
            ErrorMes("Protocol search failed: " + sError);
            :RETURN {};
        :ENDIF;

        :RETURN aResults;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("GetRecentProtocolRows");
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`DocSearchAsDataset`](DocSearchAsDataset.md)
- [`DocSearchFullText`](DocSearchFullText.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
- [`array`](../types/array.md)
