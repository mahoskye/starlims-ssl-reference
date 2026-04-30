---
title: "ENDREGION"
summary: "Keyword that marks the end of a :REGION block; it has no standalone runtime behavior."
id: ssl.keyword.endregion
element_type: keyword
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ENDREGION

Keyword that marks the end of a [`:REGION`](REGION.md) block; it has no standalone runtime behavior.

`:ENDREGION;` closes a preceding [`:REGION`](REGION.md) block. SSL stores the text between `:REGION name;` and `:ENDREGION;` as region content, so `:ENDREGION;` is not used as an independent executable statement. It accepts no arguments, returns no value, and has no side effects of its own.

## When to use

- When closing every [`:REGION`](REGION.md) block — `:ENDREGION;` is required to complete the region capture.

## Syntax

```ssl
:ENDREGION;
```

## Keyword group

**Group:** Organization
**Role:** closer

## Best practices

!!! success "Do"
    - Close every [`:REGION`](REGION.md) block with a matching `:ENDREGION;` before returning to normal script statements.
    - Use a valid identifier in the opening [`:REGION`](REGION.md) name so the region can be retrieved reliably with [`GetRegion()`](../functions/GetRegion.md).

!!! failure "Don't"
    - Treat `:ENDREGION;` as executable logic. It only closes a region capture started by [`:REGION`](REGION.md).
    - Use [`:REGION`](REGION.md) and `:ENDREGION` when you only want editor folding. Prefer `/* region` and `/* endregion` comments for code organization.

## Caveats

- SSL keywords are case-sensitive, so `:endregion` is not valid syntax.

## Examples

### Closing a named region template

`:ENDREGION;` ends the region capture so the template text can be retrieved with [`GetRegion()`](../functions/GetRegion.md). The `%USER%` placeholder is replaced with the current `MYUSERNAME` value at retrieval time.

```ssl
:PROCEDURE BuildHeaderTemplate;
    :DECLARE aSource, aTarget, sHeader;

    aSource := {"%USER%"};
    aTarget := {MYUSERNAME};

    /* Capture a reusable text template;
    :REGION ReportHeader;
Laboratory report
Prepared for: %USER%
    :ENDREGION;

    sHeader := GetRegion("ReportHeader", aSource, aTarget);
    UsrMes(sHeader);

    :RETURN sHeader;
:ENDPROC;

/* Usage;
DoProc("BuildHeaderTemplate");
```

`UsrMes` displays this output when the current user is `jsmith`:

```
Laboratory report
Prepared for: jsmith
```

## Related

- [`REGION`](REGION.md)
- [`GetRegion`](../functions/GetRegion.md)
