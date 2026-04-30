---
title: "DocRemoveUsersFromGroup"
summary: "Removes one or more users from an existing Documentum group."
id: ssl.function.docremoveusersfromgroup
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocRemoveUsersFromGroup

Removes one or more users from an existing Documentum group.

Pass the target group name and an array of user names. The function returns [`.T.`](../literals/true.md) when the group update completes successfully and [`.F.`](../literals/false.md) when the removal operation fails. Passing [`NIL`](../literals/nil.md) for `sGroupName` or `aUsers` raises an error before the Documentum call starts.

When the named group cannot be found, the underlying removal call fails and this function returns [`.F.`](../literals/false.md) rather than surfacing that backend error directly.

## When to use

- When removing selected users from an existing Documentum group.
- When updating group membership during offboarding, transfer, or access review work.
- When you need a simple success or failure result for a batch removal request.

## Syntax

```ssl
DocRemoveUsersFromGroup(sGroupName, aUsers)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sGroupName` | [string](../types/string.md) | yes | — | Name of the existing group to update |
| `aUsers` | [array](../types/array.md) | yes | — | One-dimensional array of user names to remove |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the users are removed successfully; [`.F.`](../literals/false.md) when the group update fails

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sGroupName` is [`NIL`](../literals/nil.md). | `sGroupName argument cannot be null` |
| `aUsers` is [`NIL`](../literals/nil.md). | `aUsers argument cannot be null` |

## Best practices

!!! success "Do"
    - Validate that `sGroupName` and `aUsers` are populated before calling the function.
    - Check the boolean return value and treat [`.F.`](../literals/false.md) as an operation failure.
    - Build the `aUsers` array from validated user names before calling the function.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for either argument.
    - Assume the boolean result identifies which user caused the failure.
    - Assume [`.F.`](../literals/false.md) means only one specific problem such as a missing group.

## Caveats

- If the target group cannot be updated, the function returns [`.F.`](../literals/false.md).
- The boolean result is operation-level only. It does not report which user removal failed.

## Examples

### Remove one user from a known group

Wraps a single user name in a one-element array and reports success or failure.

```ssl
:PROCEDURE RemoveOneUser;
    :DECLARE aUsers, bRemoved;

    aUsers := {"jsmith"};

    bRemoved := DocRemoveUsersFromGroup("QC_Analysts", aUsers);

    :IF bRemoved;
        UsrMes("Removed user from QC_Analysts");
    :ELSE;
        ErrorMes("Failed to update QC_Analysts");
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("RemoveOneUser");
```

### Remove a validated user list from one project group

Constructs a group name from a project code, removes the supplied user list, reports the outcome, and returns the boolean so the caller can react to a failure.

```ssl
:PROCEDURE RemoveProjectUsers;
    :PARAMETERS sProjectCode, aUsersToRemove;
    :DECLARE sGroupName, bRemoved;

    sGroupName := "PRJ_" + Upper(sProjectCode) + "_TEAM";

    bRemoved := DocRemoveUsersFromGroup(sGroupName, aUsersToRemove);

    :IF bRemoved;
        UsrMes("Updated group " + sGroupName);
    :ELSE;
        ErrorMes("Could not update group " + sGroupName);
    :ENDIF;

    :RETURN bRemoved;
:ENDPROC;

/* Usage;
DoProc("RemoveProjectUsers", {"ALPHA", {"jsmith"}});
```

### Remove users from several groups and capture per-group results

Applies the same user list removal to each group in a list, records each per-group result in a [`CreateUdObject`](CreateUdObject.md), and returns the full result array.

```ssl
:PROCEDURE RemoveUsersFromGroups;
    :PARAMETERS aGroupNames, aUsersToRemove;
    :DECLARE aResults, oResult, sGroupName;
    :DECLARE nIndex, bRemoved;

    aResults := {};

    :FOR nIndex := 1 :TO ALen(aGroupNames);
        sGroupName := aGroupNames[nIndex];
        bRemoved := DocRemoveUsersFromGroup(sGroupName, aUsersToRemove);

        oResult := CreateUdObject();
        oResult:groupName := sGroupName;
        oResult:success := bRemoved;

        AAdd(aResults, oResult);

        :IF bRemoved;
            UsrMes("Updated group " + sGroupName);
            /* Displays updated group name on success;
        :ELSE;
            ErrorMes("Failed to update group " + sGroupName);
            /* Displays failed group name on failure;
        :ENDIF;
    :NEXT;

    :RETURN aResults;
:ENDPROC;

/* Usage;
DoProc("RemoveUsersFromGroups", {{"QC_Analysts", "QA_Team"}, {"jsmith"}});
```

## Related

- [`DocAddUsersToGroup`](DocAddUsersToGroup.md)
- [`DocRemoveAllUsersFromGroup`](DocRemoveAllUsersFromGroup.md)
- [`DocCreateGroup`](DocCreateGroup.md)
- [`DocExistsUser`](DocExistsUser.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
