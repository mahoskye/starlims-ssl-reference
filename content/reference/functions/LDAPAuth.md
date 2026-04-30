---
title: "LDAPAuth"
summary: "Authenticates a user by binding directly to an LDAP server."
id: ssl.function.ldapauth
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LDAPAuth

Authenticates a user by binding directly to an LDAP server.

`LDAPAuth` opens an LDAP connection to the specified host and port, optionally enables SSL/TLS, and attempts to bind with the supplied user name and password. On success it returns an empty string. On failure it raises an exception instead of returning a status code.

If `nLdapPort` is omitted, the function uses `389`. If `bSecure` is omitted, it uses [`.F.`](../literals/false.md). When `sLdapDistinctiveName` is `"ntlm"` (case-insensitive), the bind switches to NTLM authentication.

## When to use

- When you already know the user name to bind with and only need to validate the credentials.
- When you need a direct LDAP bind instead of first searching for a distinguished name.
- When you want a simple success-or-exception authentication flow in SSL code.

## Syntax

```ssl
LDAPAuth(sLdapHost, [nLdapPort], sLdapUserName, [sLdapPassword], [sLdapDistinctiveName], [bSecure])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sLdapHost` | [string](../types/string.md) | yes | — | LDAP server host name or address |
| `nLdapPort` | [number](../types/number.md) | no | `389` | LDAP server port |
| `sLdapUserName` | [string](../types/string.md) | yes | — | User name passed to the bind operation |
| `sLdapPassword` | [string](../types/string.md) | no | `""` | Password passed to the bind operation. An empty password raises an exception. |
| `sLdapDistinctiveName` | [string](../types/string.md) | no | `""` | Special authentication mode selector. Use `"ntlm"` to perform an NTLM bind. |
| `bSecure` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | When [`.T.`](../literals/true.md), enables SSL/TLS on the LDAP connection |

## Returns

**[string](../types/string.md)** — Returns `""` when the bind succeeds.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sLdapHost` or `sLdapUserName` is empty. | `The parameters are not correct.(sLdapHost or sLdapUserName are null)` |
| `sLdapPassword` is empty. | `The password cannot be null` |
| The LDAP bind fails with an LDAP error. | `Error occurred :\nBinding operation for user : {sLdapUserName} failed with error : \n{message}` |
| The LDAP bind fails with a general error. | `Exception :\nBinding operation for user : {sLdapUserName} failed with error : \n{message}` |
| Connection creation fails. | `Error connecting to the server : {sLdapHost} \n{message}` |

## Best practices

!!! success "Do"
    - Validate `sLdapHost`, `sLdapUserName`, and `sLdapPassword` before calling the function so failures are easier to explain to users.
    - Use `bSecure` with the correct LDAPS port when the directory requires encrypted binds.
    - Treat an empty return value as success and handle failures in [`:CATCH`](../keywords/CATCH.md) by reading `GetLastSSLError():Description`.

!!! failure "Don't"
    - Treat the return value as a boolean or status code. This function succeeds with `""` and raises exceptions on errors.
    - Omit `sLdapPassword` for a normal bind. An empty password triggers `The password cannot be null`.
    - Pass `sLdapDistinctiveName` unless you intentionally need the NTLM mode switch. Other behavior is not implemented here.

## Caveats

- This function performs a direct bind only. It does not search LDAP to discover a user DN first.
- `sLdapDistinctiveName` is only checked for the value `"ntlm"` in a case-insensitive comparison.
- The function always disposes the LDAP connection before returning or propagating an exception.

## Examples

### Validate credentials with the default port

Authenticate a user with the default LDAP port and treat an empty result as success.

```ssl
:PROCEDURE ValidateLdapUser;
	:PARAMETERS sLdapHost, sUserName, sPassword;
	:DECLARE sResult, oErr;

	:TRY;
		sResult := LDAPAuth(sLdapHost,,sUserName,sPassword);

		:IF Empty(sResult);
			UsrMes("LDAP authentication succeeded");
			:RETURN .T.;
		:ENDIF;

		:RETURN .F.;
	:CATCH;
		oErr := GetLastSSLError();
		/* Displays on failure: LDAP authentication failed;
		UsrMes("LDAP authentication failed: " + oErr:Description);
		:RETURN .F.;
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ValidateLdapUser", {"ldap.example.com", "jsmith", "user-secret"});
```

### Use LDAPS on a custom port

Authenticate over SSL/TLS by supplying both the LDAPS port and the `bSecure` flag.

```ssl
:PROCEDURE ValidateSecureLdapUser;
	:PARAMETERS sUserName, sPassword;
	:DECLARE sLdapHost, nLdapPort, sResult, oErr;

	sLdapHost := "ldap.corp.example.com";
	nLdapPort := 636;

	:TRY;
		sResult := LDAPAuth(sLdapHost, nLdapPort, sUserName, sPassword,,.T.);

		:IF Empty(sResult);
			UsrMes("Secure LDAP authentication succeeded");
			:RETURN .T.;
		:ENDIF;

		:RETURN .F.;
	:CATCH;
		oErr := GetLastSSLError();
		/* Displays on failure: Secure LDAP authentication failed;
		UsrMes("Secure LDAP authentication failed: " + oErr:Description);
		:RETURN .F.;
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ValidateSecureLdapUser", {"jsmith", "user-secret"});
```

### Authenticate with NTLM mode and explicit input checks

Validate required inputs up front and request NTLM authentication explicitly.

```ssl
:PROCEDURE ValidateNtlmLdapUser;
	:PARAMETERS sLdapHost, sUserName, sPassword;
	:DECLARE sResult, oErr;

	:IF Empty(sLdapHost) .OR. Empty(sUserName) .OR. Empty(sPassword);
		UsrMes("LDAP host, user name, and password are required");
		:RETURN .F.;
	:ENDIF;

	:TRY;
		sResult := LDAPAuth(sLdapHost,,sUserName,sPassword,"ntlm");

		:IF Empty(sResult);
			UsrMes("NTLM LDAP authentication succeeded");
			:RETURN .T.;
		:ENDIF;

		:RETURN .F.;
	:CATCH;
		oErr := GetLastSSLError();
		/* Displays on failure: NTLM LDAP authentication failed;
		UsrMes("NTLM LDAP authentication failed: " + oErr:Description);
		:RETURN .F.;
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ValidateNtlmLdapUser", {"ldap.corp.example.com", "jsmith", "user-secret"});
```

## Related

- [`LDAPAuthEX`](LDAPAuthEX.md)
- [`SearchLDAPUser`](SearchLDAPUser.md)
- [`string`](../types/string.md)
- [`boolean`](../types/boolean.md)
