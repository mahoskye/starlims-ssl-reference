---
title: "DeleteInlineCode"
summary: "Removes a named inline code entry."
id: ssl.function.deleteinlinecode
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DeleteInlineCode

Removes a named inline code entry.

`DeleteInlineCode` removes an inline code entry by name and returns [`.T.`](../literals/true.md) when the call completes without error. The argument is converted to a string and the lookup is case-insensitive, so `"MyBlock"`, `"myblock"`, and `"MYBLOCK"` all target the same entry.

If no inline-code collection has been created yet, the call still succeeds and returns [`.T.`](../literals/true.md). If a collection exists but the requested name is not present, the function raises `<sName> not in scope.` After a successful deletion, that name is no longer available through [`GetInlineCode`](GetInlineCode.md).

## When to use

- When you need to remove temporary inline code after finishing with it.
- When you need to clear an old named block before reusing the same name for updated inline code.
- When you need to clean up dynamically registered code so later logic does not pick it up by mistake.

## Syntax

```ssl
DeleteInlineCode(sName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sName` | [string](../types/string.md) | yes | — | Name of the inline code entry to delete. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the call completes without error, whether the named entry was removed or no inline-code collection existed yet.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| An inline-code collection exists but the requested name is not present. `<sName>` is replaced with the actual value of `sName`. | `<sName> not in scope.` |

## Best practices

!!! success "Do"
    - Save the inline code with [`GetInlineCode`](GetInlineCode.md) before deleting it if you may need the text again.
    - Delete temporary inline code as soon as the workflow no longer needs it.
    - Reuse the same logical name only after removing the older definition.

!!! failure "Don't"
    - Pass the inline code contents to `DeleteInlineCode`; pass the registered name.
    - Assume a missing name is ignored once inline code exists; that path raises a runtime error.
    - Keep stale inline code registered if later logic might resolve the same name.

## Caveats

- `DeleteInlineCode` does not return the deleted source. Retrieve it first with [`GetInlineCode`](GetInlineCode.md) if you need to preserve it.

## Examples

### Delete a temporary inline code block after saving its text

Retrieves the inline code source with [`GetInlineCode`](GetInlineCode.md) before removing the named entry, preserving the text for later use.

```ssl
:PROCEDURE RemoveTempInlineCode;
    :DECLARE sCodeName, sSavedCode, bDeleted;

    sCodeName := "TempMessage";

    :BEGININLINECODE "TempMessage";
        :DECLARE sMessage;

        sMessage := "Review complete";

        :RETURN sMessage;
    :ENDINLINECODE;

    sSavedCode := GetInlineCode(sCodeName, {});
    bDeleted := DeleteInlineCode(sCodeName);

    UsrMes("Deleted inline code: " + LimsString(bDeleted));  /* Displays deletion status;
    UsrMes("Saved text length: " + LimsString(Len(sSavedCode)));  /* Displays saved text length;

    :RETURN bDeleted;
:ENDPROC;

/* Usage;
DoProc("RemoveTempInlineCode");
```

### Replace an older inline code definition with a new one

Removes the previous definition before registering a replacement under the same name, then confirms the updated definition is in scope.

```ssl
:PROCEDURE RefreshInlineTemplate;
    :DECLARE sCodeName, sCurrentCode, bDeleted;

    sCodeName := "OrderSummary";

    :BEGININLINECODE "OrderSummary";
        :DECLARE sStatus;

        sStatus := "Original";

        :RETURN sStatus;
    :ENDINLINECODE;

    bDeleted := DeleteInlineCode(sCodeName);

    :BEGININLINECODE "OrderSummary";
        :DECLARE sUpdatedStatus;

        sUpdatedStatus := "Updated";

        :RETURN sUpdatedStatus;
    :ENDINLINECODE;

    sCurrentCode := GetInlineCode(sCodeName, {});

    UsrMes("Previous template removed: " + LimsString(bDeleted));  /* Displays deletion status;
    UsrMes("Current inline code:");
    UsrMes(sCurrentCode);  /* Displays updated inline code text;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("RefreshInlineTemplate");
```

## Related

- [`GetInlineCode`](GetInlineCode.md)
- [`GetRegion`](GetRegion.md)
- [`GetRegionEx`](GetRegionEx.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
