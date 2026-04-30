---
title: "ErrorMes"
summary: "Logs an error message and returns the resulting message string."
id: ssl.function.errormes
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ErrorMes

Logs an error message and returns the resulting message string.

`ErrorMes` converts both arguments to strings and passes them to the same message path as [`UsrMes`](UsrMes.md), but with forced writing enabled. Use it when a failure message must be persisted even if regular user-message logging is disabled.

## When to use

- When a failure or exception must always be written through the message system.
- When you want the same two-part caption/message pattern as [`UsrMes`](UsrMes.md), but with forced logging.
- When you still want the resulting message string returned to your code.

## Syntax

```ssl
ErrorMes(vCaption, vMessage)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vCaption` | any | yes | — | Caption or lead text for the error message. |
| `vMessage` | any | yes | — | Message body or detail text. |

## Returns

**[string](../types/string.md)** — The string returned by the underlying message routine after the error message is processed.

## Best practices

!!! success "Do"
    - Pass clear string values for the caption and detail text.
    - Use `ErrorMes` for failures that must be written even when normal user-message logging is not enough.
    - In [`:CATCH`](../keywords/CATCH.md) blocks, log the `:Description` value from [`GetLastSSLError`](GetLastSSLError.md) so the stored message contains the runtime error text.

!!! failure "Don't"
    - Use `ErrorMes` for routine status updates or non-critical notices. Prefer [`UsrMes`](UsrMes.md) or [`InfoMes`](InfoMes.md) for non-error messaging.
    - Pass arrays or objects unless their string form is exactly what you want recorded.
    - Rely on undocumented formatting details beyond the fact that it behaves like [`UsrMes`](UsrMes.md) with forced writing enabled.

## Caveats

- Additional formatting details are not documented, so rely on the returned string and the fact that the message is written.

## Examples

### Log a validation failure

Log a simple validation error and keep the returned message string.

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

`ErrorMes` displays:

```text
Validation Failed: Sample S-001 is missing a result value
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

`ErrorMes` displays:

```text
SaveResult failed: Sample S-001: <error description>
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

`ErrorMes` displays:

```text
Batch approval failed: BATCH-001 rolled back: <error description>
```

## Related

- [`UsrMes`](UsrMes.md)
- [`InfoMes`](InfoMes.md)
- [`string`](../types/string.md)
