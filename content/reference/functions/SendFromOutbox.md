---
title: "SendFromOutbox"
summary: "Sends every email currently queued in the outbox."
id: ssl.function.sendfromoutbox
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SendFromOutbox

Sends every email currently queued in the outbox.

`SendFromOutbox()` reads the queued outbox entries, attempts to send each one,
deletes the entries that were sent successfully, and leaves failed entries in the outbox. It always processes the full queue and returns [`.T.`](../literals/true.md) only when every queued email was sent successfully.

## When to use

- When your process queues email first and sends it in a later batch step.
- When you need to clear a backlog of pending outbox messages.
- When you want one call to attempt delivery for every currently queued email.

## Syntax

```ssl
SendFromOutbox([bIgnoreErrors], [bUseCDO], [nTimeout])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `bIgnoreErrors` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Present in the signature. Outbox processing catches per-email send failures, continues with later rows, and returns [`.F.`](../literals/false.md) if any row fails. |
| `bUseCDO` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Passed through to the underlying send operation. |
| `nTimeout` | [number](../types/number.md) | no | `240` | Send timeout in seconds. A negative value is treated as the absolute timeout value with alternate send behavior. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the outbox is empty or when every queued email is sent successfully; [`.F.`](../literals/false.md) when one or more queued emails fail.

## Best practices

!!! success "Do"
    - Check the return value, because one batch can contain both successful and failed sends.
    - Review the remaining outbox entries after a [`.F.`](../literals/false.md) result and retry them after fixing the cause.
    - Use this function for queue-draining jobs after messages have already been added with [`SendToOutbox`](SendToOutbox.md).

!!! failure "Don't"
    - Assume a [`.F.`](../literals/false.md) return means nothing was sent. Earlier rows may already have been delivered and removed from the outbox.
    - Assume the function stops at the first failure. It continues through the full outbox.
    - Use this function to compose or queue new messages. It only processes messages that are already in the outbox.

## Caveats

- Failed rows are recorded and processing continues with the next queued email.

## Examples

### Send the current outbox batch

Drain the current outbox queue and report whether all messages were delivered or some failed and remain for retry.

```ssl
:PROCEDURE SendQueuedMail;
    :DECLARE bAllSent, sMessage;

    bAllSent := SendFromOutbox();

    :IF bAllSent;
        sMessage := "All queued emails were sent.";
    :ELSE;
        sMessage := "Some queued emails failed. Review the remaining outbox entries.";
    :ENDIF;

    UsrMes(sMessage);
    /* Displays success or failure status;

    :RETURN bAllSent;
:ENDPROC;

/* Usage;
DoProc("SendQueuedMail");
```

### Send with explicit transport settings

Pass explicit transport settings and handle partial failure by checking the return value.

```ssl
:PROCEDURE RunOutboxBatch;
    :DECLARE bAllSent, bUseCDO, nTimeout;

    bUseCDO := .F.;
    nTimeout := 120;

    bAllSent := SendFromOutbox(.T., bUseCDO, nTimeout);

    :IF .NOT. bAllSent;
        UsrMes("Outbox batch completed with one or more failures.");
        :RETURN .F.;
    :ENDIF;

    UsrMes("Outbox batch completed successfully.");

    :RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("RunOutboxBatch");
```

## Related

- [`SendLimsEmail`](SendLimsEmail.md)
- [`SendToOutbox`](SendToOutbox.md)
- [`boolean`](../types/boolean.md)
- [`number`](../types/number.md)
