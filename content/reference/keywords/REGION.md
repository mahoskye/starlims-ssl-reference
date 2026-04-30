---
title: "REGION"
summary: "Starts a named region block whose body is stored as text for later retrieval with GetRegion()."
id: ssl.keyword.region
element_type: keyword
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# REGION

Starts a named region block whose body is stored as text for later retrieval with [`GetRegion`](../functions/GetRegion.md)`()`.

`:REGION` opens a named block that continues until [`:ENDREGION`](ENDREGION.md)`;`. SSL captures the text inside the block, stores it under the region name, and makes it available through [`GetRegion`](../functions/GetRegion.md). The captured body is not executed inline where the `:REGION` appears, so this keyword is not a general-purpose code-organization feature like `/* region` comments.

## Behavior

`:REGION` takes a required identifier name and captures everything up to the matching [`:ENDREGION`](ENDREGION.md)`;` as raw text.

The stored region name is matched case-insensitively when you call [`GetRegion`](../functions/GetRegion.md)`()`. If the same name is defined again, the later definition replaces the earlier stored text.

Unlike [`:BEGININLINECODE`](BEGININLINECODE.md), the region body is stored as text rather than validated as executable SSL. Use `/* region` and `/* endregion` comments instead when you only want editor folding or visual grouping.

## When to use

- When you want to store reusable text under a name and retrieve it later with
  [`GetRegion`](../functions/GetRegion.md)`()`.
- When you need lightweight placeholder replacement by calling
  [`GetRegion`](../functions/GetRegion.md)`()` with source and destination arrays.
- When you want a stored text block that is not validated as SSL code.

## Syntax

```ssl
:REGION RegionName;
region body text
:ENDREGION;
```

## Parameters

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `RegionName` | Identifier | Yes | Name used to store and later retrieve the region text. Matching is case-insensitive at runtime. |

## Keyword group

**Group:** Organization
**Role:** opener

## Best practices

!!! success "Do"
    - Use `:REGION` for stored text that you plan to retrieve with [`GetRegion`](../functions/GetRegion.md)`()`.
    - Choose descriptive identifier names so the region's purpose is obvious at the call site.
    - Keep placeholder tokens consistent when you plan to replace them with [`GetRegion`](../functions/GetRegion.md)`(sName, aSource, aDestination)`.

!!! failure "Don't"
    - Use quotes around the region name. `:REGION` takes an identifier, not a string literal.
    - Expect the region body to execute where it is declared. The body is captured as text and retrieved later.
    - Use `:REGION` when you only want code folding. Prefer `/* region` and `/* endregion` comments for that purpose.

## Caveats

- `:REGION` must be closed by a matching [`:ENDREGION`](ENDREGION.md)`;`.
- `:REGION` and [`:ENDREGION`](ENDREGION.md) are case-sensitive keywords and must be uppercase.
- [`GetRegion`](../functions/GetRegion.md)`()` raises an error if the requested region name is not in scope.
- Leading and trailing line breaks immediately inside the region body are trimmed before the text is stored.

## Examples

### Store and retrieve a simple text block

Defines a region inside a procedure, retrieves its text with [`GetRegion`](../functions/GetRegion.md), and displays the result. The region body becomes the displayed message.

```ssl
:PROCEDURE ShowWelcomeBanner;
    :DECLARE sBanner;

:REGION WelcomeBanner;
Welcome to the quality control workspace
:ENDREGION;

    sBanner := GetRegion("WelcomeBanner");
    UsrMes(sBanner);

    :RETURN sBanner;
:ENDPROC;

/* Usage;
DoProc("ShowWelcomeBanner");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
Welcome to the quality control workspace
```

### Replace placeholder tokens in stored text

Stores a reusable template with `{USER}` and `{DATE}` placeholders and substitutes real values when retrieving it. The username and date are system values that vary per user and session; the example shows representative output.

```ssl
:PROCEDURE BuildLoginNotice;
    :DECLARE aSource, aDestination, sNotice;

:REGION LoginNotice;
User {USER} signed in on {DATE}
:ENDREGION;

    aSource := {"{USER}", "{DATE}"};
    aDestination := {MYUSERNAME, DToC(Today())};

    sNotice := GetRegion("LoginNotice", aSource, aDestination);
    UsrMes(sNotice);

    :RETURN sNotice;
:ENDPROC;

/* Usage;
DoProc("BuildLoginNotice");
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
User jsmith signed in on 04/23/2026
```

### Choose between multiple stored templates

Selects one of two region templates at runtime based on a status parameter. With `sStatus` set to `"COMPLETE"`, the complete-message region is retrieved and displayed.

```ssl
:PROCEDURE BuildStatusMessage;
    :PARAMETERS sStatus;
    :DEFAULT sStatus, "PENDING";
    :DECLARE sMessage, sRegionName;

:REGION PendingMessage;
The sample is still pending review
:ENDREGION;

:REGION CompleteMessage;
The sample review is complete
:ENDREGION;

    sRegionName := "PendingMessage";

    :IF Upper(sStatus) == "COMPLETE";
        sRegionName := "CompleteMessage";
    :ENDIF;

    sMessage := GetRegion(sRegionName);
    UsrMes(sMessage);

    :RETURN sMessage;
:ENDPROC;

/* Usage;
DoProc("BuildStatusMessage", {"COMPLETE"});
```

[`UsrMes`](../functions/UsrMes.md) displays:

```text
The sample review is complete
```

## Related

- [`ENDREGION`](ENDREGION.md)
- [`GetRegion`](../functions/GetRegion.md)
- [`BEGININLINECODE`](BEGININLINECODE.md)
