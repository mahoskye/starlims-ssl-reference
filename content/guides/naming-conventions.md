# Naming Conventions

SSL has well-established naming conventions for variables, procedures, classes, and constants. New and refactored code should follow them; legacy code may diverge — preserve the surrounding style when making targeted edits.

## Variables — Hungarian prefix + camelCase

Variable names start with a single-letter prefix indicating their type, followed by a descriptive camelCase name.

| Prefix | Type | Examples |
|--------|------|----------|
| `s` | [string](../reference/types/string.md) | `sName`, `sOrderNo` |
| `n` | [number](../reference/types/number.md) | `nCount`, `nTotal` |
| `b` | [boolean](../reference/types/boolean.md) | `bIsValid`, `bExists` |
| `d` | [date](../reference/types/date.md) | `dStartDate`, `dExpiry` |
| `a` | [array](../reference/types/array.md) | `aResults`, `aOrderList` |
| `o` | [object](../reference/types/object.md) | `oCustomer`, `oDataset` |
| `fn` | [codeblock](../reference/types/codeblock.md) | `fnFilter`, `fnCallback` |
| `v` | variant / any | `vResult`, `vParam` |

**Length:** keep variable names ≤ 20 characters after the prefix; procedure and function names ≤ 30 characters.

**Exceptions:**

- Loop counters may use single letters: `i`, `j`, `k`, `x`, `y`, `z`
- Constants use `UPPER_SNAKE_CASE` (no Hungarian prefix)
- The literals [`NIL`](../reference/literals/nil.md), [`.T.`](../reference/literals/true.md), and [`.F.`](../reference/literals/false.md) are language tokens, not identifiers
- Preserve established acronym casing from surrounding code or external schema names

## Procedures and classes — PascalCase

- **Procedure names** are PascalCase, ideally **verb + noun**: `ValidateOrder`, `ProcessQCSample`, `CalculateTotal`, `InitializeState`.
- **Class names** are PascalCase: `OrderProcessor`, `SampleValidator`.

## Object property casing

| Property kind | Casing | Examples |
|---------------|--------|----------|
| User-defined object (UDO) properties | lowerCamelCase, no type prefix | `oOrder:orderNo`, `oState:isValid` |
| Built-in / system object properties | PascalCase (defined by STARLIMS) | `oError:Description`, `oSeq:SequenceName` |

## Constants

Constants are declared like any other variable but named in `UPPER_SNAKE_CASE` and assigned once near the top of the script:

```ssl
:DECLARE LOGGED_STATUS, MAX_ATTEMPTS, DEFAULT_TIMEOUT;

LOGGED_STATUS := "Logged";
MAX_ATTEMPTS := 3;
DEFAULT_TIMEOUT := 30;
```

## Built-in function casing

Built-in function names should be written in their documented casing — usually PascalCase ([`Len`](../reference/functions/Len.md), [`ALen`](../reference/functions/ALen.md), [`UsrMes`](../reference/functions/UsrMes.md)). SSL is case-insensitive for identifiers, but matching documented casing keeps code searchable and consistent.

Canonical exceptions to PascalCase: [`_AND`](../reference/functions/_AND.md), [`_OR`](../reference/functions/_OR.md), [`_XOR`](../reference/functions/_XOR.md), [`_NOT`](../reference/functions/_NOT.md), [`DOW`](../reference/functions/DOW.md), [`DOY`](../reference/functions/DOY.md), [`LIMSDate`](../reference/functions/LIMSDate.md).

## Code organization regions

For editor-level grouping (folding, navigation), use comment-based regions:

```ssl
/* region Validation;
    /* ... validation procedures ...;
/* endregion;
```

Do **not** use [`:REGION`](../reference/keywords/REGION.md) / [`:ENDREGION`](../reference/keywords/ENDREGION.md) for code organization — those are functional text-capture constructs, not editor folds, and have runtime semantics.
