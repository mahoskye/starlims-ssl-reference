---
title: "SetGroupSeparator"
summary: "Changes the group (thousands) separator character used when numbers are formatted as strings across the application."
id: ssl.function.setgroupseparator
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# SetGroupSeparator

Changes the group (thousands) separator character used when numbers are formatted as strings across the application.

`SetGroupSeparator` changes the global group separator to `sGroupSep` and returns the previous setting. `sGroupSep` must be exactly one character long; passing [`NIL`](../literals/nil.md), an empty string, or a multi-character string raises an error.

## When to use

- When you need to support localized numeric input that uses a different group separator than the default (e.g., comma or period).
- When your application parses numeric values from multiple sources and must standardize group separator interpretation to avoid misparsing.
- When switching application localization and numeric formatting conventions at runtime.
- When enforcing consistent numeric entry formatting across all forms and calculations.

## Syntax

```ssl
SetGroupSeparator(sGroupSep)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sGroupSep` | [string](../types/string.md) | yes | — | The character to use as the group separator in numeric values (typically a comma or space). |

## Returns

**[string](../types/string.md)** — The previous group separator value before the change was applied.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `sGroupSep` is [`NIL`](../literals/nil.md). | `Argument: sGroupSep cannot be null.` |
| `sGroupSep` is empty or not exactly one character. | `Wrong value for argument: sGroupSep` |

## Best practices

!!! success "Do"
    - Always provide a single, non-empty character as the separator.
    - Check the need for separator change at application startup or user profile update.
    - Use [`GetGroupSeparator`](GetGroupSeparator.md) to retrieve the current separator before changing it, especially in shared environments.

!!! failure "Don't"
    - Pass multi-character strings or empty values as `sGroupSep`.
    - Frequently switch the separator mid-session unless all components are aware of the change; the setting is global and unpredictable changes can cause inconsistent parsing.
    - Assume the initial separator value without querying; other modules may have changed it.

## Caveats

- Changing the separator affects all subsequent numeric operations globally; parts of the application that expect a different separator may behave incorrectly.
- There is no validation that `sGroupSep` does not conflict with the current decimal separator.

## Examples

### Switch the separator for a bulk import and restore afterward

Switch the separator for a bulk import, then restore the original setting when done.

```ssl
:PROCEDURE ImportNumericData;
	:DECLARE sOriginalSep, sImportSep, sFormattedValue, sLogMessage;
	:DECLARE nSampleValue, nIndex, nTotalProcessed;
	:DECLARE aImportData;

	sOriginalSep := GetGroupSeparator();
	sImportSep := ",";
	nTotalProcessed := 0;

	aImportData := {"1,234.56", "45,678.90", "987,654.32"};

	SetGroupSeparator(sImportSep);
	sLogMessage := "Switched group separator from " + sOriginalSep + " to " + sImportSep + " for import";
	UsrMes(sLogMessage);
	/* Displays import separator change;

	:FOR nIndex := 1 :TO ALen(aImportData);
		sFormattedValue := aImportData[nIndex];
		nSampleValue := Val(sFormattedValue);
		nTotalProcessed := nTotalProcessed + 1;
		sLogMessage := "Row " + LimsString(nIndex) + ": imported " + sFormattedValue + " = "
			+ LimsString(nSampleValue);
		UsrMes(sLogMessage);
		/* Displays imported row details;
	:NEXT;

	SetGroupSeparator(sOriginalSep);
	sLogMessage := "Restored original group separator: " + sOriginalSep;
	UsrMes(sLogMessage);
	/* Displays restored separator;

	:RETURN nTotalProcessed;
:ENDPROC;

/* Usage;
DoProc("ImportNumericData");
```

### Update both separators for a locale and roll back on error

Change group and decimal separator together during a localization update, with rollback if either change fails.

```ssl
:PROCEDURE UpdateUserLocalization;
	:DECLARE sGroupSep, sDecimalSep, sCurrentGroup, sCurrentDecimal;
	:DECLARE sUserID, sRegion, sFormatMessage, oUserProfile;

	sUserID := "USR-2024-001";
	sRegion := "German";

	sCurrentGroup := GetGroupSeparator();
	sCurrentDecimal := GetDecimalSeparator();

	sGroupSep := ".";
	sDecimalSep := ",";

	:TRY;
		oUserProfile := CreateUdObject();
		oUserProfile:UserID := sUserID;
		oUserProfile:Region := sRegion;
		oUserProfile:PreferredGroupSep := sGroupSep;
		oUserProfile:PreferredDecimalSep := sDecimalSep;

		SetGroupSeparator(sGroupSep);
		SetDecimalSeparator(sDecimalSep);

		:IF GetGroupSeparator() == sGroupSep .AND. GetDecimalSeparator() == sDecimalSep;
			sFormatMessage := "Localization updated for user " + sUserID + " to " + sRegion
				+ " region";
			InfoMes(sFormatMessage);
			/* Displays localization update status;
		:ELSE;
			sFormatMessage := "Failed to update localization for user " + sUserID;
			ErrorMes(sFormatMessage);
			/* Displays localization failure;
		:ENDIF;

		sFormatMessage := "Active separators - Group: " + GetGroupSeparator() + " Decimal: "
			+ GetDecimalSeparator();
		InfoMes(sFormatMessage);
		/* Displays active separator values;
	:CATCH;
		ErrorMes("Localization update failed: " + GetLastSSLError():Description);
		/* Displays localization failure reason;
		SetGroupSeparator(sCurrentGroup);
		SetDecimalSeparator(sCurrentDecimal);
	:FINALLY;
		oUserProfile := NIL;
	:ENDTRY;

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("UpdateUserLocalization");
```

## Related

- [`GetGroupSeparator`](GetGroupSeparator.md)
- [`string`](../types/string.md)
