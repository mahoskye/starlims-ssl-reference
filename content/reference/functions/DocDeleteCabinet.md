---
title: "DocDeleteCabinet"
summary: "Deletes a Documentum cabinet by cabinet identifier."
id: ssl.function.docdeletecabinet
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocDeleteCabinet

Deletes a Documentum cabinet by cabinet identifier.

`DocDeleteCabinet` takes a required `sCabinetId` and an optional `bDeepDelete` flag. If you omit `bDeepDelete`, the function uses [`.T.`](../literals/true.md). The function returns [`.T.`](../literals/true.md) when the delete succeeds and [`.F.`](../literals/false.md) when the Documentum operation fails.

Passing [`NIL`](../literals/nil.md) for `sCabinetId` raises an immediate SSL argument error. Other delete failures return [`.F.`](../literals/false.md) and leave details in the current Documentum error state, which you can inspect with [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md).

## When to use

- When you need a boolean success result for a cabinet delete attempt.
- When you want the default delete behavior without passing the second argument.
- When your code will inspect the current Documentum error state immediately after a failed delete.

## Syntax

```ssl
DocDeleteCabinet(sCabinetId, [bDeepDelete])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sCabinetId` | [string](../types/string.md) | yes | — | Cabinet reference to delete. |
| `bDeepDelete` | [boolean](../types/boolean.md) | no | [`.T.`](../literals/true.md) | Delete mode flag passed to the Documentum cabinet delete operation. If omitted, the function uses [`.T.`](../literals/true.md). |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the cabinet delete succeeds. [`.F.`](../literals/false.md) when the backend delete call fails.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sCabinetId` is [`NIL`](../literals/nil.md). | `sCabinetId argument cannot be null` |

## Best practices

!!! success "Do"
    - Check the boolean result immediately after the call.
    - Pass `bDeepDelete` explicitly when your workflow depends on a specific delete mode.
    - Read [`DocCommandFailed`](DocCommandFailed.md) and [`DocGetErrorMessage`](DocGetErrorMessage.md) right after a [`.F.`](../literals/false.md) result when you need the failure details from this delete attempt.
    - Use this within an initialized Documentum session.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `sCabinetId`; that raises an immediate SSL argument error.
    - Treat [`.F.`](../literals/false.md) as self-describing; inspect the stored Documentum error state if you need to know why the delete failed.
    - Delay reading the Documentum error state after a failed delete. A later Documentum call can replace it.

## Caveats

- Only [`NIL`](../literals/nil.md) is checked by the SSL wrapper before the delete call is made.
- Backend delete failures return [`.F.`](../literals/false.md) instead of raising a second documented SSL exception from this function.
- This function relies on the current Documentum session state.

## Examples

### Delete one cabinet using the default recursive behavior

Deletes a cabinet by ID using the default deep-delete mode and displays either a success message or the Documentum error when the call returns [`.F.`](../literals/false.md).

```ssl
:PROCEDURE DeleteObsoleteCabinet;
	:PARAMETERS sCabinetId;
	:DEFAULT sCabinetId, "ARCHIVE_2020";
	:DECLARE bDeleted;

	bDeleted := DocDeleteCabinet(sCabinetId);

	:IF .NOT. bDeleted;
		:IF DocCommandFailed();
			ErrorMes("Cabinet delete failed: " + DocGetErrorMessage());
			/* Displays on failure: cabinet delete failed;
		:ENDIF;

		:RETURN .F.;
	:ENDIF;

	UsrMes("Cabinet deleted: " + sCabinetId);

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("DeleteObsoleteCabinet", {"ARCHIVE_2020"});
```

### Pass [`.F.`](../literals/false.md) for `bDeepDelete` to use the non-default delete mode

Passes [`.F.`](../literals/false.md) for `bDeepDelete` to use non-recursive delete mode, then displays either a success message or the Documentum error when the call fails.

```ssl
:PROCEDURE DeleteEmptyCabinetOnly;
	:PARAMETERS sCabinetId;
	:DECLARE bDeleted, sErrMsg;

	bDeleted := DocDeleteCabinet(sCabinetId, .F.);

	:IF bDeleted;
		UsrMes("Empty cabinet deleted: " + sCabinetId);
		:RETURN .T.;
	:ENDIF;

	:IF DocCommandFailed();
		sErrMsg := DocGetErrorMessage();
		ErrorMes("Cabinet delete failed: " + sErrMsg);
		/* Displays on failure: cabinet delete failed;
	:ENDIF;

	:RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("DeleteEmptyCabinetOnly", {"ARCHIVE-2023"});
```

### Delete multiple cabinets and collect per-cabinet failure details

Iterates a list of cabinet IDs, attempts each delete, and collects a failure object — including any Documentum error message — for every cabinet that was not deleted successfully.

```ssl
:PROCEDURE DeleteCabinetsBatch;
	:DECLARE aCabinetIds, aFailures, oFailure, sCabinetId, sErrMsg, nIndex;

	aCabinetIds := {"ARCHIVE-2023", "ARCHIVE-2024", "ARCHIVE-2025"};
	aFailures := {};

	:FOR nIndex := 1 :TO ALen(aCabinetIds);
		sCabinetId := aCabinetIds[nIndex];

		:IF DocDeleteCabinet(sCabinetId);
			:LOOP;
		:ENDIF;

		sErrMsg := "";

		:IF DocCommandFailed();
			sErrMsg := DocGetErrorMessage();
		:ENDIF;

		oFailure := CreateUdObject();
		oFailure:cabinetId := sCabinetId;
		oFailure:errorMessage := sErrMsg;
		AAdd(aFailures, oFailure);
	:NEXT;

	:RETURN aFailures;
:ENDPROC;

/* Usage;
DoProc("DeleteCabinetsBatch");
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocDeleteFolder`](DocDeleteFolder.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocInitDocumentumInterface`](DocInitDocumentumInterface.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
