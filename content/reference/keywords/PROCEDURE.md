---
title: "PROCEDURE"
summary: "Declares a named routine body that can contain executable SSL statements and end with :ENDPROC ;."
id: ssl.keyword.procedure
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# PROCEDURE

Declares a named routine body that can contain executable SSL statements and end with [`:ENDPROC`](ENDPROC.md) `;`.

The `:PROCEDURE` keyword introduces a procedure or method name, after which the body may optionally start with [`:PARAMETERS`](PARAMETERS.md) and [`:DEFAULT`](DEFAULT.md) lines before the routine's executable statements. In standard scripts, same-file procedures are invoked with [`DoProc`](../functions/DoProc.md); external script entry points or specific external procedures are invoked with [`ExecFunction`](../functions/ExecFunction.md). Inside a class file, `:PROCEDURE` is also used to declare methods, including the special `Constructor` routine.

## Behavior

:PROCEDURE opens a routine definition that must close with [`:ENDPROC`](ENDPROC.md) `;`. The declared routine name becomes available for calls, and when [`:PARAMETERS`](PARAMETERS.md) is present, each parameter name receives caller-supplied values by position.

Within a standard script procedure body, the conventional order is:

```ssl
:PROCEDURE ProcedureName;
    :PARAMETERS sParam1, sParam2;
    :DEFAULT sParam2, "";
    :DECLARE vLocal;

    /* Procedure logic;

:ENDPROC;
```

At runtime, a procedure can leave early with [`:RETURN`](RETURN.md) `value;`. If execution reaches [`:ENDPROC`](ENDPROC.md) `;` without an explicit return, the routine exits with an empty result.

## When to use

- When you need a named reusable routine in a script file.
- When logic should accept caller-supplied values through [`:PARAMETERS`](PARAMETERS.md).
- When the routine may need to return a result with [`:RETURN`](RETURN.md).
- When organizing script-level helpers or class methods into clear routine boundaries.

## Syntax

Procedure declaration:

```ssl
:PROCEDURE ProcedureName;
```

Typical complete form in a script:

```ssl
:PROCEDURE ProcedureName;
    :PARAMETERS sParam1[, sParam2, ...];
    :DEFAULT paramN, defaultValue;
    :DECLARE vLocal1[, vLocal2, ...];

    /* Statements;

    :RETURN value;
:ENDPROC;
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ProcedureName` | Identifier | Yes | The routine name declared by `:PROCEDURE`. In class files, the special name `Constructor` declares the class constructor. |

## Returns

`:PROCEDURE` itself produces no value. A procedure can return any value via [`:RETURN`](RETURN.md) `;`; execution that reaches [`:ENDPROC`](ENDPROC.md) `;` without a return exits with an empty result.

## Exceptions

Malformed procedure declarations fail at compile time. Common problems include a missing procedure name, missing [`:ENDPROC`](ENDPROC.md) `;`, or placing required opening-body statements such as [`:PARAMETERS`](PARAMETERS.md) in the wrong order.

## Keyword group

**Group:** Procedures & Classes
**Role:** opener

## Best practices

!!! success "Do"
    - Use a clear PascalCase procedure name that reflects the routine's job.
    - Put [`:PARAMETERS`](PARAMETERS.md) first in the body when the routine accepts arguments, and place any [`:DEFAULT`](DEFAULT.md) lines immediately after it.
    - Call same-file script procedures with [`DoProc`](../functions/DoProc.md) `("ProcedureName", {args})`, and use [`:RETURN`](RETURN.md) when the caller needs a result.

!!! failure "Don't"
    - Call a custom script procedure directly as `ProcedureName(args)`. Use [`DoProc`](../functions/DoProc.md) for same-file procedures or [`ExecFunction`](../functions/ExecFunction.md) for external scripts.
    - Omit [`:ENDPROC`](ENDPROC.md) `;` or treat it as optional. The procedure body must close explicitly.
    - Use [`DoProc`](../functions/DoProc.md) inside class methods. Inside a class, call sibling or inherited routines with `Me:Method()` or `Base:Method()`.

## Caveats

- `:PROCEDURE` is case-sensitive and must be written in uppercase.
- [`:DEFAULT`](DEFAULT.md) lines belong immediately after [`:PARAMETERS`](PARAMETERS.md), not on [`:DECLARE`](DECLARE.md) lines.
- More than 20 parameters is allowed, but it produces a performance warning.
- Script-level visibility annotations such as `/*@private;` and `/*@protected;` apply only to script procedures and must appear immediately before `:PROCEDURE`.

## Examples

### Defining and calling a same-file procedure

Defines a small reusable helper and calls it with [`DoProc`](../functions/DoProc.md) from another procedure in the same script. With `nLeft` set to `7` and `nRight` set to `5`, the total is `12`.

```ssl
:PROCEDURE CalculateTotal;
	:PARAMETERS nLeft, nRight;

	:RETURN nLeft + nRight;
:ENDPROC;


:PROCEDURE ShowTotal;
	:DECLARE nTotal, sMessage;

	nTotal := DoProc("CalculateTotal", {7, 5});
	sMessage := "Total: " + LimsString(nTotal);

	UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("ShowTotal");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Total: 12
```

### Using PARAMETERS and DEFAULT inside a procedure body

Demonstrates optional trailing parameters with [`:DEFAULT`](DEFAULT.md). With `sStatus` defaulting to `"Logged"` and `bIncludePrefix` defaulting to [`.T.`](../literals/true.md), the first call produces the full prefixed message; the second call overrides both defaults.

```ssl
:PROCEDURE BuildStatusMessage;
	:PARAMETERS sSampleID, sStatus, bIncludePrefix;
	:DEFAULT sStatus, "Logged";
	:DEFAULT bIncludePrefix, .T.;
	:DECLARE sMessage;

	sMessage := sSampleID + " is " + sStatus;

	:IF bIncludePrefix;
		sMessage := "Sample " + sMessage;
	:ENDIF;

	:IF sStatus == "Logged";
		sMessage := sMessage + " and ready for review";
	:ENDIF;

	:RETURN sMessage;
:ENDPROC;


:PROCEDURE ShowStatusExamples;
	:DECLARE sDefaultMsg, sCustomMsg;

	sDefaultMsg := DoProc("BuildStatusMessage", {"S-1001"});
	sCustomMsg := DoProc("BuildStatusMessage", {"S-1002", "Complete", .F.});

	InfoMes(sDefaultMsg);
	InfoMes(sCustomMsg);
:ENDPROC;

/* Usage;
DoProc("ShowStatusExamples");
```

[`InfoMes`](../functions/InfoMes.md) displays:

```text
Sample S-1001 is Logged and ready for review
S-1002 is Complete
```

### Combining a public entry procedure with a private helper

Shows how `/*@private;` restricts a helper to the current script while leaving the entry procedure accessible to callers. With three status strings in mixed case and spacing, each is normalized to uppercase before the count is returned.

```ssl
/*@private;
:PROCEDURE NormalizeStatus;
	:PARAMETERS sStatus;

	:RETURN Upper(AllTrim(sStatus));
:ENDPROC;


:PROCEDURE ProcessStatusList;
	:PARAMETERS aStatuses;
	:DECLARE nIndex, aNormalized;

	aNormalized := {};

	:FOR nIndex := 1 :TO ALen(aStatuses);
		AAdd(aNormalized, DoProc("NormalizeStatus", {aStatuses[nIndex]}));
	:NEXT;

	UsrMes("Processed " + LimsString(ALen(aNormalized)) + " statuses");

	:RETURN aNormalized;
:ENDPROC;

/* Usage;
DoProc("ProcessStatusList", {{"  Pending  ", "in progress", "COMPLETE"}});
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Processed 3 statuses
```

## Related

- [`PARAMETERS`](PARAMETERS.md)
- [`DEFAULT`](DEFAULT.md)
- [`ENDPROC`](ENDPROC.md)
- [`RETURN`](RETURN.md)
- [`DoProc`](../functions/DoProc.md)
- [`ExecFunction`](../functions/ExecFunction.md)
