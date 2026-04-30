---
title: "SetUserPassword"
summary: "Updates a user's password and returns the stored password hash."
id: ssl.function.setuserpassword
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SetUserPassword

Updates a user's password and returns the stored password hash.

`SetUserPassword()` hashes `sPassword`, attempts to store the new value for `sUserName`, and returns the hash when the update succeeds. If the update does not succeed, the function returns `""`.

The function raises an exception when either argument is [`NIL`](../literals/nil.md). It does not reject empty strings, and it does not perform password-policy or password-history checks. When `sUserName` matches the current session user, the function also stores the new password in the session under `STARLIMSPass`.

## When to use

- When you need to complete a password reset or forced password-change flow.
- When you have already validated the caller and any password-policy rules.
- When you need the resulting stored hash after a successful password update.

## Syntax

```ssl
SetUserPassword(sUserName, sPassword)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sUserName` | [string](../types/string.md) | yes | — | User name whose password should be updated. Passing [`NIL`](../literals/nil.md) raises an exception. Empty string is allowed but typically results in `""` being returned because no user is updated. |
| `sPassword` | [string](../types/string.md) | yes | — | New password value to hash and store. Passing [`NIL`](../literals/nil.md) raises an exception. Empty string is allowed and is hashed as provided. |

## Returns

**[string](../types/string.md)** — The stored password hash when the update succeeds; otherwise `""`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sUserName` or `sPassword` is [`NIL`](../literals/nil.md). | `Password parameter cannot be null.` |

## Best practices

!!! success "Do"
    - Validate both arguments before calling, especially when empty strings are not acceptable in your workflow.
    - Use [`ChkPassword`](ChkPassword.md) to re-authenticate a user before changing an existing password.
    - Use [`ChkNewPassword`](ChkNewPassword.md) separately when you need password-history checks.
    - Check the return value and treat `""` as an update failure.

!!! failure "Don't"
    - Assume this function enforces password complexity, password history, or other policy rules.
    - Assume empty strings raise an exception. Only [`NIL`](../literals/nil.md) is rejected by the documented implementation.
    - Ignore the return value when the password change must be confirmed.
    - Expose the new password carelessly in current-user flows, because the session is updated when `sUserName` matches the active user.

## Caveats

- Both `sUserName` and `sPassword` throw the same exception message when [`NIL`](../literals/nil.md) is passed.

## Examples

### Set a password and confirm success

Update one user and confirm that the function returned a stored hash.

```ssl
:PROCEDURE ResetSingleUserPassword;
	:DECLARE sUserName, sNewPassword, sStoredHash;

	sUserName := "jsmith";
	sNewPassword := "N3wP@ss2024!";

	sStoredHash := SetUserPassword(sUserName, sNewPassword);

	:IF Empty(sStoredHash);
		ErrorMes("Password update did not complete for " + sUserName);
		/* Displays on failure: password update did not complete;
		:RETURN "";
	:ENDIF;

	UsrMes("Password updated for " + sUserName);
	/* Displays on success: password updated;

	:RETURN sStoredHash;
:ENDPROC;

/* Usage;
DoProc("ResetSingleUserPassword");
```

### Re-authenticate before changing a password

Require the current password to be correct before storing the new one.

```ssl
:PROCEDURE ChangePasswordAfterCheck;
	:PARAMETERS sUserName, sCurrentPassword, sNewPassword;
	:DECLARE bAuthenticated, sStoredHash;

	bAuthenticated := ChkPassword(sUserName, sCurrentPassword);

	:IF !bAuthenticated;
		ErrorMes("Current credentials were not accepted.");
		:RETURN "";
	:ENDIF;

	sStoredHash := SetUserPassword(sUserName, sNewPassword);

	:IF Empty(sStoredHash);
		ErrorMes("Password update did not complete.");
		:RETURN "";
	:ENDIF;

	UsrMes("Password updated successfully for " + sUserName);
	/* Displays on success: password updated successfully;

	:RETURN sStoredHash;
:ENDPROC;

/* Usage;
DoProc("ChangePasswordAfterCheck", {"jsmith", "CurrentPass!", "NewPass2026!"});
```

### Apply password-history checks in a reset loop

Process multiple requested resets, skipping values that already appear in each user's stored password history.

```ssl
:PROCEDURE ResetPasswordsWithHistoryCheck;
	:DECLARE aResetRequests, aHistoryByUser, nIndex;
	:DECLARE sUserName, sNewPassword, sStoredHash, aPrevPasswords;

	aResetRequests := {
		{"jsmith", "TempPass2026!"},
		{"adoe", "SpringReset88#"}
	};

	aHistoryByUser := {
		{"jsmith", {"Winter2025!", "Fall2025!"}},
		{"adoe", {"Legacy!23", "Older!77"}}
	};

	:FOR nIndex := 1 :TO ALen(aResetRequests);
		sUserName := aResetRequests[nIndex, 1];
		sNewPassword := aResetRequests[nIndex, 2];
		aPrevPasswords := aHistoryByUser[nIndex, 2];

		:IF !ChkNewPassword(sNewPassword, aPrevPasswords);
			UsrMes("Skipped " + sUserName + " because the password was used before.");
			/* Displays when skipped: password was used before;
			:LOOP;
		:ENDIF;

		sStoredHash := SetUserPassword(sUserName, sNewPassword);

		:IF Empty(sStoredHash);
			ErrorMes("Password update did not complete for " + sUserName);
			/* Displays on failure: password update did not complete;
			:LOOP;
		:ENDIF;

		UsrMes("Password updated for " + sUserName);
		/* Displays on success: password updated;
	:NEXT;
:ENDPROC;

/* Usage;
DoProc("ResetPasswordsWithHistoryCheck");
```

## Related

- [`ChkNewPassword`](ChkNewPassword.md)
- [`ChkPassword`](ChkPassword.md)
- [`string`](../types/string.md)
