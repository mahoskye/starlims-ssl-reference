---
title: "DocCreateGroup"
summary: "Creates a Documentum group and returns its identifier."
id: ssl.function.doccreategroup
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocCreateGroup

Creates a Documentum group and returns its identifier.

`DocCreateGroup` requires a non-[`NIL`](../literals/nil.md) group name and accepts an optional description. It returns the created group's identifier as a string. If the create operation does not return an identifier, the function returns an empty string.

## When to use

- When provisioning Documentum groups from an SSL workflow.
- When synchronizing security groups from another system into Documentum.
- When later steps need the returned group identifier.

## Syntax

```ssl
DocCreateGroup(sGroupName, [sDescription])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sGroupName` | [string](../types/string.md) | yes | — | Group name to create. |
| `sDescription` | [string](../types/string.md) | no | omitted | Optional group description. |

## Returns

**[string](../types/string.md)** — Group identifier when the create call succeeds, otherwise an empty string.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sGroupName` is [`NIL`](../literals/nil.md). | `sGroupName argument cannot be null` |

## Best practices

!!! success "Do"
    - Pass a meaningful group name every time you call the function.
    - Capture the returned identifier when later steps need to refer to the created group.
    - Check for an empty-string result before assuming the group was created.
    - Read [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after an empty result when you need the Documentum failure details.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sGroupName`; that raises an immediate SSL error.
    - Assume an empty-string result means the group already existed. Treat it as an unsuccessful create call unless your workflow proves otherwise.
    - Delay reading the Documentum error state after a failed create attempt.

## Caveats

- Blank strings for `sGroupName` are allowed by the public SSL contract and are not rejected by the function itself.

## Examples

### Create one group with only the required argument

Creates a Documentum group using just the required name and displays either the returned group identifier or a message when the result is empty.

```ssl
:PROCEDURE CreateProjectGroup;
    :DECLARE sGroupID;

    sGroupID := DocCreateGroup("Project Alpha Team");

    :IF Empty(sGroupID);
        UsrMes("Documentum group creation did not return a group ID");
        :RETURN "";
    :ENDIF;

    /* Displays created group ID;
    UsrMes("Created Documentum group: " + sGroupID);
    :RETURN sGroupID;
:ENDPROC;

DoProc("CreateProjectGroup");
```

### Create multiple groups with descriptions and collect failures

Iterates a list of name-and-description pairs, creates each group, and collects the names of any groups whose create call returned an empty identifier.

```ssl
:PROCEDURE CreateDepartmentGroups;
    :DECLARE aGroups, aFailed, sGroupID, sGroupName, sDescription, nIndex;

    aGroups := {
        {"Engineering", "Engineering team"},
        {"Quality Control", "Quality team"},
        {"Manufacturing", "Manufacturing team"}
    };

    aFailed := {};

    :FOR nIndex := 1 :TO ALen(aGroups);
        sGroupName := aGroups[nIndex, 1];
        sDescription := aGroups[nIndex, 2];
        sGroupID := DocCreateGroup(sGroupName, sDescription);

        :IF Empty(sGroupID);
            AAdd(aFailed, sGroupName);
        :ENDIF;
    :NEXT;

    :RETURN aFailed;
:ENDPROC;

DoProc("CreateDepartmentGroups");
```

### Capture Documentum error details immediately after a failed create

Creates a group with a description, then reads the Documentum error message immediately when the create call returns an empty identifier.

```ssl
:PROCEDURE ProvisionProjectTeam;
    :DECLARE sGroupName, sGroupDesc, sGroupID, sErrMsg;

    sGroupName := "Project Alpha Team";
    sGroupDesc := "Automated workflow group for Project Alpha members";
    sGroupID := DocCreateGroup(sGroupName, sGroupDesc);

    :IF .NOT. Empty(sGroupID);
        /* Displays created group ID;
        UsrMes("Group created successfully: " + sGroupID);
        :RETURN sGroupID;
    :ENDIF;

    :IF DocCommandFailed();
        sErrMsg := DocGetErrorMessage();
        /* Displays on failure: group create failed;
        ErrorMes("Group create failed: " + sErrMsg);
    :ENDIF;

    :RETURN "";
:ENDPROC;

DoProc("ProvisionProjectTeam");
```

## Related

- [`DocAddUsersToGroup`](DocAddUsersToGroup.md)
- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocCreateUser`](DocCreateUser.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`string`](../types/string.md)
