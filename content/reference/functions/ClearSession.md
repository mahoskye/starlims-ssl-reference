---
title: "ClearSession"
summary: "Clears all values from the current session."
id: ssl.function.clearsession
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ClearSession

Clears all values from the current session.

`ClearSession` removes every value currently stored in the active session. It takes no arguments and returns [`NIL`](../literals/nil.md) when the clear operation succeeds.

Unlike [`AddToSession`](AddToSession.md) and [`GetFromSession`](GetFromSession.md), this function does not handle a missing `Session` context silently. If the `Session` public variable is not available in the current execution context, `ClearSession` raises an error instead of returning a fallback value.

## When to use

- When a workflow should start over with no previously stored session values.
- When a logout or user-switch action should remove session-scoped data.
- When temporary session values from an earlier step should not affect later processing.

## Syntax

```ssl
ClearSession();
```

## Parameters

This function has no parameters.

## Returns

**NIL** — Returned after the current session is cleared successfully.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| The `Session` public variable is not available in the current execution context. | `Variable [Session] is undefined!` |

## Best practices

!!! success "Do"
    - Use this function only when you intend to remove all session values.
    - Call it at clear lifecycle boundaries such as logout or workflow reset.
    - Pair it with [`AddToSession`](AddToSession.md) and [`GetFromSession`](GetFromSession.md) when rebuilding session state after a reset.

!!! failure "Don't"
    - Call this function in the middle of a workflow that still depends on existing session values.
    - Use it when you only need to remove one stored value. `ClearSession` removes the entire session, not a single key.
    - Assume it behaves like [`AddToSession`](AddToSession.md) or [`GetFromSession`](GetFromSession.md) when `Session` is unavailable. This function fails instead of falling back silently.

## Caveats

- After `ClearSession` runs, [`GetFromSession`](GetFromSession.md) returns an empty string for any key that was in the cleared session.
- The function expects the `Session` public variable to exist. If your code can run outside normal session-backed request handling, make sure that context is available before calling `ClearSession`.

## Examples

### Clear session during logout

Adds two session values, calls `ClearSession`, then reads back the cleared key to confirm it is gone.

```ssl
:PROCEDURE HandleUserLogout;
	:DECLARE sUserID, sStoredUserID;

	sUserID := "JSMITH";

	AddToSession("UserID", sUserID);
	AddToSession("CurrentView", "PendingWork");

	ClearSession();

	sStoredUserID := GetFromSession("UserID");

	:IF Empty(sStoredUserID);
		UsrMes("Session cleared during logout.");
	:ELSE;
		UsrMes("Session still contains UserID.");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("HandleUserLogout");
```

### Reset session before rebuilding workflow state

Clears stale session values from a previous workflow step, then stores a fresh set of values for the next step.

```ssl
:PROCEDURE RestartOrderReview;
	:DECLARE sOrderNo, sReviewMode, sStoredReviewMode;

	sOrderNo := "WO-2024-0891";
	sReviewMode := "PENDING_REVIEW";

	AddToSession("OrderNo", sOrderNo);
	AddToSession("ReviewMode", "IN_PROGRESS");
	AddToSession("SelectedTab", "History");

	ClearSession();

	AddToSession("OrderNo", sOrderNo);
	AddToSession("ReviewMode", sReviewMode);

	sStoredReviewMode := GetFromSession("ReviewMode");

	:IF sStoredReviewMode == "PENDING_REVIEW";
		UsrMes("Order review restarted with a clean session.");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("RestartOrderReview");
```

## Related

- [`AddToSession`](AddToSession.md)
- [`GetFromSession`](GetFromSession.md)
