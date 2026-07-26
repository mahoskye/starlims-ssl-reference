---
title: "Literals"
summary: "3 literal values - boolean and null constants."
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Literals

**3 literal values** — boolean and null constants.

These are the only named constants in the language, and each carries non-obvious comparison and empty-check behavior worth reading before use. Number, string, date, and array values are written directly (`42`, `"text"`, `{1, 2}`) and are covered on their [type pages](../types/index.md).

| Literal | SSL syntax | Description |
|---------|------------|-------------|
| [false](false.md) | `.F.` | Represents the boolean value false in SSL expressions, with specific behaviors in comparison, type coercion, and empty checks. |
| [nil](nil.md) | `NIL` | Represents the absence of a value — an explicit empty or uninitialized state in SSL expressions and conditions. |
| [true](true.md) | `.T.` | Represents the boolean value true in SSL expressions and conditions. |
