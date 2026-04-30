---
title: "GetByName"
summary: "Retrieves the value of a variable by name from local or public storage."
id: ssl.function.getbyname
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetByName

Retrieves the value of a variable by name from local or public storage.

Returns the value associated with the specified variable name from the current SSL local or public scope. The name is case-sensitive and must be non-empty. If the variable does not exist, the runtime raises an error. Use this function when the variable name is only known at runtime — for static references, access the variable directly or use [`SetByName`](SetByName.md).

## When to use

- When you need to look up a variable whose name is supplied at runtime, such as from user input, configuration, or scripting.
- When building generic tools or utilities that inspect or process arbitrary session variables by their names.
- When you must resolve variable names dynamically, especially in workflows involving variable indirection or user-supplied identifiers.

## Syntax

```ssl
GetByName(sName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sName` | [string](../types/string.md) | yes | — | The name of the variable to retrieve. Case-sensitive. |

## Returns

**any** — The value of the variable with the specified name

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sName` is [`NIL`](../literals/nil.md) or empty. | `Variable name cannot be missing.` |
| The variable named `sName` does not exist in the current scope. | `Variable [name] is undefined!` |

## Best practices

!!! success "Do"
    - Always verify that the name argument is non-empty and not null before calling.
    - Be consistent in case usage for variable names across your codebase.
    - Implement robust error handling wherever the variable might not exist.

!!! failure "Don't"
    - Assume that missing or empty names are handled gracefully.
    - Create variables distinguished only by letter case (e.g., `Status` vs `status`).
    - Assume the variable will always be found and unconditionally use the result.

## Caveats

- This function does not create, alter, or initialize variables; it only retrieves existing ones.

## Examples

### Retrieve a variable whose name is known only at runtime

Create a variable with [`CreateLocal`](CreateLocal.md), then retrieve it by name using a string variable rather than a direct reference.

```ssl
:PROCEDURE GetUserVariable;
    :DECLARE sVarName, sValue, sResult;
    sVarName := "sUserName";
    CreateLocal(sVarName, "Alice");
    sValue := GetByName(sVarName);
    sResult := "Value of " + sVarName + " is: " + LimsString(sValue);
    UsrMes(sResult);
:ENDPROC;

/* Usage;
DoProc("GetUserVariable");
```

`UsrMes` displays:

```text
Value of sUserName is: Alice
```

### Collect a set of named variables into a report

Set up several named session variables, then retrieve them by name in a loop and format the results as a report.

```ssl
:PROCEDURE CollectSessionValues;
    :DECLARE aVarNames, aResults, sReport, sVal, nIndex, nCount;

    CreateLocal("sUserId", "jsmith");
    CreateLocal("sWorkstation", "WS-01");
    CreateLocal("sDepartment", "Laboratory");
    CreateLocal("sRole", "Analyst");

    aVarNames := {"sUserId", "sWorkstation", "sDepartment", "sRole"};
    aResults := {};
    nCount := ALen(aVarNames);

    :FOR nIndex := 1 :TO nCount;
        sVal := GetByName(aVarNames[nIndex]);
        AAdd(aResults, sVal);
    :NEXT;

    sReport := "Session Audit Report" + Chr(13) + Chr(10);
    :FOR nIndex := 1 :TO nCount;
        sReport += aVarNames[nIndex] + ": " + LimsString(aResults[nIndex]) + Chr(13) + Chr(10);
    :NEXT;

    UsrMes(sReport);
:ENDPROC;

/* Usage;
DoProc("CollectSessionValues");
```

`UsrMes` displays:

```text
Session Audit Report
sUserId: jsmith
sWorkstation: WS-01
sDepartment: Laboratory
sRole: Analyst
```

### Inspect session variable types using dynamic lookup

Create several session variables of different types, then retrieve each by name and report both the value and its SSL type string.

```ssl
:PROCEDURE InspectSessionState;
    :DECLARE sVarName, sReport, vValue, aVarNames, nIndex, sTypeName, sFormattedLine;

    CreateLocal("sCurrentUser", "jsmith");
    CreateLocal("nSessionTimeout", 300);
    CreateLocal("bIsAuthenticated", .T.);

    aVarNames := {"sCurrentUser", "nSessionTimeout", "bIsAuthenticated"};

    sReport := "";
    :FOR nIndex := 1 :TO ALen(aVarNames);
        sVarName := aVarNames[nIndex];
        vValue := GetByName(sVarName);
        sTypeName := LimsTypeEx(vValue);
        sFormattedLine := sVarName + " = " + LimsString(vValue) + " (" + sTypeName + ")";
        sReport += sFormattedLine + Chr(13) + Chr(10);
    :NEXT;

    UsrMes(sReport);
    :RETURN sReport;
:ENDPROC;

/* Usage;
DoProc("InspectSessionState");
```

`UsrMes` displays:

```text
sCurrentUser = jsmith (STRING)
nSessionTimeout = 300 (DOUBLE)
bIsAuthenticated = .T. (LOGIC)
```

## Related

- [`AddProperty`](AddProperty.md)
- [`CreateLocal`](CreateLocal.md)
- [`CreatePublic`](CreatePublic.md)
- [`HasProperty`](HasProperty.md)
- [`IsDefined`](IsDefined.md)
- [`LKill`](LKill.md)
- [`SetByName`](SetByName.md)
- [`string`](../types/string.md)
