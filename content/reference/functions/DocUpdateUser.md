---
title: "DocUpdateUser"
summary: "Updates a Documentum user and returns the backend result message."
id: ssl.function.docupdateuser
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocUpdateUser

Updates a Documentum user and returns the backend result message.

`DocUpdateUser` requires `sLoginName` and `sPassword`, then optionally accepts `sUserName`, `sEMail`, `sDefaultFolder`, `sGroupName`, `sPermissionSet`, and `nUserPrivileges`. If `sLoginName` or `sPassword` is [`NIL`](../literals/nil.md), the function raises an error before attempting the update. If `nUserPrivileges` is omitted or [`NIL`](../literals/nil.md), the function uses `0`. The function returns the backend string result, or an empty string when the update path does not return a value.

## When to use

- When an SSL script needs to submit updated Documentum user details.
- When a workflow needs the backend result message after an update attempt.
- When the update should include an explicit privilege value instead of the default `0`.

## Syntax

```ssl
DocUpdateUser(sLoginName, sPassword, [sUserName], [sEMail], [sDefaultFolder], [sGroupName], [sPermissionSet], [nUserPrivileges])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sLoginName` | [string](../types/string.md) | yes | — | Login name of the Documentum user to update |
| `sPassword` | [string](../types/string.md) | yes | — | Password supplied for the update call |
| `sUserName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | User name value to pass to the update call |
| `sEMail` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Email value to pass to the update call |
| `sDefaultFolder` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Default folder value to pass to the update call |
| `sGroupName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Group name value to pass to the update call |
| `sPermissionSet` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Permission set value to pass to the update call |
| `nUserPrivileges` | [number](../types/number.md) | no | `0` | Numeric privilege value to pass to the update call |

## Returns

**[string](../types/string.md)** — The backend result message, or an empty string when the update path does not return a value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sLoginName` is [`NIL`](../literals/nil.md). | `sLoginName argument cannot be null` |
| `sPassword` is [`NIL`](../literals/nil.md). | `sPassword argument cannot be null` |

## Best practices

!!! success "Do"
    - Validate that `sLoginName` and `sPassword` are assigned before calling the function.
    - Omit trailing optional arguments you do not need, and skip only the positions required to reach a later argument.
    - Check whether the returned string is empty before treating the update as confirmed.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sLoginName` or `sPassword`. Those arguments raise an immediate error instead of attempting the update.
    - Assume omitted optional arguments have a documented repository-side effect beyond being forwarded as omitted values.
    - Ignore an empty return string when later logic depends on a confirmed update result.

## Examples

### Update a user's display name and email

Passes only the required credentials plus display name and email, then displays the backend result string.

```ssl
:PROCEDURE UpdateUserContact;
    :DECLARE sLoginName, sPassword, sUserName, sEMail, sResult;

    sLoginName := "jsmith";
    sPassword := "SecureP@ss123";
    sUserName := "John Smith";
    sEMail := "john.smith@example.com";

    sResult := DocUpdateUser(sLoginName, sPassword, sUserName, sEMail);

    :IF Empty(sResult);
        UsrMes("DocUpdateUser returned an empty result for " + sLoginName);
        :RETURN "";
    :ENDIF;

    UsrMes(sResult);
    /* Displays backend result message on success;

    :RETURN sResult;
:ENDPROC;

/* Usage;
DoProc("UpdateUserContact");
```

### Update folder, group, and permission set by skipping optional positions

Skips the `sUserName` and `sEMail` positions using adjacent commas so that only the folder, group, and permission set are updated.

```ssl
:PROCEDURE UpdateUserAccess;
    :DECLARE sLoginName, sPassword, sDefaultFolder, sGroupName;
    :DECLARE sPermissionSet, sResult;

    sLoginName := "jsmith";
    sPassword := "SecureP@ss123";
    sDefaultFolder := "/Documentum/LabUsers";
    sGroupName := "LabUsers";
    sPermissionSet := "LabUserWrite";

    sResult := DocUpdateUser(
        sLoginName,
        sPassword,,,
        sDefaultFolder,
        sGroupName,
        sPermissionSet
    );

    :IF Empty(sResult);
        ErrorMes("DocUpdateUser returned an empty result for " + sLoginName);
        :RETURN "";
    :ENDIF;

    UsrMes(sResult);
    /* Displays backend result message on success;

    :RETURN sResult;
:ENDPROC;

/* Usage;
DoProc("UpdateUserAccess");
```

### Update all fields with error handling

Passes all eight arguments and wraps the call in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) to handle SSL exceptions, using [`GetLastSSLError`](GetLastSSLError.md) to extract the failure description.

```ssl
:PROCEDURE UpdateUserWithHandling;
    :DECLARE sLoginName, sPassword, sUserName, sEMail, sDefaultFolder;
    :DECLARE sGroupName, sPermissionSet, nUserPrivileges, sResult, oErr;

    sLoginName := "labadmin";
    sPassword := "SecureP@ss123";
    sUserName := "Laboratory Administrator";
    sEMail := "labadmin@example.com";
    sDefaultFolder := "/Documentum/Admin";
    sGroupName := "DocAdmins";
    sPermissionSet := "AdminFull";
    nUserPrivileges := 5;

    :TRY;
        sResult := DocUpdateUser(
            sLoginName,
            sPassword,
            sUserName,
            sEMail,
            sDefaultFolder,
            sGroupName,
            sPermissionSet,
            nUserPrivileges
        );

        :IF Empty(sResult);
            ErrorMes("DocUpdateUser returned an empty result for " + sLoginName);
            :RETURN "";
        :ENDIF;

        UsrMes(sResult);
        /* Displays backend result message on success;

        :RETURN sResult;
    :CATCH;
        oErr := GetLastSSLError();

        :IF Empty(oErr);
            ErrorMes("DocUpdateUser failed for " + sLoginName);
        :ELSE;
            ErrorMes("DocUpdateUser failed: " + oErr:Description);
            /* Displays failure details when available;
        :ENDIF;

        :RETURN "";
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("UpdateUserWithHandling");
```

## Related

- [`DocCreateUser`](DocCreateUser.md)
- [`DocDeleteUser`](DocDeleteUser.md)
- [`DocExistsUser`](DocExistsUser.md)
- [`GetLastSSLError`](GetLastSSLError.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
