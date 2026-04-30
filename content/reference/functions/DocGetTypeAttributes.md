---
title: "DocGetTypeAttributes"
summary: "Retrieves the attribute definitions for a Documentum type as a two-dimensional array."
id: ssl.function.docgettypeattributes
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocGetTypeAttributes

Retrieves the attribute definitions for a Documentum type as a two-dimensional array.

If `sTypeName` is [`NIL`](../literals/nil.md), the function raises an argument error before the Documentum call is attempted. Other Documentum-side failures are converted into an empty array. When `ALen(aAttrs) == 0` and you need to know whether the lookup failed, check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after the call.

## When to use

- When you need to inspect the available attributes for a Documentum type before creating
  validation, mapping, or UI logic.
- When downstream logic needs the attribute description, numeric type code, declared
  length, or repeating flag for each field.
- When you want a structured array result instead of parsing the dataset string returned
  by [`DocGetTypeAttributesAsDataset`](DocGetTypeAttributesAsDataset.md).
- When you need to distinguish a usable type-definition result from an empty lookup by
  checking the Documentum command status after the call.

## Syntax

```ssl
DocGetTypeAttributes(sTypeName)
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `sTypeName` | [string](../types/string.md) | yes | — | Documentum type name to inspect. Passing [`NIL`](../literals/nil.md) raises an exception. |

## Returns

**[array](../types/array.md)** — A two-dimensional array. Each row is a 6-element array.

| Position | Type | Value |
| --- | --- | --- |
| `row[1]` | [string](../types/string.md) | Attribute name |
| `row[2]` | any | Value slot in the shared attribute row format. This function does not populate a current document value here. |
| `row[3]` | [string](../types/string.md) | Attribute description |
| `row[4]` | [number](../types/number.md) | Numeric attribute type code |
| `row[5]` | [number](../types/number.md) | Declared attribute length |
| `row[6]` | [boolean](../types/boolean.md) | [`.T.`](../literals/true.md) when the attribute is repeating, otherwise [`.F.`](../literals/false.md) |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sTypeName` is [`NIL`](../literals/nil.md). | `sTypeName argument cannot be null` |

## Best practices

!!! success "Do"
    - Initialize and log in to the Documentum interface before calling `DocGetTypeAttributes` in workflows that use Documentum APIs.
    - Treat each result row as a fixed-position array and read values by their documented 1-based positions.
    - Check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after an empty result when you need to know whether the lookup failed.
    - Use `row[4]`, `row[5]`, and `row[6]` for schema decisions such as type-sensitive validation, length checks, and handling repeating attributes.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sTypeName`; that raises an error instead of returning an empty array.
    - Treat each row as an object with named properties such as `:Name` or `:Description`.
    - Assume an empty array always means the type simply has no attributes; it can also mean the Documentum command failed.
    - Treat `row[2]` as a current document value returned from this function; this API reports type-definition metadata.

## Caveats

- The function rejects only [`NIL`](../literals/nil.md) for `sTypeName`. Other values are passed to the Documentum layer.
- `row[4]` is a numeric type code, not a descriptive type name.
- Use [`DocGetTypeAttributesAsDataset`](DocGetTypeAttributesAsDataset.md) instead if you specifically need the dataset-string form of the same lookup.

## Examples

### List attribute names for a known type

Fetches all attributes for the `dm_document` type and prints each attribute's name alongside its description, exiting early when the result is empty.

```ssl
:PROCEDURE ListTypeAttributes;
    :DECLARE sTypeName, aAttrs, nIndex, sLine;

    sTypeName := "dm_document";
    aAttrs := DocGetTypeAttributes(sTypeName);

    :IF ALen(aAttrs) == 0;
        UsrMes("No attributes returned for " + sTypeName);
        :RETURN aAttrs;
    :ENDIF;

    :FOR nIndex := 1 :TO ALen(aAttrs);
        sLine := aAttrs[nIndex, 1] + " - " + aAttrs[nIndex, 3];
        UsrMes(sLine);
    :NEXT;

    :RETURN aAttrs;
:ENDPROC;

/* Usage;
DoProc("ListTypeAttributes");
```

`UsrMes` displays:

```text
No attributes returned for dm_document
[attribute name] - [attribute description]
```

### Separate repeating and single-value attributes

Counts how many attributes are single-value and how many are repeating for a caller-supplied type name, then displays a summary line.

```ssl
:PROCEDURE SummarizeTypeAttributes;
    :PARAMETERS sTypeName;
    :DECLARE aAttrs, nRepeating, nSingle, nIndex, sSummary;

    nRepeating := 0;
    nSingle := 0;
    aAttrs := DocGetTypeAttributes(sTypeName);

    :IF ALen(aAttrs) == 0;
        :RETURN aAttrs;
    :ENDIF;

    :FOR nIndex := 1 :TO ALen(aAttrs);
        :IF aAttrs[nIndex, 6];
            nRepeating += 1;
        :ELSE;
            nSingle += 1;
        :ENDIF;
    :NEXT;

    sSummary := "Type " + sTypeName
		        + " has " + LimsString(nSingle)
		        + " single-value attributes and " + LimsString(nRepeating)
		        + " repeating attributes";
    UsrMes(sSummary);

    :RETURN aAttrs;
:ENDPROC;

/* Usage;
DoProc("SummarizeTypeAttributes", {"dm_document"});
```

[`UsrMes`](UsrMes.md) displays:

```text
Type [type name] has [n] single-value attributes and [n] repeating attributes
```

### Distinguish an empty result from a failed Documentum lookup

Logs in to Documentum, fetches type attributes, and distinguishes a failed lookup (indicated by [`DocCommandFailed`](DocCommandFailed.md)) from a type that returned no attributes, then prints the name and type code of each attribute found.

```ssl
:PROCEDURE AuditTypeDefinition;
    :PARAMETERS sDocBase, sUser, sPassword, sTypeName;
    :DECLARE aAttrs, nIndex, sError;

    DocInitDocumentumInterface();

    :TRY;
        :IF .NOT. DocLoginToDocumentum(sDocBase, sUser, sPassword);
            ErrorMes("Documentum login failed: " + DocGetErrorMessage());
            :RETURN {};
        :ENDIF;

        aAttrs := DocGetTypeAttributes(sTypeName);

        :IF ALen(aAttrs) == 0;
            :IF DocCommandFailed();
                sError := DocGetErrorMessage();
                ErrorMes("Type attribute lookup failed: " + sError);
            :ELSE;
                UsrMes("No attributes returned for type " + sTypeName);
            :ENDIF;

            :RETURN aAttrs;
        :ENDIF;

        :FOR nIndex := 1 :TO ALen(aAttrs);
            UsrMes(aAttrs[nIndex, 1] + " type="
	                + LimsString(aAttrs[nIndex, 4]));
        :NEXT;

        :RETURN aAttrs;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("AuditTypeDefinition", {"ProductionDB", "doc_user", "secret", "dm_document"});
```

Possible output:

```text
Documentum login failed: [Documentum error]
Type attribute lookup failed: [Documentum error]
No attributes returned for type dm_document
[attribute name] type=[type code]
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocGetMetadata`](DocGetMetadata.md)
- [`DocGetTypeAttributesAsDataset`](DocGetTypeAttributesAsDataset.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
- [`boolean`](../types/boolean.md)
