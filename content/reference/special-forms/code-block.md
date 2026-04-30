---
title: "code-block"
summary: "Defines an anonymous code block with bound variables and a single expression body. A code block can be created at the top level, passed as a function argument, or assigned to a variable for later execution."
id: ssl.special_form.code-block
element_type: special_form
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# code-block

## What it does

Defines an anonymous code block with bound variables and a single expression body. A code block can be created at the top level, passed as a function argument, or assigned to a variable for later execution.

A code block uses the form `{|param1, param2| expression}`. The compiler requires at least one bound variable between the pipes. Invoke a code block with [`Eval`](../functions/Eval.md), or pass it to built-ins such as [`AEval`](../functions/AEval.md), [`AEvalA`](../functions/AEvalA.md), and [`AScan`](../functions/AScan.md) that accept code blocks directly. [`LimsTypeEx`](../functions/LimsTypeEx.md) reports the value as `CODEBLOCK`.

At runtime, a code block is a callable value. When invoked, the runtime evaluates the expression body using the supplied arguments plus any referenced values from the surrounding scope captured by reference.

## When to use it

- When you need to pass custom logic as an argument to another function, such as
  filtering or iterating with [`AEval`](../functions/AEval.md).
- When you want to create small, reusable behaviors without defining a named
  procedure.
- When deferring execution or controlling the time and context in which a piece
  of code runs.

## Syntax

```ssl
{|param1| expression}
{|param1, param2| expression}
```

Code blocks contain a single expression, not a sequence of statements. When the block is evaluated, that expression produces the return value.

## Context rules

Code blocks can be used in:

- Function arguments: `AEval(aItems, {|sItem| UsrMes(sItem)})`
- Assignment right-hand side: `fnNext := {|nValue| nValue + 1}`
- Top-level expressions
- Nested inside another code block expression

Code blocks cannot appear as the left-hand side of an assignment.

## Notes for daily SSL work

!!! success "Do"
    - Use code blocks for behavior that will be used as a parameter, returned,
      or deferred for later execution.
    - Clearly declare all parameters needed within the code block head.
    - Use code blocks to avoid repetition in higher-order functions.

!!! failure "Don't"
    - Define long or complex business logic directly inside code blocks. Code blocks are single expressions; delegate larger logic to named procedures.
    - Rely implicitly on outer variables unless intentional. Making dependencies explicit enhances clarity and minimizes accidental reliance on external state.
    - Copy and paste similar logic instead of abstracting it with a code block.

## Errors and edge cases

- Code blocks contain a single expression, not multiple statements.
- The compiler requires at least one bound variable between the pipes.
- Comparing code blocks directly is not supported.
- Executing a code block with missing required parameters results in a runtime error.
- Outer variables referenced inside a code block are captured by reference. Changes to those variables in the outer scope are visible inside later [`Eval`](../functions/Eval.md) calls.

## Examples

### Inline iteration with AEval

Passes a code block directly to [`AEval`](../functions/AEval.md) to call [`UsrMes`](../functions/UsrMes.md) for each element in the array without writing a named procedure.

```ssl
:DECLARE aItems;

aItems := {"SAMPLE-001", "SAMPLE-002", "SAMPLE-003"};

AEval(aItems, {|sItem| UsrMes("Processing: " + sItem)});
```

[`UsrMes`](../functions/UsrMes.md) displays (once per element):

```
Processing: SAMPLE-001
Processing: SAMPLE-002
Processing: SAMPLE-003
```

### Custom filtering with Eval

Assigns a filter condition to a variable and uses [`Eval`](../functions/Eval.md) to apply it to each element. The array `{15, 8, 42, 23, 3, 19, 7, 31}` has five values greater than 10.

```ssl
:PROCEDURE FilterHighValues;
    :DECLARE aNumbers, aFiltered, fnIsHigh, nIndex;

    aNumbers := {15, 8, 42, 23, 3, 19, 7, 31};

    fnIsHigh := {|nValue| nValue > 10};

    aFiltered := {};
    :FOR nIndex := 1 :TO ALen(aNumbers);
        :IF Eval(fnIsHigh, aNumbers[nIndex]);
            AAdd(aFiltered, aNumbers[nIndex]);
        :ENDIF;
    :NEXT;

    UsrMes("Found " + LimsString(ALen(aFiltered)) + " values above 10");

    :RETURN aFiltered;
:ENDPROC;

/* Usage;
DoProc("FilterHighValues");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```
Found 5 values above 10
```

### Capturing outer variables by reference

Shows that a code block captures its surrounding scope by reference. When `nBase` changes from 10 to 100, subsequent [`Eval`](../functions/Eval.md) calls produce the updated result.

```ssl
:PROCEDURE CaptureDemo;
    :DECLARE nBase, fnAdd;

    nBase := 10;

    fnAdd := {|nX| nX + nBase};

    UsrMes(LimsString(Eval(fnAdd, 5)));  /* Displays with nBase = 10;

    nBase := 100;

    UsrMes(LimsString(Eval(fnAdd, 5)));  /* Displays with nBase = 100;
:ENDPROC;

/* Usage;
DoProc("CaptureDemo");
```

## Related elements

- [`AEval`](../functions/AEval.md)
- [`AEvalA`](../functions/AEvalA.md)
- [`Eval`](../functions/Eval.md)
- [`AScan`](../functions/AScan.md)
