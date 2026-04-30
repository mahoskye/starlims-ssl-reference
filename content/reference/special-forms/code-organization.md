---
title: "Code Organization"
summary: "Comment regions group related procedures or code sections in long files. They are purely organizational - they have no effect on compilation or execution, but development tools use them for code folding and navigation."
id: ssl.special_form.code-organization
element_type: special_form
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# Code Organization

## What it does

Comment regions group related procedures or code sections in long files. They are purely organizational — they have no effect on compilation or execution, but development tools use them for code folding and navigation.

## When to use it

- When a long script file needs logical sections visible in the editor's code-folding panel.
- When organizing a script into named areas such as "Public API", "Validation Helpers", or "Private Helpers".
- When collaborating on a file where consistent section markers help readers
  navigate quickly.

## Syntax

```ssl
/* region Region Name;

/* region content;

/* endregion;
```

`/* region` and `/* endregion` follow standard SSL comment syntax — they end with `;` and are treated as comments by the compiler. Region names use **Title Case** by convention.

## Context rules

- Regions can be nested.
- `/* region` and `/* endregion` are case-sensitive.
- The region name is free-form text on the same line as `/* region`.
- Region markers apply no scoping rules to variables or procedures inside them.

## Notes for daily SSL work

!!! success "Do"
    - Use Title Case for region names (e.g., `Validation Helpers`, `Database Operations`).
    - Nest regions for logical sub-sections within larger areas.
    - Keep region names short and descriptive so the code-folding panel is easy to scan.

!!! failure "Don't"
    - Confuse `/* region` comment markers with the [`:REGION`](../keywords/REGION.md) / [`:ENDREGION`](../keywords/ENDREGION.md) keywords — those are a separate construct for storing named text blocks.
    - Use regions as a substitute for splitting genuinely unrelated logic into separate scripts.

## Errors and edge cases

- An unclosed `/* region` has no compiler effect but may confuse editor folding.
- [`:REGION`](../keywords/REGION.md) / [`:ENDREGION`](../keywords/ENDREGION.md) keywords are **not** the same as comment regions. They are a legacy construct used for storing and retrieving named text blocks via [`GetRegion`](../functions/GetRegion.md) and [`GetRegionEx`](../functions/GetRegionEx.md). See [`REGION`](../keywords/REGION.md) and [`ENDREGION`](../keywords/ENDREGION.md) for details.

## Examples

### Organizing a script with public and private regions

Groups a script's procedures into three named regions: declarations, public API, and private helpers. The `/*@private;` access modifier is placed inside the private region.

```ssl
/* region Declarations;
:DECLARE sGlobalConfig, nMaxRetries;
/* endregion;

/* region Public API;

:PROCEDURE GetSampleStatus;
	:PARAMETERS sSampleId;
	/* ... ;
:ENDPROC;

:PROCEDURE UpdateSampleStatus;
	:PARAMETERS sSampleId, sNewStatus;
	/* ... ;
:ENDPROC;

/* endregion;

/* region Private Helpers;

/*@private;

:PROCEDURE FormatStatusMessage;
	:PARAMETERS sStatus;
	:RETURN "Status: " + sStatus;
:ENDPROC;

/* endregion;
```

## Related elements

- [`REGION`](../keywords/REGION.md)
- [`ENDREGION`](../keywords/ENDREGION.md)
- [`access-modifiers`](access-modifiers.md)
