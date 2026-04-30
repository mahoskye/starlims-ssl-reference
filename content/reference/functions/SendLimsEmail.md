---
title: "SendLimsEmail"
summary: "Sends an email through SMTP and returns whether the send succeeded."
id: ssl.function.sendlimsemail
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SendLimsEmail

Sends an email through SMTP and returns whether the send succeeded.

`SendLimsEmail` sends a message immediately using the supplied SMTP server and recipient list. The function supports attachments, CC/BCC recipients, SMTP authentication, TLS/SSL, HTML bodies, and an optional encrypted certificate payload. When `bIgnoreErrors` is [`.T.`](../literals/true.md), failures are logged and the function returns [`.F.`](../literals/false.md). When `bIgnoreErrors` is [`.F.`](../literals/false.md), the function raises the underlying error instead.

## When to use

- When a script must send an email immediately instead of queueing it in the outbox.
- When the message needs attachments, CC/BCC recipients, or an HTML body.
- When the SMTP server requires a port, user name, password, or SSL/TLS.
- When the caller needs to choose between fail-fast behavior and [`.F.`](../literals/false.md) on send failure.

## Syntax

```ssl
SendLimsEmail(
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
    [bUseCDO],
    [nTimeout],
    [bUseSSL],
    [bIsBodyHTML],
    [sEncryptedData]
)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSMTP` | [string](../types/string.md) | yes | — | SMTP server name. [`NIL`](../literals/nil.md) raises or returns [`.F.`](../literals/false.md) depending on `bIgnoreErrors`. An empty string also causes the send to fail. |
| `aRecipients` | [array](../types/array.md) | yes | — | Recipient email addresses. [`NIL`](../literals/nil.md) raises or returns [`.F.`](../literals/false.md) depending on `bIgnoreErrors`. The send also fails if the array is empty. |
| `sFromWho` | [string](../types/string.md) | yes | — | Sender address. [`NIL`](../literals/nil.md) raises or returns [`.F.`](../literals/false.md) depending on `bIgnoreErrors`. An empty string also causes the send to fail. |
| `sSubject` | [string](../types/string.md) | no | `""` | Subject line. The surfaced signature allows it to be omitted, but the normal send path rejects an empty subject. |
| `sMessageBody` | [string](../types/string.md) | no | `"***"` | Message body text. |
| `aAttachList` | [array](../types/array.md) | no | `{}` | Attachment file paths. Empty paths or missing files cause the send to fail. |
| `aCCList` | [array](../types/array.md) | no | `{}` | CC recipient addresses. |
| `aBCCList` | [array](../types/array.md) | no | `{}` | BCC recipient addresses. |
| `sReplyTo` | [string](../types/string.md) | no | `""` | Reply-to address. |
| `nPort` | [number](../types/number.md) | no | `25` | SMTP server port. |
| `sUName` | [string](../types/string.md) | no | `""` | SMTP user name. |
| `sUPass` | [string](../types/string.md) | no | `""` | SMTP password. |
| `bIgnoreErrors` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | When [`.T.`](../literals/true.md), logs the failure and returns [`.F.`](../literals/false.md). When [`.F.`](../literals/false.md), raises the error instead. |
| `bUseCDO` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Legacy transport flag retained in the public signature. |
| `nTimeout` | [number](../types/number.md) | no | `240` | Timeout in seconds. |
| `bUseSSL` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Enables a secure SMTP connection. |
| `bIsBodyHTML` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Treats `sMessageBody` as HTML. |
| `sEncryptedData` | [string](../types/string.md) | no | `""` | Encrypted certificate payload used for signed or encrypted email scenarios. Invalid payload data causes the send to fail. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the email is sent successfully; [`.F.`](../literals/false.md) when sending fails and `bIgnoreErrors` is [`.T.`](../literals/true.md). Raises an error instead of returning [`.F.`](../literals/false.md) when `bIgnoreErrors` is [`.F.`](../literals/false.md).

## Exceptions

When `bIgnoreErrors` is [`.F.`](../literals/false.md), the function raises instead of returning [`.F.`](../literals/false.md):

| Trigger | Exception message |
| --- | --- |
| `sSMTP` is [`NIL`](../literals/nil.md). | `sSMTP argument cannot be null.` |
| `aRecipients` is [`NIL`](../literals/nil.md). | `aRecipients argument cannot be null.` |
| `sFromWho` is [`NIL`](../literals/nil.md). | `sFromWho argument cannot be null.` |
| The SMTP server name is blank or otherwise invalid. | `SMTP Server parameters are invalid.` |
| `aRecipients` is empty. | `The To field is empty.` |
| `sSubject` is empty. | `The Subject field is empty.` |
| An attachment path in `aAttachList` is empty. | `The attachment path is empty.` |
| An attachment file does not exist. | `The following file was not found : <path>` |
| `sEncryptedData` cannot be decrypted. | `The string cannot be decrypted` |
| `sEncryptedData` cannot be deserialized into certificate information. | `The Certificate Info cannot be deserialized.` |

## Best practices

!!! success "Do"
    - Pass a non-empty SMTP server name, recipient array, sender address, and subject.
    - Keep recipient, CC, BCC, and attachment values in arrays, even when only one item is needed.
    - Set `bUseSSL` to [`.T.`](../literals/true.md) when the SMTP server requires a secure connection.
    - Check the boolean return value when `bIgnoreErrors` is [`.T.`](../literals/true.md).
    - Validate attachment paths before calling the function.

!!! failure "Don't"
    - Rely on the surfaced optional signature to mean blank required fields are safe. Empty SMTP, sender, recipient, and subject values can still fail at runtime.
    - Pass a string where the function expects an array of addresses or attachments.
    - Ignore a [`.F.`](../literals/false.md) return when `bIgnoreErrors` is [`.T.`](../literals/true.md). That means the send failed and only the error handling mode changed.
    - Mark HTML content as plain text. Set `bIsBodyHTML` correctly so the message body is interpreted as intended.
    - Pass attachment paths that are blank or missing on disk.

## Caveats

- The first three parameters are required by contract, and blank values can also fail even when the parameter itself is not [`NIL`](../literals/nil.md).
- `bIgnoreErrors` defaults to [`.T.`](../literals/true.md), so callers that need fail-fast behavior should pass [`.F.`](../literals/false.md) explicitly.

## Examples

### Send a plain-text notification

Send a simple notification using the default parameters: plain text, no attachments, and `bIgnoreErrors` defaulting to [`.T.`](../literals/true.md).

```ssl
:PROCEDURE SendNotificationEmail;
	:DECLARE sSMTP, aRecipients, sFromWho, sSubject, sMessage, bSent;

	sSMTP := "mail.example.com";
	aRecipients := {"analyst@example.com"};
	sFromWho := "noreply@example.com";
	sSubject := "Sample Analysis Complete";
	sMessage := "Your sample has been processed and results are available.";

	bSent := SendLimsEmail(sSMTP, aRecipients, sFromWho, sSubject, sMessage);

	:IF .NOT. bSent;
		UsrMes("Email was not sent.");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("SendNotificationEmail");
```

`UsrMes` displays:

```text
Email was not sent.
```

### Send an HTML message with attachments and TLS

Send an HTML-formatted report with a PDF attachment over TLS, using an explicit port and credentials. `bIgnoreErrors` is [`.F.`](../literals/false.md), so failures raise immediately.

```ssl
:PROCEDURE SendTestReportEmail;
	:DECLARE sSMTP, aRecipients, sFromWho, sSubject, sHtmlBody;
	:DECLARE aAttachments, aCCList, aBCCList, sReplyTo;
	:DECLARE nPort, sUName, sUPass, bSent;

	sSMTP := "smtp.lab.example.com";
	aRecipients := {"analyst1@lab.example.com", "analyst2@lab.example.com"};
	sFromWho := "automation@lab.example.com";
	sSubject := "Automated Test Report";

	sReplyTo := "noreply@lab.example.com";
	nPort := 587;
	sUName := "automation_user";
	sUPass := "smtp_password";

	aAttachments := {"C:\\Reports\\TestResults_001.pdf"};
	aCCList := {"manager@lab.example.com"};
	aBCCList := {};

	sHtmlBody := "<html><body>";
	sHtmlBody += "<h2>Automated Test Report</h2>";
	sHtmlBody += "<p>The latest report is attached.</p>";
	sHtmlBody += "</body></html>";

	bSent := SendLimsEmail(
		sSMTP,
		aRecipients,
		sFromWho,
		sSubject,
		sHtmlBody,
		aAttachments,
		aCCList,
		aBCCList,
		sReplyTo,
		nPort,
		sUName,
		sUPass,
		.F.,
		.F.,
		60,
		.T.,
		.T.
	);

	:IF bSent;
		UsrMes("Test report email sent successfully.");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("SendTestReportEmail");
```

`UsrMes` displays:

```text
Test report email sent successfully.
```

## Related

- [`Email`](../classes/Email.md)
- [`SendFromOutbox`](SendFromOutbox.md)
- [`SendToOutbox`](SendToOutbox.md)
- [`array`](../types/array.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
