---
title: "SendOutlookReminder"
summary: "Sends an Outlook-style meeting invitation email and returns whether delivery succeeded."
id: ssl.function.sendoutlookreminder
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SendOutlookReminder

Sends an Outlook-style meeting invitation email and returns whether delivery succeeded.

`SendOutlookReminder()` builds a calendar meeting request from the supplied dates, subject, summary, location, organizer, and attendee values, then sends it through the specified SMTP server. The function returns [`.T.`](../literals/true.md) when the send completes successfully. When `bIgnoreErrors` is [`.T.`](../literals/true.md), failures are logged and the function returns [`.F.`](../literals/false.md). When `bIgnoreErrors` is [`.F.`](../literals/false.md), the underlying error is raised instead.

## When to use

- When you need recipients to receive a calendar invitation rather than a plain email.
- When a workflow must send one meeting request to one or more attendees.
- When you need SMTP authentication, a custom port, or SSL for the send.
- When the caller needs to choose between fail-fast behavior and a [`.F.`](../literals/false.md) return value.

## Syntax

```ssl
SendOutlookReminder(
    sSMTP,
    dStart,
    dEnd,
    sSubject,
    sSummary,
    sLocation,
    sOrganizerName,
    sOrganizerEmail,
    sAttendeeName,
    sAttendeeEmail,
    [nPort],
    [sUName],
    [sUPass],
    bIgnoreErrors,
    [bUseSSL]
)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sSMTP` | [string](../types/string.md) | yes | — | SMTP server name. Blank values fail the send. |
| `dStart` | [date](../types/date.md) | yes | — | Meeting start date and time. |
| `dEnd` | [date](../types/date.md) | yes | — | Meeting end date and time. |
| `sSubject` | [string](../types/string.md) | yes | — | Subject used for the email and meeting request title. Blank values fail the send. |
| `sSummary` | [string](../types/string.md) | yes | — | Body text included in the invitation details. Blank values fail the send. |
| `sLocation` | [string](../types/string.md) | yes | — | Meeting location text. Pass `""` when you do not want to show a location. |
| `sOrganizerName` | [string](../types/string.md) | yes | — | Organizer display name. Blank values fail the send. |
| `sOrganizerEmail` | [string](../types/string.md) | yes | — | Organizer email address. Blank values fail the send. |
| `sAttendeeName` | [string](../types/string.md) | yes | — | Attendee display name, or a comma-separated list of attendee names. Keep the number of names aligned with `sAttendeeEmail`. |
| `sAttendeeEmail` | [string](../types/string.md) | yes | — | Attendee email address, or a comma-separated list of attendee addresses. Blank values fail the send. |
| `nPort` | [number](../types/number.md) | no | `25` | SMTP port. `0` is also treated as `25`. |
| `sUName` | [string](../types/string.md) | no | `""` | SMTP user name. |
| `sUPass` | [string](../types/string.md) | no | `""` | SMTP password. |
| `bIgnoreErrors` | [boolean](../types/boolean.md) | yes | — | When [`.T.`](../literals/true.md), logs the failure and returns [`.F.`](../literals/false.md). When [`.F.`](../literals/false.md), raises the error instead. |
| `bUseSSL` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Enables SSL for the SMTP connection. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the meeting invitation is sent successfully; [`.F.`](../literals/false.md) when sending fails and `bIgnoreErrors` is [`.T.`](../literals/true.md). Raises an error instead of returning [`.F.`](../literals/false.md) when `bIgnoreErrors` is [`.F.`](../literals/false.md).

## Exceptions

When `bIgnoreErrors` is [`.F.`](../literals/false.md), the function raises instead of returning [`.F.`](../literals/false.md):

| Trigger | Exception message |
| --- | --- |
| `sSMTP` is blank. | `SMTP` |
| `sAttendeeName` or `sAttendeeEmail` is blank. | `attendeeName or attendeeEmail are empty` |
| `sOrganizerName` or `sOrganizerEmail` is blank. | `organizerName or organizerEmail are empty` |
| `sSubject` or `sSummary` is blank. | `subject or summary are empty` |
| Mail delivery fails. | The underlying SMTP exception |

## Best practices

!!! success "Do"
    - Pass non-empty `sSMTP`, `sSubject`, `sSummary`, organizer, and attendee values.
    - Keep comma-separated attendee names and email addresses in the same order and count.
    - Pass `""` for `sLocation` when the invite has no location instead of omitting the parameter.
    - Set `bIgnoreErrors` to [`.F.`](../literals/false.md) when the caller must stop on delivery or configuration failures.
    - Supply `nPort`, `sUName`, `sUPass`, and `bUseSSL` explicitly when your SMTP server requires them.

!!! failure "Don't"
    - Omit `bIgnoreErrors`. It is required and has no default.
    - Pass blank organizer or attendee fields. The function rejects them.
    - Let comma-separated attendee names and email addresses drift out of sync. That can produce failed or mispaired recipients.
    - Assume a [`.F.`](../literals/false.md) return means the function validated everything up front. It only means the send failed and the error was suppressed.

## Caveats

- The function does not validate that comma-separated attendee name and email lists have the same length before building recipients.
- Empty attendee email entries are skipped while the function builds the recipient list.
- The generated invitation includes a built-in 15-minute display reminder.

## Examples

### Send one meeting invitation

Send a calendar invitation for a one-hour meeting to a single attendee using plain SMTP. `bIgnoreErrors` is [`.T.`](../literals/true.md), so the return value indicates whether the send succeeded.

```ssl
:PROCEDURE SendSingleReminder;
    :DECLARE sSMTP, dStart, dEnd, sSubject, sSummary, sLocation;
    :DECLARE sOrganizerName, sOrganizerEmail, sAttendeeName, sAttendeeEmail;
    :DECLARE bSent;

    sSMTP := "mail.example.com";
    dStart := DateFromNumbers(2026, 4, 15, 9, 0, 0, 0, .F.);
    dEnd := DateFromNumbers(2026, 4, 15, 10, 0, 0, 0, .F.);
    sSubject := "Sample Review Meeting";
    sSummary := "Review logged samples and assign follow-up actions.";
    sLocation := "Conference Room B";
    sOrganizerName := "Jane Smith";
    sOrganizerEmail := "jane.smith@example.com";
    sAttendeeName := "John Doe";
    sAttendeeEmail := "john.doe@example.com";

    bSent := SendOutlookReminder(
        sSMTP,
        dStart,
        dEnd,
        sSubject,
        sSummary,
        sLocation,
        sOrganizerName,
        sOrganizerEmail,
        sAttendeeName,
        sAttendeeEmail,
        25,
        "",
        "",
        .T.,
        .F.
    );

    UsrMes("Reminder sent: " + LimsString(bSent));

    :RETURN bSent;
:ENDPROC;

/* Usage;
DoProc("SendSingleReminder");
```

[`UsrMes`](UsrMes.md) displays:

```text
Reminder sent: <T or F>
```

### Send one invite to multiple attendees with SMTP authentication

Pass comma-separated name and email strings to send a single invitation to three attendees. `bIgnoreErrors` is [`.T.`](../literals/true.md), so a failed send returns [`.F.`](../literals/false.md) instead of raising.

```ssl
:PROCEDURE SendTeamReminder;
    :DECLARE sSMTP, dStart, dEnd, sSubject, sSummary, sLocation;
    :DECLARE sOrganizerName, sOrganizerEmail, sAttendeeNames, sAttendeeEmails;
    :DECLARE nPort, sUName, sUPass, bSent;

    sSMTP := "smtp.lab.example.com";
    dStart := DateFromNumbers(2026, 4, 15, 13, 0, 0, 0, .F.);
    dEnd := DateFromNumbers(2026, 4, 15, 14, 0, 0, 0, .F.);
    sSubject := "Quarterly QC Review";
    sSummary := "Review open actions, overdue work, and upcoming sample load.";
    sLocation := "Teams / Room 204";
    sOrganizerName := "Sarah Mitchell";
    sOrganizerEmail := "sarah.mitchell@example.com";
    sAttendeeNames := "John Davis,Maria Garcia,Robert Chen";
    sAttendeeEmails := "john.davis@example.com,maria.garcia@example.com,robert.chen@example.com";
    nPort := 587;
    sUName := "scheduler@example.com";
    sUPass := "smtp-password";

    bSent := SendOutlookReminder(
        sSMTP,
        dStart,
        dEnd,
        sSubject,
        sSummary,
        sLocation,
        sOrganizerName,
        sOrganizerEmail,
        sAttendeeNames,
        sAttendeeEmails,
        nPort,
        sUName,
        sUPass,
        .T.,
        .T.
    );

    :IF .NOT. bSent;
        UsrMes("Meeting request was not sent.");
    :ENDIF;

    :RETURN bSent;
:ENDPROC;

/* Usage;
DoProc("SendTeamReminder");
```

[`UsrMes`](UsrMes.md) displays on failure:

```text
Meeting request was not sent.
```

### Fail fast and inspect the raised error

Pass `bIgnoreErrors` as [`.F.`](../literals/false.md) so any validation or delivery failure raises immediately. Wrap the call in `:TRY;` to inspect the error with [`GetLastSSLError`](GetLastSSLError.md) before deciding how to respond.

```ssl
:PROCEDURE SendCriticalReminder;
    :DECLARE sSMTP, dStart, dEnd, sSubject, sSummary, sLocation;
    :DECLARE sOrganizerName, sOrganizerEmail, sAttendeeName, sAttendeeEmail;
    :DECLARE nPort, sUName, sUPass, bSent, oErr;

    sSMTP := "smtp.secure.example.com";
    dStart := DateFromNumbers(2026, 4, 16, 8, 30, 0, 0, .F.);
    dEnd := DateFromNumbers(2026, 4, 16, 9, 0, 0, 0, .F.);
    sSubject := "Deviation Review";
    sSummary := "Immediate review of the recorded deviation is required.";
    sLocation := "QA Office";
    sOrganizerName := "Quality Lead";
    sOrganizerEmail := "quality.lead@example.com";
    sAttendeeName := "Operations Manager";
    sAttendeeEmail := "ops.manager@example.com";
    nPort := 465;
    sUName := "quality.lead@example.com";
    sUPass := "smtp-password";

    :TRY;
        bSent := SendOutlookReminder(
            sSMTP,
            dStart,
            dEnd,
            sSubject,
            sSummary,
            sLocation,
            sOrganizerName,
            sOrganizerEmail,
            sAttendeeName,
            sAttendeeEmail,
            nPort,
            sUName,
            sUPass,
            .F.,
            .T.
        );
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("Reminder send failed: " + oErr:Description);
        :RETURN .F.;
    :ENDTRY;

    :RETURN bSent;
:ENDPROC;

/* Usage;
DoProc("SendCriticalReminder");
```

[`ErrorMes`](ErrorMes.md) displays on failure:

```text
Reminder send failed: <error description>
```

## Related

- [`SendLimsEmail`](SendLimsEmail.md)
- [`SendFromOutbox`](SendFromOutbox.md)
- [`DateFromNumbers`](DateFromNumbers.md)
- [`GetLastSSLError`](GetLastSSLError.md)
- [`boolean`](../types/boolean.md)
- [`date`](../types/date.md)
- [`string`](../types/string.md)
