---
title: "GetPrinters"
summary: "Returns a list of printer names currently installed on the system."
id: ssl.function.getprinters
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetPrinters

Returns a list of printer names currently installed on the system.

`GetPrinters` returns the printer names currently available to the running environment. It takes no arguments and returns an array where each element is a printer name string.

If no printers are installed, the function returns an empty array.

## When to use

- When building a printing or report generation workflow that offers users a choice of printer.
- When verifying that a required printer is installed as part of an administration or setup process.
- When automating system diagnostics or logging available printers for troubleshooting.

## Syntax

```ssl
GetPrinters()
```

## Parameters

This function takes no parameters.

## Returns

**[array](../types/array.md)** — An array of printer name strings. Returns an empty array when no printers are installed.

## Best practices

!!! success "Do"
    - Check `ALen(aPrinters)` before assuming a printer is available.
    - Call the function again when you need a fresh printer list after setup or configuration changes.
    - Validate that a required printer name exists before starting printer-dependent work.

!!! failure "Don't"
    - Assume every environment has at least one installed printer.
    - Treat an old printer list as current after printer configuration has changed.
    - Start a print workflow without first confirming that the expected printer is present.

## Caveats

- Results depend on the printers installed on the machine where the function runs.

## Examples

### List available printers for user selection

Gets the current printer list and displays each name, or shows a no-printer message when the array is empty.

```ssl
:PROCEDURE ShowPrinterList;
	:DECLARE aPrinters, nIndex, sPrinterList;

	aPrinters := GetPrinters();

	:IF ALen(aPrinters) == 0;
		UsrMes("No printers are currently installed.");
		:RETURN aPrinters;
	:ENDIF;

	sPrinterList := "Available printers:" + Chr(13) + Chr(10);

	:FOR nIndex := 1 :TO ALen(aPrinters);
		sPrinterList += "- " + aPrinters[nIndex] + Chr(13) + Chr(10);
	:NEXT;

	UsrMes(sPrinterList);  /* Displays available printer names;

	:RETURN aPrinters;
:ENDPROC;

/* Usage;
DoProc("ShowPrinterList");
```

### Validate printer presence before a printer-dependent task

Uses [`AScan`](AScan.md) to check whether a required printer name appears in the returned list, returning [`.T.`](../literals/true.md) or [`.F.`](../literals/false.md) accordingly.

```ssl
:PROCEDURE ValidateRequiredPrinter;
	:PARAMETERS sRequiredPrinter;
	:DECLARE aPrinters, nPos;

	aPrinters := GetPrinters();
	nPos := AScan(aPrinters, sRequiredPrinter);

	:IF nPos > 0;
		UsrMes("Printer is available: " + sRequiredPrinter);
		/* Displays when found;
		:RETURN .T.;
	:ENDIF;

	UsrMes("Printer is not installed: " + sRequiredPrinter);
	/* Displays when absent;
	:RETURN .F.;
:ENDPROC;

/* Usage;
DoProc("ValidateRequiredPrinter", {"HP LaserJet Pro M404dn"});
```

### Compare printer snapshots after configuration changes

Captures the printer list before and after a configuration step, then computes which printers were added or removed by checking each snapshot against the other.

```ssl
:PROCEDURE ComparePrinterSnapshots;
	:DECLARE aBefore, aAfter, aAdded, aRemoved, oDiff;
	:DECLARE sPrinter, nIndex;

	aBefore := GetPrinters();

	/* Run printer setup or ask the user to refresh device mappings;

	aAfter := GetPrinters();
	aAdded := {};
	aRemoved := {};

	:FOR nIndex := 1 :TO ALen(aAfter);
		sPrinter := aAfter[nIndex];
		:IF AScan(aBefore, sPrinter) == 0;
			AAdd(aAdded, sPrinter);
		:ENDIF;
	:NEXT;

	:FOR nIndex := 1 :TO ALen(aBefore);
		sPrinter := aBefore[nIndex];
		:IF AScan(aAfter, sPrinter) == 0;
			AAdd(aRemoved, sPrinter);
		:ENDIF;
	:NEXT;

	oDiff := CreateUdObject();
	oDiff:addedPrinters := aAdded;
	oDiff:removedPrinters := aRemoved;
	oDiff:beforeCount := ALen(aBefore);
	oDiff:afterCount := ALen(aAfter);

	:RETURN oDiff;
:ENDPROC;

/* Usage;
DoProc("ComparePrinterSnapshots");
```

## Related

- [`array`](../types/array.md)
- [`string`](../types/string.md)
