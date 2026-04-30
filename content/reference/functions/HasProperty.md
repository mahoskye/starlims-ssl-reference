---
title: "HasProperty"
summary: "Checks whether a value exposes a named property."
id: ssl.function.hasproperty
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# HasProperty

Checks whether a value exposes a named property.

`HasProperty()` returns [`.T.`](../literals/true.md) when the supplied value exposes the named property and [`.F.`](../literals/false.md) when it does not. It is an existence check only; it does not read or assign the property's value.

The function throws if `oTarget` or `sPropName` is [`NIL`](../literals/nil.md). It is most useful with dynamic objects and other values that support property access.

## When to use

- When verifying that an object meets a specific schema or has required properties before performing operations that depend on them.
- When validating input or output objects to ensure essential fields are present before processing.
- When writing robust code that distinguishes missing properties from properties set to [`NIL`](../literals/nil.md) or default values.

## Syntax

```ssl
HasProperty(oTarget, sPropName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `oTarget` | [object](../types/object.md) | yes | — | The value to inspect for a property |
| `sPropName` | [string](../types/string.md) | yes | — | The property name to look up |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) if the property exists on the supplied value, [`.F.`](../literals/false.md) otherwise

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `oTarget` is [`NIL`](../literals/nil.md). | `Argument oTarget cannot be null.` |
| `sPropName` is [`NIL`](../literals/nil.md). | `Argument sPropName cannot be null.` |

## Best practices

!!! success "Do"
    - Use `HasProperty()` before reading optional properties from dynamic objects.
    - Keep property names consistent across [`AddProperty`](AddProperty.md), `HasProperty()`, and [`SetByName`](SetByName.md) calls.
    - Treat `HasProperty()` as a presence check only, then read the value separately.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `oTarget` or `sPropName`; the function raises an error instead of returning [`.F.`](../literals/false.md).
    - Use `HasProperty` to fetch a value. It only tells you whether the property exists.
    - Assume every SSL value supports property lookup. Values without properties can raise a runtime error.

## Caveats

- If the supplied value does not support property lookup, the call can raise a runtime error instead of returning [`.F.`](../literals/false.md).

## Examples

### Check whether an optional property exists before reading it

Guards against a missing property before attempting to read it, then adds the property and shows that the same check now passes. Both branches produce distinct messages, demonstrating that the check accurately reflects the object's current state.

```ssl
:PROCEDURE SendUserNotification;
    :DECLARE oUserProfile, sNotificationText;

    oUserProfile := CreateUdObject();
    oUserProfile:Name := "Jane Analyst";
    oUserProfile:Department := "Quality Control";

    :IF !HasProperty(oUserProfile, "Email");
        sNotificationText := "Notification cannot be sent because Email is missing.";
        UsrMes(sNotificationText);
        /* Displays missing-email message;
    :ENDIF;

    AddProperty(oUserProfile, "Email");
    oUserProfile:Email := "jane.analyst@lab.example.com";

    :IF HasProperty(oUserProfile, "Email");
        sNotificationText := "Sending notification to " + oUserProfile:Email;
        UsrMes(sNotificationText);
        /* Displays email notification message;
    :ENDIF;

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("SendUserNotification");
```

### Update fields conditionally based on property presence

Iterates over several properties, updating only those that exist on the object. `LastModified` was never added, so its branch is skipped and only two fields are logged as updated.

```ssl
:PROCEDURE UpdateSampleFields;
    :DECLARE oSample, sStatus, aUpdatedFields, sLog;

    sStatus := "ACTIVE";
    aUpdatedFields := {};

    oSample := CreateUdObject();
    AddProperty(oSample, {"SampleID", "Status", "Notes"});
    oSample:SampleID := "LAB-2024-0042";
    oSample:Notes := "Initial review complete";

    :IF HasProperty(oSample, "Status");
        oSample:Status := sStatus;
        AAdd(aUpdatedFields, "Status");
    :ENDIF;

    :IF HasProperty(oSample, "Notes");
        oSample:Notes := "Updated via batch process";
        AAdd(aUpdatedFields, "Notes");
    :ENDIF;

    :IF HasProperty(oSample, "LastModified");
        oSample:LastModified := Today();
        AAdd(aUpdatedFields, "LastModified");
    :ENDIF;

    sLog := "Fields updated: " + LimsString(ALen(aUpdatedFields));
    UsrMes(sLog);

    :RETURN aUpdatedFields;
:ENDPROC;

/* Usage;
DoProc("UpdateSampleFields");
```

[`UsrMes`](UsrMes.md) displays:

```text
Fields updated: 2
```

## Related

- [`AddProperty`](AddProperty.md)
- [`GetByName`](GetByName.md)
- [`GetInternal`](GetInternal.md)
- [`SetByName`](SetByName.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
