---
title: "Rat"
summary: "Finds the last occurrence of a substring in a string and returns its one-based position."
id: ssl.function.rat
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Rat

Finds the last occurrence of a substring in a string and returns its one-based position.

`Rat()` searches `source` for the rightmost occurrence of `subStr`. It returns a one-based match position, or `0` when the substring is not present.

Use `Rat()` when you need the last delimiter, suffix marker, or final repeated token in a string. If you need the first occurrence instead, use [`At`](At.md).

## When to use

- When you need the last delimiter in a file name, path, or qualified name.
- When you need to split text into a prefix and trailing segment.
- When later logic depends on the rightmost occurrence rather than the first.

## Syntax

```ssl
Rat(subStr, source)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `subStr` | [string](../types/string.md) | yes | — | Substring to look for. |
| `source` | [string](../types/string.md) | yes | — | String to search. |

## Returns

**[number](../types/number.md)** — The one-based position of the last match, or `0` when no match is found.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `subStr` is [`NIL`](../literals/nil.md). | `Argument subStr cannot be null.` |
| `source` is [`NIL`](../literals/nil.md). | `Argument source cannot be null.` |

## Best practices

!!! success "Do"
    - Check for `0` before using the result as a string position.
    - Use `Rat()` when you need the last occurrence rather than the first.
    - Validate inputs when null values are possible.
    - Use the returned position directly with string functions that expect one-based indexes.

!!! failure "Don't"
    - Assume the result is zero-based. `Rat()` returns `1` for a match at the first character.
    - Assume `0` means an error. `0` means the substring was not found.
    - Pass null arguments when you expect a not-found result. Null inputs raise a runtime error.
    - Use `Rat()` when you actually need the first occurrence. Use [`At()`](At.md) for that case.

## Caveats

- An empty `subStr` returns `0`.
- An empty `source` also returns `0` when `subStr` is not empty.
- The result is one-based, so convert carefully when working with zero-based external systems.

## Examples

### Find a file extension

Locate the last period in a file name before extracting the extension.

```ssl
:PROCEDURE ExtractFileExtension;
    :DECLARE sFileName, sExtension, nDotPos;

    sFileName := "report_Q4_2024.pdf";
    nDotPos := Rat(".", sFileName);

    :IF nDotPos > 0;
        sExtension := SubStr(sFileName, nDotPos + 1);
        UsrMes("Extension: " + sExtension);
        /* Displays the extracted extension;
    :ELSE;
        UsrMes("No extension found");
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("ExtractFileExtension");
```

### Split the last path segment

Use the last slash to separate a path into its directory and trailing file name.

```ssl
:PROCEDURE SplitPath;
    :PARAMETERS sPath;
    :DECLARE sDirectory, sFileName, nSlashPos;

    nSlashPos := Rat("/", sPath);

    :IF nSlashPos > 0;
        sDirectory := Left(sPath, nSlashPos - 1);
        sFileName := SubStr(sPath, nSlashPos + 1);
    :ELSE;
        sDirectory := "";
        sFileName := sPath;
    :ENDIF;

    UsrMes("Directory: " + sDirectory);
    /* Displays the directory portion;
    UsrMes("File: " + sFileName);
    /* Displays the trailing file name;
:ENDPROC;

/* Usage;
DoProc("SplitPath", {"/home/user/reports/quarterly.xlsx"});
```

### Parse a `Category.Script.Procedure` name

Use `Rat()` twice to split a fully qualified procedure reference into category, script, and procedure parts.

```ssl
:PROCEDURE ParseQualifiedName;
    :PARAMETERS sQualifiedName;
    :DECLARE sCategory, sScript, sProcedure, sScriptPart, nLastDotPos,
        nPrevDotPos;

    sCategory := "";
    sScript := "";
    sProcedure := "";

    nLastDotPos := Rat(".", sQualifiedName);

    :IF nLastDotPos = 0;
        sScript := sQualifiedName;
    :ELSE;
        sProcedure := SubStr(sQualifiedName, nLastDotPos + 1);
        sScriptPart := Left(sQualifiedName, nLastDotPos - 1);
        nPrevDotPos := Rat(".", sScriptPart);

        :IF nPrevDotPos = 0;
            sScript := sQualifiedName;
            sProcedure := "";
        :ELSE;
            sCategory := Left(sScriptPart, nPrevDotPos - 1);
            sScript := SubStr(sScriptPart, nPrevDotPos + 1);
        :ENDIF;
    :ENDIF;

    UsrMes("Category: " + sCategory);
    /* Displays the category segment when present;
    UsrMes("Script: " + sScript);
    /* Displays the script segment;
    UsrMes("Procedure: " + sProcedure);
    /* Displays the procedure segment when present;
:ENDPROC;

/* Usage;
DoProc("ParseQualifiedName", {"System.Reports.GenerateMonthly"});
```

## Related

- [`At`](At.md)
- [`LimsAt`](LimsAt.md)
- [`StrSrch`](StrSrch.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
