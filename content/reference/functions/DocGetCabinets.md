---
title: "DocGetCabinets"
summary: "Returns the cabinet names available from the current Documentum connection."
id: ssl.function.docgetcabinets
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# DocGetCabinets

Returns the cabinet names available from the current Documentum connection.

`DocGetCabinets()` queries Documentum for cabinets and returns a one-dimensional array of strings. Each element is a cabinet name. The function takes no arguments. If the underlying Documentum call does not return a result, SSL receives an empty array.

## When to use

- When you need the current list of available cabinet names before browsing or storing documents.
- When validating a cabinet name selected by a user or loaded from configuration.
- When reconciling Documentum cabinet names with values stored in a STARLIMS table.

## Syntax

```ssl
DocGetCabinets()
```

## Parameters

This function takes no parameters.

## Returns

**[array](../types/array.md)** — A one-dimensional array of strings. Each element is a cabinet name.

## Best practices

!!! success "Do"
    - Check `ALen(aCabinets)` before iterating or validating against the result.
    - Treat the result as a list of names only. If you need more than the name, fetch that data separately.
    - Use [`DocCommandFailed`](DocCommandFailed.md) or [`DocGetErrorMessage`](DocGetErrorMessage.md) when an empty array might indicate a failed Documentum call rather than simply no results.

!!! failure "Don't"
    - Assume the array contains cabinet objects or metadata fields. This function returns names only.
    - Assume the result order is stable. The raw query does not apply an `ORDER BY` clause.
    - Call the function repeatedly inside tight loops when one lookup can be reused.

## Caveats

- An empty result can mean either a Documentum backend failure or an installation with no cabinets. Check [`DocCommandFailed`](DocCommandFailed.md) to distinguish the two.

## Examples

### List all cabinet names

Calls `DocGetCabinets()`, exits early when the result is empty, then prints each cabinet name in turn.

```ssl
:PROCEDURE ListCabinetNames;
    :DECLARE aCabinets, nIndex, sCabinetName;

    aCabinets := DocGetCabinets();

    :IF ALen(aCabinets) == 0;
        UsrMes("No cabinets were returned.");
        :RETURN;
    :ENDIF;

    :FOR nIndex := 1 :TO ALen(aCabinets);
        sCabinetName := aCabinets[nIndex];
        UsrMes("Cabinet: " + sCabinetName); /* Displays each cabinet name;
    :NEXT;
:ENDPROC;

/* Usage;
DoProc("ListCabinetNames");
```

### Validate a configured cabinet name

Searches the cabinet list for a case-insensitive match against a configured name, then checks [`DocCommandFailed`](DocCommandFailed.md) on a negative result to distinguish a backend failure from a genuinely missing cabinet.

```ssl
:PROCEDURE ValidateCabinetName;
    :PARAMETERS sTargetCabinet;
    :DECLARE aCabinets, bExists;

    aCabinets := DocGetCabinets();
    bExists := AScan(
        aCabinets,
        {|sName| Upper(sName) == Upper(sTargetCabinet)}
    ) > 0;

    :IF bExists;
        UsrMes("Cabinet is available: " + sTargetCabinet);
        :RETURN .T.;
    :ENDIF;

    :IF DocCommandFailed();
        ErrorMes("Documentum lookup failed: " + DocGetErrorMessage());
        /* Displays on command failure: lookup failed;
        :RETURN .F.;
    :ENDIF;

    UsrMes("Cabinet was not found: " + sTargetCabinet);
    :RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("ValidateCabinetName", {"QA_Reports"});
```

### Reconcile cabinets against a control table

Fetches the live cabinet list, checks [`DocCommandFailed`](DocCommandFailed.md) immediately, then compares against configured cabinet names from a control table and inserts an audit row for each cabinet that is missing in Documentum.

```ssl
:PROCEDURE AuditConfiguredCabinets;
    :DECLARE aCabinets, aConfigured, aMissing, sCabinetName, nIndex;

    aCabinets := DocGetCabinets();

    :IF DocCommandFailed();
        ErrorMes("Unable to retrieve cabinets: " + DocGetErrorMessage());
        /* Displays on command failure: cabinet retrieval failed;
        :RETURN {};
    :ENDIF;

    aConfigured := LSelect1("SELECT cabinet_name
        FROM doc_cabinet_config
        WHERE active_flag = ?
        ORDER BY cabinet_name
    ",, {"Y"});
    aMissing := {};

    :FOR nIndex := 1 :TO ALen(aConfigured);
        sCabinetName := aConfigured[nIndex, 1];

        :IF AScan(aCabinets, {|sName| Upper(sName) == Upper(sCabinetName)}) == 0;
            AAdd(aMissing, sCabinetName);

            RunSQL("
	            INSERT INTO doc_cabinet_audit (
                    cabinet_name, status
                )
                VALUES (
                    ?, ?
                )
            ",, {sCabinetName, "Missing in Documentum"});
        :ENDIF;
    :NEXT;

    :RETURN aMissing;
:ENDPROC;

/* Usage;
DoProc("AuditConfiguredCabinets");
```

## Related

- [`DocCommandFailed`](DocCommandFailed.md)
- [`DocGetErrorMessage`](DocGetErrorMessage.md)
- [`DocGetFolders`](DocGetFolders.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
