---
title: "PdfSupport"
summary: "Provides methods to create, modify, secure, save, and print PDF documents."
id: ssl.class.pdfsupport
element_type: class
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# PdfSupport

Provides methods to create, modify, secure, save, and print PDF documents.

`PdfSupport` starts with a new empty PDF document and a default text style. You can add pages from image files or another PDF, open an existing PDF for modification, place text on existing pages, configure document security settings, save the result, or print a PDF file to a named printer. Security settings are applied to the document in memory and take effect when you save the PDF.

## When to use

- When you need to programmatically generate or modify PDF documents in an automated process.
- When merging pages from multiple PDFs or images into a single, consolidated PDF is required.
- When enforcing security and permissions on PDF files, such as password protection or restricting printing/extraction.
- When automating the printing of PDFs to specific printers via Adobe Reader.
- When you need granular control over annotations, forms, and document assembly within a PDF workflow.

## Constructors

### `PdfSupport{}`

Creates a new empty PDF document. New instances use a default text style of Verdana, size 20, in black.

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `PageCount` | [number](../types/number.md) | read-only | The total number of pages in the PDF document. |
| `UserPassword` | [string](../types/string.md) | write-only | The user password required to open the PDF document. |
| `OwnerPassword` | [string](../types/string.md) | write-only | The owner password for the PDF document that controls permissions. |
| `DocumentSecurityLevel` | [string](../types/string.md) | read-write | The document security level. Valid values are `None`, `Encrypted40Bit`, and `Encrypted128Bit`. |
| `PermitAccessibilityExtractContent` | [boolean](../types/boolean.md) | read-write | Whether content extraction for accessibility is permitted. |
| `PermitAnnotations` | [boolean](../types/boolean.md) | read-write | Whether adding or modifying annotations is permitted. |
| `PermitAssembleDocument` | [boolean](../types/boolean.md) | read-write | Whether assembling the document (inserting, rotating, or deleting pages) is permitted. |
| `PermitExtractContent` | [boolean](../types/boolean.md) | read-write | Whether extracting text and graphics is permitted. |
| `PermitFormsFill` | [boolean](../types/boolean.md) | read-write | Whether filling form fields is permitted. |
| `PermitFullQualityPrint` | [boolean](../types/boolean.md) | read-write | Whether printing to full quality is permitted. |
| `PermitModifyDocument` | [boolean](../types/boolean.md) | read-write | Whether modifying the document content is permitted. |
| `PermitPrint` | [boolean](../types/boolean.md) | read-write | Whether printing the document is permitted. |

## Methods

| Name | Returns | Description |
|------|---------|-------------|
| `AddPageFromImage` | none | Adds a new page from an image file. |
| `AddPDFDocument` | none | Imports all pages from another PDF. |
| `AddTextOnPage` | none | Draws text on an existing page using the current text style. |
| `SetTextStyle` | none | Sets the text style used for later text drawing. |
| `Open` | none | Opens an existing PDF for modification. |
| `OpenProtectedDocument` | none | Opens a password-protected PDF for modification. |
| `Save` | none | Saves the current PDF document to a file. |
| `Print` | none | Prints a specified PDF file to a named printer. |
| `Protect` | none | Applies a predefined security profile to the current PDF document. |

### `AddPageFromImage`

Adds a new page to the current PDF document from an image file. The new page is sized to match the image dimensions.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sFileName` | [string](../types/string.md) | yes | The file path to the image file to add as a page. |

**Returns:** none — No return value.

**Raises:**
- **When the image file does not exist:** `File not found!`

### `AddPDFDocument`

Imports all pages from another PDF into the current PDF document.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sFileName` | [string](../types/string.md) | yes | The file path to the PDF document to import pages from. |

**Returns:** none — No return value.

### `AddTextOnPage`

Draws text on an existing page at the specified coordinates using the current text style.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sText` | [string](../types/string.md) | yes | The text string to draw on the page. |
| `nPageNumber` | [number](../types/number.md) | yes | The page number to add text to. Use an integer page number that refers to an existing page. |
| `nX` | [number](../types/number.md) | yes | The X coordinate position for the text. |
| `nY` | [number](../types/number.md) | yes | The Y coordinate position for the text. |

**Returns:** none — No return value.

**Raises:**
- **When page number is not an integer or is greater than the current page count:** `Page number is invalid!`

### `SetTextStyle`

Sets the font name, size, style, and color used by later `AddTextOnPage` calls.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sFontName` | [string](../types/string.md) | yes | The name of the font family to use. |
| `nFontSize` | [number](../types/number.md) | yes | The font size in points. |
| `sFontStyle` | [string](../types/string.md) | yes | The font style. Supported values include `Regular`, `Bold`, `Italic`, `BoldItalic`, `Underline`, and `Strikeout`. |
| `sFontColor` | [string](../types/string.md) | yes | The color name for the text, such as `Black`, `Red`, or `Blue`. |

**Returns:** none — No return value.

### `Open`

Opens an existing PDF file for modification. The opened file becomes the current document.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sFileName` | [string](../types/string.md) | yes | The file path to the PDF document to open. |

**Returns:** none — No return value.

### `OpenProtectedDocument`

Opens a password-protected PDF file for modification. The opened file becomes the current document.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sFileName` | [string](../types/string.md) | yes | The file path to the protected PDF document to open. |
| `sPassword` | [string](../types/string.md) | yes | The password required to open the protected PDF document. |

**Returns:** none — No return value.

### `Save`

Saves the current PDF document to the specified file path.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sFileName` | [string](../types/string.md) | yes | The file path where the PDF document will be saved. |

**Returns:** none — No return value.

### `Print`

Prints the specified PDF file to the specified printer using the Adobe Reader executable path you provide.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sAdobeReaderPath` | [string](../types/string.md) | yes | The file path to the Adobe Reader executable. |
| `sFileName` | [string](../types/string.md) | yes | The file path to the PDF document to print. |
| `sPrinterName` | [string](../types/string.md) | yes | The name of the printer to send the print job to. |

**Returns:** none — No return value.

**Raises:**
- **When the Adobe Reader path is empty:** `No full qualified path to AcroRd32.exe or Acrobat.exe is set.`
- **When the printer name is empty:** `No printer name set.`
- **When the PDF file does not exist:** `The file <resolved path> does not exist.`

### `Protect`

Applies a predefined protection profile to the current PDF document using the same password for both user and owner access.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sPassword` | [string](../types/string.md) | yes | The password to apply as both the user password and the owner password. |

**Returns:** none — No return value.

`Protect` sets `DocumentSecurityLevel` to `Encrypted128Bit` and applies these permission values:

| Property | Value after `Protect` |
|----------|-----------------------|
| `PermitAccessibilityExtractContent` | [`.F.`](../literals/false.md) |
| `PermitAnnotations` | [`.F.`](../literals/false.md) |
| `PermitAssembleDocument` | [`.F.`](../literals/false.md) |
| `PermitExtractContent` | [`.F.`](../literals/false.md) |
| `PermitFormsFill` | [`.T.`](../literals/true.md) |
| `PermitFullQualityPrint` | [`.F.`](../literals/false.md) |
| `PermitModifyDocument` | [`.T.`](../literals/true.md) |
| `PermitPrint` | [`.F.`](../literals/false.md) |

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Set document passwords and permission properties before `Save` so the saved PDF includes those settings.
    - Use a positive integer page number that already exists before calling `AddTextOnPage`.
    - Call `SetTextStyle` before `AddTextOnPage` when you need a font, size, style, or color other than the default Verdana 20 black text.
    - Use `Protect` when its built-in security profile matches your needs, then adjust permission properties before `Save` if you need different settings.
    - Pass a valid Adobe Reader executable path, a valid PDF file path, and a valid printer name to `Print`.

!!! failure "Don't"
    - Change passwords or permission properties after `Save` and expect an already-written file to change — those settings only take effect when the document is saved again.
    - Call `AddPageFromImage` with a missing image file — it throws `File not found!`.
    - Pass a page number that is non-integer or beyond the current page count to `AddTextOnPage` — it throws `Page number is invalid!`.
    - Rely on page number `0` or negative page numbers — the method expects an existing page and those values are outside the supported usage.
    - Expect `SetTextStyle` to change text that was already drawn — it only affects later `AddTextOnPage` calls.
    - Assume `Protect` preserves previously assigned passwords or permission values — it overwrites them with its own preset security settings.
    - Treat `Print` as saving or printing the in-memory document automatically — it prints the file path you pass to the method.

## Caveats

- Use page numbers from 1 through `PageCount`. Page numbers outside that range are not supported.
- `DocumentSecurityLevel` only accepts `None`, `Encrypted40Bit`, or `Encrypted128Bit`; other values throw `DocumentSecurityLevel must be a string and have one of the values: None, Encrypted40Bit or Encrypted128Bit`.
- `SetTextStyle` expects a recognized font style name and a valid color name.
- `Print` prints the file path you pass to it, not the in-memory document.

## Examples

### Add text to a page from an image

Imports a JPEG as a new PDF page, then calls `SetTextStyle` to switch to bold green Arial before drawing a label at coordinates (50, 50) with `AddTextOnPage`. The default text style (Verdana 20 black) is only overridden for calls after `SetTextStyle`.

```ssl
:PROCEDURE AddTextOverlayToImage;
    :DECLARE oPdf, sImagePath, sOutputPath, sLabel;

    sImagePath := "C:/Documents/InspectionPhoto.jpg";
    sOutputPath := "C:/Documents/LabeledPhoto.pdf";
    sLabel := "PASS - Inspected";

    oPdf := PdfSupport{};
    oPdf:AddPageFromImage(sImagePath);

    oPdf:SetTextStyle("Arial", 14, "Bold", "Green");
    oPdf:AddTextOnPage(sLabel, 1, 50, 50);
    oPdf:Save(sOutputPath);

    UsrMes("Image exported to PDF with text overlay");
:ENDPROC;

/* Usage;
DoProc("AddTextOverlayToImage");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Image exported to PDF with text overlay
```

### Assemble and secure a multi-source PDF

Merges a header image, all pages from an existing PDF, and a footer image into one document, then sets `Encrypted128Bit` security and disables printing, modifying, and content extraction before saving. The page count reflects the total pages across all merged sources.

```ssl
:PROCEDURE AssembleSecureMultiSourcePdf;
    :DECLARE oPdf, sImage1, sImage2, sExistingPdf;
    :DECLARE sOutputPath, sUserPass, sOwnerPass, sMsg;
    :DECLARE nPageCount;

    sImage1 := "/documents/report_header.png";
    sImage2 := "/documents/report_footer.png";
    sExistingPdf := "/documents/reference.pdf";
    sOutputPath := "/documents/final_report.pdf";
    sUserPass := "UserPass2024";
    sOwnerPass := "OwnerPass2024";

    oPdf := PdfSupport{};
    oPdf:AddPageFromImage(sImage1);
    oPdf:AddPDFDocument(sExistingPdf);
    oPdf:AddPageFromImage(sImage2);

    nPageCount := oPdf:PageCount;

    oPdf:DocumentSecurityLevel := "Encrypted128Bit";
    oPdf:UserPassword := sUserPass;
    oPdf:OwnerPassword := sOwnerPass;
    oPdf:PermitPrint := .F.;
    oPdf:PermitModifyDocument := .F.;
    oPdf:PermitExtractContent := .F.;
    oPdf:Save(sOutputPath);

    sMsg := "Assembled PDF has " + LimsString(nPageCount);
    sMsg := sMsg + " pages and is print-protected";

    UsrMes(sMsg);
:ENDPROC;

/* Usage;
DoProc("AssembleSecureMultiSourcePdf");
```

[`UsrMes`](../functions/UsrMes.md) displays (page count depends on merged sources):

```text
Assembled PDF has 5 pages and is print-protected
```

### Protect and print a PDF report

Opens an existing PDF, draws a title on page 1, then applies `Protect`, which sets a 128-bit security profile. The `PermitModifyDocument` override shows that individual permissions can be tightened after `Protect`. The final `Print` call sends the saved file path to Adobe Reader. It does not print the in-memory document.

```ssl
:PROCEDURE GenerateSecureReport;
    :PARAMETERS sPdfPath, sPrinterName;
    :DEFAULT sPdfPath, "C:/Reports/QuarterlyReport.pdf";
    :DEFAULT sPrinterName, "HP_LaserJet_5000";
    :DECLARE oPdf, sAdobePath, sReportTitle, sOutputPath, oErr;

    sAdobePath := "C:/Program Files/Adobe/Acrobat DC/Acrobat/Acrobat.exe";
    sReportTitle := "Q4 Analytical Results";
    sOutputPath := "C:/Reports/Secure_QuarterlyReport.pdf";

    oPdf := PdfSupport{};
    oPdf:Open(sPdfPath);

    oPdf:SetTextStyle("Arial", 12, "Bold", "Black");
    oPdf:AddTextOnPage(sReportTitle, 1, 50, 50);

    oPdf:Protect("SecureReport123");
    oPdf:PermitModifyDocument := .F.;
    oPdf:Save(sOutputPath);

    :TRY;
        oPdf:Print(sAdobePath, sOutputPath, sPrinterName);
        UsrMes("Report generated and sent to printer: " + sPrinterName);
    :CATCH;
        oErr := GetLastSSLError();
        UsrMes("Print failed: " + oErr:Description);
        /* Displays on failure: Print failed;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("GenerateSecureReport");
```

## Related

- [`object`](../types/object.md)
