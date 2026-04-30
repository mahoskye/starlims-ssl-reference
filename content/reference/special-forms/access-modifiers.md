---
title: "Access Modifiers"
summary: "SSL supports two comment-based access modifiers that control procedure visibility. Place one on the line immediately before a :PROCEDURE declaration."
id: ssl.special_form.access-modifiers
element_type: special_form
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Access Modifiers

## What it does

SSL supports two comment-based access modifiers that control procedure visibility. Place one on the line immediately before a [`:PROCEDURE`](../keywords/PROCEDURE.md) declaration.

`/*@private;` marks a procedure as private, callable only from other procedures within the same script file. External scripts and inheriting scripts cannot invoke it.

`/*@protected;` marks a procedure as protected, callable from the same script file and from scripts that inherit from or extend the containing class or category. External scripts cannot invoke it.

Procedures with no modifier are **public** by default and can be called from anywhere.

## When to use it

- When a helper procedure is an implementation detail that external callers should never invoke directly, use `/*@private;`.
- When a shared utility needs to be available to inheriting scripts but hidden from unrelated external callers, use `/*@protected;`.
- When organizing a script with a clear public API boundary alongside internal implementation procedures.

## Syntax

```ssl
/*@private;
:PROCEDURE ProcedureName;

/*@protected;
:PROCEDURE ProcedureName;
```

## Context rules

The modifier must appear on the line **immediately before** the [`:PROCEDURE`](../keywords/PROCEDURE.md) keyword. The exact syntax is `/*@private;` or `/*@protected;`, with no spaces between `/*` and `@`, and the modifier name must be lowercase. Procedures without a modifier are public by default. The compiler extracts these annotations before parsing; they are not regular comments.

| Modifier | Same script | Inheriting scripts | External scripts |
| --- | --- | --- | --- |
| *(none — default)* | Yes | Yes | Yes |
| `/*@protected;` | Yes | Yes | No |
| `/*@private;` | Yes | No | No |

!!! warning "Script-level procedures only"
    Access modifiers only work on **script-level procedures**, standalone [`:PROCEDURE`](../keywords/PROCEDURE.md) blocks in server scripts and data sources. They have **no effect on methods inside [`:CLASS`](../keywords/CLASS.md) blocks**. The class compilation path does not process these annotations, so placing `/*@private;` before a class method will be silently ignored.

## Notes for daily SSL work

!!! success "Do"
    - Put `/*@private;` on the line immediately before [`:PROCEDURE`](../keywords/PROCEDURE.md) with no blank lines between them.
    - Use `/*@protected;` for shared utilities that inheriting scripts need but external callers should not access.
    - Default to public only when external invocation is intentional.

!!! failure "Don't"
    - Place access modifiers inside [`:CLASS`](../keywords/CLASS.md) blocks; they are silently ignored there.
    - Add spaces between `/*` and `@`.
    - Use uppercase letters in the modifier name (`/*@Private;` is not recognized).

## Errors and edge cases

- A blank line between the modifier and [`:PROCEDURE`](../keywords/PROCEDURE.md) breaks the association; the modifier will not apply to the procedure.
- Access modifiers inside [`:CLASS`](../keywords/CLASS.md) blocks are silently ignored with no compile error.
- The modifier applies only to the single procedure immediately following it.

## Examples

### Combining public, protected, and private procedures

Shows all three visibility levels in one script. `GetSample` is the public entry point, `ValidateSample` is available to inheriting scripts, and `FormatSampleLog` is internal only.

```ssl
/* region Sample Management API;

:PROCEDURE GetSample;
    :PARAMETERS sSampleId;
    :DECLARE aSample;

    aSample := LSelect1("
        SELECT *
        FROM samples
        WHERE sample_id = ?
    ",, {sSampleId});
    :RETURN aSample;
:ENDPROC;

/*@protected;
:PROCEDURE ValidateSample;
    :PARAMETERS aSample;
    :RETURN ALen(aSample) > 0;
:ENDPROC;

/*@private;
:PROCEDURE FormatSampleLog;
    :PARAMETERS sSampleId, sAction;
    :RETURN DToS(Now()) + " | " + sSampleId + " | " + sAction;
:ENDPROC;

/* endregion;
```

In this example:

- `GetSample` — public, callable from anywhere
- `ValidateSample` — protected, callable from this script and inheriting scripts
- `FormatSampleLog` — private, callable only within this script
