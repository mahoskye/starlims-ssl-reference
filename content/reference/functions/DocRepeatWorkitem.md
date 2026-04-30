---
title: "DocRepeatWorkitem"
summary: "Repeats a Documentum workitem and can reassign it to a new user list."
id: ssl.function.docrepeatworkitem
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocRepeatWorkitem

Repeats a Documentum workitem and can reassign it to a new user list.

`DocRepeatWorkitem` requires `sWorkitemId` and `aUsers`. It optionally accepts `sSignOffUser`, `sSignOffPass`, and `sSignOffReason`. If `sWorkitemId` or `aUsers` is [`NIL`](../literals/nil.md), the function raises an error before attempting the repeat operation. Otherwise, it returns [`.T.`](../literals/true.md) when the repeat succeeds and [`.F.`](../literals/false.md) when it does not.

## When to use

- When a workflow workitem must be repeated and assigned to one or more users.
- When a workflow step needs an approval or signoff trail during the repeat.
- When automation needs a boolean success result instead of custom repeat logic.

## Syntax

```ssl
DocRepeatWorkitem(sWorkitemId, aUsers, [sSignOffUser], [sSignOffPass], [sSignOffReason])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sWorkitemId` | [string](../types/string.md) | yes | — | Identifier of the workitem to repeat |
| `aUsers` | [array](../types/array.md) | yes | — | Array of user IDs that receive the repeated workitem |
| `sSignOffUser` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Signoff user name passed with the repeat request |
| `sSignOffPass` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Signoff password passed with the repeat request |
| `sSignOffReason` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Signoff reason passed with the repeat request |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the workitem repeat succeeds; otherwise [`.F.`](../literals/false.md)

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sWorkitemId` is [`NIL`](../literals/nil.md). | `sWorkitemId argument cannot be null` |
| `aUsers` is [`NIL`](../literals/nil.md). | `aUsers argument cannot be null` |

## Best practices

!!! success "Do"
    - Validate that `sWorkitemId` and `aUsers` are assigned before calling the function.
    - Check the boolean return value and handle [`.F.`](../literals/false.md) explicitly in workflow logic.
    - Pass the optional signoff values when the repeat must capture approval context.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sWorkitemId` or `aUsers`. The function raises an error before the repeat is attempted.
    - Assume the repeat succeeded without checking the return value.
    - Pass signoff values unless the surrounding process actually requires them.

## Caveats

- A [`.F.`](../literals/false.md) result indicates the repeat did not succeed, but the function does not return a separate failure message.

## Examples

### Repeat a workitem for a new assignee list

Shows the minimum call form using only the two required parameters: the workitem ID and the user list.

```ssl
:PROCEDURE RepeatWorkitemBasic;
	:DECLARE sWorkitemId, sMessage;
	:DECLARE aUsers, bRepeated;

	sWorkitemId := "WI-2024-00423";
	aUsers := {"jsmith", "mwilliams"};

	bRepeated := DocRepeatWorkitem(sWorkitemId, aUsers);

	:IF bRepeated;
		sMessage := "Repeated workitem " + sWorkitemId;
	:ELSE;
		sMessage := "Could not repeat workitem " + sWorkitemId;
	:ENDIF;

	UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("RepeatWorkitemBasic");
```

`UsrMes` displays:

```text
Repeated workitem WI-2024-00423
Could not repeat workitem WI-2024-00423
```

### Repeat a workitem with signoff details

Shows the full five-argument call form, passing signoff credentials and a reason alongside the workitem ID and user list.

```ssl
:PROCEDURE RepeatWorkitemWithSignoff;
	:DECLARE sWorkitemId, sSignOffUser, sSignOffPass, sSignOffReason;
	:DECLARE sMessage, bRepeated;
	:DECLARE aUsers;

	sWorkitemId := "WI-2024-00847";
	aUsers := {"jsmith", "mwilson"};
	sSignOffUser := "supervisor01";
	sSignOffPass := "S3cur3P@ss";
	sSignOffReason := "Return this step for corrected data review";

	bRepeated := DocRepeatWorkitem(
		sWorkitemId,
		aUsers,
		sSignOffUser,
		sSignOffPass,
		sSignOffReason
	);

	:IF bRepeated;
		sMessage := "Repeated " + sWorkitemId + " with signoff context";
	:ELSE;
		sMessage := "Repeat request failed for " + sWorkitemId;
	:ENDIF;

	UsrMes(sMessage);

	:RETURN bRepeated;
:ENDPROC;

/* Usage;
DoProc("RepeatWorkitemWithSignoff");
```

`UsrMes` displays:

```text
Repeated WI-2024-00847 with signoff context
Repeat request failed for WI-2024-00847
```

## Related

- [`DocPauseWorkflow`](DocPauseWorkflow.md)
- [`DocResumeWorkflow`](DocResumeWorkflow.md)
- [`DocStopWorkflow`](DocStopWorkflow.md)
- [`DocGetTasks`](DocGetTasks.md)
- [`DocGetWorkflowStatus`](DocGetWorkflowStatus.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
