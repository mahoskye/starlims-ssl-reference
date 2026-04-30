---
title: "GetInternal"
summary: "Retrieves the current value of a named property from a value that supports property access."
id: ssl.function.getinternal
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# GetInternal

Retrieves the current value of a named property from a value that supports property access.

`GetInternal` takes a target value and a property name, then returns the value resolved by that target's property lookup logic. The function itself does not modify the target. It raises an error when `oTarget` or `sPropName` is [`NIL`](../literals/nil.md). For dynamic objects, trying to read a property that does not exist raises a runtime error.

## When to use

- When you need to read a property by name at runtime.
- When the property name is stored in a variable rather than written as `oValue:PropertyName` in code.
- When you want to pair a dynamic read with [`HasProperty`](HasProperty.md) before accessing a property on a dynamic object.
- When you are iterating over a list of property names and reading each one in turn.

## Syntax

```ssl
GetInternal(oTarget, sPropName)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `oTarget` | [object](../types/object.md) | yes | — | Value whose property will be read |
| `sPropName` | [string](../types/string.md) | yes | — | Name of the property to retrieve |

## Returns

**any** — Current value returned for the named property.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `oTarget` is [`NIL`](../literals/nil.md). | `Argument oTarget cannot be null.` |
| `sPropName` is [`NIL`](../literals/nil.md). | `Argument sPropName cannot be null.` |
| A dynamic object does not contain the named property. | `Property not found: <propertyName>.` |

## Best practices

!!! success "Do"
    - Check that the target value and property name are available before calling.
    - Use [`HasProperty`](HasProperty.md) first when the property may be absent on a dynamic object.
    - Use `GetInternal` when the property name is dynamic and cannot be written directly in source.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `oTarget` or `sPropName`. The function raises an error instead of returning an empty value.
    - Assume every dynamic object has the property you want. Missing dynamic properties raise a runtime error.
    - Use `GetInternal` when you need to write a property. Use [`SetInternal`](SetInternal.md) for assignment.

## Caveats

- `GetInternal` only performs the lookup. It does not create properties or change the target value.

## Examples

### Read a property by name

Read a single property from a dynamic object when the property name is known at runtime.

```ssl
:PROCEDURE GetConfigTimeout;
	:DECLARE oConfig, sPropName, nTimeout;

	oConfig := CreateUdObject();
	oConfig:QueryTimeout := 60;
	sPropName := "QueryTimeout";

	nTimeout := GetInternal(oConfig, sPropName);

	UsrMes("Query timeout: " + LimsString(nTimeout));

	:RETURN nTimeout;
:ENDPROC;

/* Usage;
DoProc("GetConfigTimeout");
```

[`UsrMes`](UsrMes.md) displays:

```text
Query timeout: 60
```

### Guard dynamic reads with [`HasProperty`](HasProperty.md)

Check whether each property exists before reading it from a dynamic object.

```ssl
:PROCEDURE SummarizeSample;
	:DECLARE oSample, aFields, sFieldName, sSummary, vValue, nIndex;

	oSample := CreateUdObject();
	oSample:SampleID := "LAB-2024-0042";
	oSample:Status := "Active";
	oSample:Analyst := "JSmith";

	aFields := {"SampleID", "Status", "Analyst", "Priority"};
	sSummary := "Sample values: ";

	:FOR nIndex := 1 :TO ALen(aFields);
		sFieldName := aFields[nIndex];

		:IF HasProperty(oSample, sFieldName);
			vValue := GetInternal(oSample, sFieldName);
			sSummary := sSummary + sFieldName + "=" + LimsString(vValue);
		:ELSE;
			sSummary := sSummary + sFieldName + "=<missing>";
		:ENDIF;

		:IF nIndex < ALen(aFields);
			sSummary := sSummary + ", ";
		:ENDIF;
	:NEXT;

	UsrMes(sSummary);

	:RETURN sSummary;
:ENDPROC;

/* Usage;
DoProc("SummarizeSample");
```

[`UsrMes`](UsrMes.md) displays:

```text
Sample values: SampleID=LAB-2024-0042, Status=Active, Analyst=JSmith, Priority=<missing>
```

### Catch a failed dynamic lookup

Handle the runtime error raised when a dynamic object does not contain the requested property.

```ssl
:PROCEDURE ReadOptionalPriority;
	:DECLARE oSample, sPropName, vValue, oErr, sMessage;

	oSample := CreateUdObject();
	oSample:SampleID := "LAB-2024-0847";
	oSample:Status := "Pending";
	sPropName := "Priority";
	sMessage := "";

	:TRY;
		vValue := GetInternal(oSample, sPropName);
		sMessage := "Priority: " + LimsString(vValue);
	:CATCH;
		oErr := GetLastSSLError();
		sMessage := "Lookup failed: " + oErr:Description;
	:ENDTRY;

	UsrMes(sMessage);

	:RETURN sMessage;
:ENDPROC;

/* Usage;
DoProc("ReadOptionalPriority");
```

[`UsrMes`](UsrMes.md) displays when the property is absent:

```text
Lookup failed: Property not found: Priority.
```

## Related

- [`ExecInternal`](ExecInternal.md)
- [`GetInternalC`](GetInternalC.md)
- [`HasProperty`](HasProperty.md)
- [`SetInternal`](SetInternal.md)
- [`SetInternalC`](SetInternalC.md)
- [`string`](../types/string.md)
- [`array`](../types/array.md)
