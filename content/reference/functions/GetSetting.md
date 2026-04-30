---
title: "GetSetting"
summary: "Retrieves a single named setting."
id: ssl.function.getsetting
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetSetting

Retrieves a single named setting.

`GetSetting` accepts a setting name and returns the stored value for that name. The value is surfaced as the matching SSL value type. In practice, settings are returned as string, numeric, date, or Boolean values. If the setting name is not found, the function returns an empty string.

## When to use

- When you need one setting value at runtime.
- When a workflow depends on configurable values such as paths, limits, or flags.
- When you want to avoid hard-coding a value that administrators may change.

## Syntax

```ssl
GetSetting(sName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sName` | [string](../types/string.md) | yes | — | Name of the setting to retrieve. |

## Returns

**any** — The stored value for `sName`, returned as the native SSL type (string, number, date, or boolean). Returns `""` when the name is not found.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sName` is [`NIL`](../literals/nil.md). | `Argument name cannot be null.` |

## Best practices

!!! success "Do"
    - Pass a real setting name string, not [`NIL`](../literals/nil.md).
    - Check the returned value before using it in type-sensitive logic.
    - Use [`LimsTypeEx`](LimsTypeEx.md) when the setting may hold different value types.
    - Use [`GetSettings`](GetSettings.md) when you need several settings together.

!!! failure "Don't"
    - Assume a missing setting returns [`NIL`](../literals/nil.md). `GetSetting` returns an empty string when the name is not found.
    - Treat every returned value as text. Numeric, date, and Boolean settings keep their value type.
    - Use [`Empty()`](Empty.md) by itself to decide whether a setting is missing when `0` or [`.F.`](../literals/false.md) are valid values.

## Caveats

- Because a missing setting and a configured empty-string setting both surface as `""`, `GetSetting` alone cannot distinguish those cases.

## Examples

### Read a string setting

Reads a text setting and branches on whether it is empty, displaying a message in each case.

```ssl
:PROCEDURE ShowOutputPath;
	:DECLARE sSettingName, sOutputPath;

	sSettingName := "ReportOutputPath";
	sOutputPath := GetSetting(sSettingName);

	:IF sOutputPath == "";
		UsrMes("ReportOutputPath is not configured");
		:RETURN;
	:ENDIF;

	UsrMes("Reports will be written to " + sOutputPath);
	/* Displays configured output path;
:ENDPROC;

/* Usage;
DoProc("ShowOutputPath");
```

### Read a Boolean feature flag safely

Uses [`LimsTypeEx`](LimsTypeEx.md) to check both the returned type and value before branching, guarding against an unconfigured setting or a non-boolean value stored under the same name.

```ssl
:PROCEDURE CheckFeatureFlag;
	:DECLARE vSetting, sSettingType, sSettingName;

	sSettingName := "EnableAdvancedReporting";
	vSetting := GetSetting(sSettingName);
	sSettingType := LimsTypeEx(vSetting);

	:IF sSettingType == "STRING" .AND. vSetting == "";
		UsrMes(sSettingName + " is not configured");
		:RETURN;
	:ENDIF;

	:IF sSettingType != "LOGIC";
		ErrorMes(sSettingName + " must contain a Boolean value");
		:RETURN;
	:ENDIF;

	:IF vSetting == .T.;
		UsrMes("Advanced reporting is enabled");
	:ELSE;
		UsrMes("Advanced reporting is disabled");
	:ENDIF;
:ENDPROC;

/* Usage;
DoProc("CheckFeatureFlag");
```

### Normalize a numeric setting with fallback handling

Uses [`:TRY`](../keywords/TRY.md)/[`:CATCH`](../keywords/CATCH.md) and [`:BEGINCASE`](../keywords/BEGINCASE.md) to handle three storage possibilities: already numeric, missing, or stored as a numeric string. It falls back to a hard-coded default of `30000` when the setting is absent.

```ssl
:PROCEDURE GetTimeoutValue;
	:DECLARE vSetting, sSettingType, sSettingName;
	:DECLARE nTimeout, oErr;

	sSettingName := "DatabaseTimeout";
	nTimeout := 30000;

	:TRY;
		vSetting := GetSetting(sSettingName);
		sSettingType := LimsTypeEx(vSetting);

		:BEGINCASE;
		:CASE sSettingType == "NUMERIC";
			nTimeout := vSetting;
			:EXITCASE;
		:CASE sSettingType == "STRING" .AND. vSetting == "";
			/* Use the default timeout when the setting is missing;
			:EXITCASE;
		:CASE sSettingType == "STRING" .AND. IsNumeric(vSetting);
			nTimeout := Val(vSetting);
			:EXITCASE;
		:OTHERWISE;
			ErrorMes(sSettingName + " must contain a numeric value");
			:EXITCASE;
		:ENDCASE;
	:CATCH;
		oErr := GetLastSSLError();
		ErrorMes("Failed to read " + sSettingName + ": " + oErr:Description);
		/* Displays read failure details;
	:ENDTRY;

	:RETURN nTimeout;
:ENDPROC;

/* Usage;
DoProc("GetTimeoutValue");
```

## Related

- [`GetSettings`](GetSettings.md)
- [`LimsTypeEx`](LimsTypeEx.md)
- [`string`](../types/string.md)
