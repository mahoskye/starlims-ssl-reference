---
title: "Email"
summary: "Composes, loads, saves, sends, or queues email messages with attachments and optional signing or encryption."
id: ssl.class.email
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Email

Composes, loads, saves, sends, or queues email messages with attachments and optional signing or encryption.

Email lets SSL code build a message, send it through SMTP, save it to a message file, load a saved message for later sending, or queue it for outbox delivery. Create it with `Email{}` when you want methods to return [`.F.`](../literals/false.md) and populate `Exception` instead of raising, or use `Email{.F.}` when you want failures to raise and be handled with [`:TRY`](../keywords/TRY.md) and [`GetLastSSLError`](../functions/GetLastSSLError.md). Before `Send`, `SaveMessage`, or [`SendToOutbox`](../functions/SendToOutbox.md), set `From`, `To`, `Subject`, and `Body`. Before `Send` or [`SendToOutbox`](../functions/SendToOutbox.md), also set `SMTPServerName` and `SMTPServerPort`. SMTP credentials are optional and are only used when `SMTPServerUserName` is not empty.

## When to use

- When an SSL script needs to send an email message directly through SMTP.
- When a script should queue mail for later delivery instead of sending it immediately.
- When a workflow needs attachments, HTML body content, message signing, or message encryption.
- When you need to resend a previously saved message file with fresh SMTP settings.

## Constructors

### `Email{}`

Creates an `Email` object with exception suppression enabled by default. Operations return [`.T.`](../literals/true.md) or [`.F.`](../literals/false.md), and failures are exposed through the `Exception` property.

### `Email{bIgnoreExceptions}`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `bIgnoreExceptions` | [boolean](../types/boolean.md) | yes | When [`.T.`](../literals/true.md), methods suppress exceptions and return [`.F.`](../literals/false.md) on failure. When [`.F.`](../literals/false.md), failures raise exceptions. |

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `Attachments` | [array](../types/array.md) | read-write | File paths to attach when building the message. |
| `BCC` | [array](../types/array.md) | read-write | Blind carbon copy recipients. |
| `Body` | [string](../types/string.md) | read-write | Message body text. |
| `CC` | [array](../types/array.md) | read-write | Carbon copy recipients. |
| `Exception` | [`SSLError`](SSLError.md) | read-only | Most recent failure captured by the object. |
| `From` | [string](../types/string.md) | read-write | Sender address. |
| `IgnoreExceptions` | [boolean](../types/boolean.md) | read-write | Controls whether failures are suppressed or raised. |
| `IsHTMLBody` | [boolean](../types/boolean.md) | read-write | When [`.T.`](../literals/true.md), the body is sent as HTML as well as plain text. |
| `LogSMTP` | [boolean](../types/boolean.md) | read-write | Writes an SMTP session log for direct `Send` calls. |
| `SMTPServerName` | [string](../types/string.md) | read-write | SMTP server host name. |
| `SMTPServerPort` | [number](../types/number.md) | read-write | SMTP server port. |
| `SMTPSecureConnection` | [boolean](../types/boolean.md) | read-write | Enables a secure SMTP connection. |
| `SMTPServerUserName` | [string](../types/string.md) | read-write | SMTP login user name. |
| `SMTPServerUserPassword` | [string](../types/string.md) | read-write | SMTP login password. |
| `SMTPTimeout` | [number](../types/number.md) | read-write | Timeout in seconds for direct `Send` calls. `0` uses the default timeout. |
| `Subject` | [string](../types/string.md) | read-write | Message subject. |
| `To` | [array](../types/array.md) | read-write | Primary recipients. |

## Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `LoadMessage(sPathToMessage)` | [boolean](../types/boolean.md) | Loads a message file for later `Send`. |
| `SaveMessage(sPathToMessage)` | [boolean](../types/boolean.md) | Saves the current message to a file in message format. |
| `Send()` | [boolean](../types/boolean.md) | Sends the current message through SMTP. |
| [`SendToOutbox()`](../functions/SendToOutbox.md) | [boolean](../types/boolean.md) | Queues the current message for later delivery. |
| `SetEncryptCertificateFromPath(sPathToCertificate, sCertificatePassword)` | [boolean](../types/boolean.md) | Loads the encryption certificate from a file. |
| `SetEncryptCertificateFromStore(sCertificateEmailAddress, sCertificateStoreName)` | [boolean](../types/boolean.md) | Loads the encryption certificate from a certificate store. |
| `SetSignCertificateFromPath(sPathToCertificate, sCertificatePassword)` | [boolean](../types/boolean.md) | Loads the signing certificate from a file. |
| `SetSignCertificateFromStore(sCertificateEmailAddress, sCertificateStoreName)` | [boolean](../types/boolean.md) | Loads the signing certificate from a certificate store. |

### `LoadMessage`

Loads a saved message file for later `Send()`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sPathToMessage` | [string](../types/string.md) | yes | Message file to load. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the message was loaded.

### `SaveMessage`

Saves the current property-based message to a file.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sPathToMessage` | [string](../types/string.md) | yes | File path where the message should be saved. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the message was saved.

### `Send`

Sends the current or loaded message through the configured SMTP server.

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the message was sent.

### [`SendToOutbox`](../functions/SendToOutbox.md)

Queues the current property-based message for later delivery.

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the message was queued.

### `SetSignCertificateFromStore`

Loads the signing certificate from a certificate store lookup.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sCertificateEmailAddress` | [string](../types/string.md) | yes | Email address used to search the certificate store. |
| `sCertificateStoreName` | [string](../types/string.md) | yes | Store name. Valid values are `AddressBook`, `AuthRoot`, `CertificateAuthority`, `Disallowed`, `My`, `Root`, `TrustedPeople`, and `TrustedPublisher`. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when a signing certificate was found and loaded.

### `SetEncryptCertificateFromStore`

Loads the encryption certificate from a certificate store lookup.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sCertificateEmailAddress` | [string](../types/string.md) | yes | Email address used to search the certificate store. |
| `sCertificateStoreName` | [string](../types/string.md) | yes | Store name. Valid values are `AddressBook`, `AuthRoot`, `CertificateAuthority`, `Disallowed`, `My`, `Root`, `TrustedPeople`, and `TrustedPublisher`. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when an encryption certificate was found and loaded.

### `SetSignCertificateFromPath`

Loads the signing certificate from a certificate file.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sPathToCertificate` | [string](../types/string.md) | yes | Path to the certificate file. |
| `sCertificatePassword` | [string](../types/string.md) | yes | Password for `.pfx` files. Ignored for non-`.pfx` certificate files. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the signing certificate was loaded.

### `SetEncryptCertificateFromPath`

Loads the encryption certificate from a certificate file.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sPathToCertificate` | [string](../types/string.md) | yes | Path to the certificate file. |
| `sCertificatePassword` | [string](../types/string.md) | yes | Password for `.pfx` files. Ignored for non-`.pfx` certificate files. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) when the encryption certificate was loaded.

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Set `From`, `To`, `Subject`, and `Body` before calling `Send`, `SaveMessage`, or [`SendToOutbox`](../functions/SendToOutbox.md).
    - Set `To` to a non-empty array of recipient addresses.
    - Set `SMTPServerName` and `SMTPServerPort` before calling `Send` or [`SendToOutbox`](../functions/SendToOutbox.md).
    - Use `Email{}` when you want non-throwing behavior and plan to inspect `oEmail:Exception:Description` after a failure.
    - Use `Email{.F.}` inside [`:TRY`](../keywords/TRY.md) and handle failures with [`GetLastSSLError()`](../functions/GetLastSSLError.md) when the script should stop on email errors.
    - Validate attachment paths and certificate inputs before sending or queueing mail.
    - Use [`SendToOutbox`](../functions/SendToOutbox.md) when delivery should be deferred to later processing.

!!! failure "Don't"
    - Assume `Email{}` raises on failure — it suppresses exceptions by default and returns [`.F.`](../literals/false.md) instead.
    - Leave `To` unset or empty before `Send`, `SaveMessage`, or [`SendToOutbox`](../functions/SendToOutbox.md).
    - Omit required message fields — the message must include `From`, `Subject`, and `Body` before it can be built.
    - Omit `SMTPServerName` or set `SMTPServerPort` to `0` when calling `Send` or [`SendToOutbox`](../functions/SendToOutbox.md) — SMTP validation fails.
    - Rely on `SMTPTimeout` or `LogSMTP` for queued outbox delivery — those settings apply to direct `Send` behavior, not later outbox processing.
    - Pass an invalid certificate store name, an unknown certificate email address, or a missing certificate file — the certificate methods fail and the email cannot be signed or encrypted.
    - Expect `LoadMessage` to populate the editable properties used by `SaveMessage` or [`SendToOutbox`](../functions/SendToOutbox.md) — loaded message content is only reused by `Send`.

## Caveats

- `LoadMessage` and `SaveMessage` require a non-empty file path.
- If `SMTPServerUserName` is empty, `Send` connects without attempting SMTP login.
- After a successful `LoadMessage`, `Send` transmits the loaded message content with the current SMTP settings; `SaveMessage` and [`SendToOutbox`](../functions/SendToOutbox.md) always use the current property values, not the loaded content.

## Examples

### Send a notification email

Shows the basic `Email{}` pattern: set all required properties, call `Send()`, and check the boolean result. Because `Email{}` suppresses exceptions, a failure returns [`.F.`](../literals/false.md) and the error detail is available through `oEmail:Exception:Description`.

```ssl
:PROCEDURE SendNotificationEmail;
	:DECLARE oEmail, bSent;

	oEmail := Email{};

	oEmail:From := "starlims@company.com";
	oEmail:To := {"labtech1@company.com"};
	oEmail:Subject := "Process complete";
	oEmail:Body := "Sample analysis completed successfully.";
	oEmail:IsHTMLBody := .F.;

	oEmail:SMTPServerName := "smtp.company.com";
	oEmail:SMTPServerPort := 587;
	oEmail:SMTPSecureConnection := .T.;
	oEmail:SMTPServerUserName := "starlims@company.com";
	oEmail:SMTPServerUserPassword := "<smtp-password>";
	oEmail:SMTPTimeout := 60;

	bSent := oEmail:Send();

	:IF bSent;
		UsrMes("Notification email sent.");
	:ELSE;
		/* Displays on failure: notification email failed;
		UsrMes("Notification email failed: " 
				+ oEmail:Exception:Description);
	:ENDIF;

	:RETURN bSent;
:ENDPROC;

/* Run the procedure;
DoProc("SendNotificationEmail");
```

### Queue a signed report for outbox delivery

Uses `Email{.F.}` so failures raise exceptions, then wraps the operation in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md). Signs the message with a `.pfx` certificate before queuing it with [`SendToOutbox()`](../functions/SendToOutbox.md). Since `IgnoreExceptions` is [`.F.`](../literals/false.md), certificate load failures propagate to [`:CATCH`](../keywords/CATCH.md) rather than silently returning [`.F.`](../literals/false.md).

```ssl
:PROCEDURE QueueSignedReport;
	:DECLARE oEmail, bQueued, oErr;

	oEmail := Email{.F.};

	oEmail:From := "reports@laboratory.com";
	oEmail:To := {"manager@laboratory.com"};
	oEmail:CC := {"quality@laboratory.com"};
	oEmail:Subject := "Q4 laboratory results";
	oEmail:Body := "The signed report is attached for review.";
	oEmail:Attachments := {"C:/Reports/Q4Results.pdf"};

	oEmail:SMTPServerName := "smtp.laboratory.com";
	oEmail:SMTPServerPort := 587;
	oEmail:SMTPSecureConnection := .T.;
	oEmail:SMTPServerUserName := "reports@laboratory.com";
	oEmail:SMTPServerUserPassword := "<smtp-password>";

	:TRY;
		oEmail:SetSignCertificateFromPath("C:/Certificates/report-signing.pfx",
			"Secret123");

		bQueued := oEmail:SendToOutbox();

		:IF bQueued;
			UsrMes("Signed report queued for delivery.");
		:ELSE;
			/* Displays on failure: email queueing failed;
			UsrMes("Email queueing failed: " 
					+ oEmail:Exception:Description);
		:ENDIF;

		:RETURN bQueued;

	:CATCH;
		oErr := GetLastSSLError();
		/* Displays on failure: email queueing failed;
		UsrMes("Email queueing failed: " + oErr:Description);

		:RETURN .F.;
	:ENDTRY;
:ENDPROC;

/* Run the procedure;
DoProc("QueueSignedReport");
```

## Related

- [`SSLError`](SSLError.md)
- [`object`](../types/object.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
- [`number`](../types/number.md)
