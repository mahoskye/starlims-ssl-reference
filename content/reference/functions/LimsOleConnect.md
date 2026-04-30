---
title: "LimsOleConnect"
summary: "Creates an object from a ProgID so SSL code can work with an OLE or COM automation server."
id: ssl.function.limsoleconnect
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LimsOleConnect

Creates an object from a ProgID so SSL code can work with an OLE or COM automation server.

`LimsOleConnect` converts its argument to text, resolves that text as a ProgID, and creates the corresponding object. In the usual OLE or COM automation case, the returned value exposes the server's properties and methods through normal SSL object syntax.

Use this function when SSL needs to drive an external automation server such as Excel, Word, or another ProgID-based integration. Pair it with [`EndLimsOleConnect`](EndLimsOleConnect.md) when you are finished with the object.

## When to use

- When SSL needs to create an automation object from a registered ProgID.
- When you are integrating with applications such as Excel or Word through their automation interfaces.
- When an existing integration already provides a ProgID-based component you need to call from SSL.

## Syntax

```ssl
LimsOleConnect(vProgId)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vProgId` | any | yes | — | Value whose text form is used as the ProgID to create |

## Returns

**[object](../types/object.md)** — The created object for the requested ProgID.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| The ProgID cannot be resolved or the object cannot be created. | `<COM error message>` |

## Best practices

!!! success "Do"
    - Pass a known, valid ProgID.
    - Release the object with [`EndLimsOleConnect`](EndLimsOleConnect.md) when you are done.
    - Wrap the call in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) when the ProgID or the target application may be unavailable.

!!! failure "Don't"
    - Assume every ProgID is registered on every machine.
    - Skip cleanup after creating automation objects.
    - Document or code against members unless the target automation server actually provides them.

## Caveats

- Available members depend entirely on the object created by that ProgID.
- Cleanup is not automatic; use [`EndLimsOleConnect`](EndLimsOleConnect.md) explicitly when you finish with the object.
- The ProgID `StarLIMS.SoapClient.SoapClient` is handled specially and returns the platform SOAP client object instead of creating an external COM server.

## Examples

### Create and use an Excel automation object

Create an Excel automation object, read a property, and release it.

```ssl
:PROCEDURE AutomateExcel;
    :DECLARE oExcel, sStatus;

    oExcel := LimsOleConnect("Excel.Application");
    oExcel:Visible := .T.;

    sStatus := "Excel version: " + LimsString(oExcel:Version);
    UsrMes(sStatus); /* Displays the Excel version;

    EndLimsOleConnect(oExcel);
:ENDPROC;

/* Usage;
DoProc("AutomateExcel");
```

### Handle connection failure with guaranteed cleanup

Try to start Excel, report failures, and always release the object.

```ssl
:PROCEDURE OpenExcelSafely;
    :DECLARE oExcel, oErr, sStatus;

    oExcel := NIL;

    :TRY;
        oExcel := LimsOleConnect("Excel.Application");
        oExcel:Visible := .F.;
        sStatus := "Connected to Excel version " + LimsString(oExcel:Version);
        UsrMes(sStatus); /* Displays the Excel version when the connection succeeds;
    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("Unable to create automation object: " + oErr:Description);
        /* Displays the failure reason;
    :FINALLY;
        EndLimsOleConnect(oExcel);
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("OpenExcelSafely");
```

## Related

- [`EndLimsOleConnect`](EndLimsOleConnect.md)
- [`string`](../types/string.md)
