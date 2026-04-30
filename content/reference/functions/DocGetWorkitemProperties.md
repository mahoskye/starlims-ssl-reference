---
title: "DocGetWorkitemProperties"
summary: "Retrieves workflow flags and linked document IDs for a Documentum work item."
id: ssl.function.docgetworkitemproperties
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocGetWorkitemProperties

Retrieves workflow flags and linked document IDs for a Documentum work item.

`DocGetWorkitemProperties` returns a positional SSL array for the specified work item. The first three elements are booleans for delegation, repeatability, and sign-off requirements. Any remaining elements are document IDs from the work item's packages.

The returned array always uses the same order. If the current user is the workflow supervisor, the delegation and repeatability values are forced to [`.T.`](../literals/true.md). Otherwise those two values come from the work item itself.

## When to use

- When you need to decide whether a work item can be delegated or repeated.
- When you need to check whether a work item requires sign-off before continuing workflow logic.
- When you need the IDs of documents attached to a work item package.

## Syntax

```ssl
DocGetWorkitemProperties(sWorkitemId)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sWorkitemId` | [string](../types/string.md) | yes | — | ID of the Documentum work item to inspect. |

## Returns

**[array](../types/array.md)** — A positional array with three booleans followed by zero or more document IDs.

| Position | Type | Meaning |
|----------|------|---------|
| `aProps[1]` | [boolean](../types/boolean.md) | [`.T.`](../literals/true.md) when the work item is delegatable for the current user. |
| `aProps[2]` | [boolean](../types/boolean.md) | [`.T.`](../literals/true.md) when the work item is repeatable for the current user. |
| `aProps[3]` | [boolean](../types/boolean.md) | [`.T.`](../literals/true.md) when the work item requires sign-off. |
| `aProps[4+]` | [string](../types/string.md) | Document IDs from the work item package, if any. |

If the work item has no linked documents, the array length is `3`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sWorkitemId` is [`NIL`](../literals/nil.md). | `sWorkitemId argument cannot be null` |

## Best practices

!!! success "Do"
    - Read the returned array by fixed position, not by guessing from value type.
    - Check `ALen(aProps)` before iterating document IDs from `aProps[4]` onward.
    - Wrap the call in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the work item may be missing or inaccessible.
    - Treat the first two booleans as current-user workflow permissions, especially for supervisor scenarios.

!!! failure "Don't"
    - Assume the document list starts at `aProps[1]`; the first three entries are always booleans.
    - Assume `aProps[1]` and `aProps[2]` always reflect the stored work item flags without regard to the current user.
    - Assume every work item has linked documents; the array may contain only three elements.
    - Build logic that depends on custom labels or metadata in the result; this function returns only positional values.

## Caveats

- The document values are IDs from the work item packages, not expanded document metadata.

## Examples

### Read the three workflow flags

Reads the first three elements of the properties array and displays each as a boolean, showing whether delegation, repeatability, and sign-off are active for the current user.

```ssl
:PROCEDURE ShowWorkitemFlags;
    :DECLARE sWorkitemId, aProps, bCanDelegate, bCanRepeat, bNeedsSignOff;

    sWorkitemId := "0900001280001234";
    aProps := DocGetWorkitemProperties(sWorkitemId);

    bCanDelegate := aProps[1];
    bCanRepeat := aProps[2];
    bNeedsSignOff := aProps[3];

    UsrMes("Delegatable: " + LimsString(bCanDelegate));
    /* Displays delegation state;
    UsrMes("Repeatable: " + LimsString(bCanRepeat));
    /* Displays repeatable state;
    UsrMes("Sign-off required: " + LimsString(bNeedsSignOff));
    /* Displays sign-off state;
:ENDPROC;

/* Usage;
DoProc("ShowWorkitemFlags");
```

### List linked document IDs

Checks [`ALen`](ALen.md) to detect when no packages are attached, then iterates from position 4 onward to print each linked document ID.

```ssl
:PROCEDURE ListWorkitemDocuments;
    :PARAMETERS sWorkitemId;
    :DECLARE aProps, nIndex;

    aProps := DocGetWorkitemProperties(sWorkitemId);

    :IF ALen(aProps) == 3;
        UsrMes("No linked documents for work item " + sWorkitemId);
        /* Displays when no documents are linked;

        :RETURN;
    :ENDIF;

    :FOR nIndex := 4 :TO ALen(aProps);
        UsrMes("Document ID: " + aProps[nIndex]);
        /* Displays each linked document ID;
    :NEXT;
:ENDPROC;

/* Usage;
DoProc("ListWorkitemDocuments", {"0900001280001234"});
```

### Route follow-up logic from the returned values

Reads the three boolean flags and the document count, then selects a workflow route based on sign-off, delegation, repeatability, and document presence. Uses [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) to handle work items that are missing or inaccessible.

```ssl
:PROCEDURE EvaluateWorkitemRouting;
    :PARAMETERS sWorkitemId;
    :DECLARE aProps, bCanDelegate, bCanRepeat, bNeedsSignOff, nDocCount;
    :DECLARE sRoute;

    :TRY;
        aProps := DocGetWorkitemProperties(sWorkitemId);

        bCanDelegate := aProps[1];
        bCanRepeat := aProps[2];
        bNeedsSignOff := aProps[3];
        nDocCount := ALen(aProps) - 3;

        :BEGINCASE;
        :CASE bNeedsSignOff;
            sRoute := "SignOffReview";
            :EXITCASE;
        :CASE bCanDelegate .AND. nDocCount > 0;
            sRoute := "DelegateWithDocuments";
            :EXITCASE;
        :CASE bCanRepeat;
            sRoute := "RepeatStep";
            :EXITCASE;
        :OTHERWISE;
            sRoute := "StandardProcessing";
            :EXITCASE;
        :ENDCASE;

        UsrMes("Selected route: " + sRoute);
        /* Displays the selected route;

        :RETURN sRoute;
    :CATCH;
        ErrorMes("Unable to read work item properties");

        :RETURN "";
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("EvaluateWorkitemRouting", {"0900001280001234"});
```

## Related

- [`DocAcquireWorkitem`](DocAcquireWorkitem.md)
- [`DocDelegateWorkitem`](DocDelegateWorkitem.md)
- [`DocRepeatWorkitem`](DocRepeatWorkitem.md)
- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
