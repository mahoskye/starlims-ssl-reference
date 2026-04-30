---
title: "UsrMes"
summary: "Writes a user message to the user log and returns the formatted log text."
id: ssl.function.usrmes
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# UsrMes

Writes a user message to the user log and returns the formatted log text.

`UsrMes` takes a caption and an optional message, formats them with runtime context, writes the result to the user log, and returns the full formatted text. The formatted output includes the current user, date, time, product version, execution location, process details, and the final caption.

If `vCaption` is empty, the function uses `****User message****` as the caption. If `vMessage` is empty, the function copies `vCaption` into the message body and still uses `****User message****` as the caption. When user-message logging is disabled, `UsrMes` returns an empty string and does not write anything.

## When to use

- When you want to log a custom user message with metadata for auditing or debugging.
- When you want the formatted log text back for later display or reuse.
- When a message should respect the normal user-message logging setting.
- When you want a non-error message instead of a forced error log entry.

## Syntax

```ssl
UsrMes(vCaption, [vMessage])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vCaption` | any | yes | — | Caption text, or the message content when `vMessage` is omitted or empty. |
| `vMessage` | any | no | [`NIL`](../literals/nil.md) | Message body text. |

## Returns

**[string](../types/string.md)** — The full formatted log text. If user-message logging is disabled, returns an empty string.

## Best practices

!!! success "Do"
    - Pass both `vCaption` and `vMessage` when you want separate caption and message text in the log.
    - Use `UsrMes` for standard user-facing or diagnostic messages that should respect the normal user-message setting.
    - Capture the return value when later code needs the exact formatted text that was logged.

!!! failure "Don't"
    - Rely on empty arguments unless you intentionally want the default `****User message****` caption behavior.
    - Use `UsrMes` when the message must be written even if user-message logging is disabled. Use [`ErrorMes`](ErrorMes.md) for that case.
    - Assume complex values will be rendered in a user-friendly way. The function logs each argument through its string form.

## Caveats

- The returned string contains both the formatted caption line and the message body, separated by blank lines.

## Examples

### Write a caption and message

Pass both arguments to write separate caption and message text to the user log. The function returns the full formatted log entry, which includes runtime metadata such as the current user, date, time, and product version.

```ssl
:PROCEDURE ShowUserNotification;
	:DECLARE sMessageText;

	sMessageText := "Sample login completed successfully";

	UsrMes("Login Status", sMessageText);
:ENDPROC;

/* Usage;
DoProc("ShowUserNotification");
```

### Rely on the default caption

When the second argument is omitted, `UsrMes` uses `****User message****` as the caption and moves the single argument into the message body. Capturing the return value lets later code reuse the formatted log text.

```ssl
:PROCEDURE LogSingleTextMessage;
	:DECLARE sLoggedText;

	sLoggedText := UsrMes("Instrument maintenance completed");

	:IF !Empty(sLoggedText);
		InfoMes("Last user message", sLoggedText); /* Displays returned log text;
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("LogSingleTextMessage");
```

### Build a multi-line audit-style message

Build the message body from dynamic fields first, then log it and return the formatted entry for downstream use. The returned string is suitable for displaying in a second dialog or writing to an external log.

```ssl
:PROCEDURE LogAuditEvent;
	:DECLARE sAction, sAuditBody, sLoggedText;

	sAction := "Released batch 24-0419";
	sAuditBody := "Operator: " + MYUSERNAME + Chr(13) + Chr(10);
	sAuditBody += "Action: " + sAction + Chr(13) + Chr(10);
	sAuditBody += "Logged on: " + DToC(Today()) + " " + Time();

	sLoggedText := UsrMes("Batch Audit", sAuditBody);

	:RETURN sLoggedText;
:ENDPROC;

/* Usage;
DoProc("LogAuditEvent");
```

## Related

- [`ErrorMes`](ErrorMes.md)
- [`InfoMes`](InfoMes.md)
- [`string`](../types/string.md)
