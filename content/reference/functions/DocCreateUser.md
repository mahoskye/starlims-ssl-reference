---
title: "DocCreateUser"
summary: "Creates a new user account and returns its identifier."
id: ssl.function.doccreateuser
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocCreateUser

Creates a new user account and returns its identifier.

`DocCreateUser` requires `sLoginName` and `sPassword`, then optionally accepts `sUserName`, `sEmail`, `sDefaultFolder`, `sGroupName`, `sPermissionSet`, and `nUserPrivileges`. If `sLoginName` or `sPassword` is [`NIL`](../literals/nil.md), the function raises an error before attempting creation. Optional string arguments can be omitted, and `nUserPrivileges` defaults to `0` when omitted. On success, the function returns the created user identifier as a string. If the create operation does not return a value, the function returns an empty string.

## When to use

- When automating user provisioning and you need to create accounts from SSL.
- When a workflow must assign user profile or access settings during account creation.
- When later steps need the created user's identifier.

## Syntax

```ssl
DocCreateUser(
    sLoginName,
    sPassword,
    [sUserName],
    [sEmail],
    [sDefaultFolder],
    [sGroupName],
    [sPermissionSet],
    [nUserPrivileges]
)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sLoginName` | [string](../types/string.md) | yes | — | Login name for the new user account |
| `sPassword` | [string](../types/string.md) | yes | — | Password for the new user account |
| `sUserName` | [string](../types/string.md) | no | omitted | Display name for the new user account |
| `sEmail` | [string](../types/string.md) | no | omitted | Email address for the new user account |
| `sDefaultFolder` | [string](../types/string.md) | no | omitted | Default folder for the new user |
| `sGroupName` | [string](../types/string.md) | no | omitted | Group name to assign to the user |
| `sPermissionSet` | [string](../types/string.md) | no | omitted | Permission set to assign to the user |
| `nUserPrivileges` | [number](../types/number.md) | no | `0` | Numeric privilege value for the new user |

## Returns

**[string](../types/string.md)** — The created user identifier, or an empty string when the create operation does not return a value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sLoginName` is [`NIL`](../literals/nil.md). | `sLoginName argument cannot be null` |
| `sPassword` is [`NIL`](../literals/nil.md). | `sPassword argument cannot be null` |

## Best practices

!!! success "Do"
    - Validate that `sLoginName` and `sPassword` are assigned before calling the
      function.
    - Pass optional attributes during creation when the account needs folder,
      group, permission, or privilege settings immediately.
    - Check whether the returned identifier is empty before treating the create
      operation as successful.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sLoginName` or `sPassword`. Those arguments raise an immediate error instead of creating the user.
    - Assume omitted optional arguments will automatically produce the profile, folder, group, or permission settings you want.
    - Treat the call as successful without checking the returned identifier.

## Caveats

- Omitting `nUserPrivileges`, or passing [`NIL`](../literals/nil.md), uses `0`.

## Examples

### Create a user with required credentials only

Creates a Documentum user account with only a login name and password and displays the returned identifier or an error when the result is empty.

```ssl
:PROCEDURE CreateBasicUser;
    :DECLARE sLoginName, sPassword, sUserId;

    sLoginName := "jsmith";
    sPassword := "SecureP@ss123";

    sUserId := DocCreateUser(sLoginName, sPassword);

    :IF Empty(sUserId);
        ErrorMes("DocCreateUser did not return a user identifier");
        :RETURN "";
    :ENDIF;

    UsrMes("Created user ID: " + sUserId);
    /* Displays the created user ID on success;

    :RETURN sUserId;
:ENDPROC;

/* Usage;
DoProc("CreateBasicUser");
```

### Create a user with profile and access settings

Creates a full user account by passing all eight arguments: login name, password, display name, email, default folder, group, permission set, and privilege level.

```ssl
:PROCEDURE CreateLabTechUser;
    :DECLARE sLoginName, sPassword, sUserName, sEmail, sDefaultFolder;
    :DECLARE sGroupName, sPermissionSet, nUserPrivileges, sUserId;

    sLoginName := "labtech_jsmith";
    sPassword := "SecureP@ss123";
    sUserName := "John Smith";
    sEmail := "j.smith@lab.example.com";
    sDefaultFolder := "/Laboratory/Technicians";
    sGroupName := "LabTechnicians";
    sPermissionSet := "TechnicianReadWrite";
    nUserPrivileges := 0;

    sUserId := DocCreateUser(
        sLoginName,
        sPassword,
        sUserName,
        sEmail,
        sDefaultFolder,
        sGroupName,
        sPermissionSet,
        nUserPrivileges
    );

    :IF Empty(sUserId);
        ErrorMes(
            "User creation returned an empty identifier for " + sLoginName
        );
        /* Displays a failure message for the requested login;
        :RETURN "";
    :ENDIF;

    UsrMes("Created user " + sUserName + " with ID " + sUserId);
    /* Displays the created user name and ID on success;

    :RETURN sUserId;
:ENDPROC;

/* Usage;
DoProc("CreateLabTechUser");
```

### Catch null-argument errors and check for an empty result

Wraps the call in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) to handle a [`NIL`](../literals/nil.md)-argument exception and also guards against an empty identifier result to cover both failure paths.

```ssl
:PROCEDURE CreateUserWithHandling;
    :DECLARE sLoginName, sPassword, sUserId, oErr;

    sLoginName := "testuser";
    sPassword := "SecureP@ss123";

    :TRY;
        sUserId := DocCreateUser(sLoginName, sPassword);

        :IF Empty(sUserId);
            ErrorMes(
                "DocCreateUser returned an empty identifier for "
                + sLoginName
            );
            /* Displays a failure message when no identifier is returned;
            :RETURN "";
        :ENDIF;

        UsrMes("Created user ID: " + sUserId);
        /* Displays the created user ID on success;
        :RETURN sUserId;
    :CATCH;
        oErr := GetLastSSLError();

        :IF Empty(oErr);
            ErrorMes("DocCreateUser failed for " + sLoginName);
            /* Displays a generic failure message for the login;
        :ELSE;
            ErrorMes("DocCreateUser failed: " + oErr:Description);
            /* Displays the failure details returned by SSL;
        :ENDIF;

        :RETURN "";
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("CreateUserWithHandling");
```

## Related

- [`DocExistsUser`](DocExistsUser.md)
- [`DocUpdateUser`](DocUpdateUser.md)
- [`DocDeleteUser`](DocDeleteUser.md)
- [`GetLastSSLError`](GetLastSSLError.md)
- [`string`](../types/string.md)
- [`number`](../types/number.md)
