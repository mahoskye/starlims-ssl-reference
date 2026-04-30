---
title: "DocRemoveAllUsersFromGroup"
summary: "Removes every user from a Documentum group."
id: ssl.function.docremoveallusersfromgroup
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocRemoveAllUsersFromGroup

Removes every user from a Documentum group.

Pass the target group name. The function returns [`.T.`](../literals/true.md) when the group is updated successfully and [`.F.`](../literals/false.md) when the removal operation fails. Passing [`NIL`](../literals/nil.md) for `sGroupName` raises an error before the Documentum call starts.

When the named group cannot be found, the underlying operation fails and this function returns [`.F.`](../literals/false.md) rather than raising that error directly.

## When to use

- When you need to clear an existing group's membership before rebuilding it.
- When decommissioning a group and you need to remove all current members.
- When handling administrative cleanup where partial user removal is not the goal.

## Syntax

```ssl
DocRemoveAllUsersFromGroup(sGroupName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sGroupName` | [string](../types/string.md) | yes | — | Name of the group to clear |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when all users are removed successfully; [`.F.`](../literals/false.md) when the group update fails

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sGroupName` is [`NIL`](../literals/nil.md). | `sGroupName argument cannot be null` |

## Best practices

!!! success "Do"
    - Validate that `sGroupName` is populated before calling the function.
    - Check the boolean return value and treat [`.F.`](../literals/false.md) as an operation failure.
    - Re-add users explicitly after a successful reset if you are rebuilding group membership.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sGroupName`.
    - Assume a [`.F.`](../literals/false.md) result means only one specific problem such as a missing group.
    - Use this function when you need to remove only selected users from the group.

## Caveats

- If the group cannot be updated, the function returns [`.F.`](../literals/false.md).
- The boolean result does not identify the specific backend failure.

## Examples

### Clear one existing group

Calls `DocRemoveAllUsersFromGroup` with a hardcoded group name and reports success or failure with branched messaging calls.

```ssl
:PROCEDURE ClearExistingGroup;
    :DECLARE sGroupName, bCleared;

    sGroupName := "LabUsers";

    bCleared := DocRemoveAllUsersFromGroup(sGroupName);

    :IF bCleared;
        UsrMes("Cleared group " + sGroupName);
        /* Displays cleared group name;
    :ELSE;
        ErrorMes("Failed to clear group " + sGroupName);
        /* Displays clear failure with group name;
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("ClearExistingGroup");
```

### Reset a project group before repopulating it

Builds the group name from a project code, clears the group, reports the outcome, and returns the boolean so the caller can react to a failure.

```ssl
:PROCEDURE ResetProjectGroup;
    :PARAMETERS sProjectCode;
    :DECLARE sGroupName, bCleared;

    sGroupName := "PRJ_" + Upper(sProjectCode) + "_TEAM";

    bCleared := DocRemoveAllUsersFromGroup(sGroupName);

    :IF bCleared;
        UsrMes("Reset group " + sGroupName);
        /* Displays reset group name;
    :ELSE;
        ErrorMes("Could not reset group " + sGroupName);
        /* Displays reset failure with group name;
    :ENDIF;

    :RETURN bCleared;
:ENDPROC;

/* Usage;
DoProc("ResetProjectGroup", {"ALPHA"});
```

### Clear multiple groups and capture per-group results

Iterates a list of group names, records the outcome of each clear operation in a [`CreateUdObject`](CreateUdObject.md) result, and accumulates all results into an array for the caller.

```ssl
:PROCEDURE ClearDocumentGroups;
    :PARAMETERS aGroupNames;
    :DECLARE aResults, oResult, sGroupName;
    :DECLARE nIndex, bCleared;

    aResults := {};

    :FOR nIndex := 1 :TO ALen(aGroupNames);
        sGroupName := aGroupNames[nIndex];
        bCleared := DocRemoveAllUsersFromGroup(sGroupName);

        oResult := CreateUdObject();
        oResult:groupName := sGroupName;
        oResult:success := bCleared;
        AAdd(aResults, oResult);

        :IF bCleared;
            UsrMes("Cleared group " + sGroupName);
            /* Displays cleared group name;
        :ELSE;
            ErrorMes("Failed to clear group " + sGroupName);
            /* Displays clear failure with group name;
        :ENDIF;
    :NEXT;

    :RETURN aResults;
:ENDPROC;

/* Usage;
DoProc("ClearDocumentGroups", {{"LabUsers", "QATeam"}});
```

## Related

- [`DocCreateGroup`](DocCreateGroup.md)
- [`DocAddUsersToGroup`](DocAddUsersToGroup.md)
- [`DocRemoveUsersFromGroup`](DocRemoveUsersFromGroup.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
