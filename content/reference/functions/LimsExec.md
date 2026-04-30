---
title: "LimsExec"
summary: "Launches an external application without waiting for it to finish."
id: ssl.function.limsexec
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LimsExec

Launches an external application without waiting for it to finish.

`LimsExec` starts a process and returns immediately. Use it when SSL should continue running after the application has been launched. It returns [`.T.`](../literals/true.md) when the process is created successfully and [`.F.`](../literals/false.md) when startup fails after parameter validation. A [`.T.`](../literals/true.md) result only means the process started; it does not mean the external program completed successfully.

The `sApplication` argument must identify a valid executable. You can pass arguments separately through `sArguments`, or omit `sArguments` and include the full command line in `sApplication`. When `sArguments` is omitted or empty, `LimsExec` splits any trailing text out of `sApplication` and uses that as the process arguments. If you need SSL to wait for the external application to exit, use [`RunApp`](RunApp.md) instead.

## When to use

- When you need to launch an external tool and continue SSL processing immediately.
- When you want to hide or show the launched application's window.
- When another part of the workflow will verify the external tool's outcome later.

## Syntax

```ssl
LimsExec(sApplication, [bShow], [sArguments])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sApplication` | [string](../types/string.md) | yes | — | Executable path, or a full command line when `sArguments` is omitted. |
| `bShow` | [boolean](../types/boolean.md) | no | [`.F.`](../literals/false.md) | Whether to show the launched window. |
| `sArguments` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Command-line arguments passed to the application. When omitted or empty, trailing text in `sApplication` is parsed as the argument string. |

## Returns

**[boolean](../types/boolean.md)** — Returns [`.T.`](../literals/true.md) when the process starts successfully, or [`.F.`](../literals/false.md) when process creation fails after parameter validation.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sApplication` is [`NIL`](../literals/nil.md). | `LimsExec (Parameter 'sApplication')` |

## Best practices

!!! success "Do"
    - Use `sArguments` for normal argument passing so the executable path stays clear and easy to validate.
    - Check the boolean result and inspect [`GetLastSSLError`](GetLastSSLError.md) when the launch returns [`.F.`](../literals/false.md).
    - Use [`RunApp`](RunApp.md) instead when the workflow must wait for the external program to finish.

!!! failure "Don't"
    - Assume [`.T.`](../literals/true.md) means the external program completed successfully. It only means the process was started.
    - Pass an empty, malformed, or unquoted executable path. Invalid `sApplication` values raise exceptions instead of returning [`.F.`](../literals/false.md).
    - Ignore paths with spaces when embedding the full command line in `sApplication`. Quote the executable path first so SSL can split the command correctly.

## Caveats

- Only a [`NIL`](../literals/nil.md) `sApplication` raises an exception — empty strings and invalid paths return [`.F.`](../literals/false.md) and set the last SSL error.
- Startup failures return [`.F.`](../literals/false.md), set the last SSL error, and write the error message.
- When `bShow` is [`.F.`](../literals/false.md), the function requests a hidden window, but the final behavior still depends on the launched application.

## Examples

### Launch a tool and continue immediately

Start a known executable with explicit arguments and continue the SSL script without waiting for completion.

```ssl
:PROCEDURE LaunchAuditExport;
	:DECLARE sApp, sArgs, bStarted;

	sApp := "C:\Tools\AuditExport.exe";
	sArgs := "/user admin /period quarterly";
	bStarted := LimsExec(sApp, .T., sArgs);

	:IF bStarted;
		UsrMes("Audit export was started");
	:ELSE;
		ErrorMes("Audit export could not be started");
	:ENDIF;

	:RETURN bStarted;
:ENDPROC;

/* Usage;
DoProc("LaunchAuditExport");
```

### Launch silently and report the startup error

Run a background utility without showing its window and surface the last SSL error when startup fails.

```ssl
:PROCEDURE PrintBarcodeLabel;
	:DECLARE sApp, sArgs, sSampleID, bStarted, oErr;

	sSampleID := "LAB-2024-0042";
	sApp := "C:\Program Files\BarcodePrint\LabelPrinter.exe";
	sArgs := "/silent /label " + sSampleID;
	bStarted := LimsExec(sApp, .F., sArgs);

	:IF bStarted;
		UsrMes("Barcode print job was submitted for " + sSampleID);
	:ELSE;
		oErr := GetLastSSLError();
		ErrorMes(
			"Barcode print launch failed: " + oErr:Description
		);  /* Displays on failure: last SSL error message;
	:ENDIF;

	:RETURN bStarted;
:ENDPROC;

/* Usage;
DoProc("PrintBarcodeLabel");
```

### Pass the full command line in `sApplication`

Omit `sArguments` and let `LimsExec` split a quoted executable path from the rest of the command line.

```ssl
:PROCEDURE LaunchQuotedCommand;
	:DECLARE sCommand, bStarted;

	sCommand := '"C:\Program Files\Acme Tools\Exporter.exe" /mode silent /batch B-1042';
	bStarted := LimsExec(sCommand);

	:IF .NOT. bStarted;
		ErrorMes("Exporter launch failed");
	:ENDIF;

	:RETURN bStarted;
:ENDPROC;

/* Usage;
DoProc("LaunchQuotedCommand");
```

## Related

- [`RunApp`](RunApp.md)
- [`GetLastSSLError`](GetLastSSLError.md)
- [`ClearLastSSLError`](ClearLastSSLError.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
