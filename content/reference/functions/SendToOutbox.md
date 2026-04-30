---
title: "SendToOutbox"
summary: "Queues an email request in LIMSEMAILOUTBOX for later delivery instead of sending it immediately."
id: ssl.function.sendtooutbox
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SendToOutbox

Queues an email request in `LIMSEMAILOUTBOX` for later delivery instead of sending it immediately.

Use `SendToOutbox` when your workflow needs to persist the message first and send it later with [`SendFromOutbox`](SendFromOutbox.md). The function stores recipient, sender, subject, body, attachment, and SMTP settings, then returns a boolean result for the queue operation.

## When to use

- When message creation and message delivery happen in separate steps.
- When you want outbound email requests recorded before a later send pass.
- When a batch process or scheduled job will call [`SendFromOutbox`](SendFromOutbox.md) later.

## Syntax

```ssl
SendToOutbox(
    sSMTP,
    aRecipients,
    sFromWho,
    [sSubject],
    [sMessageBody],
    [aAttachList],
    [aCCList],
    [aBCCList],
    [sReplyTo],
    [nPort],
    [sUName],
    [sUPass],
    [bIgnoreErrors],
    [bUseSSL],
    [bIsBodyHTML],
    [sEncryptedData]
)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSMTP` | [string](../types/string.md) | yes | — | SMTP server name. [`NIL`](../literals/nil.md) is handled by `bIgnoreErrors`; an empty string is invalid. |
| `aRecipients` | [array](../types/array.md) | yes | — | Recipient address array. [`NIL`](../literals/nil.md) is handled by `bIgnoreErrors`; an empty array is invalid. |
| `sFromWho` | [string](../types/string.md) | yes | — | Sender address. [`NIL`](../literals/nil.md) is handled by `bIgnoreErrors`; an empty string is invalid. |
| `sSubject` | [string](../types/string.md) | no | `""` | Subject line. |
| `sMessageBody` | [string](../types/string.md) | no | `"***"` | Message body text. |
| `aAttachList` | [array](../types/array.md) | no | `{}` | Attachment path array. |
| `aCCList` | [array](../types/array.md) | no | `{}` | CC recipient array. |
| `aBCCList` | [array](../types/array.md) | no | `{}` | BCC recipient array. |
| `sReplyTo` | [string](../types/string.md) | no | `""` | Reply-to address. |
| `nPort` | [number](../types/number.md) | no | `25` | SMTP port. `0` is also treated as `25`. |
| `sUName` | [string](../types/string.md) | no | `""` | SMTP user name. |
| `sUPass` | [string](../types/string.md) | no | `""` | SMTP password. |
| `bIgnoreErrors` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Accepted for API compatibility. The three required-argument validation throws occur unconditionally regardless of this value. |
| `bUseSSL` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Uses a secure SMTP connection. |
| `bIsBodyHTML` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Marks the body as HTML. |
| `sEncryptedData` | [string](../types/string.md) | no | `""` | Additional encrypted payload stored with the queued message. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the outbox row is written successfully; [`.F.`](../literals/false.md) when the queue operation fails without raising, such as the `bIgnoreErrors` handling for [`NIL`](../literals/nil.md) required arguments.

A successful return means the message was queued, not delivered.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sSMTP` is [`NIL`](../literals/nil.md) or empty. | `SMTP`. |
| `aRecipients` is [`NIL`](../literals/nil.md) or empty. | `recipients`. |
| `sFromWho` is [`NIL`](../literals/nil.md) or empty. | `fromWho`. |

These exceptions are raised unconditionally regardless of `bIgnoreErrors`.

## Best practices

!!! success "Do"
    - Validate `sSMTP`, `aRecipients`, and `sFromWho` before calling so you do not depend on runtime argument errors.
    - Pass explicit arrays for attachments, CC, and BCC when those lists are part of the workflow.
    - Use [`SendFromOutbox`](SendFromOutbox.md) as the follow-up step when queued messages should actually be delivered.
    - Set `bIgnoreErrors` to [`.F.`](../literals/false.md) when the caller should surface and handle validation failures explicitly.

!!! failure "Don't"
    - Treat a successful return as proof that the email was sent. It only means the request was queued.
    - Pass `""` for `sSMTP` or `sFromWho`, or pass an empty recipient array. Those values are still invalid.
    - Use `SendToOutbox` when the requirement is immediate delivery. Use [`SendLimsEmail`](SendLimsEmail.md) for direct send behavior.
    - Assume `bIgnoreErrors` suppresses every failure. Its special handling only covers [`NIL`](../literals/nil.md) required arguments before the queue call proceeds.

## Caveats

- The `bIgnoreErrors` parameter is accepted in the signature but does not suppress the required-argument exceptions. Treat those three throws as unconditional.

## Examples

### Queue a basic email

Queue a plain-text message using the three required parameters and the subject and body. Check the return value to confirm the row was written.

```ssl
:PROCEDURE QueueBasicEmail;
	:DECLARE aRecipients, bQueued, sFromWho, sMessageBody, sSMTP, sSubject;

	sSMTP := "smtp.example.com";
	aRecipients := {"user@example.com"};
	sFromWho := "noreply@example.com";
	sSubject := "Sample ready";
	sMessageBody := "Your sample is ready for review.";

	bQueued := SendToOutbox(sSMTP, aRecipients, sFromWho, sSubject, sMessageBody);

	:IF bQueued;
		UsrMes("Email was queued.");
	:ELSE;
		UsrMes("Email was not queued.");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("QueueBasicEmail");
```

### Queue an HTML email with attachments and CC/BCC

Queue an HTML message with a PDF attachment, CC and BCC recipients, and SMTP authentication. The message is stored for later batch delivery.

```ssl
:PROCEDURE QueueHtmlEmail;
	:DECLARE aAttachList, aBCCList, aCCList, aRecipients, bQueued;
	:DECLARE sBody, sFromWho, sReplyTo, sSMTP, sSubject, sUName, sUPass;

	sSMTP := "smtp.example.com";
	aRecipients := {"primary@example.com"};
	sFromWho := "qa@example.com";
	sSubject := "Certificate package";
	sBody := "<p>Your certificate package is attached.</p>";
	aAttachList := {"C:\\Reports\\Certificate.pdf"};
	aCCList := {"supervisor@example.com"};
	aBCCList := {"audit@example.com"};
	sReplyTo := "support@example.com";
	sUName := "smtp-user";
	sUPass := "smtp-password";

	bQueued := SendToOutbox(
		sSMTP,
		aRecipients,
		sFromWho,
		sSubject,
		sBody,
		aAttachList,
		aCCList,
		aBCCList,
		sReplyTo,
		587,
		sUName,
		sUPass,
		.T.,
		.T.,
		.T.
	);

	:IF bQueued;
		UsrMes("HTML email was queued.");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("QueueHtmlEmail");
```

### Raise and handle validation errors explicitly

Wrap the call in `:TRY;` to catch the unconditional validation errors and inspect the failure with [`GetLastSSLError`](GetLastSSLError.md).

```ssl
:PROCEDURE QueueEmailFailFast;
	:DECLARE aAttachList, aBCCList, aCCList, aRecipients, bQueued, oErr;
	:DECLARE sBody, sFromWho, sReplyTo, sSMTP, sSubject, sUName, sUPass;

	sSMTP := "smtp.example.com";
	aRecipients := {"manager@example.com"};
	sFromWho := "workflow@example.com";
	sSubject := "Approval required";
	sBody := "A record is waiting for approval.";
	aAttachList := {};
	aCCList := {};
	aBCCList := {};
	sReplyTo := "";
	sUName := "";
	sUPass := "";
	bQueued := .F.;

	:TRY;
		bQueued := SendToOutbox(
			sSMTP,
			aRecipients,
			sFromWho,
			sSubject,
			sBody,
			aAttachList,
			aCCList,
			aBCCList,
			sReplyTo,
			25,
			sUName,
			sUPass,
			.F.
		);
	:CATCH;
		oErr := GetLastSSLError();
		/* Displays on failure: queue failed;
		ErrorMes("Queue failed: " + oErr:Description);
	:ENDTRY;

	:IF bQueued;
		UsrMes("Approval email was queued.");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("QueueEmailFailFast");
```

## Related

- [`SendFromOutbox`](SendFromOutbox.md)
- [`SendLimsEmail`](SendLimsEmail.md)
- [`array`](../types/array.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
