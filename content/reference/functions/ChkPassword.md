---
title: "ChkPassword"
summary: "Checks whether a user name and password combination is accepted."
id: ssl.function.chkpassword
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ChkPassword

Checks whether a user name and password combination is accepted.

`ChkPassword` returns [`.T.`](../literals/true.md) when the supplied credentials are accepted and [`.F.`](../literals/false.md) otherwise. If `sUserName` is [`NIL`](../literals/nil.md), the function uses the current session user. If `sPassword` is [`NIL`](../literals/nil.md), the function treats it as `""`.

When `sUserName` contains a backslash, such as `DOMAIN\user`, the function first tries Windows authentication with that domain-qualified name. If that check does not succeed, the function then continues with the application password check for the user name portion after the backslash.

For application passwords, the function accepts either the current stored password hash or an older salted password format. If the legacy salted value matches, the function updates the stored password through [`SetUserPassword`](SetUserPassword.md) and still returns [`.T.`](../literals/true.md).

## When to use

- When you need to verify credentials before allowing a sensitive action.
- When you need to re-authenticate the current user before changing account data.
- When your script accepts either standard application credentials or `DOMAIN\user` style input.

## Syntax

```ssl
ChkPassword([sUserName], [sPassword])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sUserName` | [string](../types/string.md) | no | current session user | User name to validate. If [`NIL`](../literals/nil.md), the function uses the current session user. If the value contains `\`, the function first attempts Windows authentication and then falls back to the user name portion for the application password check if needed. |
| `sPassword` | [string](../types/string.md) | no | `""` | Password to validate. If [`NIL`](../literals/nil.md), the function uses an empty string. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the credentials are accepted; otherwise [`.F.`](../literals/false.md).

## Best practices

!!! success "Do"
    - Pass `sUserName` and `sPassword` explicitly when you are validating user-entered credentials.
    - Check the boolean result and handle failure without assuming the reason.
    - Use [`ChkNewPassword`](ChkNewPassword.md) for password-history checks and [`SetUserPassword`](SetUserPassword.md) only after re-authentication succeeds.

!!! failure "Don't"
    - Rely on the implicit current-user fallback unless that behavior is intentional.
    - Assume [`.F.`](../literals/false.md) means the user record does not exist. It only means the supplied credentials were not accepted.
    - Use `ChkPassword` as a password-policy or password-strength check.

## Caveats

- `ChkPassword` returns only [`.T.`](../literals/true.md) or [`.F.`](../literals/false.md). It does not report why a check failed.
- For `DOMAIN\user` input, a failed Windows authentication attempt does not stop processing; the function then continues with the application password check for `user`.
- A successful match against the older salted password format updates the stored password value before returning [`.T.`](../literals/true.md).

## Examples

### Validate credentials from a login form

Validates a user name and password passed as procedure parameters and displays an accepted or rejected message based on the result.

```ssl
:PROCEDURE ValidateLogin;
	:PARAMETERS sUserName, sPassword;
	:DECLARE bIsValid, sMessage;

	bIsValid := ChkPassword(sUserName, sPassword);

	:IF bIsValid;
		sMessage := "Credentials accepted for " + sUserName;
	:ELSE;
		sMessage := "Credentials were not accepted for " + sUserName;
	:ENDIF;

	UsrMes(sMessage);

	:RETURN bIsValid;
:ENDPROC;

/* Usage;
DoProc("ValidateLogin", {"jsmith", "SecurePass123"});
```

[`UsrMes`](UsrMes.md) displays one of:

```text
Credentials accepted for jsmith
```

```text
Credentials were not accepted for jsmith
```

### Re-authenticate the current session user

Passes [`NIL`](../literals/nil.md) for `sUserName` so `ChkPassword` uses the current session user from [`GetUserData`](GetUserData.md), and displays the result.

```ssl
:PROCEDURE ConfirmCurrentUser;
	:PARAMETERS sPassword;
	:DECLARE bConfirmed, sUserName;

	sUserName := GetUserData();
	bConfirmed := ChkPassword(NIL, sPassword);

	:IF bConfirmed;
		UsrMes("Re-authentication succeeded for " + sUserName);
	:ELSE;
		UsrMes("Re-authentication failed for " + sUserName);
	:ENDIF;

	:RETURN bConfirmed;
:ENDPROC;

/* Usage;
DoProc("ConfirmCurrentUser", {"SecurePass123"});
```

[`UsrMes`](UsrMes.md) displays one of:

```text
Re-authentication succeeded for jsmith
```

```text
Re-authentication failed for jsmith
```

### Accept domain-qualified or application credentials

Accepts either a `DOMAIN\user` name or a plain application user name, then calls [`SetUserPassword`](SetUserPassword.md) only when the credential check succeeds.

```ssl
:PROCEDURE ChangePasswordAfterCheck;
	:PARAMETERS sUserName, sCurrentPassword, sNewPassword;
	:DECLARE bAuthenticated, sStoredHash;

	bAuthenticated := ChkPassword(sUserName, sCurrentPassword);

	:IF !bAuthenticated;
		UsrMes("Current credentials were not accepted.");
		:RETURN "";
	:ENDIF;

	sStoredHash := SetUserPassword(sUserName, sNewPassword);

	:IF Empty(sStoredHash);
		ErrorMes("Password update did not complete.");
		:RETURN "";
	:ENDIF;

	UsrMes("Password updated successfully for " + sUserName);

	:RETURN sStoredHash;
:ENDPROC;

/* Usage;
DoProc("ChangePasswordAfterCheck", {"jsmith", "OldPass123", "NewSecurePass!"});
```

[`UsrMes`](UsrMes.md) or [`ErrorMes`](ErrorMes.md) displays one of:

```text
Current credentials were not accepted.
```

```text
Password update did not complete.
```

```text
Password updated successfully for jsmith
```

## Related

- [`ChkNewPassword`](ChkNewPassword.md)
- [`GetUserData`](GetUserData.md)
- [`SetUserPassword`](SetUserPassword.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
