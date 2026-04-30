---
title: "DocAddUsersToGroup"
summary: "Adds one or more users to an existing Documentum group."
id: ssl.function.docadduserstogroup
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocAddUsersToGroup

Adds one or more users to an existing Documentum group.

Pass the target group name and an array of user names. The function returns [`.T.`](../literals/true.md) when the group update succeeds and [`.F.`](../literals/false.md) when the add operation fails. Passing [`NIL`](../literals/nil.md) for `sGroupName` or `aUsers` raises an error before the add attempt starts.

## When to use

- When assigning a batch of users to an existing Documentum group.
- When rebuilding project or department group membership from application data.
- When automating access provisioning workflows that need a simple success or failure result.

## Syntax

```ssl
DocAddUsersToGroup(sGroupName, aUsers)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sGroupName` | [string](../types/string.md) | yes | — | Name of the existing target group |
| `aUsers` | [array](../types/array.md) | yes | — | One-dimensional array of user names to add |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the users are added successfully; [`.F.`](../literals/false.md) when the group update fails

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sGroupName` is [`NIL`](../literals/nil.md). | `sGroupName argument cannot be null` |
| `aUsers` is [`NIL`](../literals/nil.md). | `aUsers argument cannot be null` |

## Best practices

!!! success "Do"
    - Validate that `sGroupName` and `aUsers` are populated before calling the function.
    - Check the boolean return value and handle [`.F.`](../literals/false.md) as an operation failure.
    - Build the `aUsers` array from validated user names before calling the function.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for either argument.
    - Assume the boolean result tells you which user caused a failure.
    - Assume [`.F.`](../literals/false.md) means only one specific problem such as a missing group.

## Caveats

- A [`.F.`](../literals/false.md) result is operation-level only. It does not identify which user or validation step caused the failure.
- The documented contract does not define partial-success behavior, so callers should treat the result as success or failure for the whole request.

## Examples

### Add a set of users to an existing group

Passes a hard-coded list of user names to a named group and displays whether the operation succeeded.

```ssl
:PROCEDURE AddNewHiresToLabUsers;
    :DECLARE aNewHires, bAdded;

    aNewHires := {"jsmith", "mwilson", "rbrown", "kgarcia", "lmartinez"};

    bAdded := DocAddUsersToGroup("LabUsers", aNewHires);

    :IF bAdded;
        UsrMes("Added users to LabUsers");
    :ELSE;
        ErrorMes("Failed to add users to LabUsers");
    :ENDIF;

    :RETURN bAdded;
:ENDPROC;

/* Usage;
DoProc("AddNewHiresToLabUsers");
```

### Build the group name from a project code and sync the team

Constructs a Documentum group name from a project code passed as a procedure parameter, then adds the project team members to that group.

```ssl
:PROCEDURE SyncProjectTeamToSecurityGroup;
    :PARAMETERS sProjectCode;
    :DECLARE sGroupName, aUpdatedTeam, bAdded;

    sGroupName := "Project_" + Upper(sProjectCode) + "_Team";
    aUpdatedTeam := {"jsmith", "mwilliams", "rbrown"};

    bAdded := DocAddUsersToGroup(sGroupName, aUpdatedTeam);

    :IF bAdded;
        UsrMes("Updated group " + sGroupName);
    :ELSE;
        ErrorMes("Failed to update group " + sGroupName);
        /* Displays on failure: Failed to update group name;
    :ENDIF;

    :RETURN bAdded;
:ENDPROC;

/* Usage;
DoProc("SyncProjectTeamToSecurityGroup", {"ALPHA"});
```

### Load active users from a query and add them to the department group

Queries active users for a department passed as a parameter, builds the user array from query results, and adds them to a Documentum group named after the department.

```ssl
:PROCEDURE SyncHRGroupsToDMS;
    :PARAMETERS sDepartment;
    :DECLARE sGroupName, sSQL, aRows, aUsersToAdd;
    :DECLARE nIndex, bAdded;

    sGroupName := Upper(sDepartment) + "_Documents";
    aUsersToAdd := {};

    sSQL := "
	    SELECT user_id
        FROM hr_users
        WHERE department = ?
          AND status = 'ACTIVE'
    ";

    aRows := LSelect1(sSQL,, {sDepartment});

    :FOR nIndex := 1 :TO ALen(aRows);
        AAdd(aUsersToAdd, aRows[nIndex, 1]);
    :NEXT;

    bAdded := DocAddUsersToGroup(sGroupName, aUsersToAdd);

    :IF bAdded;
        UsrMes(
            "Added " + LimsString(ALen(aUsersToAdd)) +
            " users to " + sGroupName
        );
        /* Displays: Added count and group name;
    :ELSE;
        ErrorMes("Failed to update group " + sGroupName);
        /* Displays on failure: Failed to update group name;
    :ENDIF;

    :RETURN bAdded;
:ENDPROC;

/* Usage;
DoProc("SyncHRGroupsToDMS", {"ENGINEERING"});
```

## Related

- [`DocCreateGroup`](DocCreateGroup.md)
- [`DocRemoveUsersFromGroup`](DocRemoveUsersFromGroup.md)
- [`DocRemoveAllUsersFromGroup`](DocRemoveAllUsersFromGroup.md)
- [`DocExistsUser`](DocExistsUser.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
