---
title: "Operators"
summary: "32 operators - arithmetic, comparison, logical, bitwise, and assignment."
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Operators

**32 operators** — arithmetic, comparison, logical, bitwise, and assignment.

## Precedence Table

Operators listed from highest precedence (binds tightest) to lowest. Operators at the same level are evaluated according to their associativity.

| Precedence | Operator | Symbol | Associativity |
|------------|----------|--------|---------------|
| Highest — Unary | [bang](bang.md) | `!` | right |
| Unary | [increment](increment.md) | `++` | none |
| Unary | [decrement](decrement.md) | `--` | none |
| Unary | [not](not.md) | `.NOT.` | right |
| Additive | [minus](minus.md) | `-` | left |
| Additive | [plus](plus.md) | `+` | left |
| Multiplicative | [multiply](multiply.md) | `*` | left |
| Multiplicative | [divide](divide.md) | `/` | left |
| Multiplicative | [modulo](modulo.md) | `%` | left |
| Power | [power](power.md) | `^` | right |
| Power | [double-star-power](double-star-power.md) | `**` | right |
| Shift | [shift-left](shift-left.md) | `<<` | left |
| Shift | [shift-right](shift-right.md) | `>>` | left |
| Relational | [less-than](less-than.md) | `<` | left |
| Relational | [greater-than](greater-than.md) | `>` | left |
| Relational | [less-than-or-equal](less-than-or-equal.md) | `<=` | left |
| Relational | [greater-than-or-equal](greater-than-or-equal.md) | `>=` | left |
| Equality | [equals](equals.md) | `=` | left |
| Equality | [strict-equals](strict-equals.md) | `==` | left |
| Equality | [not-equals](not-equals.md) | `!=` | left |
| Equality | [not-equals-legacy](not-equals-legacy.md) | `<>` | left |
| Equality | [hash](hash.md) | `#` | left |
| Containment | [dollar](dollar.md) | `$` | left |
| Logical AND | [and](and.md) | `.AND.` | left |
| Logical OR | [or](or.md) | `.OR.` | left |
| Assignment | [assignment](assignment.md) | `:=` | right |
| Assignment | [add-assign](add-assign.md) | `+=` | right |
| Assignment | [subtract-assign](subtract-assign.md) | `-=` | right |
| Assignment | [multiply-assign](multiply-assign.md) | `*=` | right |
| Assignment | [divide-assign](divide-assign.md) | `/=` | right |
| Assignment | [modulo-assign](modulo-assign.md) | `%=` | right |
| Lowest — Assignment | [power-assign](power-assign.md) | `^=` | right |
