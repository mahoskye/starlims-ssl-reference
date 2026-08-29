# Variable Scope

SSL resolves a variable name outward through the call stack, not just inside the
routine that uses it. A name a script never declares is **not private to that
script**: assigning to it can reach up and overwrite a variable belonging to
whatever called it, silently and with no error.

Declaring every name a routine uses is what keeps that from happening.

## Name resolution order

When a script, procedure, or method references a name, the runtime looks for it
in this order:

1. **Current scope** — names introduced by [`:DECLARE`](../reference/keywords/DECLARE.md),
   [`:PARAMETERS`](../reference/keywords/PARAMETERS.md), or
   [`CreateLocal`](../reference/functions/CreateLocal.md) in the routine that is running.
2. **Caller scopes** — the scopes of the routines currently on the call stack,
   innermost first.
3. **Public variables** — names introduced by [`:PUBLIC`](../reference/keywords/PUBLIC.md)
   or [`CreatePublic`](../reference/functions/CreatePublic.md).

The search stops at the first match. This applies to **writes as well as reads**
— an assignment does not automatically create a variable in the current scope.

Reading a caller's variable works but generates a warning. Writing to one does
not announce itself at all.

## Declaring is what makes a name private

[`:DECLARE`](../reference/keywords/DECLARE.md) creates the name in the current
scope, so resolution stops there instead of continuing outward. A routine that
declares a name gets its own variable: a same-named variable in a caller is
neither read nor written, and still holds its original value after the callee
returns.

[`CreateLocal`](../reference/functions/CreateLocal.md) does the same thing for a
name that is only known at runtime.

## An undeclared name is not private

If the current scope never declares a name, resolution continues outward and a
write lands on the first match it finds. When a script invoked through
[`ExecFunction`](../reference/functions/ExecFunction.md) or
[`DoProc`](../reference/functions/DoProc.md) assigns to a name its caller also
uses undeclared, both routines are using the same variable.

[`:FOR`](../reference/keywords/FOR.md) is where this bites most often, because a
`:FOR` header assigns to its loop variable — and generic counters like `i` are
exactly the names two unrelated scripts are most likely to share.

Two scripts, neither declaring anything:

```ssl
/* Test.Exterior;
:FOR i := 1 :TO 3;
    UsrMes("Exterior i = " + LimsString(i));
    ExecFunction("Test.Interior");
    UsrMes("Exterior i is now " + LimsString(i));
:NEXT;
```

```ssl
/* Test.Interior;
:FOR i := 1 :TO 3;
    UsrMes("Interior i = " + LimsString(i));
:NEXT;
```

`Test.Interior` never declares `i`, so its loop header resolves `i` outward and
finds the caller's. The interior loop drives that shared variable past the
exterior loop's limit, and the exterior loop exits after a single pass:

```text
Exterior i = 1
Interior i = 1
Interior i = 2
Interior i = 3
Exterior i is now 4
```

Nothing reports an error. The exterior loop simply appears to run once.

### The fix

Declare the loop variable in the called script:

```ssl
/* Test.Interior;
:DECLARE i;

:FOR i := 1 :TO 3;
    UsrMes("Interior i = " + LimsString(i));
:NEXT;
```

`Test.Interior` now has its own `i`, the caller's counter is untouched, and the
exterior loop runs every iteration:

```text
Exterior i = 1
Interior i = 1
Interior i = 2
Interior i = 3
Exterior i is now 1
Exterior i = 2
Interior i = 1
Interior i = 2
Interior i = 3
Exterior i is now 2
Exterior i = 3
Interior i = 1
Interior i = 2
Interior i = 3
Exterior i is now 3
```

The protection comes from the **callee** declaring the name. A script cannot
defend its own variables against a script it calls that leaves names undeclared,
so treat declaration as an obligation every script owes its callers.

!!! warning "Distinctive names reduce collisions, but declaring is the fix"
    Giving a counter a script-specific name (`nSampleIdx` rather than `i`) makes
    an accidental collision far less likely and is worth doing — see
    [Naming Conventions](naming-conventions.md). It is defense in depth, not a
    substitute: any undeclared name can still collide with a caller's name of
    the same spelling.

## Public variables

[`:PUBLIC`](../reference/keywords/PUBLIC.md) and
[`CreatePublic`](../reference/functions/CreatePublic.md) create names that are
resolved by name rather than by position on the call stack, so a routine can
reach them without any caller having declared them. They stay available until
the current program context clears them.

Publics are checked **last**, so a current-scope or caller-scope name of the same
spelling wins over a public one of the same name.

Use publics for state that genuinely must be shared across scopes, and give them
stable, specific names — anything on the call stack can overwrite them.

## Class fields

[`:DECLARE`](../reference/keywords/DECLARE.md) in a class body declares class
fields rather than locals. Inside a method, a bare identifier always resolves as
a local or [`:PARAMETERS`](../reference/keywords/PARAMETERS.md) entry — never as
a class field of the same name. Qualify field access with
[`Me:`](../reference/special-forms/me.md), or
[`Base:`](../reference/special-forms/base.md) for an inherited parent field.

## Resolving names at runtime

When the name itself is data, these functions follow the same resolution order:

| Function | Purpose |
|----------|---------|
| [`GetByName`](../reference/functions/GetByName.md) | Read a variable by name from local or public storage |
| [`SetByName`](../reference/functions/SetByName.md) | Write by name — may update a **caller's** variable rather than create a local |
| [`CreateLocal`](../reference/functions/CreateLocal.md) | Create or overwrite a name in the current scope |
| [`CreatePublic`](../reference/functions/CreatePublic.md) | Create or overwrite a public variable |
| [`IsDefined`](../reference/functions/IsDefined.md) | Test whether a name exists in the current scope |
| [`LKill`](../reference/functions/LKill.md) | Remove a variable by name |

[`SetByName`](../reference/functions/SetByName.md) carries the same hazard as a
plain assignment, and more visibly: if the name is not in the current scope, it
walks out to caller scopes and publics before deciding to create anything.

## Rules

- Declare every name a routine uses, including [`:FOR`](../reference/keywords/FOR.md)
  loop counters — declaration is the only thing that makes a name private to the
  current scope
- Assume any undeclared name may already exist in a caller; an assignment to it
  is a write to the caller's variable, not a new variable
- Declare in scripts you call as well as scripts you write — the callee's
  declaration is what protects the caller
- Prefer script-specific counter names over bare `i`, `j`, `k` in scripts that
  call other scripts, as defense in depth
- Use [`:PUBLIC`](../reference/keywords/PUBLIC.md) only for state that must
  genuinely cross scopes, never for routine-local working values
- Qualify class fields with [`Me:`](../reference/special-forms/me.md) inside
  methods; a bare identifier there is always a local

## Related

- [`:DECLARE`](../reference/keywords/DECLARE.md) — introduce names in the current scope
- [`:PUBLIC`](../reference/keywords/PUBLIC.md) — share names down the call stack
- [`:PARAMETERS`](../reference/keywords/PARAMETERS.md) — declare a routine's arguments
- [`:FOR`](../reference/keywords/FOR.md) — counted loops and their loop variable
- [Type System](type-system.md) — initialization values and type checking
- [Naming Conventions](naming-conventions.md) — Hungarian prefixes and counter naming
