---
title: "EndLimsOleConnect"
summary: "Disposes an object previously created for OLE automation use."
id: ssl.function.endlimsoleconnect
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# EndLimsOleConnect

Disposes an object previously created for OLE automation use.

`EndLimsOleConnect` releases an OLE automation object created by [`LimsOleConnect`](LimsOleConnect.md) and returns an empty string. Use it as the normal cleanup step after you finish using the automation object.

## When to use

- When you have finished using an object returned by [`LimsOleConnect`](LimsOleConnect.md).
- When you want cleanup to happen explicitly instead of waiting for later runtime cleanup.
- When you are putting OLE automation work inside a [`:TRY`](../keywords/TRY.md) / [`:FINALLY`](../keywords/FINALLY.md) pattern.

## Syntax

```ssl
EndLimsOleConnect([oConnection])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `oConnection` | [object](../types/object.md) | no | [`NIL`](../literals/nil.md) | OLE automation object to release, typically the value returned by [`LimsOleConnect`](LimsOleConnect.md) |

## Returns

**[string](../types/string.md)** — Always returns an empty string

## Best practices

!!! success "Do"
    - Pair [`LimsOleConnect`](LimsOleConnect.md) with `EndLimsOleConnect` in the same workflow.
    - Keep cleanup near the code that creates the automation object.
    - Prefer a [`:FINALLY`](../keywords/FINALLY.md) block when later statements might fail.

!!! failure "Don't"
    - Leave OLE automation objects undisposed after use. That can keep external resources alive longer than intended.
    - Assume this function validates that the object came from the expected ProgID or automation server. It only performs the cleanup step for OLE automation objects.
    - Use repeated cleanup calls as a control-flow signal. The function's documented contract is disposal plus an empty-string return value, not a status report.

## Caveats

- If `oConnection` is not an OLE automation object, the function skips cleanup and still returns an empty string.

## Examples

### Release an OLE automation object

Create an automation object, use it, and then release it explicitly.

```ssl
:PROCEDURE ShowExcelVersion;
    :DECLARE oExcel, sVersion;

    oExcel := LimsOleConnect("Excel.Application");
    sVersion := "Excel version: " + LimsString(oExcel:Version);

    UsrMes(sVersion);

    EndLimsOleConnect(oExcel);
:ENDPROC;

/* Usage;
DoProc("ShowExcelVersion");
```

[`UsrMes`](UsrMes.md) displays:

```text
Excel version: <version>
```

The version string reflects the installed Excel version and differs per environment.

### Clean up in a [`:FINALLY`](../keywords/FINALLY.md) block

Release the automation object even when later work raises an error.

```ssl
:PROCEDURE ExportWithOleCleanup;
    :DECLARE oExcel, sWorkbookPath, oErr;

    sWorkbookPath := "C:\\Temp\\results.xlsx";
    oExcel := NIL;

    :TRY;
        oExcel := LimsOleConnect("Excel.Application");
        oExcel:Visible := .F.;
        oExcel:Workbooks:Add();
        oExcel:ActiveWorkbook:SaveAs(sWorkbookPath);

        UsrMes("Workbook saved to " + sWorkbookPath);
        /* Displays saved workbook path;
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("OLE export failed: " + oErr:Description);
        /* Displays on failure: OLE export failed;
    :FINALLY;
        EndLimsOleConnect(oExcel);
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ExportWithOleCleanup");
```

## Related

- [`LimsOleConnect`](LimsOleConnect.md)
- [`object`](../types/object.md)
- [`string`](../types/string.md)
