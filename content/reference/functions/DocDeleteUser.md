---
title: "DocDeleteUser"
summary: "Deletes a Documentum user by login name."
id: ssl.function.docdeleteuser
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocDeleteUser

Deletes a Documentum user by login name.

`DocDeleteUser` accepts one required string argument, `sLoginName`. If `sLoginName` is [`NIL`](../literals/nil.md), the function raises an error before attempting the deletion. When the delete call completes successfully, the function returns [`.T.`](../literals/true.md). If the delete path does not return a value, the function returns [`.F.`](../literals/false.md).

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

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the delete completes successfully. [`.F.`](../literals/false.md) only when the delete path does not return a value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sLoginName` is [`NIL`](../literals/nil.md). | `sLoginName argument cannot be null` |

## Best practices

!!! success "Do"
    - Pass a real login name, not [`NIL`](../literals/nil.md) or an unvalidated value.
    - Check the boolean return value before reporting success.
    - Use [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the user may already be missing or the delete must be reported clearly.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sLoginName`; the function raises an error before it attempts deletion.
    - Assume the user exists before calling the function.
    - Report success without checking the returned boolean.

## Caveats

- When the target user does not exist in Documentum, the backend raises `Failed: Object does not exist` rather than returning [`.F.`](../literals/false.md). Use [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) to handle this case.

## Examples

### Delete one user by login name and check the result

Calls `DocDeleteUser` with a hardcoded login name and displays a success or failure message based on the boolean return value.

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

Validates that `sLoginName` is non-empty before calling the function, then wraps the call in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) to handle the `Failed: Object does not exist` exception that the backend raises when the user is not found.

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

        :IF Empty(oErr);
            ErrorMes("DocDeleteUser failed for " + sLoginName);
        :ELSE;
            ErrorMes("DocDeleteUser failed: " + oErr:Description);
            /* Displays on failure with backend details;
        :ENDIF;

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
- [`GetLastSSLError`](GetLastSSLError.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
