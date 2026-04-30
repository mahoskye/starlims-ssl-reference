---
title: "GetFromSession"
summary: "Retrieves the value associated with a specified key from the current user session."
id: ssl.function.getfromsession
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetFromSession

Retrieves the value associated with a specified key from the current user session.

Use `GetFromSession` to read a value that was previously stored in the current session under a string key. Passing [`NIL`](../literals/nil.md) for `sKey` raises an error. If the key does not exist, the function returns an empty string. It also returns an empty string when the `Session` public variable is not available in the current execution context.

## When to use

- When you need to retrieve user-specific values previously stored in the session during a workflow.
- When you want to verify if a session token or temporary flag exists for conditional processing.
- When you need to restore settings or state that was saved between pages or requests.
- When implementing authentication flows that depend on values being retained between HTTP requests.

## Syntax

```ssl
GetFromSession(sKey)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sKey` | [string](../types/string.md) | yes | — | Session key to retrieve the associated value. |

## Returns

**any** — The value stored for `sKey`. Returns an empty string when the key is not present or when session access is unavailable in the current context.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sKey` is [`NIL`](../literals/nil.md). | `Argument: sKey cannot be null.` |

## Best practices

!!! success "Do"
    - Check for an empty result before assuming the key exists.
    - Use stable, descriptive key names so related scripts read the same session entry consistently.
    - Pair session reads with the code paths that create or clear the same keys.

!!! failure "Don't"
    - Assume a missing key will raise an error. `GetFromSession` returns an empty string instead.
    - Pass [`NIL`](../literals/nil.md) as the key. That raises an exception.
    - Treat an empty result as proof that the stored value was intentionally an empty string unless your workflow controls that distinction.

## Caveats

- A genuinely stored empty string is indistinguishable from a missing key based on `GetFromSession` alone.

## Examples

### Retrieve a simple session value

Fetches a value previously stored in the session under a known key and displays it; uses [`LimsString`](LimsString.md) to safely convert the session value to a string for concatenation.

```ssl
:PROCEDURE GetStoredUsername;
	:DECLARE sUserKey, sUserName;

	sUserKey := "preferred_username";
	sUserName := GetFromSession(sUserKey);

	UsrMes("Retrieved username: " + LimsString(sUserName));

	:RETURN sUserName;
:ENDPROC;

/* Usage;
DoProc("GetStoredUsername");
```

[`UsrMes`](UsrMes.md) displays:

```
Retrieved username: jsmith
```

### Guard workflow logic based on a session flag

Reads the `UserName` key and branches on whether it is empty, so the workflow only proceeds when the user has already been authenticated and stored in the session.

```ssl
:PROCEDURE ProcessUserWorkflow;
	:DECLARE sUserName, bIsAuthenticated;

	sUserName := GetFromSession("UserName");
	bIsAuthenticated := !Empty(sUserName);

	:IF bIsAuthenticated;
		UsrMes("Welcome, " + sUserName + ". Proceeding with workflow.");
	:ELSE;
		UsrMes("Access denied. Please log in before proceeding.");
	:ENDIF;

	:RETURN bIsAuthenticated;
:ENDPROC;

/* Usage;
DoProc("ProcessUserWorkflow");
```

### Assemble a settings summary from several session keys

Reads multiple keys in one procedure, substitutes defaults for any that are missing, and builds a single summary string for downstream workflow logic.

```ssl
:PROCEDURE RestoreUserPreferences;
	:DECLARE sUserName, sReviewMode, sPageSize;
	:DECLARE sMessage;

	sUserName := GetFromSession("UserName");
	sReviewMode := GetFromSession("ReviewMode");
	sPageSize := GetFromSession("PageSize");

	sMessage := "User=" + LimsString(sUserName);

	:IF Empty(sReviewMode);
		sMessage += ", mode=default";
	:ELSE;
		sMessage += ", mode=" + LimsString(sReviewMode);
	:ENDIF;

	:IF Empty(sPageSize);
		sMessage += ", page size=system default";
	:ELSE;
		sMessage += ", page size=" + LimsString(sPageSize);
	:ENDIF;

	UsrMes(sMessage);

	:RETURN sMessage;
:ENDPROC;

/* Usage;
DoProc("RestoreUserPreferences");
```

[`UsrMes`](UsrMes.md) displays:

```
User=jsmith, mode=read-only, page size=25
```

## Related

- [`AddToSession`](AddToSession.md)
- [`ClearSession`](ClearSession.md)
- [`string`](../types/string.md)
