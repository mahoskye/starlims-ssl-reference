---
title: "IsProductionModeOn"
summary: "Returns .T. when the application's production mode flag is enabled and .F. otherwise."
id: ssl.function.isproductionmodeon
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# IsProductionModeOn

Returns [`.T.`](../literals/true.md) when the application's production mode flag is enabled and [`.F.`](../literals/false.md) otherwise.

`IsProductionModeOn` reads the environment configuration set at startup. It takes no parameters and raises no exceptions. Use it to enable stricter behavior, suppress diagnostic output, or restrict features to production environments.

## When to use

- When you need to enforce stricter operations, security rules, or feature flags only in production environments.
- When logging, diagnostics, or debug utilities should behave differently between production and non-production environments.
- When displaying UI indicators or restricting user actions based on whether the system is in production mode.
- When implementing environment-specific code branches where production configuration requires unique handling.

## Syntax

```ssl
IsProductionModeOn()
```

## Parameters

This function takes no parameters.

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) if the application is running in production mode; [`.F.`](../literals/false.md) otherwise.

## Best practices

!!! success "Do"
    - Use this function to clearly separate code paths that should only run in production environments.
    - Combine this function with logging or error-handling logic for environments where stricter compliance is necessary.

!!! failure "Don't"
    - Rely on it for detailed environment distinctions beyond production vs. non-production. The function provides only a binary [`.T.`](../literals/true.md)/[`.F.`](../literals/false.md) value and does not distinguish between various non-production modes.
    - Use it as a substitute for user authentication or license validation logic. Production mode only reflects the application environment, not user rights or licenses.

## Caveats

- Returns only production vs. non-production — it does not indicate which specific non-production environment is active (e.g., development, staging).
- Changes to the production mode status require a configuration update and restart; the result does not reflect real-time changes during a session.
- This function does not validate license types or features.

## Examples

### Show a warning badge only in production

Display a caution message when the environment is production so users know they are not in a safe sandbox. The message fires only when `bIsProduction` is [`.T.`](../literals/true.md).

```ssl
:PROCEDURE ShowProductionBadge;
	:DECLARE bIsProduction, sBadgeMessage;

	bIsProduction := IsProductionModeOn();

	:IF bIsProduction;
		sBadgeMessage := "PRODUCTION MODE ACTIVE - Exercise caution";
		UsrMes(sBadgeMessage);
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("ShowProductionBadge");
```

### Suppress debug logging in production

Allow detailed trace output only in non-production environments to protect performance and sensitive data. The log entry fires only when `bIsProd` is [`.F.`](../literals/false.md).

```ssl
:PROCEDURE LogIfNotProduction;
	:DECLARE sModule, sMessage, sLogEntry, bIsProd;

	bIsProd := IsProductionModeOn();
	sModule := "DataProcessing";
	sMessage := "Processing batch of 500 records";

	:IF ! bIsProd;
		sLogEntry := "[" + sModule + "] DEBUG: " + sMessage;
		UsrMes(sLogEntry);
	:ENDIF;

	:RETURN;
:ENDPROC;

/* Usage;
DoProc("LogIfNotProduction");
```

### Enforce role-based access in production

Apply stricter role validation in production while allowing any user through in non-production. The procedure returns [`.T.`](../literals/true.md) if access is granted and [`.F.`](../literals/false.md) if it is denied.

```ssl
:PROCEDURE ValidateApiEndpoint;
	:DECLARE bIsProduction, bAccessGranted, sEndpoint, sUserRole;
	:DECLARE sRequiredRole, sValidationMsg;

	bAccessGranted := .F.;
	sUserRole := "analyst";
	sRequiredRole := "supervisor";
	sEndpoint := "lims.api.samples.submit";

	bIsProduction := IsProductionModeOn();

	:IF bIsProduction;
		:IF sUserRole == sRequiredRole;
			bAccessGranted := .T.;
			sValidationMsg := "Access granted: role verified in production";
		:ELSE;
			bAccessGranted := .F.;
			sValidationMsg := "Access denied: elevated role required in production for " + sEndpoint;
		:ENDIF;
	:ELSE;
		bAccessGranted := .T.;
		sValidationMsg := "Access granted in non-production environment";
	:ENDIF;

	UsrMes(sValidationMsg);  /* Displays access result;

	:RETURN bAccessGranted;
:ENDPROC;

/* Usage;
DoProc("ValidateApiEndpoint");
```

## Related

- [`InBatchProcess`](InBatchProcess.md)
- [`boolean`](../types/boolean.md)
