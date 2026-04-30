---
title: "GetGroupSeparator"
summary: "Returns the current group separator as a string."
id: ssl.function.getgroupseparator
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetGroupSeparator

Returns the current group separator as a string.

`GetGroupSeparator` returns the separator text currently used for grouped numeric formatting. It takes no parameters and returns the separator directly, such as `,`, `.`, or a space. Use it when code needs the current separator as text, especially before formatting values or when saving and restoring the setting around a temporary change.

## When to use

- When you need the current group separator as text.
- When building locale-aware numeric formatting or parsing logic.
- When comparing the active separator against an expected character.
- When saving the current separator before calling [`SetGroupSeparator`](SetGroupSeparator.md).

## Syntax

```ssl
GetGroupSeparator();
```

## Parameters

This function takes no parameters.

## Returns

**[string](../types/string.md)** — The current group separator.

## Best practices

!!! success "Do"
    - Read the separator from `GetGroupSeparator` when code needs the active value.
    - Use the returned string consistently in formatting or parsing logic.
    - Save the current separator before a temporary call to [`SetGroupSeparator`](SetGroupSeparator.md) so you can restore it.

!!! failure "Don't"
    - Hardcode `,` or `.` when code is expected to follow the active numeric format.
    - Assume the separator cannot change during the life of the session.
    - Use `GetGroupSeparator` as a substitute for changing the setting; call [`SetGroupSeparator`](SetGroupSeparator.md) when you need a different separator.

## Caveats

- If you cache the value and later change it with [`SetGroupSeparator`](SetGroupSeparator.md), the cached value will no longer match the current setting.

## Examples

### Display the current group separator

Show the active group separator in a user message.

```ssl
:PROCEDURE DisplayGroupSeparator;
    :DECLARE sGroupSep, sMessage;

    sGroupSep := GetGroupSeparator();
    sMessage := "Group separator: [" + sGroupSep + "]";

    UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("DisplayGroupSeparator");
```

[`UsrMes`](UsrMes.md) displays:

```text
Group separator: [,]
```

### Check whether a formatted value uses the current separator

Compare a text value against the active separator before further processing.

```ssl
:PROCEDURE UsesCurrentGroupSeparator;
    :PARAMETERS sFormattedValue;
    :DECLARE sGroupSep, bUsesCurrentSep;

    sGroupSep := GetGroupSeparator();
    bUsesCurrentSep := sGroupSep $ sFormattedValue;

    :IF bUsesCurrentSep;
        UsrMes("Value uses the current group separator: " + sFormattedValue);
    :ELSE;
        UsrMes("Value does not use the current group separator.");
    :ENDIF;

    :RETURN bUsesCurrentSep;
:ENDPROC;

/* Usage;
DoProc("UsesCurrentGroupSeparator", {"1,234,567"});
```

When called with `"1,234,567"`, [`UsrMes`](UsrMes.md) displays:

```text
Value uses the current group separator: 1,234,567
```

### Save and restore the separator around a temporary change

Capture the current separator, switch it temporarily, then restore the original value.

```ssl
:PROCEDURE RestoreGroupSeparator;
    :DECLARE sOriginalSep, sPreviousSep, sCurrentSep;

    sOriginalSep := GetGroupSeparator();
    sPreviousSep := SetGroupSeparator(".");
    sCurrentSep := GetGroupSeparator();

    UsrMes("Previous: [" + sPreviousSep + "]");
    UsrMes("Current: [" + sCurrentSep + "]");

    SetGroupSeparator(sOriginalSep);
:ENDPROC;

/* Usage;
DoProc("RestoreGroupSeparator");
```

## Related

- [`SetGroupSeparator`](SetGroupSeparator.md)
- [`string`](../types/string.md)
