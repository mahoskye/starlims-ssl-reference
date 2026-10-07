---
title: "DocDeleteUser"
summary: "Deletes a Documentum user by login name."
id: ssl.function.docdeleteuser
element_type: function
doc_status: published
starlims:
  applies_to: [11, 12]
  verified_against: [11]
---

# DocDeleteUser

Deletes a Documentum user by login name.

`DocDeleteUser` accepts one required string argument, `sLoginName`. If `sLoginName` is [`NIL`](../literals/nil.md), the function raises an error before attempting the deletion. When the delete completes successfully, the function returns [`.T.`](../literals/true.md). It returns [`.F.`](../literals/false.md) when Documentum does not confirm the delete. A user that does not exist raises an error instead (see [Exceptions](#exceptions)).

## When to use

- When an SSL script needs to remove a Documentum user account.
- When automation must delete a specific Documentum login.
- When later logic needs a simple [`.T.`](../literals/true.md) or [`.F.`](../literals/false.md) result from the delete call.

## Syntax

```ssl
DocDeleteUser(sLoginName)
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `sLoginName` | [string](../types/string.md) | yes | — | Login name of the Documentum user to delete |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the delete completes successfully. [`.F.`](../literals/false.md) when Documentum does not confirm the delete. A missing user raises instead (see [Exceptions](#exceptions)).

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sLoginName` is [`NIL`](../literals/nil.md). | `sLoginName argument cannot be null` |
| The user does not exist in Documentum. | `Failed: Object does not exist` |

## Best practices

!!! success "Do"
    - Pass a real login name, not [`NIL`](../literals/nil.md) or an unvalidated value.
    - Check the boolean return value before reporting success.
    - Use [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the user may already be missing or the delete must be reported clearly.
    - Call the function within an initialized, logged-in Documentum session ([`DocInitDocumentumInterface`](DocInitDocumentumInterface.md), [`DocLoginToDocumentum`](DocLoginToDocumentum.md)).

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sLoginName`; the function raises an error before it attempts deletion.
    - Assume the user exists before calling the function.
    - Report success without checking the returned boolean.

## Caveats

- When the target user does not exist in Documentum, the call raises `Failed: Object does not exist` rather than returning [`.F.`](../literals/false.md). Use [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) to handle this case.

## Examples

### Delete one user by login name and check the result

Calls `DocDeleteUser` with a hardcoded login name and logs a success or failure message based on the boolean return value. Assumes the caller already has a Documentum session open.

```ssl
:PROCEDURE DeleteDocUser;
    :DECLARE sLoginName, bDeleted;

    sLoginName := "jsmith";
    bDeleted := DocDeleteUser(sLoginName);

    :IF bDeleted;
        UsrMes("Deleted Documentum user " + sLoginName);
    :ELSE;
        ErrorMes("DocDeleteUser did not confirm deletion for " + sLoginName);
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("DeleteDocUser");
```

### Validate input and catch errors such as a missing user

Validates that `sLoginName` is non-empty before calling the function, then wraps the call in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) to handle the `Failed: Object does not exist` exception that is raised when the user is not found. Assumes the caller already has a Documentum session open.

```ssl
:PROCEDURE DeleteDocUserSafe;
    :PARAMETERS sLoginName;
    :DECLARE bDeleted, oErr;

    :IF Empty(sLoginName);
        ErrorMes("User name is required");
        :RETURN .F.;
    :ENDIF;

    :TRY;
        bDeleted := DocDeleteUser(sLoginName);

        :IF .NOT. bDeleted;
            ErrorMes("DocDeleteUser did not confirm deletion for " + sLoginName);
        :ELSE;
            UsrMes("Deleted Documentum user " + sLoginName);
        :ENDIF;

        :RETURN bDeleted;
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("DocDeleteUser failed: " + oErr:Description);
        /* Logs on failure with the error details;

        :RETURN .F.;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("DeleteDocUserSafe", {"jsmith"});
```

## Related

- [`DocCreateUser`](DocCreateUser.md)
- [`DocExistsUser`](DocExistsUser.md)
- [`DocUpdateUser`](DocUpdateUser.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`DocLoginToDocumentum`](DocLoginToDocumentum.md)
- [`GetLastSSLError`](GetLastSSLError.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
