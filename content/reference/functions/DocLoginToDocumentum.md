---
title: "DocLoginToDocumentum"
summary: "Authenticates to a Documentum repository for the current initialized Documentum context."
id: ssl.function.doclogintodocumentum
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocLoginToDocumentum

Authenticates to a Documentum repository for the current initialized Documentum context.

`DocLoginToDocumentum` attempts a login by using the repository name, user name, and password you provide. It returns [`.T.`](../literals/true.md) when the login succeeds and [`.F.`](../literals/false.md) when the login attempt fails.

This function does not create the Documentum context itself. Call [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md) first, then use `DocLoginToDocumentum` before calling other Documentum functions that require an authenticated session.

## When to use

- Before calling Documentum functions that need an authenticated connection.
- When you need to connect to a specific Documentum repository as a specific user.
- When you want to check login success directly and then inspect the current Documentum error state if the login fails.

## Syntax

```ssl
DocLoginToDocumentum(sDocBase, sUser, sPassword)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sDocBase` | [string](../types/string.md) | yes | — | Documentum repository name to log in to. |
| `sUser` | [string](../types/string.md) | yes | — | User name for the Documentum login. |
| `sPassword` | [string](../types/string.md) | yes | — | Password for the Documentum login. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the login succeeds. [`.F.`](../literals/false.md) when the login attempt fails.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sDocBase` is [`NIL`](../literals/nil.md). | `sDocBase argument cannot be null` |
| `sUser` is [`NIL`](../literals/nil.md). | `sUser argument cannot be null` |
| `sPassword` is [`NIL`](../literals/nil.md). | `sPassword argument cannot be null` |

## Best practices

!!! success "Do"
    - Call [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md) before `DocLoginToDocumentum`.
    - Check the boolean return value immediately and read [`DocGetErrorMessage`](DocGetErrorMessage.md) right away when the login fails.
    - Close the Documentum context with [`DocEndDocumentumInterface`](DocEndDocumentumInterface.md) when the work is finished.

!!! failure "Don't"
    - Call this function before initializing the Documentum interface context.
    - Continue with other Documentum operations after a [`.F.`](../literals/false.md) result.
    - Wait until later in the workflow to inspect the failure state, because another Documentum call can replace it.

## Caveats

- The current Documentum error state is cleared before the login attempt runs.
- A later Documentum call can replace the current failure state and message.

## Examples

### Log in and branch on success

Initializes the Documentum context, attempts a login, and uses [`:TRY`](../keywords/TRY.md)/[`:FINALLY`](../keywords/FINALLY.md) to ensure the context is always ended regardless of the login outcome.

```ssl
:PROCEDURE LoginToDocumentum;
    :DECLARE sDocBase, sUser, sPassword, bLoggedIn;

    sDocBase := "Repository1";
    sUser := "doc_user";
    sPassword := "secret";

    DocInitDocumentumInterface();

    :TRY;
        bLoggedIn := DocLoginToDocumentum(sDocBase, sUser, sPassword);

        :IF .NOT. bLoggedIn;
            ErrorMes("Documentum login failed: " + DocGetErrorMessage());
            /* Displays on failure;
            :RETURN .F.;
        :ENDIF;

        UsrMes("Connected to " + sDocBase);
        /* Displays on success;

        :RETURN .T.;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("LoginToDocumentum");
```

### Capture the recorded failure state

Reads both the boolean return value and [`DocCommandFailed`](DocCommandFailed.md) after a failed login, showing that the two signals can be checked together to confirm the failure.

```ssl
:PROCEDURE CheckDocumentumLoginFailure;
    :DECLARE sDocBase, sUser, sPassword;
    :DECLARE bLoggedIn, bFailed, sErrMsg;

    sDocBase := "Repository1";
    sUser := "baduser";
    sPassword := "badpass";

    DocInitDocumentumInterface();

    :TRY;
        bLoggedIn := DocLoginToDocumentum(sDocBase, sUser, sPassword);
        bFailed := DocCommandFailed();

        :IF .NOT. bLoggedIn .AND. bFailed;
            sErrMsg := DocGetErrorMessage();
            UsrMes("Login failed: " + sErrMsg);
            :RETURN .F.;
        :ENDIF;

        :RETURN bLoggedIn;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("CheckDocumentumLoginFailure");
```

[`UsrMes`](UsrMes.md) displays:

```text
Login failed: <Documentum error message>
```

### Reinitialize and log in to a different repository

Connects to two different repositories in sequence by ending and reinitializing the Documentum context between logins.

```ssl
:PROCEDURE SwitchDocumentumRepository;
    :DECLARE sFirstBase, sSecondBase, sUser, sPassword;
    :DECLARE bLoggedIn;

    sFirstBase := "Repository1";
    sSecondBase := "Repository2";
    sUser := "doc_user";
    sPassword := "secret";

    DocInitDocumentumInterface();

    :TRY;
        bLoggedIn := DocLoginToDocumentum(sFirstBase, sUser, sPassword);

        :IF .NOT. bLoggedIn;
            ErrorMes("First login failed: " + DocGetErrorMessage());
            /* Displays after first failure;
            :RETURN .F.;
        :ENDIF;

        UsrMes("Connected to " + sFirstBase);
        /* Displays after first login;

        DocEndDocumentumInterface();
        DocInitDocumentumInterface();

        bLoggedIn := DocLoginToDocumentum(sSecondBase, sUser, sPassword);

        :IF .NOT. bLoggedIn;
            ErrorMes("Second login failed: " + DocGetErrorMessage());
            /* Displays after second failure;
            :RETURN .F.;
        :ENDIF;

        UsrMes("Connected to " + sSecondBase);
        /* Displays after second login;

        :RETURN .T.;
    :FINALLY;
        DocEndDocumentumInterface();
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("SwitchDocumentumRepository");
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocEndDocumentumInterface`](DocEndDocumentumInterface.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
