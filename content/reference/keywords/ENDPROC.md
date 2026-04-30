---
title: "ENDPROC"
summary: "Terminates a procedure block and signals the end of its executable statements."
id: ssl.keyword.endproc
element_type: keyword
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ENDPROC

Terminates a procedure block and signals the end of its executable statements.

The `:ENDPROC` keyword closes a procedure that started with [`:PROCEDURE`](PROCEDURE.md). Every valid procedure definition must be explicitly terminated with `:ENDPROC;`. Reaching `:ENDPROC` ends the procedure if execution has not already left earlier through [`:RETURN`](RETURN.md).

`:ENDPROC` is structural rather than expressive: it does not take arguments and does not return a value. Use [`:RETURN`](RETURN.md) when you need to leave a procedure early or send a result back to the caller.

## When to use

- When closing every [`:PROCEDURE`](PROCEDURE.md) block — `:ENDPROC;` is required to terminate the definition.

## Syntax

```ssl
:ENDPROC;
```

## Keyword group

**Group:** Procedures & Classes
**Role:** closer

## Best practices

!!! success "Do"
    - End every [`:PROCEDURE`](PROCEDURE.md) block with `:ENDPROC;`.
    - Use [`:RETURN`](RETURN.md) for early exits or returned values.
    - Keep procedure boundaries visually clear with consistent indentation and spacing.

!!! failure "Don't"
    - Omit `:ENDPROC;` or rely on an implicit end to the procedure.
    - Use `:ENDPROC` as a substitute for [`:RETURN`](RETURN.md) when you need to exit early.
    - Place extra procedure-body statements after the closing `:ENDPROC;`.

## Caveats

- Constructors also end with `:ENDPROC;` because they are declared with `:PROCEDURE Constructor;` syntax.
- SSL keywords are case-sensitive, so `:endproc` is not valid syntax.

## Examples

### Closing a procedure after normal execution

`:ENDPROC;` closes the procedure after all statements have run. The procedure builds a status message and displays it before reaching its natural end.

```ssl
:PROCEDURE ShowLabStatus;
    :DECLARE sStatus, sMessage;

    sStatus := "Operational";
    sMessage := "Laboratory status: " + sStatus;

    UsrMes(sMessage);
:ENDPROC;

/* Usage;
DoProc("ShowLabStatus");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Laboratory status: Operational
```

## Related

- [`PROCEDURE`](PROCEDURE.md)
- [`RETURN`](RETURN.md)
- [`CLASS`](CLASS.md)
- [`PARAMETERS`](PARAMETERS.md)
