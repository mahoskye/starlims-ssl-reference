---
title: "DocGetTasks"
summary: "Retrieves Documentum workflow tasks as a two-dimensional array."
id: ssl.function.docgettasks
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocGetTasks

Retrieves Documentum workflow tasks as a two-dimensional array.

`DocGetTasks` returns one row per available task. Each row is a fixed 12-element array containing sender, dates, task details, and workflow identifiers and titles.

When `sWorkflowId` is a non-empty string, the function returns only tasks for the matching workflow ID. The comparison is case-insensitive. When `sWorkflowId` is [`NIL`](../literals/nil.md) or an empty string, no workflow filter is applied and the function returns all available tasks.

If the underlying Documentum call fails, the function returns an empty array. Check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) immediately after the call when you need to distinguish a true no-results case from a backend failure.

## When to use

- When you need the current task list for one specific Documentum workflow.
- When you need task metadata such as due date, priority, or workflow title for display or routing.
- When you need to inspect all available inbox tasks by passing [`NIL`](../literals/nil.md) or `""` as the filter.

## Syntax

```ssl
DocGetTasks(sWorkflowId)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sWorkflowId` | [string](../types/string.md) | yes | — | Workflow ID to filter by. Pass a non-empty string to return only that workflow's tasks. Pass [`NIL`](../literals/nil.md) or `""` to return all available tasks. |

## Returns

**[array](../types/array.md)** — A two-dimensional array. Each row is a 12-element array.

| Position | Type | Value |
|----------|------|-------|
| `row[1]` | [string](../types/string.md) | Sent by |
| `row[2]` | [date](../types/date.md) | Date sent |
| `row[3]` | [string](../types/string.md) | Task name |
| `row[4]` | [date](../types/date.md) | Due date |
| `row[5]` | [number](../types/number.md) | Priority |
| `row[6]` | [string](../types/string.md) | Task state |
| `row[7]` | [string](../types/string.md) | Task object ID |
| `row[8]` | [string](../types/string.md) | Item ID |
| `row[9]` | [string](../types/string.md) | Workflow ID |
| `row[10]` | [string](../types/string.md) | Workflow name |
| `row[11]` | [string](../types/string.md) | Workflow subject |
| `row[12]` | [string](../types/string.md) | Workflow title |

## Best practices

!!! success "Do"
    - Access each task row by its documented 1-based positions such as `aTasks[nIndex, 3]` for the task name or `aTasks[nIndex, 9]` for the workflow ID.
    - Check [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) when `ALen(aTasks) == 0` and you need to know whether the empty result came from a failure.
    - Pass a non-empty `sWorkflowId` when you want one workflow only, because [`NIL`](../literals/nil.md) and `""` remove the filter and return all available tasks.

!!! failure "Don't"
    - Treat each result row as an object with named properties. Each task is returned as an array row.
    - Assume [`NIL`](../literals/nil.md) or `""` means no tasks. Those inputs request all available tasks.
    - Assume every empty result means there are no tasks. A failed Documentum call also returns an empty array.

## Caveats

- Passing [`NIL`](../literals/nil.md) or `""` returns all available tasks instead of raising an error.

## Examples

### List task names for one workflow

Queries Documentum for all tasks matching a specific workflow ID and prints each task name, exiting early when the result is empty.

```ssl
:PROCEDURE ListWorkflowTasks;
    :DECLARE sWorkflowId, aTasks, nIndex;

    sWorkflowId := "WF-100245";
    aTasks := DocGetTasks(sWorkflowId);

    :IF ALen(aTasks) == 0;
        UsrMes("No tasks found for workflow " + sWorkflowId);
        /* Displays when empty: No tasks found for workflow;

        :RETURN aTasks;
    :ENDIF;

    :FOR nIndex := 1 :TO ALen(aTasks);
        UsrMes(aTasks[nIndex, 3]);
        /* Displays per task: task name;
    :NEXT;

    :RETURN aTasks;
:ENDPROC;

/* Usage;
DoProc("ListWorkflowTasks");
```

### Detect lookup failures when filtering by workflow

Calls `DocGetTasks` with a workflow ID and distinguishes a backend failure (empty result with [`DocCommandFailed`](DocCommandFailed.md) set) from a workflow that genuinely has no tasks, returning an empty array with an error message only on failure.

```ssl
:PROCEDURE GetWorkflowTasksSafe;
    :PARAMETERS sWorkflowId;
    :DECLARE aTasks, sError;

    aTasks := DocGetTasks(sWorkflowId);

    :IF ALen(aTasks) == 0 .AND. DocCommandFailed();
        sError := DocGetErrorMessage();
        ErrorMes("Task lookup failed: " + sError);
        /* Displays on failure: Task lookup failed;

        :RETURN {};
    :ENDIF;

    :RETURN aTasks;
:ENDPROC;

/* Usage;
DoProc("GetWorkflowTasksSafe", {"WF-100245"});
```

### Group all available tasks by workflow title

Fetches all inbox tasks by passing [`NIL`](../literals/nil.md) as the filter, then counts how many tasks belong to each distinct workflow title and returns a summary array of `{title, count}` pairs.

```ssl
:PROCEDURE SummarizeInboxTasksByWorkflow;
    :DECLARE aTasks, aSummary, sWorkflowTitle, nPos, nIndex;

    aTasks := DocGetTasks(NIL);
    aSummary := {};

    :IF ALen(aTasks) == 0 .AND. DocCommandFailed();
        ErrorMes("Unable to retrieve tasks: " + DocGetErrorMessage());
        /* Displays on failure: Unable to retrieve tasks;

        :RETURN {};
    :ENDIF;

    :FOR nIndex := 1 :TO ALen(aTasks);
        sWorkflowTitle := aTasks[nIndex, 12];
        nPos := AScan(aSummary, {|aRow| aRow[1] == sWorkflowTitle});

        :IF nPos == 0;
            AAdd(aSummary, {sWorkflowTitle, 1});
        :ELSE;
            aSummary[nPos, 2] += 1;
        :ENDIF;
    :NEXT;

    :RETURN aSummary;
:ENDPROC;

/* Usage;
DoProc("SummarizeInboxTasksByWorkflow");
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocGetTasksCount`](DocGetTasksCount.md)
- [`DocStartWorkflow`](DocStartWorkflow.md)
- [`array`](../types/array.md)
- [`date`](../types/date.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
