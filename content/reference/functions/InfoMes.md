---
title: "InfoMes"
summary: "Logs an informational user message and returns the same formatted string as UsrMes."
id: ssl.function.infomes
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# InfoMes

Logs an informational user message and returns the same formatted string as [`UsrMes`](UsrMes.md).

`InfoMes` uses the same message behavior as [`UsrMes`](UsrMes.md). It accepts the same two arguments, converts them to strings, applies the same fallback handling for empty values, and returns the formatted message text. Unlike [`ErrorMes`](ErrorMes.md), it does not force the message to be written when regular user-message logging is disabled.

## When to use

- When you want code to clearly express that a message is informational rather than an error.
- When you want the same caption-and-detail behavior as [`UsrMes`](UsrMes.md).
- When you want the formatted message string returned to your code.

## Syntax

```ssl
InfoMes(vCaption, [vMessage])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vCaption` | any | yes | — | Caption text, or the message content when `vMessage` is omitted or empty. |
| `vMessage` | any | no | — | Message body or additional detail text. |

## Returns

**[string](../types/string.md)** — The formatted message string. If ordinary user-message logging is disabled, `InfoMes` returns an empty string.

## Best practices

!!! success "Do"
    - Pass a short caption in `vCaption` and the detail text in `vMessage`.
    - Use `InfoMes` for routine progress notes, confirmations, and other non-error messages.
    - Use [`ErrorMes`](ErrorMes.md) when the message must still be written during error handling.

!!! failure "Don't"
    - Use `InfoMes` for failures that must always be recorded.
    - Pass arrays or objects unless their string form is exactly what you want returned and logged.
    - Rely on `InfoMes` as a guaranteed audit mechanism when ordinary user-message logging may be disabled.

## Caveats

- Both arguments are converted to strings before the message is processed.
- If `vCaption` is empty, a default user-message caption is used.
- If `vMessage` is empty, the value from `vCaption` becomes the message body and the caption is reset to the default user-message caption.
- `InfoMes` follows the same write behavior as [`UsrMes`](UsrMes.md), so it can return an empty string when ordinary user-message logging is disabled.

## Examples

### Log a simple informational message

Use a stable caption and a short detail message for routine status reporting.

```ssl
:PROCEDURE ConfirmRegistration;
	:DECLARE sSampleID, sMessage;

	sSampleID := "SMP-2024-0042";
	sMessage := "Sample " + sSampleID + " was registered successfully";

	InfoMes("Registration Complete", sMessage);
:ENDPROC;

/* Usage;
DoProc("ConfirmRegistration");
```

### Capture the returned message text

Store the returned string when later code needs the fully formatted message.

```ssl
:PROCEDURE RecordImportSummary;
	:PARAMETERS sBatchID, nImported;
	:DECLARE sCaption, sMessage, sLogged;

	sCaption := "Import Summary";
	sMessage := "Batch " + sBatchID + " imported ";
	sMessage := sMessage + LimsString(nImported) + " rows";

	sLogged := InfoMes(sCaption, sMessage);

	:RETURN sLogged;
:ENDPROC;

/* Usage;
DoProc("RecordImportSummary", {"BATCH-001", 42});
```

### Report per-item progress in a loop

Use `InfoMes` for per-item progress updates while preserving a final summary for the caller.

```ssl
:PROCEDURE RefreshSampleCache;
	:PARAMETERS aSampleIDs;
	:DECLARE nIndex, sCaption, sMessage, sLastLogged;

	sCaption := "Cache Refresh";
	sLastLogged := "";

	:FOR nIndex := 1 :TO ALen(aSampleIDs);
		sMessage := "Refreshing sample " + aSampleIDs[nIndex];
		sLastLogged := InfoMes(sCaption, sMessage);
	:NEXT;

	sMessage := "Refreshed " + LimsString(ALen(aSampleIDs)) + " samples";
	sLastLogged := InfoMes(sCaption, sMessage);

	:RETURN sLastLogged;
:ENDPROC;

/* Usage;
DoProc("RefreshSampleCache", {{"SMP-001", "SMP-002", "SMP-003"}});
```

## Related

- [`UsrMes`](UsrMes.md)
- [`ErrorMes`](ErrorMes.md)
- [`string`](../types/string.md)
