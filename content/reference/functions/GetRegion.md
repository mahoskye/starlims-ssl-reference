---
title: "GetRegion"
summary: "Retrieves a named region string from the current region scope and can optionally apply sequential text replacements."
id: ssl.function.getregion
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetRegion

Retrieves a named region string from the current region scope and can optionally apply sequential text replacements.

`GetRegion` looks up a region by name and returns its string value. Region names are matched case-insensitively. If both `aSourceValues` and `aDestinationValues` are supplied, the function replaces each source value with the corresponding destination value in order and returns the updated string. If either optional array is omitted, the function returns the region text unchanged.

Use [`GetRegionEx`](GetRegionEx.md) when you need to read from a specific region dictionary rather than the current scope.

## When to use

- When you need to retrieve text stored under a region name.
- When you want to substitute placeholders in a retrieved region string.
- When the same region text needs lightweight token replacement before display or reuse.

## Syntax

```ssl
GetRegion(sRegionName, [aSourceValues], [aDestinationValues])
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sRegionName` | [string](../types/string.md) | yes | — | Region name to look up. Matching is case-insensitive. |
| `aSourceValues` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Source strings to replace in the retrieved region text. Replacement is only attempted when both `aSourceValues` and `aDestinationValues` are supplied. |
| `aDestinationValues` | [array](../types/array.md) | no | [`NIL`](../literals/nil.md) | Replacement strings corresponding to `aSourceValues`. Must have the same number of elements as `aSourceValues`. |

## Returns

**[string](../types/string.md)** — The region text. When both `aSourceValues` and `aDestinationValues` are supplied, token replacements are applied in order before returning. Returns an empty string when region storage has not been initialized.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sRegionName` is [`NIL`](../literals/nil.md). | `Argument cannot be null.` |
| `sRegionName` is not a string. | `Argument must be of type string.` |
| `aSourceValues` or `aDestinationValues` is not an array. | `Invalid arguments for GetRegion! Should be: string, array, array.` |
| `aSourceValues` and `aDestinationValues` have different lengths. | `Invalid arguments for GetRegion! Source array's length is not equal with destination array's length.` |
| The region name is not found in the current scope. | `GetRegion: <sRegionName> not in scope.` The value substituted for `<sRegionName>` is the lowercased region name. |

## Best practices

!!! success "Do"
    - Wrap `GetRegion` in `:TRY / :CATCH` when the region may not be
      available in the current scope.
    - Pass `aSourceValues` and `aDestinationValues` as parallel arrays of equal length when doing token replacement.
    - Use placeholder-style region text such as `{USER}` or `{DATE}` when the same template needs different values at runtime.

!!! failure "Don't"
    - Assume a missing region returns a fallback value. Missing region
      names raise an error once region storage exists.
    - Pass only one replacement array and expect partial substitution. If either `aSourceValues` or `aDestinationValues` is omitted, no replacements are performed.
    - Target a custom region dictionary with `GetRegion`; use [`GetRegionEx`](GetRegionEx.md) instead.

## Caveats

- Replacements are applied in order, so overlapping source values can affect the final result.

## Examples

### Look up a region with error handling

Wraps the lookup in [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) to handle the case where the region is not in scope, displaying the content if found or the error description if the region does not exist.

```ssl
:PROCEDURE ShowBanner;
    :DECLARE sBanner;

    :TRY;
        sBanner := GetRegion("WelcomeBanner");
        /* Displays the stored region text;
        UsrMes(sBanner);
    :CATCH;
        /* Displays the missing-region error text;
        ErrorMes(GetLastSSLError():Description);
        :RETURN "";
    :ENDTRY;

    :RETURN sBanner;
:ENDPROC;

/* Usage;
DoProc("ShowBanner");
```

### Replace placeholders in region text

Reads a template region that contains `{USER}` and `{DATE}` placeholders and replaces both with runtime values in a single call, showing how parallel source and destination arrays drive the substitution.

```ssl
:PROCEDURE BuildWelcomeMessage;
    :DECLARE aSrc, aDst, sMessage;

    aSrc := {"{USER}", "{DATE}"};
    aDst := {MYUSERNAME, DToC(Today())};

    sMessage := GetRegion("WelcomeTemplate", aSrc, aDst);

    :RETURN sMessage;
:ENDPROC;

/* Usage;
DoProc("BuildWelcomeMessage");
```

## Related

- [`GetRegionEx`](GetRegionEx.md)
- [`GetInlineCode`](GetInlineCode.md)
- [`DeleteInlineCode`](DeleteInlineCode.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
