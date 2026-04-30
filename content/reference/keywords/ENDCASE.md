---
title: "ENDCASE"
summary: "Closes a :BEGINCASE block after its :CASE branches and optional :OTHERWISE branch."
id: ssl.keyword.endcase
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ENDCASE

Closes a [`:BEGINCASE`](BEGINCASE.md) block after its [`:CASE`](CASE.md) branches and optional [`:OTHERWISE`](OTHERWISE.md) branch.

Use `:ENDCASE;` to terminate a CASE structure and continue execution with the next statement after the block. A valid CASE structure must include at least one [`:CASE`](CASE.md) before `:ENDCASE;`, and [`:OTHERWISE`](OTHERWISE.md) is optional.

`:ENDCASE` does not decide whether later branches run. That behavior is controlled by [`:EXITCASE`](EXITCASE.md) inside each branch. Without [`:EXITCASE`](EXITCASE.md), later [`:CASE`](CASE.md) expressions can still be evaluated before control reaches `:ENDCASE`.

## When to use

- When closing every [`:BEGINCASE`](BEGINCASE.md) block — `:ENDCASE;` is required to terminate the structure.
- When writing multi-branch dispatch logic and you need to mark where execution resumes after all branches.

## Syntax

```ssl
:ENDCASE;
```

## Keyword group

**Group:** Control Flow
**Role:** closer

## Best practices

!!! success "Do"
    - End every [`:BEGINCASE`](BEGINCASE.md) block with a matching `:ENDCASE;`.
    - Place `:ENDCASE;` after all [`:CASE`](CASE.md) branches and any optional [`:OTHERWISE`](OTHERWISE.md) branch.
    - Keep `:ENDCASE;` paired with [`:EXITCASE`](EXITCASE.md) in branch bodies when you want single-branch behavior.

!!! failure "Don't"
    - Write `:ENDCASE;` outside a [`:BEGINCASE`](BEGINCASE.md) block.
    - Omit `:ENDCASE;` and expect SSL to close the CASE block implicitly.
    - Assume `:ENDCASE;` alone prevents later [`:CASE`](CASE.md) branches from running. Use [`:EXITCASE`](EXITCASE.md) for that.

## Caveats

- [`:OTHERWISE`](OTHERWISE.md) is optional, but if present it must appear before `:ENDCASE;`.
- CASE keywords are case-sensitive and must be uppercase.

## Examples

### Closing a CASE block and continuing afterward

`:ENDCASE;` terminates the CASE structure so the procedure can continue with the next statement. With `nStatusCode` set to `2`, the second branch matches and `sLabel` is set to `"In Review"`.

```ssl
:PROCEDURE GetSampleStatusLabel;
    :DECLARE nStatusCode, sLabel, sStatus;

    nStatusCode := 2;
    sLabel := "";

    :BEGINCASE;
    :CASE nStatusCode == 1;
        sLabel := "Submitted";
        :EXITCASE;
    :CASE nStatusCode == 2;
        sLabel := "In Review";
        :EXITCASE;
    :CASE nStatusCode == 3;
        sLabel := "Approved";
        :EXITCASE;
    :OTHERWISE;
        sLabel := "Unknown";
        :EXITCASE;
    :ENDCASE;

    sStatus := "Status: " + sLabel;
    UsrMes(sStatus);

    :RETURN sLabel;
:ENDPROC;

/* Usage;
DoProc("GetSampleStatusLabel");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Status: In Review
```

## Related

- [`BEGINCASE`](BEGINCASE.md)
- [`CASE`](CASE.md)
- [`OTHERWISE`](OTHERWISE.md)
- [`EXITCASE`](EXITCASE.md)
