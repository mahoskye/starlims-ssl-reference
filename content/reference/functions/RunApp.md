---
title: "RunApp"
summary: "Launches an external application and waits for it to exit."
id: ssl.function.runapp
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# RunApp

Launches an external application and waits for it to exit.

`RunApp` starts a process and blocks until that process finishes. Use it when SSL must pause until the external program exits. It returns [`.T.`](../literals/true.md) when the process is created successfully and the wait completes without a startup exception. It returns [`.F.`](../literals/false.md) when process startup fails after parameter validation.

The `sApplication` argument is required. You can pass arguments separately through `sArguments`, or omit `sArguments` and include the full command line in `sApplication`. When `sArguments` is omitted or empty, `RunApp` parses any trailing text out of `sApplication` and uses that text as the argument string. If you need SSL to continue immediately after launch, use [`LimsExec`](LimsExec.md) instead.

## When to use

- When SSL must wait for an external program to finish before continuing.
- When you want a simple [`.T.`](../literals/true.md) or [`.F.`](../literals/false.md) result for process startup.
- When your workflow needs to inspect [`GetLastSSLError`](GetLastSSLError.md) after a launch failure.

## Syntax

```ssl
RunApp(sApplication, [sArguments])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sApplication` | [string](../types/string.md) | yes | — | Executable path, or a full command line when `sArguments` is omitted. |
| `sArguments` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Command-line arguments passed to the application. When omitted or empty, trailing text in `sApplication` is parsed as the argument string. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) when the process starts successfully and `RunApp` finishes waiting for it to exit; [`.F.`](../literals/false.md) when process startup fails after parameter validation.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sApplication` is [`NIL`](../literals/nil.md). | `RunApp (Parameter 'application')` |

## Best practices

!!! success "Do"
    - Pass `sArguments` separately for normal usage so the executable path stays clear and easy to validate.
    - Check the boolean result and inspect [`GetLastSSLError`](GetLastSSLError.md) when `RunApp` returns [`.F.`](../literals/false.md).
    - Use [`LimsExec`](LimsExec.md) instead when the workflow should continue without waiting.

!!! failure "Don't"
    - Assume [`.T.`](../literals/true.md) means the external program completed its work successfully. `RunApp` does not report the child process exit code.
    - Pass an empty or malformed `sApplication` value. Validation errors raise exceptions instead of returning [`.F.`](../literals/false.md).
    - Use `RunApp` for long-running tools when blocking the SSL workflow would be a problem.

## Caveats

- When `sArguments` is supplied separately, `RunApp` does not perform the extra command-line parsing used when `sArguments` is empty.
- The function waits indefinitely for the launched process to exit.

## Examples

### Run a tool and wait for completion

Start a known executable, wait for it to finish, then continue the SSL workflow.

```ssl
:PROCEDURE GeneratePdfReport;
	:DECLARE sApp, sArgs, bFinished;

	sApp := "C:\Tools\DocConverter.exe";
	sArgs := '"C:\Reports\Daily Summary.docx" /outpdf';
	bFinished := RunApp(sApp, sArgs);

	:IF bFinished;
		UsrMes("PDF conversion finished");
	:ELSE;
		ErrorMes("PDF conversion could not be started");
	:ENDIF;

	:RETURN bFinished;
:ENDPROC;

/* Usage;
DoProc("GeneratePdfReport");
```

### Report the launch error after a failed start

Wait for a command-line tool to finish, and surface the last SSL error when the process could not be created.

```ssl
:PROCEDURE ExportAuditData;
	:DECLARE sApp, sArgs, bFinished, oErr;

	sApp := "C:\Program Files\Acme Tools\AuditExport.exe";
	sArgs := '/batch B-1042 /output "C:\Exports\audit.csv"';
	bFinished := RunApp(sApp, sArgs);

	:IF bFinished;
		UsrMes("Audit export finished");
	:ELSE;
		oErr := GetLastSSLError();
		/* Displays on failure: startup error;
		ErrorMes(
			"Audit export could not be started: " + oErr:Description
		);
	:ENDIF;

	:RETURN bFinished;
:ENDPROC;

/* Usage;
DoProc("ExportAuditData");
```

### Pass the full command line in `sApplication`

Omit `sArguments` and let `RunApp` split a quoted executable path from the rest of the command line before launching the process.

```ssl
:PROCEDURE LaunchQuotedCommand;
	:DECLARE sCommand, bFinished;

	sCommand := '"C:\Program Files\Acme Tools\Exporter.exe" /mode sync /batch B-1042';
	bFinished := RunApp(sCommand);

	:IF .NOT. bFinished;
		ErrorMes("Exporter could not be started");
	:ENDIF;

	:RETURN bFinished;
:ENDPROC;

/* Usage;
DoProc("LaunchQuotedCommand");
```

## Related

- [`LimsExec`](LimsExec.md)
- [`GetLastSSLError`](GetLastSSLError.md)
- [`ClearLastSSLError`](ClearLastSSLError.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
