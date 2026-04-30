---
title: "DocGetErrorMessage"
summary: "Returns the message text from the current Documentum error state."
id: ssl.function.docgeterrormessage
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocGetErrorMessage

Returns the message text from the current Documentum error state.

Use this function after a Documentum login or Documentum command to read the message from the exception currently stored in the active Documentum interface context. When no exception is recorded in that context, the function returns an empty string.

Reading the message does not clear the stored error state. Other Documentum operations can replace or clear that state, so retrieve the message as soon as you know a call failed.

## When to use

- When a Documentum login or command reports failure and you need readable detail for the user or log.
- When [`DocCommandFailed`](DocCommandFailed.md) is [`.T.`](../literals/true.md) and you want the associated message text.
- When you want to capture the current Documentum error before another Documentum call overwrites it.

## Syntax

```ssl
DocGetErrorMessage()
```

## Parameters

This function takes no parameters.

## Returns

**[string](../types/string.md)** — The current Documentum error message, or `""` when the active Documentum context has no recorded exception.

## Best practices

!!! success "Do"
    - Call `DocGetErrorMessage` immediately after a failed Documentum login or command.
    - Use it together with [`DocCommandFailed`](DocCommandFailed.md) when you need both a failure flag and readable detail.
    - Store the message in a local variable before making another Documentum call.

!!! failure "Don't"
    - Assume older errors are still available after another Documentum operation runs.
    - Treat an empty string as proof that the last business action succeeded.
    - Use this function before initializing the Documentum interface context.

## Caveats

- Documentum login and command execution paths clear the stored exception before they run, then replace it only if an error occurs.
- The returned text comes from the underlying exception message and may vary by environment or failure type.

## Examples

### Show the login failure message

Attempts a Documentum login with bad credentials, reads the error message when the login returns [`.F.`](../literals/false.md), and displays it to the user.

```ssl
:PROCEDURE ShowDocLoginError;
	:DECLARE bLoggedIn, sErrMsg;

	DocInitDocumentumInterface();

	bLoggedIn := DocLoginToDocumentum("Repository", "baduser", "badpass");

	:IF .NOT. bLoggedIn;
		sErrMsg := DocGetErrorMessage();
		UsrMes("Documentum login failed: " + sErrMsg);
		/* Displays login failure details;
	:ENDIF;

	DocEndDocumentumInterface();
:ENDPROC;

/* Usage;
DoProc("ShowDocLoginError");
```

### Capture an import error before the next call

Stores the error message immediately after a failed import so the value is preserved before any subsequent Documentum call could overwrite the error state.

```ssl
:PROCEDURE ImportWithLoggedError;
	:DECLARE sDocId, sErrMsg;

	DocInitDocumentumInterface();

	:TRY;
		:IF .NOT. DocLoginToDocumentum("Repository", "lims_user", "secret");
			ErrorMes("Login failed: " + DocGetErrorMessage());
			/* Displays login failure details;
			:RETURN;
		:ENDIF;

		sDocId := DocImportDocument(
			"C:\\Docs\\Result.pdf",
			"/Standard/Reports/2024",
			"Result.pdf",
			"PDF",
			"",
			""
		);

		:IF DocCommandFailed();
			sErrMsg := DocGetErrorMessage();
			ErrorMes("Import failed: " + sErrMsg);
			/* Displays import failure details;
			:RETURN;
		:ENDIF;

		UsrMes("Imported document ID: " + sDocId);
		/* Displays imported document ID;
	:FINALLY;
		DocEndDocumentumInterface();
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ImportWithLoggedError");
```

### Return both failure state and message from a helper

Encapsulates the [`DocCommandFailed`](DocCommandFailed.md) flag and `DocGetErrorMessage` result in a helper procedure that returns a result object, keeping the calling procedure clean.

```ssl
:PROCEDURE ReadImportStatus;
	:DECLARE oStatus;

	oStatus := CreateUdObject();
	oStatus:failed := DocCommandFailed();
	oStatus:errorMessage := "";

	:IF oStatus:failed;
		oStatus:errorMessage := DocGetErrorMessage();
	:ENDIF;

	:RETURN oStatus;
:ENDPROC;

:PROCEDURE ImportDocumentWithStatus;
	:DECLARE oStatus, sDocId;

	DocInitDocumentumInterface();

	:TRY;
		:IF .NOT. DocLoginToDocumentum("Repository", "lims_user", "secret");
			ErrorMes("Login failed: " + DocGetErrorMessage());
			:RETURN;
		:ENDIF;

		sDocId := DocImportDocument(
			"C:\\Docs\\Result.pdf",
			"/Standard/Reports/2024",
			"Result.pdf",
			"PDF",
			"",
			""
		);

		oStatus := DoProc("ReadImportStatus");

		:IF oStatus:failed;
			ErrorMes("Import failed: " + oStatus:errorMessage);
			/* Displays import failure details;
		:ELSE;
			UsrMes("Imported document ID: " + sDocId);
			/* Displays imported document ID;
		:ENDIF;
	:FINALLY;
		DocEndDocumentumInterface();
	:ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ImportDocumentWithStatus");
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocEndDocumentumInterface`](DocEndDocumentumInterface.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`DocLoginToDocumentum`](DocLoginToDocumentum.md)
- [`string`](../types/string.md)
