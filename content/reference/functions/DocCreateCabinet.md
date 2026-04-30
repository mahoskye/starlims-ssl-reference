---
title: "DocCreateCabinet"
summary: "Creates a Documentum cabinet and returns the string result from the create operation."
id: ssl.function.doccreatecabinet
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocCreateCabinet

Creates a Documentum cabinet and returns the string result from the create operation.

`DocCreateCabinet` takes a required cabinet name and optional cabinet type and ACL values. The surfaced SSL function raises immediately only when `sCabinetName` is [`NIL`](../literals/nil.md). Otherwise it forwards the provided values to the Documentum create call and returns its string result. If that call does not produce a value, the function returns an empty string.

Treat a `""` result as a failed or unusable create result and check it immediately with [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md).

## When to use

- When you need to create a cabinet from SSL code within an active Documentum
  session.
- When you want to supply only a cabinet name and let the Documentum call use its default handling for the optional values.
- When you need to specify a cabinet type or ACL during cabinet creation.

## Syntax

```ssl
DocCreateCabinet(sCabinetName, [sCabinetType], [sAcl])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `sCabinetName` | [string](../types/string.md) | yes | — | Cabinet name passed to the Documentum create call. |
| `sCabinetType` | [string](../types/string.md) | no | omitted | Optional cabinet type passed when supplied. |
| `sAcl` | [string](../types/string.md) | no | omitted | Optional ACL name passed when supplied. |

## Returns

**[string](../types/string.md)** — The string returned by the Documentum cabinet-create call, or an empty string when that call does not return a value.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sCabinetName` is [`NIL`](../literals/nil.md). | `sCabinetName argument cannot be null` |

## Best practices

!!! success "Do"
    - Pass a meaningful cabinet name so the cabinet is easy to identify.
    - Omit `sCabinetType` and `sAcl` when you do not need to override the default behavior.
    - Check for an empty return immediately, then inspect [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) before making another Documentum call.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sCabinetName`; that input raises an immediate error.
    - Assume you must provide all three arguments when only `sCabinetName` is required.
    - Treat an empty returned string as a successful cabinet create result.

## Caveats

- `sCabinetName` is checked only for [`NIL`](../literals/nil.md) at the SSL boundary. Other validation depends on the Documentum call.
- Use this function within an active Documentum session. If the create call fails, inspect [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) before making another Documentum call.

## Examples

### Create one cabinet by name and verify the result

Creates a cabinet using only the required name argument and checks the Documentum failure state when the return value is empty.

```ssl
:PROCEDURE CreateDepartmentCabinet;
	:DECLARE sCabinetName, sCreateResult;

	sCabinetName := "Department Documents";
	sCreateResult := DocCreateCabinet(sCabinetName);

	:IF Empty(sCreateResult);
		:IF DocCommandFailed();
			ErrorMes("Cabinet creation failed: " + DocGetErrorMessage());
			/* Displays on command failure;
		:ELSE;
			ErrorMes("Cabinet creation did not return a result string");
		:ENDIF;
		:RETURN "";
	:ENDIF;

	UsrMes("Cabinet created: " + sCreateResult);

	:RETURN sCreateResult;
:ENDPROC;

/* Usage;
DoProc("CreateDepartmentCabinet");
```

### Create several cabinets with explicit types and collect failures

Iterates a list of name-and-type pairs, creates each cabinet with an explicit type, collects failure objects for empty results, and reports the failure count.

```ssl
:PROCEDURE CreateTypedCabinets;
	:DECLARE aCabinets, aFailures, sCabinetName, sCabinetType, sCreateResult;
	:DECLARE oFailure, nIndex;

	aCabinets := {
		{"QA_Records_2024", "QAWorkflow"},
		{"Archive_2024", "Archive"}
	};
	aFailures := {};

	:FOR nIndex := 1 :TO ALen(aCabinets);
		sCabinetName := aCabinets[nIndex, 1];
		sCabinetType := aCabinets[nIndex, 2];
		sCreateResult := DocCreateCabinet(sCabinetName, sCabinetType);

		:IF Empty(sCreateResult);
			oFailure := CreateUdObject();
			oFailure:cabinetName := sCabinetName;
			oFailure:errorMessage := DocGetErrorMessage();
			AAdd(aFailures, oFailure);
			:LOOP;
		:ENDIF;

		UsrMes("Cabinet created: " + sCabinetName);
	:NEXT;

	:IF ALen(aFailures) > 0;
		ErrorMes("Some cabinets were not created: " + LimsString(ALen(aFailures)));
	:ENDIF;

	:RETURN aFailures;
:ENDPROC;

/* Usage;
DoProc("CreateTypedCabinets");
```

### Validate inputs and pass all three arguments with error handling

Guards against a blank cabinet name, passes all three arguments (name, type, ACL) received as procedure parameters, and distinguishes between a Documentum command failure and a no-value result.

```ssl
:PROCEDURE CreateSecureCabinet;
	:PARAMETERS sCabinetName, sCabinetType, sAcl;
	:DEFAULT sCabinetName, "";
	:DEFAULT sCabinetType, "";
	:DEFAULT sAcl, "";
	:DECLARE oErr, sCreateResult;

	:IF Empty(sCabinetName);
		ErrorMes("Cabinet name is required");
		:RETURN "";
	:ENDIF;

	:TRY;
		sCreateResult := DocCreateCabinet(sCabinetName, sCabinetType, sAcl);
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("DocCreateCabinet raised an error: " + oErr:Description); /* Displays when NIL is passed;
		:RETURN "";
	:ENDTRY;

	:IF Empty(sCreateResult);
		:IF DocCommandFailed();
			ErrorMes("DocCreateCabinet failed: " + DocGetErrorMessage());
			/* Displays on command failure;
		:ELSE;
			ErrorMes("DocCreateCabinet returned an empty result string");
		:ENDIF;
		:RETURN "";
	:ENDIF;

	UsrMes("Cabinet created successfully: " + sCreateResult);

	:RETURN sCreateResult;
:ENDPROC;

/* Usage;
DoProc("CreateSecureCabinet", {"Lab Reports", "QAWorkflow", "LabACL"});
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`string`](../types/string.md)
