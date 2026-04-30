---
title: "DECLARE"
summary: "Declares one or more variables in the current SSL scope."
id: ssl.keyword.declare
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DECLARE

Declares one or more variables in the current SSL scope.

The `:DECLARE` keyword adds one or more names to the current scope. In script, procedure, and method bodies, it declares local variables. In a class body, it declares class fields. The declared names are comma-separated identifiers, and each newly created variable starts with the empty string `""` as its initial value. `:DECLARE` is a regular statement, so SSL allows it anywhere a statement is valid, although many teams still group declarations near the top of a routine for readability.

## Behavior

`:DECLARE` creates storage for each listed name the first time that name is declared in the current runtime scope. The runtime initializes a new declared variable to the empty string, not [`NIL`](../literals/nil.md). Re-declaring the same name is accepted and does not reset the existing runtime value, so a repeated declaration is usually harmless at runtime but still poor style because it obscures where the variable was introduced.

## When to use

- When defining local working variables for a procedure, method, or script.
- When declaring class fields that should be available to all methods in the class.
- When you want variables to exist before assignment instead of relying on undeclared-variable warnings or errors.
- When you want to introduce a new variable at the point where a later block of logic starts using it.

## Syntax

```ssl
:DECLARE variable1[, variable2, ...];
```

## Parameters

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `variable1[, variable2, ...]` | Identifier list | Yes | One or more variable or field names separated by commas. |

## Keyword group

**Group:** Declarations
**Role:** modifier

## Best practices

!!! success "Do"
    - Declare variables before their first use.
    - Group related declarations near the start of a routine when that improves readability.
    - Use clear Hungarian-style names for local variables in examples and new code.

!!! failure "Don't"
    - Rely on assignment to introduce a variable. SSL expects names to be declared before use.
    - Re-declare the same name casually. SSL accepts it, but repeated declarations make scope harder to follow.
    - Scatter declarations through unrelated logic just because the language permits it. Use later declarations only when they genuinely improve clarity.

## Caveats

- `:DECLARE` does not assign a custom initial value. If you need one, declare the name and then assign it on a later statement.
- All colon-prefixed keywords are case-sensitive, so write `:DECLARE` in uppercase.

## Examples

### Defining local variables at procedure start

Declare all working variables before the procedure uses them. With the hardcoded values, the output shows `nResult` converted to a string via [`LimsString`](../functions/LimsString.md) and concatenated into the message.

```ssl
:PROCEDURE InitializeSampleRecord;
	:DECLARE sSampleID, sSampleName, nResult, sMessage;

	sSampleID := "LAB-2024-0042";
	sSampleName := "Calcium Carbonate Test";
	nResult := 98.6;

	sMessage := "Sample " + sSampleID + " - " + sSampleName;
	sMessage += " registered with result " + LimsString(nResult);
	UsrMes(sMessage);

	:RETURN sMessage;
:ENDPROC;

/* Usage;
DoProc("InitializeSampleRecord");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Sample LAB-2024-0042 - Calcium Carbonate Test registered with result 98.6
```

### Declaring a variable where a new logic block starts

`:DECLARE` can appear later in the statement flow when a new working variable becomes needed. Here `sAuditText` is only declared inside the [`:IF`](IF.md) block where it is used, keeping it scoped to its purpose.

```ssl
:PROCEDURE DescribeSampleStatus;
	:PARAMETERS sSampleID, bIncludeAudit;
	:DEFAULT bIncludeAudit, .F.;
	:DECLARE sMessage;

	sMessage := "Sample " + sSampleID + " is ready for review";

	:IF bIncludeAudit;
		:DECLARE sAuditText;

		sAuditText := "Checked by " + MYUSERNAME + " on " + DToC(Today());
		sMessage := sMessage + " (" + sAuditText + ")";
	:ENDIF;

	:RETURN sMessage;
:ENDPROC;

/* Usage;
DoProc("DescribeSampleStatus", {"LAB-001"});
```

### Declaring class fields

Use `:DECLARE` in a class body to define fields shared by all class methods. The fields declared at the class level are readable and writable from every method.

Class definition:

```ssl
:CLASS SampleContext;

:DECLARE sSampleID, nResultCount;

:PROCEDURE SetSample;
	:PARAMETERS sID;

	sSampleID := sID;
:ENDPROC;

:PROCEDURE AddResult;
	nResultCount += 1;
:ENDPROC;

:PROCEDURE Constructor;
	sSampleID := "";
	nResultCount := 0;
:ENDPROC;
```

Usage:

```ssl
:DECLARE oContext, sMessage;

oContext := CreateUdObject("SampleContext");
oContext:SetSample("LAB-2024-0042");
oContext:AddResult();

sMessage := "Tracked sample " + oContext:sSampleID;
sMessage := sMessage + " with " + LimsString(oContext:nResultCount);
sMessage := sMessage + " result";
UsrMes(sMessage);
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Tracked sample LAB-2024-0042 with 1 result
```

## Related

- [`DEFAULT`](DEFAULT.md)
- [`PUBLIC`](PUBLIC.md)
- [`PARAMETERS`](PARAMETERS.md)
