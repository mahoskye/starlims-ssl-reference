---
title: "DocGetDocuments"
summary: "Retrieves documents from a Documentum repository folder as a two-dimensional array."
id: ssl.function.docgetdocuments
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocGetDocuments

Retrieves documents from a Documentum repository folder as a two-dimensional array.

`DocGetDocuments` returns one row per matching document under the supplied repository path. Each row contains the document ID, name, type, content type, and status in fixed positions. If `sDocTypes` is omitted or passed as [`NIL`](../literals/nil.md), the function uses `dm_document` as the filter. If the folder path is invalid or no matching documents are found, the function returns an empty array.

The returned rows are sorted by document name.

## When to use

- When you need to list documents stored in a specific Documentum folder.
- When you want to restrict the results to a specific document type.
- When you need document metadata such as ID, content type, or checkout status for display or further processing.

## Syntax

```ssl
DocGetDocuments(sFolderPath, [sDocTypes])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `sFolderPath` | [string](../types/string.md) | yes | — | Repository folder path to query. Passing [`NIL`](../literals/nil.md) raises an exception. |
| `sDocTypes` | [string](../types/string.md) | no | `"dm_document"` | Document type filter. When omitted or passed as [`NIL`](../literals/nil.md), the function filters to `dm_document`. |

## Returns

**[array](../types/array.md)** — A two-dimensional array. Each row is a 5-element array of strings.

| Position | Value |
| --- | --- |
| `row[1]` | Document ID |
| `row[2]` | Document name |
| `row[3]` | Document type |
| `row[4]` | Content type |
| `row[5]` | Status |

Status is returned as one of these string values:

- `checkedin`
- `checkedout`
- `locked`

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sFolderPath` is [`NIL`](../literals/nil.md). | `sFolderPath argument cannot be null` |

## Best practices

!!! success "Do"
    - Check `ALen(aDocuments)` before iterating, because an invalid folder path or an unmatched filter returns an empty array.
    - Access document fields by their documented 1-based positions such as `aDocuments[nIndex, 2]` for the name and `aDocuments[nIndex, 5]` for the status.
    - Omit `sDocTypes` when you want the default `dm_document` behavior.

!!! failure "Don't"
    - Treat each result row as an object with named properties. Each result row is an array.
    - Assume a missing or incorrect folder path raises an exception. In normal execution it returns an empty array.
    - Pass an empty type filter when you mean to use the default. Omit the argument instead.

## Caveats

- Blank strings for `sFolderPath` are not rejected. They are passed through to the Documentum query and will likely return an empty array.
- Passing an empty string for `sDocTypes` is not the same as omitting it. Only [`NIL`](../literals/nil.md) triggers the `dm_document` default.

## Examples

### List document names in a folder

Calls `DocGetDocuments` without a type filter to list all `dm_document` entries under a folder, printing each document name in turn.

```ssl
:PROCEDURE ListRepositoryDocs;
	:DECLARE sFolderPath, aDocuments, nCount, nIndex;

	sFolderPath := "/Engineering/Specifications";
	aDocuments := DocGetDocuments(sFolderPath);
	nCount := ALen(aDocuments);

	:IF nCount == 0;
		UsrMes("No documents found in " + sFolderPath);
		/* Displays when the folder is empty;

		:RETURN aDocuments;
	:ENDIF;

	:FOR nIndex := 1 :TO nCount;
		UsrMes(aDocuments[nIndex, 2]);
		/* Displays each document name;
	:NEXT;

	:RETURN aDocuments;
:ENDPROC;

/* Usage;
DoProc("ListRepositoryDocs");
```

### Pass the document type filter explicitly

Passes an explicit document type to `DocGetDocuments` and prints the ID, name, and content type of each result, illustrating how to access individual columns by position.

```ssl
:PROCEDURE GetTypedDocuments;
	:DECLARE sFolderPath, sDocTypes, aDocuments, nCount, nIndex, sMessage;

	sFolderPath := "/Clinical/StudyReports/2024";
	sDocTypes := "dm_document";
	aDocuments := DocGetDocuments(sFolderPath, sDocTypes);
	nCount := ALen(aDocuments);

	:IF nCount == 0;
		UsrMes("No matching documents found in " + sFolderPath);
		/* Displays when no matching documents are found;

		:RETURN aDocuments;
	:ENDIF;

	:FOR nIndex := 1 :TO nCount;
		sMessage := aDocuments[nIndex, 1] + " | "
					+ aDocuments[nIndex, 2] + " | "
					+ aDocuments[nIndex, 4];
		UsrMes(sMessage);
		/* Displays the ID, name, and content type;
	:NEXT;

	:RETURN aDocuments;
:ENDPROC;

/* Usage;
DoProc("GetTypedDocuments");
```

### Group results by checkout status

Fetches documents from a folder and counts how many are checked in, checked out, or locked, then displays a summary line.

```ssl
:PROCEDURE SummarizeDocumentStatuses;
	:DECLARE sFolderPath, aDocuments, nCheckedIn, nCheckedOut, nLocked;
	:DECLARE nCount, nIndex, sStatus, sSummary;

	sFolderPath := "/Business Documents/Reports";
	aDocuments := DocGetDocuments(sFolderPath, "dm_document");
	nCount := ALen(aDocuments);
	nCheckedIn := 0;
	nCheckedOut := 0;
	nLocked := 0;

	:IF nCount == 0;
		UsrMes("No matching documents found in " + sFolderPath);
		/* Displays when no matching documents are found;

		:RETURN aDocuments;
	:ENDIF;

	:FOR nIndex := 1 :TO nCount;
		sStatus := Lower(aDocuments[nIndex, 5]);

		:BEGINCASE;
		:CASE sStatus == "checkedin";
			nCheckedIn += 1;
			:EXITCASE;
		:CASE sStatus == "checkedout";
			nCheckedOut += 1;
			:EXITCASE;
		:OTHERWISE;
			nLocked += 1;
			:EXITCASE;
		:ENDCASE;
	:NEXT;

	sSummary := "Total: " + LimsString(nCount)
				+ ", checkedin: " + LimsString(nCheckedIn)
				+ ", checkedout: " + LimsString(nCheckedOut)
				+ ", locked: " + LimsString(nLocked);
	UsrMes(sSummary);
	/* Displays the total and status counts;

	:RETURN aDocuments;
:ENDPROC;

/* Usage;
DoProc("SummarizeDocumentStatuses");
```

## Related

- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
