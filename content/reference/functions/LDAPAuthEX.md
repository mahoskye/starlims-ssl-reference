---
title: "LDAPAuthEX"
summary: "Authenticates an LDAP user by searching for exactly one directory entry and then binding as that user."
id: ssl.function.ldapauthex
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LDAPAuthEX

Authenticates an LDAP user by searching for exactly one directory entry and then binding as that user.

`LDAPAuthEX` first binds with the supplied service account, searches from `sLdapDistinguishedNameStartSearch` using a filter pattern, and then binds again with the matched entry's distinguished name and `sSearchUserPassword`. If authentication succeeds, the function returns the requested attribute value or values from the matched entry. If `sAuthAttribName` is omitted or empty, the function returns an empty string after successful authentication. When multiple attribute names are requested, the result is a comma-delimited string in the same order as `sAuthAttribName`. Missing attributes become empty slots in that string. Connection, bind, search, and validation failures raise exceptions.

## When to use

- When using a service (bind) account is required to search and authenticate users in a directory.
- When you need to retrieve one or more LDAP attributes after a successful authentication.
- When connecting to LDAP servers that require SSL.
- When user records are stored below a known search base and require a custom LDAP filter.

## Syntax

```ssl
LDAPAuthEX(sLdapHost, [nLdapPort], sBindUserName, sBindUserPassword, [sSearchUserName], sSearchUserPassword, [sLdapDistinguishedName], sLdapDistinguishedNameStartSearch, [sSearchFilter], [sAuthAttribName], [bSecure])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sLdapHost` | [string](../types/string.md) | yes | — | LDAP server host name. |
| `nLdapPort` | [number](../types/number.md) | no | `389` | LDAP server port. |
| `sBindUserName` | [string](../types/string.md) | yes | — | Service-account username used for the initial bind and search. |
| `sBindUserPassword` | [string](../types/string.md) | yes | — | Password for `sBindUserName`. Empty or omitted values cause the bind step to fail. |
| `sSearchUserName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | User identifier inserted into `sSearchFilter` with `string.Format(sSearchFilter, sSearchUserName)`. In normal usage this is the user being authenticated. |
| `sSearchUserPassword` | [string](../types/string.md) | yes | — | Password used in the second bind against the matched entry. Empty or omitted values cause authentication to fail. |
| `sLdapDistinguishedName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Accepted in the signature but has no effect on the search or bind behavior. |
| `sLdapDistinguishedNameStartSearch` | [string](../types/string.md) | yes | — | Distinguished name that defines where the LDAP search begins. |
| `sSearchFilter` | [string](../types/string.md) | no | `(&(objectClass=user)(name={0}))` | LDAP filter pattern. When supplied, it is formatted with `sSearchUserName`. The search must return exactly one entry. |
| `sAuthAttribName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Attribute name to return after successful authentication. Supply multiple names separated by commas to return multiple values in order. |
| `bSecure` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | When [`.T.`](../literals/true.md), enables SSL for the LDAP connection. |

## Returns

**[string](../types/string.md)** — Returns an empty string when `sAuthAttribName` is omitted or empty and authentication succeeds. Returns the requested attribute value when one attribute name is supplied. Returns a comma-delimited string when multiple attribute names are supplied. The function raises on authentication, bind, connection, or search failure; it does not return an error string for failed authentication.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sLdapHost` or `sBindUserName` is empty. | `The parameters are not correct.(sLdapHost or sBindUserName are null)` |
| The bind operation fails with an LDAP error. | `Error occurred :\nBinding operation for user : {sBindUserName} failed with error : \n{message}` |
| The bind operation fails with a general error. | `Exception :\nBinding operation for user : {sBindUserName} failed with error : \n{message}` |
| Connection creation fails. | `Error connecting to the server : {sLdapHost} \n{message}` |
| The LDAP search fails. | `Error : searching for: {sSearchUserName}; start search location: {sLdapDistinguishedNameStartSearch} filter: {sSearchFilter}\nreturned an error: \n{message}` |
| The search returns zero or multiple entries. | `The search returned : {count} entries for the search filter : {formattedFilter}` |
| The matched entry's DN cannot be read. | `Cannot extract the DN from the search response for the search filter : {sSearchFilter}` |
| Reading attribute values fails. | `Error reading the requested attributes {message}` |

## Best practices

!!! success "Do"
    - Use a search filter that resolves to exactly one entry for the supplied `sSearchUserName`.
    - Use [`.T.`](../literals/true.md) for `bSecure` and the appropriate LDAP SSL port when credentials must be protected in transit.
    - Omit `sAuthAttribName` when you only need an authentication check and no attribute value.
    - Request only the attributes you actually need, and keep their order stable if downstream code depends on the returned comma-delimited string.

!!! failure "Don't"
    - Rely on broad filters that can return more than one entry. The function raises unless the search finds exactly one match.
    - Pass empty passwords and expect the function to report a simple false result. Bind failures raise exceptions.
    - Assume `sLdapDistinguishedName` changes the search or bind behavior. It has no effect.
    - Request comma-containing attribute values if you need lossless multi-value parsing from the returned string. Multiple requested attributes are joined with literal commas and are not escaped.

## Caveats

- If `sSearchFilter` is omitted, the function uses `(&(objectClass=user)(name={0}))`.
- Custom filters are passed through `string.Format(sSearchFilter, sSearchUserName)`, so filters that use `{0}` are populated with `sSearchUserName` before the LDAP search runs.
- The search must return exactly one entry. Zero matches and multi-match results both raise exceptions.
- When one of the requested attributes is missing, its slot in the returned comma-delimited string is empty.
- When an attribute value itself contains commas, the returned multi-attribute string is ambiguous because values are joined without escaping.
- `sLdapDistinguishedName` is present in the signature but has no effect.

## Examples

### Authenticate without returning an attribute

Use `LDAPAuthEX` as an authentication check by leaving `sAuthAttribName` empty. A successful call returns `""`.

```ssl
:PROCEDURE AuthenticateOnly;
    :DECLARE sLdapHost, sBindUser, sBindPass, sUserName, sUserPass;
    :DECLARE sBaseDn, nLdapPort;

    sLdapHost := "ldap.example.com";
    nLdapPort := 389;
    sBindUser := "cn=svc_ldap,ou=service,dc=example,dc=com";
    sBindPass := "service-secret";
    sUserName := "jsmith";
    sUserPass := "user-secret";
    sBaseDn := "ou=users,dc=example,dc=com";

    LDAPAuthEX(
        sLdapHost,
        nLdapPort,
        sBindUser,
        sBindPass,
        sUserName,
        sUserPass,
        "",
        sBaseDn,
        "(&(objectClass=user)(sAMAccountName={0}))",
        "",
        .F.
    );

    UsrMes("LDAP authentication succeeded for " + sUserName);
:ENDPROC;

/* Usage;
DoProc("AuthenticateOnly");
```

[`UsrMes`](UsrMes.md) displays:

```text
LDAP authentication succeeded for jsmith
```

### Authenticate and read one attribute

Request a single attribute after successful authentication.

```ssl
:PROCEDURE AuthenticateAndReadMail;
    :DECLARE sLdapHost, sBindUser, sBindPass, sUserName, sUserPass;
    :DECLARE sBaseDn, sMail, nLdapPort;

    sLdapHost := "ldap.example.com";
    nLdapPort := 389;
    sBindUser := "cn=svc_ldap,ou=service,dc=example,dc=com";
    sBindPass := "service-secret";
    sUserName := "jsmith";
    sUserPass := "user-secret";
    sBaseDn := "ou=users,dc=example,dc=com";

    sMail := LDAPAuthEX(
        sLdapHost,
        nLdapPort,
        sBindUser,
        sBindPass,
        sUserName,
        sUserPass,
        "",
        sBaseDn,
        "(&(objectClass=user)(sAMAccountName={0}))",
        "mail",
        .F.
    );

    UsrMes("Authenticated mail address: " + sMail);
:ENDPROC;

/* Usage;
DoProc("AuthenticateAndReadMail");
```

[`UsrMes`](UsrMes.md) displays:

```text
Authenticated mail address: jsmith@example.com
```

### Handle LDAP failures and request multiple attributes

Use SSL, a narrower search base, and explicit exception handling when the search or bind may fail.

```ssl
:PROCEDURE AuthenticateWithErrorHandling;
    :DECLARE sLdapHost, sBindUser, sBindPass, sUserName, sUserPass;
    :DECLARE sBaseDn, sAttribValues, nLdapPort, oErr;

    sLdapHost := "ldap.example.com";
    nLdapPort := 636;
    sBindUser := "cn=svc_ldap,ou=service,dc=example,dc=com";
    sBindPass := "service-secret";
    sUserName := "jsmith";
    sUserPass := "user-secret";
    sBaseDn := "ou=research,dc=example,dc=com";

    :TRY;
        sAttribValues := LDAPAuthEX(
            sLdapHost,
            nLdapPort,
            sBindUser,
            sBindPass,
            sUserName,
            sUserPass,
            "",
            sBaseDn,
            "(&(objectClass=user)(sAMAccountName={0})(department=Research))",
            "mail,userPrincipalName",
            .T.
        );

        UsrMes("Authenticated attribute values: " + sAttribValues);
        /* Displays authenticated attribute values on success;
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("LDAP authentication failed: " + oErr:Description);
        /* Displays authentication failure details;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("AuthenticateWithErrorHandling");
```

## Related

- [`LDAPAuth`](LDAPAuth.md)
- [`SearchLDAPUser`](SearchLDAPUser.md)
- [`string`](../types/string.md)
