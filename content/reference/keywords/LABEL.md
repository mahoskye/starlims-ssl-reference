---
title: "LABEL"
summary: "Marks a named location in a procedure or script for control flow redirection."
id: ssl.keyword.label
element_type: keyword
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LABEL

Marks a named location in a procedure or script for control flow redirection.

`:LABEL` marks a jump target that [`Branch`](../functions/Branch.md)`()` can transfer control to within the current procedure or script. Reaching the label itself does not change flow; it simply marks the next statement as a possible landing point.

The stored label text includes the word `LABEL`. For example, `:LABEL CLEANUP;` is normally targeted with `Branch("LABEL CLEANUP")`. SSL also accepts mashed labels such as `:LABELCLEANUP;`, which must be targeted with the exact same text. Labels are a legacy control-flow feature, so prefer structured constructs when [`:IF`](IF.md), [`:FOR`](FOR.md), [`:WHILE`](WHILE.md), or [`:RETURN`](RETURN.md) can express the logic clearly.

## Behavior

`:LABEL` is a marker, not a block. Execution continues with the statement after the label unless control was transferred there by [`Branch`](../functions/Branch.md)`()`.

Label targets are resolved within the current procedure or script. Forward references are supported, so [`Branch`](../functions/Branch.md)`()` can jump to a label declared later in the same scope.

## When to use

- When you need a [`Branch`](../functions/Branch.md)`()` target in the current procedure or script.
- When several paths should jump to one shared cleanup or recovery section.
- When maintaining legacy SSL that already uses labels for explicit flow control.

## Syntax

```ssl
:LABEL labelText;
:LABEL labelPart moreParts;
:LABELlabelText;
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `labelText` | Identifier text | Yes | — | The label text stored by SSL. The usual spaced form is `:LABEL name;`, and SSL also accepts multiple identifier parts such as `:LABEL cleanup fast;`. Those forms are targeted with the exact stored text, such as `Branch("LABEL cleanup fast")`. SSL also accepts mashed forms such as `:LABELname;`, which must be targeted with that exact text. |

## Keyword group

**Group:** Organization
**Role:** statement

## Best practices

!!! success "Do"
    - Choose descriptive labels such as `CLEANUP` or `RECOVER` that make the jump target obvious.
    - Pass the exact stored target text to [`Branch`](../functions/Branch.md)`()`, such as `Branch("LABEL CLEANUP")` for `:LABEL CLEANUP;`.
    - Reserve labels for shared recovery or cleanup paths when structured flow would be less clear.

!!! failure "Don't"
    - Pass only the trailing name, such as `"CLEANUP"`, for a normal `:LABEL CLEANUP;` declaration. The stored text includes `LABEL`.
    - Replace ordinary [`:IF`](IF.md), loop, or [`:RETURN`](RETURN.md) flow with labels when a structured construct is sufficient.
    - Use vague names such as `L1` or `NEXT` that make jump targets harder to follow.

## Caveats

- `:LABEL name;` and `:LABELname;` are different stored texts and require different [`Branch`](../functions/Branch.md)`()` targets.
- Keyword names are case-sensitive and must be uppercase: use `:LABEL`, not `:label`.

## Examples

### Jump to a shared recovery section

Uses [`Branch`](../functions/Branch.md)`()` to redirect control to a label later in the same procedure. With `sSampleID` set to `"A1"`, whose length is less than 5, the branch fires and the recovery message displays.

```ssl
:PROCEDURE ProcessSample;
	:DECLARE sSampleID;

	sSampleID := "A1";

	:IF Len(sSampleID) < 5;
		Branch("LABEL RECOVER");
	:ENDIF;

	UsrMes("Sample ID accepted: " + sSampleID);
	:RETURN .T.;

	:LABEL RECOVER;
	UsrMes("Sample ID is too short: " + sSampleID);

	:RETURN .F.;
:ENDPROC;
```

Run with `DoProc("ProcessSample")`.

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Sample ID is too short: A1
```

### Use a mashed label target

Mashed labels omit the space after `:LABEL`, so [`Branch`](../functions/Branch.md)`()` must use that exact stored text. With `sMode` set to `"SKIP"`, the branch fires and the skip message displays.

```ssl
:PROCEDURE RouteMode;
	:DECLARE sMode;

	sMode := "SKIP";

	:IF sMode == "SKIP";
		Branch("LABELSKIP");
	:ENDIF;

	UsrMes("Processing the normal path");
	:RETURN "NORMAL";

	:LABELSKIP;
	UsrMes("Processing was skipped");

	:RETURN "SKIPPED";
:ENDPROC;
```

Run with `DoProc("RouteMode")`.

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Processing was skipped
```

## Related

- [`Branch`](../functions/Branch.md)
