---
title: "DEFAULT"
summary: "Assigns a fallback expression to a parameter when the caller omits that argument."
id: ssl.keyword.default
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DEFAULT

Assigns a fallback expression to a parameter when the caller omits that argument.

The `:DEFAULT` keyword works with a parameter that was already declared by [`:PARAMETERS`](PARAMETERS.md). In standard SSL scripts, procedures, methods, and constructors, each `:DEFAULT` line must appear immediately after [`:PARAMETERS`](PARAMETERS.md), and each line applies to one parameter. The form is `:DEFAULT paramName, defaultExpression;` with a comma between the parameter name and the expression. When the caller supplies that argument explicitly, SSL keeps the caller's value instead of using the default.

## Behavior

`:DEFAULT` is part of parameter setup, not a general-purpose assignment statement. The referenced name must already be present in the current [`:PARAMETERS`](PARAMETERS.md) list, and the fallback can be any valid SSL expression. To default multiple parameters, write multiple `:DEFAULT` lines in sequence.

!!! info
	SSL data source files use different syntax. In data source files, defaults are written inline on the [`:PARAMETERS`](PARAMETERS.md) line with [`:=`](../operators/assignment.md), not as separate `:DEFAULT` statements.

## When to use

- When a routine has optional trailing parameters with sensible fallback values.
- When you want older call sites to keep working after adding a new optional parameter.
- When a common value such as [`.F.`](../literals/false.md), [`Today()`](../functions/Today.md), or a standard status should be applied automatically.

## Syntax

```ssl
:PARAMETERS paramName[, otherParam, ...];
:DEFAULT paramName, defaultExpression;
```

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `paramName` | Identifier | Yes | Parameter name to receive the fallback value. It must already appear in the current [`:PARAMETERS`](PARAMETERS.md) list. |
| `defaultExpression` | Expression | Yes | Expression evaluated when the caller omits that argument. |

## Keyword group

**Group:** Declarations
**Role:** modifier

## Best practices

!!! success "Do"
    - Use `:DEFAULT` for optional parameters that have a clear, stable fallback value.
    - Keep `:DEFAULT` lines directly under [`:PARAMETERS`](PARAMETERS.md) so the routine interface is easy to read.
    - Prefer simple fallback expressions that make the omitted-argument behavior obvious.

!!! failure "Don't"
    - Use `:DEFAULT` as a replacement for normal assignments later in the routine. It only belongs in the parameter setup section.
    - Scatter `:DEFAULT` lines after [`:DECLARE`](DECLARE.md) or executable statements. That placement does not match SSL syntax.
    - Hide important business decisions inside surprising defaults. If a default changes behavior in a meaningful way, document it clearly.

## Caveats

- Colon-prefixed keywords are case-sensitive, so write `:DEFAULT` in uppercase.

## Examples

### Defaulting a single optional flag

Use one `:DEFAULT` line to make a trailing parameter optional. With only `sSampleID` supplied, `bIncludePrefix` defaults to [`.T.`](../literals/true.md) and the label is prefixed with `"Sample "`.

```ssl
:PROCEDURE FormatSampleLabel;
    :PARAMETERS sSampleID, bIncludePrefix;
    :DEFAULT bIncludePrefix, .T.;
    :DECLARE sLabel;

    sLabel := sSampleID;

    :IF bIncludePrefix;
        sLabel := "Sample " + sLabel;
    :ENDIF;

    InfoMes(sLabel);

    :RETURN sLabel;
:ENDPROC;

/*
Usage:
DoProc("FormatSampleLabel", {"S-001"})
;
```

[`InfoMes`](../functions/InfoMes.md) displays:

```text
Sample S-001
```

### Adding optional parameters without changing existing calls

Use multiple `:DEFAULT` lines so callers can omit new trailing arguments. `ShowDefaultedCalls` demonstrates both a minimal call and a fully specified call. The row counts depend on the database contents.

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

:PROCEDURE ShowDefaultedCalls;
    :DECLARE aDefaultRows, aCustomRows;

    aDefaultRows := DoProc("FetchSampleRows", {"LAB-2024-0042"});
    aCustomRows := DoProc("FetchSampleRows", {"LAB-2024-0042", "Complete", 10});

    /* Displays row counts for the default and custom calls;
    InfoMes("Default call returned " + LimsString(ALen(aDefaultRows)) + " row(s)");
    InfoMes("Custom call returned " + LimsString(ALen(aCustomRows)) + " row(s)");
:ENDPROC;

/*
Usage:
DoProc("ShowDefaultedCalls")
;
```

### Combining expression defaults with branch-specific logic

Default values can be expressions. Here `MYUSERNAME` and [`Today()`](../functions/Today.md) provide automatic context. The routine then branches on `bIncludeClosed` to build the appropriate query.

```ssl
:PROCEDURE SummarizeUserQueue;
    :PARAMETERS sOwner, dRunDate, bIncludeClosed;
    :DEFAULT sOwner, MYUSERNAME;
    :DEFAULT dRunDate, Today();
    :DEFAULT bIncludeClosed, .F.;
    :DECLARE sSQL, aRows, sMessage;

    :IF bIncludeClosed;
        sSQL := "
            SELECT task_id, status
            FROM task_queue
            WHERE owner = ?sOwner?
              AND run_date <= ?dRunDate?
            ORDER BY task_id
        ";
    :ELSE;
        sSQL := "
            SELECT task_id, status
            FROM task_queue
            WHERE owner = ?sOwner?
              AND run_date <= ?dRunDate?
              AND status != 'Closed'
            ORDER BY task_id
        ";
    :ENDIF;

    aRows := SQLExecute(sSQL);
    sMessage := "Returned " + LimsString(ALen(aRows)) + " task row(s) for " + sOwner;
    /* Displays the returned row count for the selected owner;
    InfoMes(sMessage);

    :RETURN aRows;
:ENDPROC;

/*
Usage:
DoProc("SummarizeUserQueue")
;
```

## Related

- [`PARAMETERS`](PARAMETERS.md)
- [`DECLARE`](DECLARE.md)
