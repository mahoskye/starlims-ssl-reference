---
title: "false"
summary: "The .F. literal represents the boolean value false in SSL. It can be written as .F. or .f. (case-insensitive). Use .F. to initialize boolean flags, to explicitly pass a false argument to a function, or to represent a negative or disabled state."
id: ssl.literal.false
element_type: literal
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# false

## What it does

The `.F.` literal represents the boolean value false in SSL. It can be written as `.F.` or `.f.` (case-insensitive). Use `.F.` to initialize boolean flags, to explicitly pass a false argument to a function, or to represent a negative or disabled state.

In all logical and conditional contexts, `.F.` is treated as boolean false and
interacts with [`.AND.`](and.md), [`.OR.`](Or.md), and [`.NOT.`](Not.md) as expected.

Comparing `.F.` to a non-boolean (for example `.F. = 0` or `.F. = 1`) raises a runtime error. Boolean equality requires both operands to be booleans. Wrap such comparisons in [`:TRY`](../keywords/TRY.md) / [`:CATCH`](../keywords/CATCH.md) or check the type explicitly if a zero-like test is what you actually want.

Uniquely among booleans, [`Empty`](../functions/Empty.md)`(.F.)` returns [`.T.`](true.md), making `.F.` test as empty. This can affect validations and presence checks.

## Syntax

`.F.` is case-insensitive; both `.F.` and `.f.` are valid SSL syntax.

- **Type:** boolean
- **Case:** case-insensitive

## Comparison behavior

| Expression                              | Result           |
| --------------------------------------- | ---------------- |
| `.F. = .F.`                             | [`.T.`](true.md) |
| `.F. = .T.`                             | `.F.`            |
| `.F. = 0`                               | runtime error    |
| `.F. = 1`                               | runtime error    |
| [`Empty`](../functions/Empty.md)`(.F.)` | [`.T.`](true.md) |

## Type coercion

| Target                                    | Result                                               |
| ----------------------------------------- | ---------------------------------------------------- |
| [string](../types/string.md)              | `".F."`                                              |
| [number](../types/number.md)              | `0`                                                  |
| JSON ([`ToJson`](../functions/ToJson.md)) | `"false"` (a string value, not a JSON boolean token) |

## Notes for daily SSL work

!!! success "Do"
    - Use `.F.` wherever a boolean false is required, especially in conditionals and flag logic.
    - Explicitly pass `.F.` as arguments for boolean parameters.

!!! failure "Don't"
    - Use `.F.` as a substitute for NIL or empty string when you mean "missing data." `.F.` is a concrete boolean, not absence, even though [`Empty`](../functions/Empty.md) returns [`.T.`](true.md).
    - Compare `.F.` directly to `0` or `1`. This raises a runtime error, not a boolean result.

## Errors and edge cases

- `.F. = 0` raises a runtime error. Use [`Empty`](../functions/Empty.md)`()` or a type check for safe zero-like tests.
- `.F.` is different from NIL and the empty string.

## Examples

### Boolean flag in a conditional

Initializes `bIsActive` to `.F.` and branches on it. Since the flag is false, the inactive path runs.

```ssl
:PROCEDURE ValidateRecord;
    :DECLARE bIsActive, sStatus;

    bIsActive := .F.;

    :IF bIsActive;
        sStatus := "Active — processing";
    :ELSE;
        sStatus := "Inactive — skipping";
    :ENDIF;

    UsrMes(sStatus);
    :RETURN sStatus;
:ENDPROC;

/* Usage;
DoProc("ValidateRecord");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Inactive — skipping
```

### Empty behavior with .F.

Demonstrates that [`Empty`](../functions/Empty.md) returns [`.T.`](true.md) for `.F.`, even though `.F.` is a concrete boolean. All three conditions below are true with `bFlag` set to `.F.`.

```ssl
:DECLARE bFlag;

bFlag := .F.;

/* Empty returns .T. for .F. — this can be surprising;
:IF Empty(bFlag);
    UsrMes("bFlag is considered empty");
:ENDIF;

/* To check if a boolean is specifically false, compare directly;
:IF bFlag = .F.;
    UsrMes("bFlag is false");
:ENDIF;

/* To check if a value is a boolean rather than missing, use LimsType;
:IF LimsType(bFlag) == "L";
    UsrMes("bFlag is a boolean, not missing");
:ENDIF;
```

## Related elements

- [`true`](true.md)
- [`nil`](nil.md)
