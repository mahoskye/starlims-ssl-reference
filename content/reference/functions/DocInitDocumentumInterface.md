---
title: "DocInitDocumentumInterface"
summary: "Creates a fresh Documentum interface context for the current execution."
id: ssl.function.docinitdocumentuminterface
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocInitDocumentumInterface

Creates a fresh Documentum interface context for the current execution.

`DocInitDocumentumInterface` starts a new Documentum context that later Documentum functions use. It does not log in, accept configuration, or return a status value. Call it before [`DocLoginToDocumentum`](DocLoginToDocumentum.md) or other Documentum operations that depend on an initialized context.

## When to use

- At the start of a block of work that will call Documentum functions.
- Before calling [`DocLoginToDocumentum`](DocLoginToDocumentum.md).
- When you need to discard the current Documentum context and start a new one.

## Syntax

```ssl
DocInitDocumentumInterface();
```

## Parameters

This function takes no parameters.

## Returns

**NIL** — Always returns [`NIL`](../literals/nil.md).

## Best practices

!!! success "Do"
    - Call this function once before the first Documentum login or operation in a workflow.
    - Pair it with [`DocEndDocumentumInterface`](DocEndDocumentumInterface.md) when the Documentum work is finished.
    - Reinitialize explicitly when you want to throw away the current Documentum context and start over.

!!! failure "Don't"
    - Treat the [`NIL`](../literals/nil.md) return value as a success flag.
    - Skip initialization and then call login or other Documentum functions against an uninitialized context.
    - Reinitialize in the middle of a workflow unless you intend to discard the current Documentum context.

## Caveats

- The new context starts without login information and without a stored Documentum error message.
- Calling it again replaces the current Documentum context with a new one.
- To inspect login or command failures after later Documentum calls, use [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md).

## Examples

### Initialize before logging in

Shows the minimum setup pattern: initializes the Documentum context, attempts a login, reports success or failure, then always ends the context.

```ssl
:PROCEDURE LoginToDocumentum;
    :DECLARE sDocBase, sUser, sPassword, bLoggedIn;

    sDocBase := "ProductionDB";
    sUser := "doc_user";
    sPassword := "doc_password";

    DocInitDocumentumInterface();

    bLoggedIn := DocLoginToDocumentum(sDocBase, sUser, sPassword);

    :IF .NOT. bLoggedIn;
        ErrorMes("Documentum login failed: " + DocGetErrorMessage());
        /* Displays on failure: login failed with an error message;
        DocEndDocumentumInterface();

        :RETURN;
    :ENDIF;

    UsrMes("Documentum login succeeded for " + sUser);

    DocEndDocumentumInterface();
:ENDPROC;

/* Usage;
DoProc("LoginToDocumentum");
```

### Reinitialize to switch between repositories

Demonstrates reconnecting to a second repository by calling `DocInitDocumentumInterface` a second time after ending the first session, discarding the previous context before starting a new one.

```ssl
:PROCEDURE SwitchDocumentumSession;
    :DECLARE sFirstBase, sSecondBase, sUser, sPassword, bLoggedIn;

    sFirstBase := "RepositoryA";
    sSecondBase := "RepositoryB";
    sUser := "doc_user";
    sPassword := "doc_password";

    DocInitDocumentumInterface();

    bLoggedIn := DocLoginToDocumentum(sFirstBase, sUser, sPassword);

    :IF .NOT. bLoggedIn;
        ErrorMes("Initial login failed: " + DocGetErrorMessage());
        /* Displays on failure: first login failed with an error message;
        DocEndDocumentumInterface();

        :RETURN;
    :ENDIF;

    UsrMes("Connected to first repository");

    DocEndDocumentumInterface();

    DocInitDocumentumInterface();

    bLoggedIn := DocLoginToDocumentum(sSecondBase, sUser, sPassword);

    :IF .NOT. bLoggedIn;
        ErrorMes("Second login failed: " + DocGetErrorMessage());
        /* Displays on failure: second login failed with an error message;
        DocEndDocumentumInterface();

        :RETURN;
    :ENDIF;

    UsrMes("Connected to second repository");

    DocEndDocumentumInterface();
:ENDPROC;

/* Usage;
DoProc("SwitchDocumentumSession");
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocEndDocumentumInterface`](DocEndDocumentumInterface.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocLoginToDocumentum`](DocLoginToDocumentum.md)
