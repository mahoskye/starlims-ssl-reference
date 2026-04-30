---
title: "DocGetMetadata"
summary: "Retrieves metadata rows for a Documentum object."
id: ssl.function.docgetmetadata
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocGetMetadata

Retrieves metadata rows for a Documentum object.

`DocGetMetadata` returns a two-dimensional array. Each row describes one metadata attribute in a fixed 6-column layout (see Returns for column details).

When `sAttributes` is omitted or passed as [`NIL`](../literals/nil.md), the function requests all available metadata for the object's type. Passing [`NIL`](../literals/nil.md) for `sObjId` raises an argument error before the Documentum call is attempted.

If the underlying Documentum call does not complete successfully, the function returns an empty array. When you need to distinguish "no rows returned" from a Documentum command failure, check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after the call.

## When to use

- When you need to inspect all metadata fields on a Documentum object.
- When you want to request only a specific subset of attributes by name.
- When downstream logic needs both the current attribute value and metadata such as type code, declared length, or repeating status.
- When you need a structured return shape instead of parsing Documentum results manually.

## Syntax

```ssl
DocGetMetadata(sObjId, [sAttributes])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sObjId` | [string](../types/string.md) | yes | — | Object ID or object path to query. Passing [`NIL`](../literals/nil.md) raises an exception. |
| `sAttributes` | [string](../types/string.md) | no | omitted | Comma-separated attribute list to request. Omit it, or pass [`NIL`](../literals/nil.md), to request all attributes. |

## Returns

**[array](../types/array.md)** — A two-dimensional array. Each row is a 6-element array.

| Position | Type | Value |
|----------|------|-------|
| `row[1]` | [string](../types/string.md) | Attribute name |
| `row[2]` | any | Current attribute value |
| `row[3]` | [string](../types/string.md) | Attribute description |
| `row[4]` | [number](../types/number.md) | Attribute type code |
| `row[5]` | [number](../types/number.md) | Declared attribute length |
| `row[6]` | [boolean](../types/boolean.md) | [`.T.`](../literals/true.md) when the attribute is repeating, otherwise [`.F.`](../literals/false.md) |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sObjId` is [`NIL`](../literals/nil.md). | `sObjId argument cannot be null` |

## Best practices

!!! success "Do"
    - Initialize the Documentum interface before calling `DocGetMetadata` in workflows that use the Documentum API.
    - Treat each result row as a fixed-position array and read values by their documented 1-based positions.
    - Omit `sAttributes` when you want the full metadata set.
    - Check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after an empty result when you need to know whether the call failed.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sObjId`; that raises an error instead of returning an empty array.
    - Treat each metadata row as an object with properties such as `:Name` or `:Value`.
    - Assume every empty array means the object simply has no metadata; it can also indicate a failed Documentum command.
    - Assume an invalid `sAttributes` list is silently ignored; a backend failure can still surface as an empty array plus a failed command state.

## Caveats

- Only [`NIL`](../literals/nil.md) is rejected for `sObjId`. Blank or invalid identifiers are passed through to the Documentum layer.
- When `sAttributes` is [`NIL`](../literals/nil.md) or blank, the backend requests the full attribute list for the object's type.
- `row[4]` is a numeric type code, not a descriptive type name.

## Examples

### List all metadata name and value pairs

Requests all metadata for a document, checks [`DocCommandFailed`](DocCommandFailed.md) on an empty result to distinguish a backend failure from an object with no attributes, and prints each name-value pair.

```ssl
:PROCEDURE ListDocumentMetadata;
	:DECLARE sObjId, aMetadata, nCount, nIndex, sLine;

	sObjId := "0900000180001234";

	DocInitDocumentumInterface();

	:TRY;
		aMetadata := DocGetMetadata(sObjId);
		nCount := ALen(aMetadata);

		:IF nCount == 0;
			:IF DocCommandFailed();
				UsrMes("Metadata lookup failed: " + DocGetErrorMessage());
				/* Displays on command failure;
			:ELSE;
				UsrMes("No metadata returned for " + sObjId);
				/* Displays when metadata is empty;
			:ENDIF;

			:RETURN aMetadata;
		:ENDIF;

		:FOR nIndex := 1 :TO nCount;
			sLine := aMetadata[nIndex, 1] + " = "
					 + LimsString(aMetadata[nIndex, 2]);
			UsrMes(sLine);
			/* Displays each attribute name and value;
		:NEXT;

		:RETURN aMetadata;
	:FINALLY;
		DocEndDocumentumInterface();
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ListDocumentMetadata");
```

### Request a specific attribute subset

Passes a comma-separated attribute list to restrict the result to two fields, then reads each row's attribute name to extract the `author` and `r_creation_date` values.

```ssl
:PROCEDURE GetSelectedMetadata;
	:DECLARE sObjId, sAttrs, aMetadata, sAuthor, sCreatedOn, nIndex;

	sObjId := "0900000180001234";
	sAttrs := "author,r_creation_date";
	sAuthor := "";
	sCreatedOn := "";

	DocInitDocumentumInterface();

	:TRY;
		aMetadata := DocGetMetadata(sObjId, sAttrs);

		:IF ALen(aMetadata) == 0;
			:RETURN aMetadata;
		:ENDIF;

		:FOR nIndex := 1 :TO ALen(aMetadata);
			:IF Upper(aMetadata[nIndex, 1]) == "AUTHOR";
				sAuthor := LimsString(aMetadata[nIndex, 2]);
			:ENDIF;

			:IF Upper(aMetadata[nIndex, 1]) == "R_CREATION_DATE";
				sCreatedOn := LimsString(aMetadata[nIndex, 2]);
			:ENDIF;
		:NEXT;

		UsrMes("Author: " + sAuthor);
		/* Displays the selected author;
		UsrMes("Created: " + sCreatedOn);
		/* Displays the creation date;

		:RETURN aMetadata;
	:FINALLY;
		DocEndDocumentumInterface();
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("GetSelectedMetadata");
```

### Audit attribute definitions in the returned rows

Fetches all metadata, counts how many attributes are repeating and how many have a declared length greater than 255, and displays a summary line using the type-code and length columns.

```ssl
:PROCEDURE AuditMetadataShape;
	:PARAMETERS sObjId;
	:DECLARE aMetadata, nRepeating, nLongFields, nIndex, sSummary;

	nRepeating := 0;
	nLongFields := 0;

	DocInitDocumentumInterface();

	:TRY;
		aMetadata := DocGetMetadata(sObjId);

		:IF ALen(aMetadata) == 0;
			:RETURN aMetadata;
		:ENDIF;

		:FOR nIndex := 1 :TO ALen(aMetadata);
			:IF aMetadata[nIndex, 6];
				nRepeating += 1;
			:ENDIF;

			:IF aMetadata[nIndex, 5] > 255;
				nLongFields += 1;
			:ENDIF;
		:NEXT;

		sSummary := "Attributes: " + LimsString(ALen(aMetadata))
					+ ", repeating: " + LimsString(nRepeating)
					+ ", length > 255: " + LimsString(nLongFields);
		UsrMes(sSummary);
		/* Displays attribute summary counts;

		:RETURN aMetadata;
	:FINALLY;
		DocEndDocumentumInterface();
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("AuditMetadataShape", {"0900000180001234"});
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocGetTypeAttributes`](DocGetTypeAttributes.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`DocSetMetadata`](DocSetMetadata.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
- [`boolean`](../types/boolean.md)
