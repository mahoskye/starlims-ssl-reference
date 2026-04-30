---
title: "ENDTRY"
summary: "Closes a structured :TRY block after its :CATCH and/or :FINALLY sections."
id: ssl.keyword.endtry
element_type: keyword
category: error-handling
tags:
  - exception-handling
  - block-closer
  - try-catch
  - finally
  - control-flow
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ENDTRY

Closes a structured [`:TRY`](TRY.md) block after its [`:CATCH`](CATCH.md) and/or [`:FINALLY`](FINALLY.md) sections.

`:ENDTRY` terminates a structured error-handling block that starts with [`:TRY`](TRY.md). In SSL, a [`:TRY`](TRY.md) block must contain at least one statement and must be followed by [`:CATCH`](CATCH.md), [`:FINALLY`](FINALLY.md), or both before the closing `:ENDTRY;`. When execution reaches `:ENDTRY`, the protected block is complete and normal statement flow continues with the next statement after the block.

`:ENDTRY` does not take parameters or expressions. It is only valid as the closing keyword for a [`:TRY`](TRY.md) structure, after the optional [`:CATCH`](CATCH.md) section and the optional [`:FINALLY`](FINALLY.md) section. Using `:ENDTRY` outside that structure, omitting it, or placing it before the required sections is invalid.

## Behavior

`:ENDTRY` closes these valid structured error-handling forms:

```ssl
:TRY;
    /* statements;
:CATCH;
    /* error handling;
:ENDTRY;
```

```ssl
:TRY;
    /* statements;
:FINALLY;
    /* cleanup;
:ENDTRY;
```

```ssl
:TRY;
    /* statements;
:CATCH;
    /* error handling;
:FINALLY;
    /* cleanup;
:ENDTRY;
```

After `:ENDTRY;`, execution resumes with the next statement unless control flow was already redirected inside the block, for example by `:RETURN;` in the [`:TRY`](TRY.md) or [`:CATCH`](CATCH.md) body. When a [`:FINALLY`](FINALLY.md) block is present, it runs before control leaves the structure.

## When to use

- When closing every [`:TRY`](TRY.md) block — `:ENDTRY;` is required to terminate the error-handling structure.

## Syntax

```ssl
:ENDTRY;
```

## Keyword group

**Group:** Error Handling
**Role:** closer

## Best practices

!!! success "Do"
    - Always include `:ENDTRY` whenever you create a [`:TRY`](TRY.md) block, regardless of whether you use [`:CATCH`](CATCH.md) or [`:FINALLY`](FINALLY.md) sections.
    - Place `:ENDTRY` only after all associated [`:CATCH`](CATCH.md) and [`:FINALLY`](FINALLY.md) sections.
    - Format `:ENDTRY` clearly and align it with its opening [`:TRY`](TRY.md) for readability.

!!! failure "Don't"
    - Omit `:ENDTRY`, expecting the block to close automatically. Omitting `:ENDTRY` causes compile-time errors and leaves error handling incomplete.
    - Insert `:ENDTRY` before these sections or outside the [`:TRY`](TRY.md) block. Early or misplaced `:ENDTRY` disrupts the intended flow and terminates exception handling prematurely.
    - Scatter related error-handling keywords, making the block hard to follow. Consistent structure improves code clarity and maintainability.

## Caveats

- `:ENDTRY` must be written in uppercase as a colon-prefixed keyword.

## Examples

### Closing a TRY/CATCH block and continuing afterward

`:ENDTRY;` closes the error-handling structure so execution continues with the next statement. When the file read succeeds, a success message displays; when it fails, the [`:CATCH`](CATCH.md) block handles the error. In both cases, the statement after `:ENDTRY;` runs.

```ssl
:PROCEDURE LoadConfigFile;
	:PARAMETERS sFilePath;
	:DECLARE sFileText, oErr;

	:TRY;
		sFileText := ReadText(sFilePath);
		UsrMes("Configuration file loaded");

	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("Unable to load configuration file: " + oErr:Description);
		/* Displays on failure: unable to load the configuration file;

	:ENDTRY;

	UsrMes("Continuing after the TRY block");
:ENDPROC;

/* Usage;
DoProc("LoadConfigFile", {"config.ini"});
```

## Related

- [`TRY`](TRY.md)
- [`CATCH`](CATCH.md)
- [`FINALLY`](FINALLY.md)
