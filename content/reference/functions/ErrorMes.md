---
title: "ErrorMes"
summary: "Writes an error message to the server log, even when user-message logging is disabled, and returns the formatted log entry."
id: ssl.function.errormes
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ErrorMes

Writes an error message to the server log, even when user-message logging is disabled, and returns the formatted log entry.

`ErrorMes` takes a caption and an optional message and formats them the same way as [`UsrMes`](UsrMes.md): a header line of runtime context that ends with the caption, then the message on the next line. Unlike [`UsrMes`](UsrMes.md), it always writes the entry, so use it when a failure message must be persisted even if regular user-message logging is disabled.

With one argument, `ErrorMes(sText)` logs `sText` as the message and uses `****User message****` as the caption. With two arguments, `ErrorMes(sCaption, sMessage)` puts `sCaption` where `****User message****` would be and logs `sMessage` on the next line. Both arguments are converted to strings.

## When to use

- When a failure or exception must always be written to the server log.
- When you want the same caption-and-message pattern as [`UsrMes`](UsrMes.md), but with forced logging.
- When you still want the formatted log entry returned to your code.

## Syntax

```ssl
ErrorMes(vCaption, [vMessage])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vCaption` | any | yes | — | Caption text. When `vMessage` is omitted or empty, this value is logged as the message and the caption is `****User message****`. |
| `vMessage` | any | no | [`NIL`](../literals/nil.md) | Message body, written on the line after the header. |

## Returns

**[string](../types/string.md)** — The full formatted log entry, the same text written to the server log. The entry starts with a header line of slash-separated fields: the current user, the date as `yyyymmdd`, the time, the product version, the script location with its line number, and the server process and machine, ending with the caption. The message follows on the next line, and the entry ends with trailing blank lines. Because `ErrorMes` always writes, it does not return the empty string that [`UsrMes`](UsrMes.md) returns when user-message logging is disabled.

For a one-argument call such as `ErrorMes("Result upload failed")`, the entry has this shape:

```text
<user> / <yyyymmdd> / <hh:mm:ss> / <version> / ServerScript.<category>.<script>.<procedure>() line: <n> / <process> on <server> / ****User message****
Result upload failed
```

## Best practices

!!! success "Do"
    - Pass a short, stable caption and the detail text as two arguments when you want to find the entry by caption in the server log.
    - Use the one-argument form for a quick message when the default `****User message****` caption is acceptable.
    - Use `ErrorMes` for failures that must be written even when normal user-message logging is disabled.
    - In [`:CATCH`](../keywords/CATCH.md) blocks, log the `:Description` value from [`GetLastSSLError`](GetLastSSLError.md) so the stored message contains the runtime error text.

!!! failure "Don't"
    - Use `ErrorMes` for routine status updates or non-critical notices. Prefer [`UsrMes`](UsrMes.md) or [`InfoMes`](InfoMes.md) for non-error messaging.
    - Pass arrays or objects unless their string form is exactly what you want recorded.
    - Parse fields out of the returned header. The user, time, version, script location, and process fields vary between calls and environments.

## Caveats

- The returned string is the whole log entry, not just the text you passed. Keep your own copy of the message text if later code needs it on its own.

## Examples

### Log a single message

Pass one argument when the default caption is enough. The text is logged on the line after the header, and the caption is `****User message****`.

```ssl
:PROCEDURE CheckInstrument;
	:PARAMETERS sInstrumentID, bOnline;

	:IF !bOnline;
		ErrorMes("Instrument " + sInstrumentID + " is offline");

		:RETURN .F.;
	:ENDIF;

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("CheckInstrument", {"HPLC-02", .F.});
```

`ErrorMes` logs:

```text
<user> / <date> / <time> / … / ****User message****
Instrument HPLC-02 is offline
```

### Log a validation failure

Log a validation error with its own caption and return the formatted log entry.

```ssl
:PROCEDURE ValidateResult;
	:PARAMETERS sSampleID, sResult;
	:DECLARE sMessage, sLogged;

	:IF Empty(sResult);
		sMessage := "Sample " + sSampleID + " is missing a result value";
		sLogged := ErrorMes("Validation Failed", sMessage);

		:RETURN sLogged;
	:ENDIF;

	:RETURN "";
:ENDPROC;

/* Usage;
DoProc("ValidateResult", {"S-001", ""});
```

`ErrorMes` logs:

```text
<user> / <date> / <time> / … / Validation Failed
Sample S-001 is missing a result value
```

### Log a caught exception

Capture the runtime error text in a [`:CATCH`](../keywords/CATCH.md) block and write it with a stable caption.

```ssl
:PROCEDURE SaveResult;
	:PARAMETERS sSampleID, sResult;
	:DECLARE oErr, sMessage;

	:TRY;
		:IF Empty(sResult);
			RaiseError("Result text is required");
		:ENDIF;

		DoProc("StoreResult", {sSampleID, sResult});
	:CATCH;
		oErr := GetLastSSLError();
		sMessage := "Sample " + sSampleID + ": " + oErr:Description;
		ErrorMes("SaveResult failed", sMessage);

		:RETURN .F.;
	:ENDTRY;

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("SaveResult", {"S-001", "Positive"});
```

`ErrorMes` logs:

```text
<user> / <date> / <time> / … / SaveResult failed
Sample S-001: <error description>
```

### Log a transaction rollback

Use `ErrorMes` for a critical batch failure where the transaction is rolled back and the failure must be recorded.

```ssl
:PROCEDURE ApproveBatch;
	:PARAMETERS sBatchID, aSampleIDs;
	:DECLARE bCommitted, nIndex, oErr, sMessage;

	bCommitted := .F.;
	BeginLimsTransaction();

	:TRY;
		:FOR nIndex := 1 :TO ALen(aSampleIDs);
			DoProc("ApproveSample", {aSampleIDs[nIndex]});
		:NEXT;

		EndLimsTransaction(, .T.);
		bCommitted := .T.;
	:CATCH;
		oErr := GetLastSSLError();
		sMessage := "Batch " + sBatchID + " rolled back: ";
		sMessage := sMessage + oErr:Description;
		ErrorMes("Batch approval failed", sMessage);
	:FINALLY;
		:IF !bCommitted;
			EndLimsTransaction(, .F.);
		:ENDIF;
	:ENDTRY;

	:RETURN bCommitted;
:ENDPROC;

/* Usage;
DoProc("ApproveBatch", {"BATCH-001", {"S-001", "S-002"}});
```

`ErrorMes` logs:

```text
<user> / <date> / <time> / … / Batch approval failed
Batch BATCH-001 rolled back: <error description>
```

## Related

- [`UsrMes`](UsrMes.md)
- [`InfoMes`](InfoMes.md)
- [`string`](../types/string.md)
