---
title: "SQLRemoveComments"
summary: "Removes SQL comments from a string and returns the cleaned SQL text."
id: ssl.function.sqlremovecomments
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SQLRemoveComments

Removes SQL comments from a string and returns the cleaned SQL text.

`SQLRemoveComments` is a string-cleanup helper. It removes [`--`](../operators/decrement.md) line comments and ordinary `/* ... */` block comments from the supplied SQL text, but it does not execute or validate the SQL. If `sStatement` is [`NIL`](../literals/nil.md), the function returns [`NIL`](../literals/nil.md). If `sStatement` is an empty string, it returns the empty string unchanged. If `sStatement` is any non-string value, the function raises an argument error.

Single-quoted SQL string literals are preserved, so comment markers inside a quoted SQL value are not stripped. Oracle optimizer hints that start with `/*+` are also preserved.

## When to use

- When you want to normalize SQL text before logging, diffing, or displaying it.
- When comments interfere with downstream text processing such as pattern matching or hashing.
- When you need to remove ordinary SQL comments but keep the executable SQL text.

## Syntax

```ssl
SQLRemoveComments(sStatement)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sStatement` | [string](../types/string.md) | yes | — | SQL text to clean. [`NIL`](../literals/nil.md) is accepted and returned unchanged. |

## Returns

**[string](../types/string.md) or NIL**

| Condition | Return type | Behavior |
|-----------|-------------|----------|
| `sStatement` is [`NIL`](../literals/nil.md) | [`NIL`](../literals/nil.md) | Returns [`NIL`](../literals/nil.md). |
| `sStatement` is `""` | [string](../types/string.md) | Returns the empty string unchanged. |
| `sStatement` is a non-empty string | [string](../types/string.md) | Returns the SQL text with [`--`](../operators/decrement.md) comments and ordinary `/* ... */` comments removed. |

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sStatement` is not a string and not [`NIL`](../literals/nil.md). | `Argument 'sStatement' must be a string` |

## Best practices

!!! success "Do"
    - Use `SQLRemoveComments` when you need cleaned SQL text for logging,
      comparison, or display.
    - Handle the [`NIL`](../literals/nil.md) return path when the source SQL text can be missing.
    - Keep optimizer hints in mind: `/*+ ... */` is preserved rather than removed.

!!! failure "Don't"
    - Treat this as SQL validation or SQL injection protection; it only
      removes supported comment forms.
    - Assume every `/* ... */` sequence will be stripped; optimizer hints
      beginning with `/*+` are left in place.
    - Pass numbers, arrays, objects, or booleans; non-string non-[`NIL`](../literals/nil.md)
      values raise an error.

## Caveats

- [`--`](../operators/decrement.md) comments are removed through the end of the line.
- The function does not check whether the remaining SQL is valid.

## Examples

### Remove line and block comments from a query

Pass SQL containing both a `/* ... */` block comment and a [`--`](../operators/decrement.md) line comment; the result is the same statement with those comment sequences stripped.

```ssl
:PROCEDURE RemoveCommentsFromSQL;
    :DECLARE sSQL, sCleaned;

    sSQL := "
        /* Get active samples */
        SELECT sample_id, sample_name, status
        FROM samples
        WHERE status = 'A' -- only active rows
    ";

    sCleaned := SQLRemoveComments(sSQL);

    UsrMes(sCleaned);
    /* Displays cleaned SQL text;

    :RETURN sCleaned;
:ENDPROC;

/* Usage;
DoProc("RemoveCommentsFromSQL");
```

### Preserve comment markers inside quoted string literals

Verify that [`--`](../operators/decrement.md) and `/* ... */` sequences inside single-quoted SQL literals are not stripped while an unquoted block comment is removed.

```ssl
:PROCEDURE PreserveQuotedMarkers;
    :DECLARE sRawSQL, sCleanSQL;

    sRawSQL := "
        SELECT sample_id, '--keep-this-text' AS literal_value
        FROM sample
        WHERE note = 'contains /* not a comment */ text'
        /* remove this block comment */
        AND status = 'A'
    ";

    sCleanSQL := SQLRemoveComments(sRawSQL);

    UsrMes(sCleanSQL);
    /* Displays cleaned SQL text with quoted literals preserved;

    :RETURN sCleanSQL;
:ENDPROC;

/* Usage;
DoProc("PreserveQuotedMarkers");
```

### Preserve an Oracle optimizer hint while removing other comments

Confirm that a `/*+ ... */` optimizer hint is kept while a regular block comment and a line comment are removed.

```ssl
:PROCEDURE PreserveOptimizerHint;
    :DECLARE sRawSQL, sCleanSQL;

    sRawSQL := "
        SELECT /*+ INDEX(sample idx_sample_status) */
               sample_id, sample_name
        FROM sample
        /* remove this note */
        WHERE status = 'A' -- keep only active rows
        ORDER BY sample_name
    ";

    sCleanSQL := SQLRemoveComments(sRawSQL);

    UsrMes(sCleanSQL);
    /* Displays cleaned SQL text with the optimizer hint preserved;

    :RETURN sCleanSQL;
:ENDPROC;

/* Usage;
DoProc("PreserveOptimizerHint");
```

## Related

- [`RunSQL`](RunSQL.md)
- [`SQLExecute`](SQLExecute.md)
- [`string`](../types/string.md)
