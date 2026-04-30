---
title: "DocGetTypeAttributesAsDataset"
summary: "Returns the attributes for a Documentum type as a dataset-formatted string."
id: ssl.function.docgettypeattributesasdataset
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocGetTypeAttributesAsDataset

Returns the attributes for a Documentum type as a dataset-formatted string.

Use this function when you need the attribute definition for a Documentum type in string form instead of the array returned by [`DocGetTypeAttributes`](DocGetTypeAttributes.md). Pass a type name such as `dm_document`; the function returns the dataset string from the current Documentum session.

## When to use

- When you need a dataset-formatted description of a Documentum type's attributes.
- When downstream code expects a string result instead of an array of attributes.
- When you need to inspect a type definition and branch based on whether a result was returned.

## Syntax

```ssl
DocGetTypeAttributesAsDataset(sTypeName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sTypeName` | [string](../types/string.md) | yes | — | Documentum type name to query. |

## Returns

**[string](../types/string.md)** — A dataset-formatted string containing the type's attributes.
Returns `""` when the underlying Documentum call does not return a dataset.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sTypeName` is [`NIL`](../literals/nil.md). | `sTypeName argument cannot be null` |

## Best practices

!!! success "Do"
    - Call [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md) before Documentum operations and check the result immediately after this call.
    - Treat an empty string as an ambiguous result until you also check [`DocCommandFailed`](DocCommandFailed.md).
    - Capture [`DocGetErrorMessage`](DocGetErrorMessage.md) right away when [`DocCommandFailed()`](DocCommandFailed.md) is [`.T.`](../literals/true.md).

!!! failure "Don't"
    - Assume `""` means only that the type has no attributes.
    - Pass [`NIL`](../literals/nil.md) for `sTypeName`.
    - Wait until later in the workflow to inspect the failure state because another Documentum call can replace it.

## Caveats

- The function does not itself tell you why an empty string was returned. Check [`DocCommandFailed`](DocCommandFailed.md) to distinguish a backend failure from a type that has no attributes.

## Examples

### Retrieve attributes for a known type

Initializes Documentum, fetches the attribute dataset for `dm_document`, and displays it when the call succeeds and returns a non-empty result.

```ssl
:PROCEDURE ShowTypeAttributes;
    :DECLARE sTypeName, sAttrs;

    DocInitDocumentumInterface();

    sTypeName := "dm_document";
    sAttrs := DocGetTypeAttributesAsDataset(sTypeName);

    :IF .NOT. DocCommandFailed() .AND. .NOT. Empty(sAttrs);
        UsrMes("Attributes for " + sTypeName + ":" + Chr(10) + sAttrs);
    :ENDIF;

    DocEndDocumentumInterface();
:ENDPROC;

/* Usage;
DoProc("ShowTypeAttributes");
```

[`UsrMes`](UsrMes.md) displays:

```
Attributes for dm_document:
[dataset text]
```

### Distinguish an empty result from a failed command

Retrieves the attribute dataset for a caller-supplied type name, distinguishing a backend failure (checked via [`DocCommandFailed`](DocCommandFailed.md)) from a successful call that returned no data.

```ssl
:PROCEDURE LoadTypeAttributes;
    :PARAMETERS sTypeName;
    :DECLARE sAttrs, sErrMsg;

    DocInitDocumentumInterface();

    sAttrs := DocGetTypeAttributesAsDataset(sTypeName);

    :IF DocCommandFailed();
        sErrMsg := DocGetErrorMessage();
        UsrMes("Unable to load type attributes: " + sErrMsg);
        /* Displays on failure: Unable to load type attributes;
        DocEndDocumentumInterface();
        :RETURN "";
    :ENDIF;

    :IF Empty(sAttrs);
        UsrMes("No attribute dataset was returned for type " + sTypeName);
    :ENDIF;

    DocEndDocumentumInterface();

    :RETURN sAttrs;
:ENDPROC;

/* Usage;
DoProc("LoadTypeAttributes", {"dm_document"});
```

### Compare two type definitions before a mapping step

Calls `DocGetTypeAttributesAsDataset` twice to retrieve source and target type definitions, returning [`.T.`](../literals/true.md) only when both calls succeed and the resulting datasets are identical.

```ssl
:PROCEDURE CompareTypeDefinitions;
    :PARAMETERS sSourceType, sTargetType;
    :DECLARE sSourceAttrs, sTargetAttrs, sErrMsg;

    DocInitDocumentumInterface();

    sSourceAttrs := DocGetTypeAttributesAsDataset(sSourceType);

    :IF DocCommandFailed();
        sErrMsg := DocGetErrorMessage();
        UsrMes("Failed to read source type attributes: " + sErrMsg);
        /* Displays on source failure: Failed to read source type attributes;
        DocEndDocumentumInterface();
        :RETURN .F.;
    :ENDIF;

    sTargetAttrs := DocGetTypeAttributesAsDataset(sTargetType);

    :IF DocCommandFailed();
        sErrMsg := DocGetErrorMessage();
        UsrMes("Failed to read target type attributes: " + sErrMsg);
        /* Displays on target failure: Failed to read target type attributes;
        DocEndDocumentumInterface();
        :RETURN .F.;
    :ENDIF;

    :IF Empty(sSourceAttrs) .OR. Empty(sTargetAttrs);
        UsrMes("One or both type definitions returned no dataset text");
        DocEndDocumentumInterface();
        :RETURN .F.;
    :ENDIF;

    DocEndDocumentumInterface();

    :RETURN sSourceAttrs == sTargetAttrs;
:ENDPROC;

/* Usage;
DoProc("CompareTypeDefinitions", {"dm_document", "dm_sysobject"});
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocGetTypeAttributes`](DocGetTypeAttributes.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`string`](../types/string.md)
