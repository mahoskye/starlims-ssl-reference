---
title: "DocExistsUser"
summary: "Determines whether a Documentum user exists for a supplied login context."
id: ssl.function.docexistsuser
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocExistsUser

Determines whether a Documentum user exists for a supplied login context.

`DocExistsUser` takes two required string arguments: `sLoginName` and `sUserName`. It checks whether `sUserName` exists for the supplied `sLoginName` context and returns [`.T.`](../literals/true.md) when the user is found or [`.F.`](../literals/false.md) when the user is not found.

## When to use

- When you need to validate a user name before assigning Documentum-based work or ownership.
- When you need to check a batch of expected users during synchronization or setup.
- When you need to guard workflow logic that should only continue when a target
  user exists.

## Syntax

```ssl
DocExistsUser(sLoginName, sUserName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sLoginName` | [string](../types/string.md) | yes | — | Login name used for the Documentum lookup context. |
| `sUserName` | [string](../types/string.md) | yes | — | User name to test for existence. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the requested user exists in the supplied lookup context. [`.F.`](../literals/false.md) otherwise.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sLoginName` is [`NIL`](../literals/nil.md). | `sLoginName argument cannot be null` |
| `sUserName` is [`NIL`](../literals/nil.md). | `sUserName argument cannot be null` |

## Best practices

!!! success "Do"
    - Pass both required string arguments every time you call the function.
    - Validate candidate user names before using them in downstream workflow logic.
    - Handle the [`.F.`](../literals/false.md) result explicitly when the user is required for the next step.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sLoginName` or `sUserName`; the function raises an error immediately.
    - Assume a successful lookup from a previous step still applies to a different user name.
    - Skip the result check when later logic depends on the user existing.

## Caveats

- Only [`NIL`](../literals/nil.md) is checked before the Documentum call. Blank strings are passed through to the lookup.

## Examples

### Check one user before continuing

Calls `DocExistsUser` with hardcoded login and user names and displays whether the user was found in Documentum.

```ssl
:PROCEDURE ValidateApprover;
    :DECLARE sLoginName, sUserName, bExists;

    sLoginName := "admin";
    sUserName := "jsmith";

    bExists := DocExistsUser(sLoginName, sUserName);

    :IF bExists;
        UsrMes("Approver is available in Documentum: " + sUserName);
        /* Displays when found;
    :ELSE;
        UsrMes("Approver was not found in Documentum: " + sUserName);
        /* Displays when not found;
    :ENDIF;

    :RETURN bExists;
:ENDPROC;

/* Usage;
DoProc("ValidateApprover");
```

### Collect missing users from a list

Iterates an array of user names, checks each one against Documentum, and returns an array containing only the names that were not found.

```ssl
:PROCEDURE FindMissingDocUsers;
    :PARAMETERS sLoginName, aUserNames;
    :DECLARE aMissingUsers, sUserName, bExists, nIndex;

    aMissingUsers := {};

    :FOR nIndex := 1 :TO ALen(aUserNames);
        sUserName := aUserNames[nIndex];
        bExists := DocExistsUser(sLoginName, sUserName);

        :IF .NOT. bExists;
            AAdd(aMissingUsers, sUserName);
        :ENDIF;
    :NEXT;

    :RETURN aMissingUsers;
:ENDPROC;

/* Usage;
DoProc("FindMissingDocUsers", {"admin", {"jsmith", "mwilson"}});
```

### Audit lookups and capture null-argument errors

Iterates a two-column array of login and user name pairs, wraps each lookup in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) to handle [`NIL`](../literals/nil.md)-argument exceptions, and collects a result row, including any error description, for every pair.

```ssl
:PROCEDURE AuditDocUsers;
    :PARAMETERS aRows;
    :DECLARE aResults, sLoginName, sUserName, bExists, oErr, nIndex;

    aResults := {};

    :FOR nIndex := 1 :TO ALen(aRows);
        sLoginName := aRows[nIndex, 1];
        sUserName := aRows[nIndex, 2];

        :TRY;
            bExists := DocExistsUser(sLoginName, sUserName);
            AAdd(aResults, {sLoginName, sUserName, bExists, "OK"});

        :CATCH;
            oErr := GetLastSSLError();
            AAdd(aResults, {sLoginName, sUserName, .F., oErr:Description});
        :ENDTRY;
    :NEXT;

    :RETURN aResults;
:ENDPROC;

/* Usage;
DoProc("AuditDocUsers", {{{"admin", "jsmith"}, {"admin", "mwilson"}}});
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
