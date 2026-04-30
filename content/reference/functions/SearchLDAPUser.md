---
title: "SearchLDAPUser"
summary: "Searches LDAP for exactly one user and returns that entry's distinguished name."
id: ssl.function.searchldapuser
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SearchLDAPUser

Searches LDAP for exactly one user and returns that entry's distinguished name.

`SearchLDAPUser` connects to the specified LDAP server, binds with the supplied bind account, runs a subtree search starting at `sLdapDistinguishedNameStartSearch`, and returns the distinguished name of the single matching entry. If `nLdapPort` is omitted it defaults to `389`. If `sSearchFilter` is omitted or empty, the function uses `(&(objectClass=user)(name={0}))`. If `bSecure` is omitted it defaults to [`.F.`](../literals/false.md).

The function requires a non-empty LDAP host and bind username. The bind password is accepted as an argument, but an empty password still causes the bind step to fail. The search must return exactly one entry; zero matches, multiple matches, bind failures, connection failures, and invalid search input all raise errors.

## When to use

- When you need a user's distinguished name before calling another LDAP or application workflow.
- When you want the built-in LDAP search to enforce a single-match result.
- When you need to search from a known base DN with either the default user-name filter or a custom filter pattern.

## Syntax

```ssl
SearchLDAPUser(sLdapHost, [nLdapPort], sBindUserName, [sBindUserPassword], [sSearchUserName], sLdapDistinguishedNameStartSearch, [sSearchFilter], [bSecure])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sLdapHost` | [string](../types/string.md) | yes | — | LDAP server host name. Empty values raise an exception. |
| `nLdapPort` | [number](../types/number.md) | no | `389` | LDAP server port. |
| `sBindUserName` | [string](../types/string.md) | yes | — | User name used for the LDAP bind step. Empty values raise an exception. |
| `sBindUserPassword` | [string](../types/string.md) | no | `""` | Password used for the LDAP bind step. Omitting it passes an empty string, and the bind fails because an empty password is rejected. |
| `sSearchUserName` | [string](../types/string.md) | no | `""` | User name inserted into the search filter. With the default filter, an empty value produces `(&(objectClass=user)(name=))`, which typically returns no matches. |
| `sLdapDistinguishedNameStartSearch` | [string](../types/string.md) | yes | — | Base distinguished name where the subtree search starts. |
| `sSearchFilter` | [string](../types/string.md) | no | `(&(objectClass=user)(name={0}))` | Filter pattern used for the LDAP search. When a custom filter is supplied, the function formats it with `sSearchUserName` before sending the request. |
| `bSecure` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Enables SSL/TLS on the LDAP connection when [`.T.`](../literals/true.md). |

## Returns

**[string](../types/string.md)** — Distinguished name of the single matching LDAP entry.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sLdapHost` or `sBindUserName` is empty. | `The parameters are not correct.(sLdapHost or sBindUserName are null)` |
| `sBindUserPassword` is empty. | `The password cannot be null` |
| The bind operation fails with an LDAP error. | `Error occurred :\nBinding operation for user : {sBindUserName} failed with error : \n{message}` |
| The bind operation fails with a general error. | `Exception :\nBinding operation for user : {sBindUserName} failed with error : \n{message}` |
| The connection to the LDAP server fails. | `Error connecting to the server : {sLdapHost} \n{message}` |
| `sLdapDistinguishedNameStartSearch` is empty. | `The variable ldapDistinguishedNameStartSearch is empty. The 'DN start search' value is mandatory!` |
| The LDAP search itself fails. | `Error : searching for: {sSearchUserName}; start search location: {sLdapDistinguishedNameStartSearch} filter: {sSearchFilter}\nreturned an error: \n{message}` |
| The search returns zero or more than one entry. | `The search returned : {count} entries for the search filter : {resolvedFilter}` |
| The matched entry's DN cannot be read. | `Cannot extract the DN from the search response for the search filter : {sSearchFilter}` |

## Best practices

!!! success "Do"
    - Pass a dedicated bind account with a real password and enough rights to search the target branch.
    - Start from the narrowest practical base DN so the search is more likely to return exactly one entry.
    - Use a custom `sSearchFilter` only when you need a different attribute match, and keep it compatible with `string.Format` substitution.

!!! failure "Don't"
    - Treat `sBindUserPassword` as safely optional in practice. Omitting it passes an empty string and the bind fails.
    - Use an overly broad filter or base DN when you need one user. The function raises an error unless the search returns exactly one entry.
    - Assume `sSearchUserName` is validated for you. An empty value can still run through the search path and usually ends in a zero-results error.

## Caveats

- Custom filters are formatted with `sSearchUserName` before execution. If your filter does not contain a `{0}` placeholder, the supplied `sSearchUserName` is ignored by the filter string itself.
- The function always performs a subtree search from the starting DN.

## Examples

### Look up a user with the default filter

Use the built-in default filter and handle lookup failures explicitly.

```ssl
:PROCEDURE GetUserDn;
    :DECLARE sLdapHost, nLdapPort, sBindUserName, sBindUserPassword;
    :DECLARE sSearchUserName, sBaseDn, sUserDn, oErr;

    sLdapHost := "ldap.example.com";
    nLdapPort := 389;
    sBindUserName := "svc_ldap_lookup";
    sBindUserPassword := "SecretPassword";
    sSearchUserName := "jsmith";
    sBaseDn := "OU=Users,DC=example,DC=com";

    :TRY;
        sUserDn := SearchLDAPUser(
            sLdapHost,
            nLdapPort,
            sBindUserName,
            sBindUserPassword,
            sSearchUserName,
            sBaseDn
        );

        /* Displays the resolved distinguished name;
        UsrMes("Found DN: " + sUserDn);
    :CATCH;
        oErr := GetLastSSLError();
        /* Displays the lookup failure reason;
        ErrorMes("LDAP lookup failed: " + oErr:Description);
    :ENDTRY;
:ENDPROC;
```

Call with `DoProc("GetUserDn")`.

### Search by a different LDAP attribute

Supply a custom filter pattern when the account name is stored in a different attribute.

```ssl
:PROCEDURE GetUserDnBySamAccountName;
    :DECLARE sUserDn, sFilter;

    sFilter := "(&(objectClass=user)(sAMAccountName={0}))";

    sUserDn := SearchLDAPUser(
        "ldap.example.com",
        389,
        "svc_ldap_lookup",
        "SecretPassword",
        "jsmith",
        "OU=Users,DC=example,DC=com",
        sFilter,
        .F.
    );

    UsrMes("Found DN: " + sUserDn);
:ENDPROC;
```

Call with `DoProc("GetUserDnBySamAccountName")`.

[`UsrMes`](UsrMes.md) displays:

```text
Found DN: <distinguished name>
```

### Resolve the DN and store it for later workflow steps

Use `SearchLDAPUser` as the lookup step in a larger workflow, then persist the result.

```ssl
:PROCEDURE ResolveAndStoreUserDn;
    :PARAMETERS sSearchUserName;
    :DECLARE sLdapHost, nLdapPort, sBindUserName, sBindUserPassword;
    :DECLARE sBaseDn, sUserDn, oErr, bUpdated;

    sLdapHost := "ldap.example.com";
    nLdapPort := 389;
    sBindUserName := "svc_ldap_lookup";
    sBindUserPassword := "SecretPassword";
    sBaseDn := "OU=Users,DC=example,DC=com";

    :TRY;
        sUserDn := SearchLDAPUser(
            sLdapHost,
            nLdapPort,
            sBindUserName,
            sBindUserPassword,
            sSearchUserName,
            sBaseDn,
            "(&(objectClass=user)(sAMAccountName={0}))",
            .F.
        );

        bUpdated := RunSQL("
            UPDATE lims_user_profile SET
                ldap_dn = ?
            WHERE username = ?
        ",, {sUserDn, sSearchUserName});

        :IF bUpdated;
            /* Displays the successful update target;
            UsrMes("Stored LDAP DN for " + sSearchUserName);
        :ELSE;
            /* Displays the user name that could not be stored;
            ErrorMes("Could not store LDAP DN for " + sSearchUserName);
        :ENDIF;
    :CATCH;
        oErr := GetLastSSLError();
        /* Displays the workflow failure reason;
        ErrorMes("LDAP workflow failed: " + oErr:Description);
    :ENDTRY;
:ENDPROC;
```

Call with `DoProc("ResolveAndStoreUserDn", {"jsmith"})`.

## Related

- [`LDAPAuth`](LDAPAuth.md)
- [`LDAPAuthEX`](LDAPAuthEX.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
