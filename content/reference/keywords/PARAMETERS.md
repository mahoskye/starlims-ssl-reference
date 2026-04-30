---
title: "PARAMETERS"
summary: "Declares named input parameters for a script, procedure, method, or constructor."
id: ssl.keyword.parameters
element_type: keyword
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# PARAMETERS

Declares named input parameters for a script, procedure, method, or constructor.

The `:PARAMETERS` keyword introduces the argument names a routine can receive. In standard SSL scripts, procedures, methods, and constructors, it appears once at the start of the body before any other statements. Each listed identifier becomes a parameter variable in the current routine scope, in the same order the caller supplies arguments. If a routine has no inputs, omit `:PARAMETERS` entirely.

## Behavior

`:PARAMETERS` defines the routine interface. It is not a general-purpose declaration statement like [`:DECLARE`](DECLARE.md), and it is the anchor for any following [`:DEFAULT`](DEFAULT.md) lines. Placement rules also matter here:

- Standard scripts and routines can omit `:PARAMETERS` when they take no arguments.
- If `:PARAMETERS` is present, it must come before any other statements in that body.
- A parameter list must contain at least one name.
- More than 20 parameters is allowed, but it produces a performance warning.

SSL data source files use a different form. In SSL and SQL data source files, parameters are declared inline with defaults on the same line, using [`:=`](../operators/assignment.md) instead of separate [`:DEFAULT`](DEFAULT.md) statements.

## When to use

- When a script, procedure, method, or constructor accepts caller-supplied values.
- When you want those inputs named explicitly instead of reading them indirectly.
- When you need to pair optional trailing arguments with [`:DEFAULT`](DEFAULT.md) lines.
- When documenting the public calling shape of a routine or data source.

## Syntax

Standard script, procedure, method, or constructor body:

```ssl
:PARAMETERS param1[, param2, ...];
```

SSL or SQL data source file:

```ssl
:PARAMETERS param1 := default1[, param2 := default2, ...];
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `param1[, param2, ...]` | Identifier list | Yes | — | One or more parameter names in call-order for a standard script, procedure, method, or constructor. |
| `:= defaultValue` | Inline default clause | Data source files only | — | Required for every parameter in SSL and SQL data source files. This inline form is only valid in data source files. |

## Keyword group

**Group:** Declarations
**Role:** opener

## Best practices

!!! success "Do"
    - Put `:PARAMETERS` first in the routine body whenever the routine accepts arguments.
    - Keep parameter names stable and descriptive because callers pass values positionally.
    - Keep parameter lists focused, and move optional trailing defaults to [`:DEFAULT`](DEFAULT.md) lines in standard SSL.

!!! failure "Don't"
    - Write `:PARAMETERS` after [`:DECLARE`](DECLARE.md), executable statements, or control flow. That placement is invalid in standard SSL bodies.
    - Use `:PARAMETERS` as a substitute for local-variable declarations. Local working names belong in [`:DECLARE`](DECLARE.md).
    - Use standard `:PARAMETERS` plus separate [`:DEFAULT`](DEFAULT.md) lines in data source files. Data sources require inline [`:=`](../operators/assignment.md) defaults on the `:PARAMETERS` line.

## Caveats

- Use at most one `:PARAMETERS` statement in a given script, procedure, method, or constructor body.
- A standard `:PARAMETERS` statement must include at least one parameter name.
- In standard SSL, [`:DEFAULT`](DEFAULT.md) lines must immediately follow `:PARAMETERS` when used.
- In SSL and SQL data source files, every parameter must include an inline default value with [`:=`](../operators/assignment.md).
- Colon-prefixed keywords are case-sensitive, so write `:PARAMETERS` in uppercase.

## Examples

### Declaring parameters for a procedure

Names the two values the caller passes in. With `sSampleID` set to `"S-1001"` and `sLabCode` set to `"LAB-A"`, the procedure builds and displays the combined message.

```ssl
:PROCEDURE DisplaySampleInfo;
    :PARAMETERS sSampleID, sLabCode;
    :DECLARE sMessage;

    sMessage := "Processing sample " + sSampleID;
    sMessage := sMessage + " in laboratory " + sLabCode;
    UsrMes(sMessage);

    :RETURN sMessage;
:ENDPROC;

/* Usage;
DoProc("DisplaySampleInfo", {"S-1001", "LAB-A"});
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Processing sample S-1001 in laboratory LAB-A
```

### Pairing PARAMETERS with DEFAULT

In standard SSL, `:PARAMETERS` comes first and any optional trailing values are added with separate [`:DEFAULT`](DEFAULT.md) lines immediately after it. The first call omits `sStatus` and `nMaxRows` (both use their defaults); the second call overrides both. Row counts depend on the database.

```ssl
:PROCEDURE FetchSampleRows;
    :PARAMETERS sSampleID, sStatus, nMaxRows;
    :DEFAULT sStatus, "Logged";
    :DEFAULT nMaxRows, 25;
    :DECLARE sSQL, aRows;

    sSQL := "
        SELECT sample_id, status, result_value
        FROM sample_result
        WHERE sample_id = ?sSampleID?
          AND status = ?sStatus?
          AND ROWNUM <= ?nMaxRows?
        ORDER BY sample_id
    ";

    aRows := SQLExecute(sSQL);

    :RETURN aRows;
:ENDPROC;

:PROCEDURE ShowFetchCalls;
    :DECLARE aDefaultRows, aCustomRows;

    aDefaultRows := DoProc("FetchSampleRows", {"LAB-2024-0042"});
    aCustomRows := DoProc("FetchSampleRows", {"LAB-2024-0042", "Complete", 10});

    InfoMes("Default call returned " + LimsString(ALen(aDefaultRows)) + " row(s)");
    InfoMes("Custom call returned " + LimsString(ALen(aCustomRows)) + " row(s)");
:ENDPROC;

/* Usage;
DoProc("ShowFetchCalls");
```

### Using PARAMETERS in a data source file

Data source files use the preprocessed inline-default form instead of separate [`:DEFAULT`](DEFAULT.md) statements. Both `sStatus` and `nMaxRows` have inline defaults that the caller can override when invoking the data source.

```ssl
:PARAMETERS sStatus := "Logged", nMaxRows := 50;

:RETURN SQLExecute("
	        SELECT sample_id, status
	        FROM sample
	        WHERE status = ?sStatus?
	          AND ROWNUM <= ?nMaxRows?
	        ORDER BY sample_id
	    ");
```

## Related

- [`DEFAULT`](DEFAULT.md)
- [`DECLARE`](DECLARE.md)
