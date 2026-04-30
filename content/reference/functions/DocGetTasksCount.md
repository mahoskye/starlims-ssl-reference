---
title: "DocGetTasksCount"
summary: "Returns the number of workflow tasks in the Documentum inbox for the active session."
id: ssl.function.docgettaskscount
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocGetTasksCount

Returns the number of workflow tasks in the Documentum inbox for the active session.

`DocGetTasksCount()` returns the current inbox task count for the active Documentum login.
If the underlying Documentum call fails, the function returns `-1`.

Use it when you need only the total number of available tasks. If you need the actual task rows, use [`DocGetTasks`](DocGetTasks.md) instead.

## When to use

- When you need to display the total number of pending workflow tasks from a user's Documentum inbox on a dashboard or automated report.
- When implementing logic that branches based on whether the Documentum inbox is empty or contains tasks.
- When monitoring workflow load or diagnosing Documentum task queue issues in real time.

## Syntax

```ssl
DocGetTasksCount()
```

## Parameters

This function takes no parameters.

## Returns

**[number](../types/number.md)** — The number of workflow tasks in the current Documentum inbox.

| Value | Meaning |
|------|---------|
| `0` or greater | The inbox task count returned by Documentum. |
| `-1` | The Documentum call failed. |

## Best practices

!!! success "Do"
    - Check for `-1` before using the returned count in workflow logic or UI.
    - Initialize the Documentum interface and log in before calling this function.
    - Pair a `-1` result with [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) when you need failure details.
    - Use this function when you need only the total count, not the individual task rows.

!!! failure "Don't"
    - Treat `-1` as a real task count. It signals a failed Documentum call.
    - Use this function before the Documentum interface is initialized and logged in.
    - Use this function when you need task details. It returns only the aggregate count.

## Caveats

- The function exposes only one failure sentinel: `-1`.
- The function returns only the total inbox count. It does not filter by workflow or distinguish task types.
- The Documentum helper layer clears the previous failure state before the call runs. If this call fails, it records the new failure and returns `-1`.

## Examples

### Show current inbox workload to user

Logs in to Documentum, reads the inbox task count, checks for the `-1` failure sentinel, and displays the current pending task count.

```ssl
:PROCEDURE ShowDashboardTaskCount;
    :DECLARE nTaskCount;

    DocInitDocumentumInterface();

    :TRY;
        :IF .NOT. DocLoginToDocumentum("Repository", "analyst", "secret");
            ErrorMes("Documentum login failed: " + DocGetErrorMessage());
            /* Displays on login failure;
            :RETURN;
        :ENDIF;

        nTaskCount := DocGetTasksCount();

        :IF nTaskCount == -1;
            ErrorMes("Could not read inbox count: " + DocGetErrorMessage());
            /* Displays on count failure;
            :RETURN;
        :ENDIF;

        UsrMes("Current pending tasks: " + LimsString(nTaskCount));
        /* Displays current pending task count;

    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ShowDashboardTaskCount");
```

### Branch workflow behavior on count vs failure

Reads the inbox count and branches on three distinct cases: a failed call (returns `-1`), an empty inbox, and a non-empty inbox, returning [`.T.`](../literals/true.md) only when there are tasks to process.

```ssl
:PROCEDURE CheckInboxBeforeWork;
    :DECLARE nTaskCount;

    nTaskCount := DocGetTasksCount();

    :IF nTaskCount == -1;
        ErrorMes("Inbox count lookup failed: " + DocGetErrorMessage());
        /* Displays on failure;
        :RETURN .F.;
    :ENDIF;

    :IF nTaskCount == 0;
        UsrMes("No Documentum inbox tasks are waiting");
        :RETURN .F.;
    :ENDIF;

    UsrMes("Processing " + LimsString(nTaskCount) + " Documentum tasks");
    /* Displays task count before processing;
    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("CheckInboxBeforeWork");
```

## Related

- [`DocLoginToDocumentum`](DocLoginToDocumentum.md)
- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocGetTasks`](DocGetTasks.md)
- [`number`](../types/number.md)
