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
| [object](../reference/types/object.md) (class instance) | [`CreateUdObject("ClassName")`](../reference/functions/CreateUdObject.md) for a user-defined class, `Email{}` for a built-in class | Always non-empty | `"O"` | `"OBJECT"` |
| dynamic object ([`SSLExpando`](../reference/classes/SSLExpando.md)) | [`CreateUdObject()`](../reference/functions/CreateUdObject.md) or `CreateUdObject({{"prop", value}})` | Always non-empty | `"B"` | `"OBJECT"` |
| [codeblock](../reference/types/codeblock.md) | `{|param| expression}` | Never empty once created | `"UI"` | `"CODEBLOCK"` |
| [netobject](../reference/types/netobject.md) | [`MakeNETObject(...)`](../reference/functions/MakeNETObject.md) | Empty only when the wrapped reference is null | `"O"` | `"OBJECT"` |
| [`NIL`](../reference/literals/nil.md) | [`NIL`](../reference/literals/nil.md) | Always empty | `"U"` for the literal expression `"NIL"` only; see [Type checking](#type-checking) | `"NIL"` |

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

Reading a caller's variable works but generates a warning. Writing to one raises no error at run time — an assignment to a name the current scope never declared can silently overwrite a caller's variable. Always declare variables locally; see [Variable Scope](variable-scope.md) for the full model.

Re-declaring an existing variable with [`:DECLARE`](../reference/keywords/DECLARE.md) is silently ignored — no error is thrown and the existing value is preserved.

## Type checking

| Function | Purpose |
|----------|---------|
| [`LimsType`](../reference/functions/LimsType.md)(sName) | Takes a **string** holding a variable name or expression, such as `LimsType("sMyVar")`, and returns a type code: `"C"`, `"N"`, `"A"`, `"D"`, `"L"`, `"B"` (dynamic object, `SSLExpando`), `"O"`, `"U"` (undeclared name, or the literal expression `"NIL"`), `"UE"` (evaluation error), or `"UI"` (unrecognized, such as a code block). A non-string argument raises an error. |
| [`LimsTypeEx`](../reference/functions/LimsTypeEx.md)(x) | Extended type info (returns full type name like `"NUMERIC"`, `"STRING"`, etc.) |
| [`IsNumeric`](../reference/functions/IsNumeric.md)(x) | True if value is numeric or numeric string |
| [`Empty`](../reference/functions/Empty.md)(x) | True if value is empty for its type |
| [`IsDefined`](../reference/functions/IsDefined.md)(sVarName) | Takes a variable name as a string, such as `IsDefined("sMyVar")`. True if the name resolves in the current scope, a caller scope, or public scope, so a [`.T.`](../reference/literals/true.md) result does not prove the variable is local |

!!! warning "`LimsType` raises for a variable that holds NIL"
    `LimsType("NIL")` returns `"U"`, but `LimsType("vValue")` raises an error when `vValue` holds [`NIL`](../reference/literals/nil.md), and so does naming an omitted [`:PARAMETERS`](../reference/keywords/PARAMETERS.md) argument. Check for [`NIL`](../reference/literals/nil.md) first with `LimsTypeEx(vValue) == "NIL"`, or use [`LimsTypeEx`](../reference/functions/LimsTypeEx.md), which accepts any value.

## Type coercion

SSL performs limited implicit type coercion:

- **Date + Number** — adds days to a date (returns date). The date must be on the left: `Today() + 1` is a date, but `1 + Today()` raises a runtime error
- **Date - Date** — returns the difference in days (returns number)
- **String + String** — concatenates; [`+`](../reference/operators/plus.md) requires both operands to be the same type
- **String - String** — trims trailing spaces from left, then concatenates

There are **no** implicit conversions between:

- Boolean and number (`.T. = 1` throws an error)
- String and boolean
- String and number (use [`Val`](../reference/functions/Val.md) and [`LimsString`](../reference/functions/LimsString.md) explicitly)

## Equality semantics

The [`=`](../reference/operators/equals.md) operator's behavior depends on the **left operand's type**:

| Left Type | Right Type | Behavior |
|-----------|-----------|----------|
| [string](../reference/types/string.md) | [string](../reference/types/string.md) | **Prefix match** — [`.T.`](../reference/literals/true.md) when the left string starts with the right string (or the right string is empty): `"abcdef" = "abc"` is `.T.`, but `"abc" = "abcdef"` is [`.F.`](../reference/literals/false.md) |
| [string](../reference/types/string.md) | non-string | Returns [`.F.`](../reference/literals/false.md) (no error) |
| [number](../reference/types/number.md) | [number](../reference/types/number.md) | Exact numeric equality |
| [number](../reference/types/number.md) | non-number | Throws runtime error |
| [boolean](../reference/types/boolean.md) | [boolean](../reference/types/boolean.md) | Value equality |
| [boolean](../reference/types/boolean.md) | non-boolean | Throws runtime error |
| [date](../reference/types/date.md) | [date](../reference/types/date.md) | Exact date/time equality |
| [date](../reference/types/date.md) | non-date | Throws runtime error |
| [object](../reference/types/object.md)/[array](../reference/types/array.md) | any | Reference equality |
| [codeblock](../reference/types/codeblock.md) | any | Throws runtime error |

[`==`](../reference/operators/strict-equals.md) follows the same rules with one difference: for two strings it is an **exact match**, so `"Logged" == "Log"` is [`.F.`](../reference/literals/false.md) while `"Logged" = "Log"` is [`.T.`](../reference/literals/true.md).

!!! warning "String equality uses prefix matching"
    SSL's [`=`](../reference/operators/equals.md) operator on strings checks whether the left string starts with the right string. `"abc" = "abc"` is true, but so is `"abcdef" = "abc"`. Use [`==`](../reference/operators/strict-equals.md) when a string comparison must be exact.
