---
title: "LCase"
summary: "Conditionally evaluates one of two SSL expressions supplied as strings."
id: ssl.function.lcase
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LCase

Conditionally evaluates one of two SSL expressions supplied as strings.

`LCase` checks `bCondition` and executes either the `sTrueValue` expression or the `sFalseValue` expression. The selected argument is not returned as plain text. It is wrapped in `:RETURN ...;` and evaluated as SSL, so the function returns whatever value that expression produces. If `bCondition` is false and `sFalseValue` is omitted, [`NIL`](../literals/nil.md), empty, or whitespace-only, `LCase` returns an empty string.

## When to use

- When you need a compact two-way choice but want only the selected branch to be evaluated.
- When each branch is naturally represented as a short SSL expression stored as text.
- When you want the false branch to fall back to an empty string.

## Syntax

```ssl
LCase(bCondition, sTrueValue, [sFalseValue])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `bCondition` | [boolean](../types/boolean.md) | yes | — | Determines which expression string `LCase` executes |
| `sTrueValue` | [string](../types/string.md) | yes | — | SSL expression text to execute when `bCondition` is true |
| `sFalseValue` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | SSL expression text to execute when `bCondition` is false. If omitted, [`NIL`](../literals/nil.md), empty, or whitespace-only, `LCase` returns an empty string |

## Returns

**any** — The value produced by the selected expression.

Behavior by branch:

- When `bCondition` is [`.T.`](../literals/true.md), `LCase` executes `sTrueValue` and returns that result.
- When `bCondition` is [`.F.`](../literals/false.md) and `sFalseValue` contains text, `LCase` executes `sFalseValue` and returns that result.
- When `bCondition` is [`.F.`](../literals/false.md) and `sFalseValue` is omitted, [`NIL`](../literals/nil.md), empty, or whitespace-only, `LCase` returns `""`.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `bCondition` or `sTrueValue` is [`NIL`](../literals/nil.md). | `Null argument passed to LCase()` |

## Best practices

!!! success "Do"
    - Pass valid SSL expressions as strings, such as variable names, function calls, or quoted literals.
    - Use quoted string literals inside the expression text when you want a string result, for example `LCase(bFlag, '"Yes"', '"No"')`.
    - Keep branch expressions short and predictable so the selected result is easy to understand.

!!! failure "Don't"
    - Treat `sTrueValue` and `sFalseValue` as plain return text. `LCase` executes them as SSL.
    - Pass unquoted text when you mean a string literal. `LCase(bFlag, "Yes", "No")` tries to evaluate `Yes` or `No` as identifiers, not string literals.
    - Use untrusted input as expression text. The selected branch is executed.

## Caveats

- `LCase` can return different value types depending on the selected expression.
- Only the selected branch is executed.
- Whitespace-only `sFalseValue` is treated the same as an empty false branch and returns `""`.
- If the selected expression is not valid in the current context, the evaluation can fail.

## Examples

### Choose between two literal labels

Pass quoted string literals as both branch arguments. Because the branch expressions are evaluated as SSL, the inner quotes make each branch a string literal rather than an identifier. With `bApproved` set to [`.T.`](../literals/true.md), the true branch fires and `sLabel` receives `"Approved"`.

```ssl
:PROCEDURE GetApprovalLabel;
    :DECLARE bApproved, sLabel;

    bApproved := .T.;
    sLabel := LCase(bApproved, '"Approved"', '"Pending Review"');

    UsrMes(sLabel);
    :RETURN sLabel;
:ENDPROC;

/* Usage;
DoProc("GetApprovalLabel");
```

[`UsrMes`](UsrMes.md) displays:

```text
Approved
```

### Use an empty false branch

Omit the false branch to get an empty string when the condition is [`.F.`](../literals/false.md). When `bNeedsReview` is [`.T.`](../literals/true.md), the suffix `"-R"` is appended; when it is [`.F.`](../literals/false.md), `sSuffix` is `""` and the base code is returned unchanged.

```ssl
:PROCEDURE BuildSampleCode;
    :DECLARE bNeedsReview, sBaseCode, sSuffix, sFinalCode;

    bNeedsReview := .T.;
    sBaseCode := "LAB-2026-001";
    sSuffix := LCase(bNeedsReview, '"-R"');

    sFinalCode := sBaseCode + sSuffix;

    :RETURN sFinalCode;
:ENDPROC;

/* Usage;
DoProc("BuildSampleCode");
```

### Return a non-string value from a variable expression

Pass variable names (without quotes) as the branch expressions to have `LCase` return the value of whichever variable is selected. With `bUseOverride` set to [`.T.`](../literals/true.md), the expression `"nOverrideLimit"` is evaluated and `nEffectiveLimit` receives `25`.

```ssl
:PROCEDURE GetEffectiveLimit;
    :DECLARE bUseOverride, nDefaultLimit, nOverrideLimit, nEffectiveLimit;

    bUseOverride := .T.;
    nDefaultLimit := 10;
    nOverrideLimit := 25;

    nEffectiveLimit := LCase(bUseOverride, "nOverrideLimit", "nDefaultLimit");

    :RETURN nEffectiveLimit;
:ENDPROC;

/* Usage;
DoProc("GetEffectiveLimit");
```

## Related

- [`IIf`](IIf.md)
- [`IF`](../keywords/IF.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
