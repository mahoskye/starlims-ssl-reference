---
title: "DocSetMetadata"
summary: "Updates one or more metadata attributes on a Documentum object."
id: ssl.function.docsetmetadata
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocSetMetadata

Updates one or more metadata attributes on a Documentum object.

`DocSetMetadata` takes a Documentum object identifier and an [array](../types/array.md) of attribute/value pairs, then submits those pairs as one metadata update operation. Pass `aAttributes` as an array of two-item arrays in the form `{{"attribute_name", value}, ...}`.

If the Documentum call completes successfully, the function returns [`.T.`](../literals/true.md). If the Documentum call fails, the function returns [`.F.`](../literals/false.md). Check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after a [`.F.`](../literals/false.md) return when you need the failure detail. Passing [`NIL`](../literals/nil.md) for `sObjId` or `aAttributes` raises an argument error before the Documentum call is attempted.

## When to use

- When you need to update several metadata fields on the same Documentum object in one call.
- When your script already has attribute name/value pairs ready to submit.
- When you need a simple success/failure result and can inspect [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) on failure.

## Syntax

```ssl
DocSetMetadata(sObjId, aAttributes)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sObjId` | [string](../types/string.md) | yes | — | Documentum object identifier to update. Passing [`NIL`](../literals/nil.md) raises an exception. |
| `aAttributes` | [array](../types/array.md) | yes | — | Array of two-item arrays in the form `{{"attribute_name", value}, ...}`. Each row supplies the attribute name at position `1` and the value at position `2`. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the metadata update completes successfully; [`.F.`](../literals/false.md) when the underlying Documentum command fails.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sObjId` is [`NIL`](../literals/nil.md). | `sObjId argument cannot be null` |
| `aAttributes` is [`NIL`](../literals/nil.md). | `aAttributes argument cannot be null` |

## Best practices

!!! success "Do"
    - Build `aAttributes` as an array of two-item arrays so each row clearly maps an attribute name to a value.
    - Check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after a [`.F.`](../literals/false.md) return.
    - Group related metadata changes into one call when they target the same object.
    - Initialize the Documentum interface before Documentum API work in scripts that manage their own session lifecycle.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sObjId` or `aAttributes`; both raise an error before any metadata update is attempted.
    - Assume a [`.F.`](../literals/false.md) return explains the failure by itself; inspect [`DocGetErrorMessage`](DocGetErrorMessage.md) while the error state is still current.
    - Pass rows that are not `{name, value}` pairs; the function expects each array element to provide the attribute name first and the value second.
    - Split one logical metadata update across multiple calls unless you need separate success handling for each call.

## Caveats

- The SSL entry point documents argument validation only for [`NIL`](../literals/nil.md) values. Blank strings, unknown attribute names, and other backend-specific validation outcomes are handled by the Documentum call, not by a separate SSL pre-check.

## Examples

### Update one metadata field

Sets a single `status` attribute on a known document and reports success or failure.

```ssl
:PROCEDURE UpdateDocumentStatus;
    :DECLARE sObjId, aAttributes, bSuccess;

    sObjId := "0900001680000b3f";
    aAttributes := {{"status", "Final"}};

    DocInitDocumentumInterface();

    :TRY;
        bSuccess := DocSetMetadata(sObjId, aAttributes);

        :IF bSuccess;
            UsrMes("Document metadata updated for " + sObjId);
        :ELSE;
            /* Displays on failure: metadata update failed;
            UsrMes("Metadata update failed: " + DocGetErrorMessage());
        :ENDIF;

        :RETURN bSuccess;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("UpdateDocumentStatus");
```

### Update several fields and inspect the failure state

Updates three fields at once and uses [`DocCommandFailed`](DocCommandFailed.md) to confirm a backend failure before reading the error message.

```ssl
:PROCEDURE UpdateDocumentProfile;
    :DECLARE sObjId, aAttributes, bSuccess;

    sObjId := "090000128000efad";
    aAttributes := {
        {"author", "Marie Curie"},
        {"category", "Chemistry"},
        {"status", "Approved"}
    };

    DocInitDocumentumInterface();

    :TRY;
        bSuccess := DocSetMetadata(sObjId, aAttributes);

        :IF .NOT. bSuccess;
            :IF DocCommandFailed();
                /* Displays on failure: metadata update failed;
                UsrMes("Metadata update failed: " + DocGetErrorMessage());
            :ENDIF;

            :RETURN .F.;
        :ENDIF;

        UsrMes("Profile metadata updated for " + sObjId);
        :RETURN .T.;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("UpdateDocumentProfile");
```

### Build a conditional metadata payload at runtime

Builds the attribute array based on an approval flag, adding approval date and flag fields when approved and a rejection flag when not, then submits the whole set in one call.

```ssl
:PROCEDURE SyncReviewMetadata;
    :PARAMETERS sObjId, sReviewedBy, bApproved;
    :DECLARE aAttributes, bSuccess, sApprovedDate;

    aAttributes := {{"reviewed_by", sReviewedBy}};

    :IF bApproved;
        sApprovedDate := DToC(Today());

        AAdd(aAttributes, {"approved_flag", "Y"});
        AAdd(aAttributes, {"approved_date", sApprovedDate});
    :ELSE;
        AAdd(aAttributes, {"approved_flag", "N"});
    :ENDIF;

    DocInitDocumentumInterface();

    :TRY;
        bSuccess := DocSetMetadata(sObjId, aAttributes);

        :IF .NOT. bSuccess .AND. DocCommandFailed();
            /* Displays on failure: review metadata sync failed;
            UsrMes("Review metadata sync failed: " + DocGetErrorMessage());
        :ENDIF;

        :RETURN bSuccess;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("SyncReviewMetadata", {"0900001680000b3f", "jdoe", .T.});
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocEndDocumentumInterface`](DocEndDocumentumInterface.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocGetMetadata`](DocGetMetadata.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
