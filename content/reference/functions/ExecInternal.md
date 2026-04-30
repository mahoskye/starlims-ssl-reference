---
title: "ExecInternal"
summary: "Calls a method on an object by name and returns that method's result."
id: ssl.function.execinternal
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# ExecInternal

Calls a method on an object by name and returns that method's result.

`ExecInternal` dynamically invokes a method on the target object `o` using the string in `sMethodName`. You can pass up to twenty-one optional arguments. The function returns whatever value the target method returns.

## When to use

- When the method name is only known at runtime.
- When you need one dispatcher to call different methods on the same object.
- When you are working with dynamic object behavior and a direct `o:Method()` call is not practical.

## Syntax

```ssl
ExecInternal(o, sMethodName, [vArg01], [vArg02], [vArg03], [vArg04], [vArg05], [vArg06], [vArg07], [vArg08], [vArg09], [vArg10], [vArg11], [vArg12], [vArg13], [vArg14], [vArg15], [vArg16], [vArg17], [vArg18], [vArg19], [vArg20], [vArg21])
```

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `o` | [object](../types/object.md) | yes | — | Target object whose method will be invoked. |
| `sMethodName` | [string](../types/string.md) | yes | — | Name of the method to call. |
| `vArg01` | any | no | [`NIL`](../literals/nil.md) | First argument passed to the target method. |
| `vArg02` | any | no | [`NIL`](../literals/nil.md) | Second argument passed to the target method. |
| `vArg03` | any | no | [`NIL`](../literals/nil.md) | Third argument passed to the target method. |
| `vArg04` | any | no | [`NIL`](../literals/nil.md) | Fourth argument passed to the target method. |
| `vArg05` | any | no | [`NIL`](../literals/nil.md) | Fifth argument passed to the target method. |
| `vArg06` | any | no | [`NIL`](../literals/nil.md) | Sixth argument passed to the target method. |
| `vArg07` | any | no | [`NIL`](../literals/nil.md) | Seventh argument passed to the target method. |
| `vArg08` | any | no | [`NIL`](../literals/nil.md) | Eighth argument passed to the target method. |
| `vArg09` | any | no | [`NIL`](../literals/nil.md) | Ninth argument passed to the target method. |
| `vArg10` | any | no | [`NIL`](../literals/nil.md) | Tenth argument passed to the target method. |
| `vArg11` | any | no | [`NIL`](../literals/nil.md) | Eleventh argument passed to the target method. |
| `vArg12` | any | no | [`NIL`](../literals/nil.md) | Twelfth argument passed to the target method. |
| `vArg13` | any | no | [`NIL`](../literals/nil.md) | Thirteenth argument passed to the target method. |
| `vArg14` | any | no | [`NIL`](../literals/nil.md) | Fourteenth argument passed to the target method. |
| `vArg15` | any | no | [`NIL`](../literals/nil.md) | Fifteenth argument passed to the target method. |
| `vArg16` | any | no | [`NIL`](../literals/nil.md) | Sixteenth argument passed to the target method. |
| `vArg17` | any | no | [`NIL`](../literals/nil.md) | Seventeenth argument passed to the target method. |
| `vArg18` | any | no | [`NIL`](../literals/nil.md) | Eighteenth argument passed to the target method. |
| `vArg19` | any | no | [`NIL`](../literals/nil.md) | Nineteenth argument passed to the target method. |
| `vArg20` | any | no | [`NIL`](../literals/nil.md) | Twentieth argument passed to the target method. |
| `vArg21` | any | no | [`NIL`](../literals/nil.md) | Twenty-first argument passed to the target method. |

## Returns

**any** — Whatever value the invoked method returns.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| `o` is [`NIL`](../literals/nil.md). | `Argument o cannot be null.` |
| `sMethodName` is [`NIL`](../literals/nil.md). | `Argument sMethodName cannot be null.` |

## Best practices

!!! success "Do"
    - Validate that both `o` and `sMethodName` are present before calling.
    - Omit unused trailing arguments instead of padding the call.
    - Use [`GetInternal`](GetInternal.md) or [`SetInternal`](SetInternal.md) when you only need dynamic property access.

!!! failure "Don't"
    - Pass [`NIL`](../literals/nil.md) for `o` or `sMethodName`. Both raise an immediate runtime error.
    - Use `ExecInternal` when a direct member call is clearer and already known at design time.
    - Assume `ExecInternal` will fix an invalid method name or incompatible argument list for you.

## Caveats

- `ExecInternal` does not define its own method-specific validation beyond the [`NIL`](../literals/nil.md) checks for `o` and `sMethodName`.
- Trailing empty argument slots are removed before the target method is called.
- The result type and any additional runtime errors depend on the target object and method being invoked.

## Examples

### Call a method chosen at runtime

Builds a user-defined object, then invokes a method named at runtime rather than at design time. The method name comes from a variable, so the dispatcher logic does not change when the method name does.

```ssl
:PROCEDURE ShowSerializedObject;
	:DECLARE oRecord, sMethodName, sXml;

	oRecord := CreateUdObject();
	oRecord:SampleID := "S-1001";
	oRecord:Status := "Logged";

	sMethodName := "Serialize";
	sXml := ExecInternal(oRecord, sMethodName);

	UsrMes(sXml);

	:RETURN sXml;
:ENDPROC;

/* Usage;
DoProc("ShowSerializedObject");
```

[`UsrMes`](UsrMes.md) displays:

```
<serialized XML representation of oRecord>
```

### Dispatch between methods with different argument counts

Calls two different methods on the same object in sequence: first `SetProperty` with two arguments to store a value, then `GetProperty` with one argument to read it back. The method name changes between calls while the dispatch pattern stays the same.

```ssl
:PROCEDURE UpdateAndReadProperty;
	:DECLARE oRecord, sMethodName, vResult, sPropertyName;

	oRecord := CreateUdObject();
	sPropertyName := "Priority";

	sMethodName := "SetProperty";
	vResult := ExecInternal(oRecord, sMethodName, sPropertyName, 2);

	sMethodName := "GetProperty";
	vResult := ExecInternal(oRecord, sMethodName, sPropertyName);

	UsrMes("Priority: " + LimsString(vResult));

	:RETURN vResult;
:ENDPROC;

/* Usage;
DoProc("UpdateAndReadProperty");
```

[`UsrMes`](UsrMes.md) displays:

```
Priority: 2
```

### Route multiple dynamic operations through one helper

Defines a single helper that routes `SET`, `GET`, and `CHECK` actions to the corresponding `ExecInternal` calls. The demo procedure then calls the helper three times with different actions to set, verify, and read back a property.

```ssl
:PROCEDURE RunObjectAction;
	:PARAMETERS oRecord, sAction, sPropertyName, vValue;

	:IF sAction == "SET";
		:RETURN ExecInternal(oRecord, "SetProperty", sPropertyName, vValue);
	:ENDIF;

	:IF sAction == "GET";
		:RETURN ExecInternal(oRecord, "GetProperty", sPropertyName);
	:ENDIF;

	:IF sAction == "CHECK";
		:RETURN ExecInternal(oRecord, "IsProperty", sPropertyName);
	:ENDIF;

	:RETURN NIL;
:ENDPROC;
```

Usage:

```ssl
:PROCEDURE DemoRunObjectAction;
	:DECLARE oRecord, bHasStatus, vStatus;

	oRecord := CreateUdObject();

	DoProc("RunObjectAction", {oRecord, "SET", "Status", "Complete"});

	bHasStatus := DoProc("RunObjectAction", {oRecord, "CHECK", "Status"});
	vStatus := DoProc("RunObjectAction", {oRecord, "GET", "Status"});

	:IF bHasStatus;
		UsrMes("Status: " + LimsString(vStatus));
	:ENDIF;

	:RETURN vStatus;
:ENDPROC;

/* Usage;
DoProc("DemoRunObjectAction");
```

[`UsrMes`](UsrMes.md) displays:

```
Status: Complete
```

## Related

- [`DoProc`](DoProc.md)
- [`ExecFunction`](ExecFunction.md)
- [`ExecUdf`](ExecUdf.md)
- [`GetInternal`](GetInternal.md)
- [`GetInternalC`](GetInternalC.md)
- [`SetInternal`](SetInternal.md)
- [`SetInternalC`](SetInternalC.md)
- [`object`](../types/object.md)
- [`string`](../types/string.md)
