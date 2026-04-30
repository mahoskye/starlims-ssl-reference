---
title: "Keywords"
summary: "38 keywords grouped by purpose."
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Keywords

**38 keywords** grouped by purpose.

## Declarations

| Keyword | Description |
|---------|-------------|
| [:DECLARE](DECLARE.md) | Declares one or more variables in the current SSL scope. |
| [:DEFAULT](DEFAULT.md) | Assigns a fallback expression to a parameter when the caller omits that argument. |
| [:INCLUDE](INCLUDE.md) | Inserts another SSL script's source into the current file so its statements compile inline. |
| [:INHERIT](INHERIT.md) | Specifies the parent class for an SSL class. |
| [:PARAMETERS](PARAMETERS.md) | Declares named input parameters for a script, procedure, method, or constructor. |
| [:PUBLIC](PUBLIC.md) | Declares global variables that can be accessed from any scope in the program. |

## Control Flow

| Keyword | Description |
|---------|-------------|
| [:BEGINCASE](BEGINCASE.md) | Starts a block for evaluating one or more boolean conditions, with an optional default branch and a required closing keyword. |
| [:CASE](CASE.md) | Executes a block of statements if a specific boolean expression evaluates to true within a case structure. |
| [:ELSE](ELSE.md) | Directs control to an alternate set of statements when the preceding `:IF` condition is false. |
| [:ENDCASE](ENDCASE.md) | Closes a `:BEGINCASE` block after its `:CASE` branches and optional `:OTHERWISE` branch. |
| [:ENDIF](ENDIF.md) | Terminates an `:IF` block, with or without an `:ELSE` branch. |
| [:EXITCASE](EXITCASE.md) | Ends the current `:CASE` or `:OTHERWISE` branch and continues with the first statement after `:ENDCASE`. |
| [:IF](IF.md) | Executes a block of statements only when a condition evaluates to true. |
| [:OTHERWISE](OTHERWISE.md) | Executes the default branch of a `:BEGINCASE` block when no earlier `:CASE` branch runs. |

## Loops

| Keyword | Description |
|---------|-------------|
| [:ENDWHILE](ENDWHILE.md) | Closes a `:WHILE` loop block. |
| [:EXITFOR](EXITFOR.md) | Terminates the innermost active `:FOR` loop immediately and continues with the statement after the matching `:NEXT`. |
| [:EXITWHILE](EXITWHILE.md) | Terminates the innermost active `:WHILE` loop and continues with the statement after the matching `:ENDWHILE`. |
| [:FOR](FOR.md) | Executes a counted loop by assigning a numeric variable, checking it against a numeric limit, and updating it after each iteration. |
| [:LOOP](LOOP.md) | Skips the rest of the current `:WHILE` or `:FOR` iteration and continues with the next iteration of the innermost active loop. |
| [:NEXT](NEXT.md) | Closes a `:FOR` loop and returns control to the loop's increment-and-test step. |
| [:STEP](STEP.md) | Sets the increment or decrement used by a `:FOR` loop between iterations. |
| [:TO](TO.md) | Sets the inclusive loop limit used by a `:FOR` loop. |
| [:WHILE](WHILE.md) | Repeats a block of statements as long as a supplied condition evaluates to true. |

## Procedures & Classes

| Keyword | Description |
|---------|-------------|
| [:CLASS](CLASS.md) | Defines a class in SSL that can declare fields, methods, an optional base class, and a constructor. |
| [:ENDPROC](ENDPROC.md) | Terminates a procedure block and signals the end of its executable statements. |
| [:PROCEDURE](PROCEDURE.md) | Declares a named routine body that can contain executable SSL statements, ending with `:ENDPROC`. |
| [:RETURN](RETURN.md) | Ends the current script, procedure, or method immediately and can optionally return a value. |

## Error Handling

| Keyword | Description |
|---------|-------------|
| [:CATCH](CATCH.md) | Handles errors raised in the immediately preceding `:TRY` block. |
| [:ENDTRY](ENDTRY.md) | Closes a structured `:TRY` block after its `:CATCH` and/or `:FINALLY` sections. |
| [:ERROR](ERROR.md) | Defines a legacy error handler for the statements that follow it in the current procedure or method. |
| [:FINALLY](FINALLY.md) | Starts the cleanup section of a `:TRY` block and always runs after the protected work completes. |
| [:RESUME](RESUME.md) | Continues execution after a legacy `:ERROR` handler, starting with the statement after the one that failed. |
| [:TRY](TRY.md) | Starts a protected block that can transfer control to `:CATCH`, `:FINALLY`, or both when errors occur. |

## Organization

| Keyword | Description |
|---------|-------------|
| [:BEGININLINECODE](BEGININLINECODE.md) | Starts a named inline SSL code block stored for later retrieval with `GetInlineCode()`. |
| [:ENDINLINECODE](ENDINLINECODE.md) | Ends a named inline SSL code block opened by `:BEGININLINECODE`. |
| [:ENDREGION](ENDREGION.md) | Marks the end of a `:REGION` block; has no standalone runtime behavior. |
| [:LABEL](LABEL.md) | Marks a named location in a procedure or script for control flow redirection. |
| [:REGION](REGION.md) | Starts a named region block whose body is stored as text for later retrieval with `GetRegion()`. |
