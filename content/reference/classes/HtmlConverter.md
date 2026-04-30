---
title: "HtmlConverter"
summary: "Converts XFD form XML into HTML form XML and exposes the most recent conversion log."
id: ssl.class.htmlconverter
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# HtmlConverter

Converts XFD form XML into HTML form XML and exposes the most recent conversion log.

Create `HtmlConverter{}` when you need to transform an XFD form definition into its HTML form XML equivalent. You can optionally load conversion options through `OptionsXml`, call `Convert()`, then inspect `Log` or `SimplifiedLog` for details from that conversion.

## When to use

- When you need to convert XFD form XML into HTML form XML.
- When the same conversion should run with explicit option XML.
- When you need to inspect the full or simplified conversion log after a run.
- When you want to reuse one converter instance across multiple conversions.

## Constructors

### `HtmlConverter{}`

Creates a converter with default conversion options and an empty log.

## Properties

| Name | Type | Access | Description |
|------|------|--------|-------------|
| `OptionsXml` | [string](../types/string.md) | write-only | Sets the conversion option XML used by subsequent `Convert` calls |
| `Log` | [string](../types/string.md) | read-only | Returns the full text of the current conversion log |
| `SimplifiedLog` | [string](../types/string.md) | read-only | Returns a shorter summary of the current conversion log with repeated conversion messages collapsed |

## Methods

| Name | Returns | Description |
|------|---------|-------------|
| `Convert` | [string](../types/string.md) | Converts XFD form XML to HTML form XML using the supplied source and target form IDs |
| `ClearLog` | none | Resets the current log to empty |

### `Convert`

Converts XFD form XML to HTML form XML using the supplied source and target form IDs.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sXml` | [string](../types/string.md) | yes | The XFD form XML to convert |
| `sXfdGuid` | [string](../types/string.md) | yes | The form ID currently present in the XFD XML |
| `sHtmlGuid` | [string](../types/string.md) | yes | The form ID to place into the converted HTML XML |

**Returns:** [string](../types/string.md) — The converted HTML XML string.

### `ClearLog`

Clears the current log.

**Returns:** none — No return value.

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Set `OptionsXml` before `Convert` when the conversion requires non-default options.
    - Read `Log` or `SimplifiedLog` after `Convert` when you need conversion details.
    - Call `ClearLog()` before a separate workflow if you want the next log to start empty.

!!! failure "Don't"
    - Call `Convert` again before reading the current log if you still need it — each conversion replaces the stored log.
    - Assume conversion problems are always reported only in the log — invalid option XML or invalid input XML can fail the operation itself.
    - Set `OptionsXml` after `Convert` and expect it to affect the conversion that already ran — options apply to later conversions.

## Caveats

- Setting `OptionsXml` replaces the current conversion options. Passing an empty or invalid options XML string fails when the property is assigned.
- `Convert` replaces the supplied `sXfdGuid` text in the source XML before it parses the form. Pass the form ID that is actually present in the XFD XML.
- `SimplifiedLog` is a summary view, not a verbatim copy of `Log`. Use `Log` when you need the full message text from the last conversion.
- `ClearLog()` clears only the stored log. It does not reset `OptionsXml`.

## Examples

### Convert XFD XML to HTML XML

This example converts XFD XML that is already available to the script and then checks the simplified log.

```ssl
:PROCEDURE ConvertFormToHtml;
	:PARAMETERS sXfdXml, sXfdGuid, sHtmlGuid;
	:DECLARE oConverter, sHtmlXml;

	oConverter := HtmlConverter{};

	sHtmlXml := oConverter:Convert(sXfdXml, sXfdGuid, sHtmlGuid);

	:IF .NOT. Empty(oConverter:SimplifiedLog);
		UsrMes(oConverter:SimplifiedLog);
	:ENDIF;

	:RETURN sHtmlXml;
:ENDPROC;

/* Usage;
DoProc("ConvertFormToHtml", {sXfdXml, sXfdGuid, sHtmlGuid});
```

`UsrMes` displays:

```text
<simplified log text>
```

### Apply options and inspect the full log

This example sets `OptionsXml` before conversion and reads the full log after the call.

```ssl
:PROCEDURE ConvertFormToHtmlWithOptions;
	:PARAMETERS sXfdXml, sXfdGuid, sHtmlGuid, sOptionsXml;
	:DECLARE oConverter, sHtmlXml, oErr;

	oConverter := HtmlConverter{};
	oConverter:OptionsXml := sOptionsXml;

	:TRY;
		sHtmlXml := oConverter:Convert(sXfdXml, sXfdGuid, sHtmlGuid);

		:IF .NOT. Empty(oConverter:Log);
			/* Displays: conversion log text;
			UsrMes(oConverter:Log);
		:ENDIF;
	:CATCH;
		oErr := GetLastSSLError();
		/* Displays on failure: conversion error;
		ErrorMes("Conversion Error", oErr:Description);
		:RETURN "";
	:ENDTRY;

	:RETURN sHtmlXml;
:ENDPROC;

/* Usage;
DoProc("ConvertFormToHtmlWithOptions",
		{sXfdXml, sXfdGuid, sHtmlGuid, sOptionsXml});
```

## Related

- [`object`](../types/object.md)
