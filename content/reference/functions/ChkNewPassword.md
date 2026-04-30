---
title: "ChkNewPassword"
summary: "Validates that a proposed password is not already present in stored password history."
id: ssl.function.chknewpassword
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ChkNewPassword

Validates that a proposed password is not already present in stored password history.

`ChkNewPassword` checks `sPassword` against `vPrevPasswords` and returns [`.T.`](../literals/true.md) when no exact match is found. Supply the history as either an array of prior passwords or a comma-separated string. If `vPrevPasswords` is [`NIL`](../literals/nil.md) or `""`, the function returns [`.T.`](../literals/true.md) because there is no history to compare.

## When to use

- When you need to prevent password reuse during a password change flow.
- When stored password history is already available as an array or comma-delimited string.
- When you need a separate history check alongside credential verification and password-update logic.

## Syntax

```ssl
ChkNewPassword(sPassword, vPrevPasswords)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sPassword` | [string](../types/string.md) | yes | — | Candidate password to validate. Passing [`NIL`](../literals/nil.md) raises an exception. |
| `vPrevPasswords` | [string](../types/string.md) or [array](../types/array.md) | yes | — | Prior passwords as either a comma-separated string or an array. Pass [`NIL`](../literals/nil.md) or `""` when no stored history is available. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when `sPassword` is not found in `vPrevPasswords`; otherwise [`.F.`](../literals/false.md).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sPassword` is [`NIL`](../literals/nil.md). | `Password parameter cannot be null.` |

## Best practices

!!! success "Do"
    - Normalize your password-history source before calling the function.
    - Pass either an array or a comma-separated string consistently.
    - Use this function alongside your normal credential-verification and password-update flow.

!!! failure "Don't"
    - Assume [`NIL`](../literals/nil.md) for `sPassword` returns [`.F.`](../literals/false.md). It raises an exception instead.
    - Treat this function as a complete password-policy check. It only checks reuse.
    - Pass ambiguous history text when the delimiter format is not controlled.

## Caveats

- String history is split on commas only. Entries are not trimmed or normalized.
- Matching is exact. The function returns [`.F.`](../literals/false.md) only when `sPassword` matches a history entry exactly.

## Examples

### Check an array of previous passwords

Checks a proposed password against an in-memory array of prior passwords. Because `"Str0ngP@ssw0rd!"` appears as the second history entry, the function returns [`.F.`](../literals/false.md) and the rejection message is displayed.

```ssl
:PROCEDURE CheckPasswordHistory;
    :DECLARE sNewPassword, aPrevPasswords, bPasswordOk, sMessage;

    sNewPassword := "Str0ngP@ssw0rd!";
    aPrevPasswords := {
        "Summer2024!",
        "Str0ngP@ssw0rd!",
        "W1nter2024@"
    };

    bPasswordOk := ChkNewPassword(sNewPassword, aPrevPasswords);

    :IF bPasswordOk;
        sMessage := "Password accepted. It has not been used recently.";
    :ELSE;
        sMessage := "Password rejected. Choose a password you have not used before.";
    :ENDIF;

    UsrMes(sMessage);

    :RETURN bPasswordOk;
:ENDPROC;

/* Usage;
DoProc("CheckPasswordHistory");
```

[`UsrMes`](UsrMes.md) displays:

```text
Password rejected. Choose a password you have not used before.
```

### Check comma-separated password history

Passes a comma-separated history string as the second argument, showing the alternative to an array. Because `"SecurePass123"` appears in the history string, the function returns [`.F.`](../literals/false.md).

```ssl
:PROCEDURE CheckPasswordHistoryString;
    :DECLARE sNewPassword, sPrevPasswords, bIsNew, sMessage;

    sNewPassword := "SecurePass123";
    sPrevPasswords := "Winter2024!,Spring2025!,SecurePass123";

    bIsNew := ChkNewPassword(sNewPassword, sPrevPasswords);

    :IF bIsNew;
        sMessage := "Password is not present in stored history.";
    :ELSE;
        sMessage := "Password was already used. Choose a different value.";
    :ENDIF;

    UsrMes(sMessage);

    :RETURN bIsNew;
:ENDPROC;

/* Usage;
DoProc("CheckPasswordHistoryString");
```

[`UsrMes`](UsrMes.md) displays:

```text
Password was already used. Choose a different value.
```

### Password change flow with reuse check

Combines [`ChkPassword`](ChkPassword.md), `ChkNewPassword`, and [`SetUserPassword`](SetUserPassword.md) in a single procedure that verifies the current credential, checks the new password against history, and updates it only when both checks pass.

```ssl
:PROCEDURE UpdateUserPasswordIfAllowed;
    :PARAMETERS sUserName, sCurrentPassword, sNewPassword, aPrevPasswords;
    :DECLARE oResult, bCurrentOk, bIsNew;

    oResult := CreateUdObject();
    oResult:success := .F.;
    oResult:message := "";

    bCurrentOk := ChkPassword(sUserName, sCurrentPassword);
    :IF !bCurrentOk;
        oResult:message := "Current password is incorrect.";
        :RETURN oResult;
    :ENDIF;

    bIsNew := ChkNewPassword(sNewPassword, aPrevPasswords);

    :IF !bIsNew;
        oResult:message := "New password was used recently. Choose a different password.";
        :RETURN oResult;
    :ENDIF;

    :TRY;
        SetUserPassword(sUserName, sNewPassword);
        oResult:success := .T.;
        oResult:message := "Password updated successfully.";
    :CATCH;
        oResult:message := GetLastSSLError():Description;
    :ENDTRY;

    :RETURN oResult;
:ENDPROC;

/* Usage;
DoProc("UpdateUserPasswordIfAllowed", {"jsmith", "OldPass123", "NewSecurePass!", {"OldPass1", "OldPass2"}});
```

## Related

- [`ChkPassword`](ChkPassword.md)
- [`SetUserPassword`](SetUserPassword.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
