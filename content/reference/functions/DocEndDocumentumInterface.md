---
title: "DocEndDocumentumInterface"
summary: "Ends the current Documentum interface context."
id: ssl.function.docenddocumentuminterface
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocEndDocumentumInterface

Ends the current Documentum interface context.

`DocEndDocumentumInterface()` closes the active Documentum session context for the current workflow. If the current context has login information, the function logs off that session first and then removes the current context. Use it when your Documentum work is finished so later code does not keep using a stale session. The function takes no parameters and returns [`NIL`](../literals/nil.md).

## When to use

- When you have finished a block of Documentum work and want to close the current session cleanly.
- When a workflow changes to a different Documentum user or repository and must
  discard the previous context first.
- When you place Documentum cleanup in a [`:FINALLY`](../keywords/FINALLY.md) block so the session is closed even after an error.

## Syntax

```ssl
DocEndDocumentumInterface();
```

## Parameters

This function takes no parameters.

## Returns

**NIL** — Always returns [`NIL`](../literals/nil.md).

## Best practices

!!! success "Do"
    - Call this function after the last Documentum operation in a workflow.
    - Put this function in a [`:FINALLY`](../keywords/FINALLY.md) block when a script logs in and then performs multiple Documentum operations.
    - Reinitialize and log in again before any later Documentum work that needs a fresh session.

!!! failure "Don't"
    - Call Documentum functions after this function without reinitializing and logging in again.
    - Treat the [`NIL`](../literals/nil.md) return value as a success flag.
    - Skip cleanup at the end of a workflow that opened a Documentum session.

## Caveats

- The function removes the current Documentum context even when no login has been established yet.
- After it runs, later Documentum operations need a new [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md) call and, when required, a new [`DocLoginToDocumentum`](DocLoginToDocumentum.md) call.

## Examples

### End a session after one Documentum operation

Logs in, checks whether a document exists, displays the result, and then calls `DocEndDocumentumInterface` to close the session, including in the login-failure path.

```ssl
:PROCEDURE CheckDocumentAndClose;
    :DECLARE sDocBase, sUser, sPassword, sDocumentId, bExists;

    sDocBase := "ProductionDB";
    sUser := "doc_user";
    sPassword := "doc_password";
    sDocumentId := "0900000180001234";

    DocInitDocumentumInterface();

    :IF .NOT. DocLoginToDocumentum(sDocBase, sUser, sPassword);
        ErrorMes("Documentum login failed: " + DocGetErrorMessage());
        /* Displays on login failure;
        DocEndDocumentumInterface();

        :RETURN;
    :ENDIF;

    bExists := DocExists(sDocumentId);

    :IF bExists;
        UsrMes("Document exists in Documentum: " + sDocumentId);
    :ELSE;
        UsrMes("Document not found in Documentum: " + sDocumentId);
    :ENDIF;

    DocEndDocumentumInterface();
:ENDPROC;

/* Usage;
DoProc("CheckDocumentAndClose");
```

### Guarantee cleanup in a TRY/CATCH/FINALLY workflow

Places `DocEndDocumentumInterface` in a [`:FINALLY`](../keywords/FINALLY.md) block so the session is always closed whether the export succeeds, fails, or raises an exception.

```ssl
:PROCEDURE ExportDocumentWithCleanup;
    :DECLARE sDocBase, sUser, sPassword, sDocumentId, sExportPath, oErr;

    sDocBase := "ProductionDB";
    sUser := "doc_user";
    sPassword := "doc_password";
    sDocumentId := "0900000180001234";

    DocInitDocumentumInterface();

    :IF .NOT. DocLoginToDocumentum(sDocBase, sUser, sPassword);
        ErrorMes("Documentum login failed: " + DocGetErrorMessage());
        /* Displays on login failure;
        DocEndDocumentumInterface();

        :RETURN;
    :ENDIF;

    :TRY;
        sExportPath := DocExportDocument(sDocumentId);

        UsrMes("Exported document to: " + sExportPath);

    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("Documentum export failed: " + oErr:Description);
        /* Displays on export failure;

    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ExportDocumentWithCleanup");
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`DocLoginToDocumentum`](DocLoginToDocumentum.md)
