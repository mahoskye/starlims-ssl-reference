---
title: "GetSettings"
summary: "Retrieves multiple named settings in one call."
id: ssl.function.getsettings
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetSettings

Retrieves multiple named settings in one call.

`GetSettings` accepts an array of setting names and returns an array of values in the same order. Each result entry comes from the same lookup behavior as [`GetSetting`](GetSetting.md): if a setting is not found, that entry is an empty string (`""`).

## When to use

- When you need several settings at runtime and want one lookup call.
- When the caller needs the results to stay aligned with an input list of names.
- When you need the same missing-setting behavior as [`GetSetting`](GetSetting.md), but for more than one name.

## Syntax

```ssl
GetSettings(aNames)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `aNames` | [array](../types/array.md) | yes | — | Array of setting names to retrieve. |

## Returns

**[array](../types/array.md)** — One entry per requested setting name, in the same order as `aNames`. Each entry is the stored SSL type for that setting (string, number, date, or boolean), or `""` when the name is not found.

## Exceptions

| Trigger                                                    | Exception message                                                                                                                     |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `aNames` is [`NIL`](../literals/nil.md) or an empty array. | `Argument name cannot be null or empty.` Note: the runtime message incorrectly names the function as [`GetSetting()`](GetSetting.md). |

## Best practices

!!! success "Do"
    - Validate that `aNames` contains at least one name before calling `GetSettings`.
    - Keep the input names in the order you want to consume the results.
    - Check individual returned values before using them in type-sensitive logic.
    - Use [`LimsTypeEx`](LimsTypeEx.md) when a returned setting may not always have the same type.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) or `{}`. `GetSettings` raises an error instead of returning an empty result.
    - Assume a missing setting returns [`NIL`](../literals/nil.md). Missing settings come back as `""`.
    - Use [`Empty()`](Empty.md) by itself to decide whether a value is missing when `0` or [`.F.`](../literals/false.md) are valid configured values.

## Caveats

- Because the result preserves input position, the caller must keep track of which name belongs to which index.
- `GetSettings` alone cannot distinguish between a missing setting and a configured setting whose value is an empty string.

## Examples

### Read several settings for display

Retrieves a short list of settings in one call and iterates over the results, printing each name and its stored value side by side.

```ssl
:PROCEDURE ShowSettings;
	:DECLARE aNames, aValues, sLine, nIndex;

	aNames := {"SystemVersion", "StationName", "InstallationKey"};
	aValues := GetSettings(aNames);

	:FOR nIndex := 1 :TO ALen(aNames);
		sLine := aNames[nIndex] + " = " + LimsString(aValues[nIndex]);
		UsrMes(sLine);  /* Displays each name/value pair;
	:NEXT;
:ENDPROC;

/* Usage;
DoProc("ShowSettings");
```

### Detect missing settings without losing index alignment

Scans the result array while preserving input order, collects names whose returned value is an empty string, and then reports all unconfigured settings in a single message.

```ssl
:PROCEDURE CheckRequiredSettings;
	:DECLARE aNames, aValues, aMissing, nIndex;

	aNames := {"DatabaseConnection", "LogLevel", "Timeout"};
	aValues := GetSettings(aNames);
	aMissing := {};

	:FOR nIndex := 1 :TO ALen(aNames);
		:IF LimsTypeEx(aValues[nIndex]) == "STRING" .AND. aValues[nIndex] == "";
			AAdd(aMissing, aNames[nIndex]);
		:ENDIF;
	:NEXT;

	:IF ALen(aMissing) > 0;
		UsrMes("Missing settings: " + BuildString(aMissing,,, ", "));
		/* Displays the missing setting names;
		:RETURN .F.;
	:ENDIF;

	UsrMes("All required settings are configured");
	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("CheckRequiredSettings");
```

### Validate a mixed-type settings bundle

Retrieves four settings at once and type-checks each one individually, returning [`.F.`](../literals/false.md) on the first mismatch and displaying a summary of all four values when every check passes.

```ssl
:PROCEDURE LoadRuntimeOptions;
	:DECLARE aNames, aValues;
	:DECLARE sMode, sLogLevel;
	:DECLARE nTimeout;
	:DECLARE bAuditEnabled;

	aNames := {"RunMode", "LogLevel", "Timeout", "AuditEnabled"};
	aValues := GetSettings(aNames);

	:IF !(LimsTypeEx(aValues[1]) == "STRING") .OR. aValues[1] == "";
		ErrorMes("RunMode must be configured as a string value");
		:RETURN .F.;
	:ENDIF;

	:IF !(LimsTypeEx(aValues[2]) == "STRING") .OR. aValues[2] == "";
		ErrorMes("LogLevel must be configured as a string value");
		:RETURN .F.;
	:ENDIF;

	:IF !(LimsTypeEx(aValues[3]) == "NUMERIC");
		ErrorMes("Timeout must be configured as a numeric value");
		:RETURN .F.;
	:ENDIF;

	:IF !(LimsTypeEx(aValues[4]) == "LOGIC");
		ErrorMes("AuditEnabled must be configured as a Boolean value");
		:RETURN .F.;
	:ENDIF;

	sMode := aValues[1];
	sLogLevel := aValues[2];
	nTimeout := aValues[3];
	bAuditEnabled := aValues[4];

	UsrMes(
		"Mode=" + sMode + ", LogLevel=" + sLogLevel + ", Timeout="
		+ LimsString(nTimeout)
		+ ", AuditEnabled=" + LimsString(bAuditEnabled)
	);
	/* Displays the validated runtime option values;

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("LoadRuntimeOptions");
```

## Related

- [`GetSetting`](GetSetting.md)
- [`LimsTypeEx`](LimsTypeEx.md)
- [`array`](../types/array.md)
- [`string`](../types/string.md)
