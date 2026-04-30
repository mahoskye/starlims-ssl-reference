---
title: "DocCreateACL"
summary: "Creates a Documentum ACL and returns the backend result string."
id: ssl.function.doccreateacl
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocCreateACL

Creates a Documentum ACL and returns the backend result string.

`DocCreateACL` requires an ACL `sAclName` and accepts optional `sDescription` and `aGroups` arguments. The wrapper exposes one-, two-, and three-argument forms. Passing [`NIL`](../literals/nil.md) for `sAclName` raises an error before the backend create call runs. When the backend call returns a value, `DocCreateACL` returns that string. When the backend call returns no value, the function returns `""`.

## When to use

- When you need to create a Documentum ACL from SSL code.
- When a workflow needs the returned ACL identifier or result string for later steps.
- When you want to provide an optional description or initial group list during
  ACL creation.

## Syntax

```ssl
DocCreateACL(sAclName, [sDescription], [aGroups])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sAclName` | [string](../types/string.md) | yes | — | ACL name to create. |
| `sDescription` | [string](../types/string.md) | no | omitted | Optional ACL description. |
| `aGroups` | [array](../types/array.md) | no | omitted | Optional array of group names to pass with the create request. |

## Returns

**[string](../types/string.md)** — Result string returned by the ACL creation call, or `""` when the backend call returns no value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sAclName` is [`NIL`](../literals/nil.md). | `sAclName argument cannot be null` |

## Best practices

!!! success "Do"
    - Pass a non-[`NIL`](../literals/nil.md) ACL name every time you call the function.
    - Check for an empty-string result before assuming the ACL was created.
    - Pass `sDescription` and `aGroups` only when you have meaningful values for them.
    - Read [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after an empty result when you need backend failure details.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sAclName`; that raises an immediate SSL error.
    - Assume `""` means the ACL already exists or that the create call succeeded.
    - Invent validation rules for ACL names or group contents that this wrapper does not document.

## Caveats

- The wrapper checks only whether `sAclName` is [`NIL`](../literals/nil.md). Other validation is handled by the backend create call.

## Examples

### Create an ACL by name only

Creates a named ACL with no description or group list and displays either the returned ACL identifier or an error when the result is empty.

```ssl
:PROCEDURE CreateLabDocumentsAcl;
    :DECLARE sAclId;

    sAclId := DocCreateACL("LabDocumentsACL");

    :IF Empty(sAclId);
        ErrorMes("DocCreateACL returned an empty result");
    :ELSE;
        UsrMes("Created ACL: " + sAclId);
        /* Displays: Created ACL with returned identifier;
    :ENDIF;

    :RETURN sAclId;
:ENDPROC;

/* Usage;
DoProc("CreateLabDocumentsAcl");
```

### Create an ACL with a description and initial group list

Builds the ACL name and description from a project code parameter, passes an initial group list, and displays the result or an error when the return value is empty.

```ssl
:PROCEDURE CreateProjectAcl;
    :PARAMETERS sProjectCode;
    :DECLARE sAclName, sDescription, sAclId, aGroups;

    sAclName := Upper(sProjectCode) + "_ACL";
    sDescription := "ACL for project " + Upper(sProjectCode);
    aGroups := {"LabUsers", "Supervisors"};

    sAclId := DocCreateACL(sAclName, sDescription, aGroups);

    :IF Empty(sAclId);
        ErrorMes("Failed to create ACL for " + sProjectCode);
        /* Displays on failure: Failed to create ACL for the project;
        :RETURN "";
    :ENDIF;

    UsrMes("Created ACL: " + sAclId);
    /* Displays: Created ACL with returned identifier;

    :RETURN sAclId;
:ENDPROC;

/* Usage;
DoProc("CreateProjectAcl", {"ALPHA"});
```

### Validate inputs and inspect the backend failure state on an empty result

Guards against an empty ACL name, strips blank group names from the input array, then calls the function and reads the Documentum failure state when the result is empty.

```ssl
:PROCEDURE CreateAclSafely;
    :PARAMETERS sAclName, sDescription, aGroups;
    :DECLARE aCleanGroups, sAclId, sErrMsg, sGroup;
    :DECLARE nIndex;

    aCleanGroups := {};

    :IF Empty(sAclName);
        ErrorMes("ACL name is required");
        :RETURN "";
    :ENDIF;

    :IF .NOT. Empty(aGroups);
        :FOR nIndex := 1 :TO ALen(aGroups);
            sGroup := AllTrim(aGroups[nIndex]);
            :IF .NOT. Empty(sGroup);
                AAdd(aCleanGroups, sGroup);
            :ENDIF;
        :NEXT;
    :ENDIF;

    :TRY;
        sAclId := DocCreateACL(sAclName, sDescription, aCleanGroups);

        :IF .NOT. Empty(sAclId);
            :RETURN sAclId;
        :ENDIF;

        :IF DocCommandFailed();
            sErrMsg := DocGetErrorMessage();
            ErrorMes("Documentum ACL creation failed: " + sErrMsg);
            /* Displays on failure: Documentum ACL creation failed;
        :ELSE;
            ErrorMes("Documentum ACL creation returned an empty result");
        :ENDIF;

        :RETURN "";
    :CATCH;
        ErrorMes("DocCreateACL raised an SSL error");
        :RETURN "";
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("CreateAclSafely", {"QualityACL", "ACL for quality", {"LabUsers", "Supervisors"}});
```

## Related

- [`DocAddUsersToGroup`](DocAddUsersToGroup.md)
- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocCreateGroup`](DocCreateGroup.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocRemoveUsersFromGroup`](DocRemoveUsersFromGroup.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
