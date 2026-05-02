# SSL Type System

SSL has eight core value types plus NIL (the absence of a value). Every variable can hold any type — SSL is dynamically typed.

## Type overview

| Type | Literal Syntax | Empty Check | LimsType | LimsTypeEx |
|------|----------------|-------------|----------|------------|
| [number](../reference/types/number.md) | `42`, `3.14`, `-5` | `0` and [`NIL`](../reference/literals/nil.md) are empty | `"N"` | `"NUMERIC"` |
| [string](../reference/types/string.md) | `"text"` | `""` and [`NIL`](../reference/literals/nil.md) are empty | `"C"` | `"STRING"` |
| [boolean](../reference/types/boolean.md) | [`.T.`](../reference/literals/true.md), [`.F.`](../reference/literals/false.md) | [`.F.`](../reference/literals/false.md) is empty, [`.T.`](../reference/literals/true.md) is not | `"L"` | `"LOGIC"` |
| [date](../reference/types/date.md) | No literal; use [`Today()`](../reference/functions/Today.md) | Null date is empty | `"D"` | `"DATE"` |
| [array](../reference/types/array.md) | `{1, 2, 3}` | Empty array `{}` is empty | `"A"` | `"ARRAY"` |
| [object](../reference/types/object.md) | [`CreateLocal()`](../reference/functions/CreateLocal.md) | Always non-empty | `"O"` | `"OBJECT"` |
| [codeblock](../reference/types/codeblock.md) | `{| ... }` | — | — | `"CODEBLOCK"` |
| [netobject](../reference/types/netobject.md) | [`MakeNETObject(...)`](../reference/functions/MakeNETObject.md) | — | — | `"OBJECT"` |
| [`NIL`](../reference/literals/nil.md) | [`NIL`](../reference/literals/nil.md) | Always empty | `"NIL"` | `"NIL"` |

## NIL semantics

[`NIL`](../reference/literals/nil.md) represents the absence of a value. Key rules:

- [`NIL`](../reference/literals/nil.md) equals only [`NIL`](../reference/literals/nil.md) — `NIL = NIL` is [`.T.`](../reference/literals/true.md), `NIL = ""` is [`.F.`](../reference/literals/false.md)
- [`Empty`](../reference/functions/Empty.md)([`NIL`](../reference/literals/nil.md)) returns [`.T.`](../reference/literals/true.md)
- Functions that fail silently often return NIL
- When calling external libraries or receiving values from the platform layer, null values surface as [`NIL`](../reference/literals/nil.md) in SSL

## Variable initialization and scope

Variables declared with [`:DECLARE`](../reference/keywords/DECLARE.md) initialize to **empty string `""`**, not [`NIL`](../reference/literals/nil.md). [`Empty`](../reference/functions/Empty.md) returns [`.T.`](../reference/literals/true.md) for `""`, `0`, [`NIL`](../reference/literals/nil.md), and [`.F.`](../reference/literals/false.md), so it is the safe way to test for an uninitialized or default-state value across types.

When a variable is referenced, lookup proceeds in this order:

1. **Local scope** — the current procedure
2. **Caller scopes** — up the call stack
3. **Public variables** — declared with [`:PUBLIC`](../reference/keywords/PUBLIC.md)

Reading a caller's variable works but generates a warning. Always declare variables locally.

Re-declaring an existing variable with [`:DECLARE`](../reference/keywords/DECLARE.md) is silently ignored — no error is thrown and the existing value is preserved.

## Type checking

| Function | Purpose |
|----------|---------|
| [`LimsType`](../reference/functions/LimsType.md)(x) | Returns type code as string (`"C"`, `"N"`, `"D"`, `"L"`, `"A"`, `"O"`, `"NIL"`) |
| [`LimsTypeEx`](../reference/functions/LimsTypeEx.md)(x) | Extended type info (returns full type name like `"NUMERIC"`, `"STRING"`, etc.) |
| [`IsNumeric`](../reference/functions/IsNumeric.md)(x) | True if value is numeric or numeric string |
| [`Empty`](../reference/functions/Empty.md)(x) | True if value is empty for its type |
| [`IsDefined`](../reference/functions/IsDefined.md)(x) | True if variable exists in current scope |

## Type coercion

SSL performs limited implicit type coercion:

- **Number + Date** — adds days to a date (returns date)
- **String + String** — concatenates; [`+`](../reference/operators/plus.md) requires both operands to be the same type
- **String - String** — trims trailing spaces from left, then concatenates

There are **no** implicit conversions between:

- Boolean and number (`.T. = 1` throws an error)
- String and boolean
- String and number (use [`Val`](../reference/functions/Val.md) and [`LimsString`](../reference/functions/LimsString.md) explicitly)

## Equality semantics

The [`=`](../reference/operators/equals.md) / [`==`](../reference/operators/strict-equals.md) operator behavior depends on the **left operand's type**:

| Left Type | Right Type | Behavior |
|-----------|-----------|----------|
| [string](../reference/types/string.md) | [string](../reference/types/string.md) | **Prefix match** — `"abc" = "ab"` is [`.F.`](../reference/literals/false.md), but `"ab" = "abc"` is [`.T.`](../reference/literals/true.md) |
| [string](../reference/types/string.md) | non-string | Returns [`.F.`](../reference/literals/false.md) (no error) |
| [number](../reference/types/number.md) | [number](../reference/types/number.md) | Exact numeric equality |
| [number](../reference/types/number.md) | non-number | Throws runtime error |
| [boolean](../reference/types/boolean.md) | [boolean](../reference/types/boolean.md) | Value equality |
| [boolean](../reference/types/boolean.md) | non-boolean | Throws runtime error |
| [date](../reference/types/date.md) | [date](../reference/types/date.md) | Exact date/time equality |
| [date](../reference/types/date.md) | non-date | Throws runtime error |
| [object](../reference/types/object.md)/[array](../reference/types/array.md) | any | Reference equality |

!!! warning "String equality uses prefix matching"
    SSL's [`=`](../reference/operators/equals.md) operator on strings checks whether the left string starts with the right string. `"abc" = "abc"` is true, but so is `"abcdef" = "abc"`. Use [`==`](../reference/operators/strict-equals.md) with [`Len`](../reference/functions/Len.md) checks or [`$`](../reference/operators/dollar.md) (contains) for exact matching when needed.
