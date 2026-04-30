---
title: "RegSetup"
summary: "Provides access to Windows registry values under HKEY_LOCAL_MACHINE."
id: ssl.class.regsetup
element_type: class
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# RegSetup

Provides access to Windows registry values under `HKEY_LOCAL_MACHINE`.

Use `RegSetup` when an SSL script needs to read machine-level configuration from the Windows registry. Create the object, open a subkey relative to `HKEY_LOCAL_MACHINE`, read one or more value names, then close the key when you are finished.

`RegOpenKey()` returns [`.T.`](../literals/true.md) when the subkey is found and opened, or [`.F.`](../literals/false.md) when the subkey does not exist. `RegQueryValue()` reads a value from the currently open key and returns [`NIL`](../literals/nil.md) when that value name is not present. `RegCloseKey()` always returns [`.T.`](../literals/true.md).

The surfaced method signatures include `access` and `type` parameters, but the current behavior ignores both parameters.

## When to use

- When you need to read application or machine configuration stored in the Windows registry.
- When a script must check environment settings before continuing.
- When an integration depends on values stored under `HKEY_LOCAL_MACHINE`.

## Constructors

### `RegSetup{}`

Creates a `RegSetup` instance with no open registry key.

## Methods

| Method | Returns | Description |
| --- | --- | --- |
| `RegOpenKey(sKey, nAccess)` | [boolean](../types/boolean.md) | Opens a subkey under `HKEY_LOCAL_MACHINE`. |
| `RegQueryValue(sSubKey, nType)` | [object](../types/object.md) | Reads a value from the currently open key. |
| `RegCloseKey()` | [boolean](../types/boolean.md) | Closes the current key handle. |

### `RegOpenKey`

Opens a registry key under `HKEY_LOCAL_MACHINE`.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `sKey` | [string](../types/string.md) | yes | Registry path relative to `HKEY_LOCAL_MACHINE`, for example `SOFTWARE\MyApp`. |
| `nAccess` | [number](../types/number.md) | yes | Accepted by the method signature, but currently ignored. |

**Returns:** [boolean](../types/boolean.md) — [`.T.`](../literals/true.md) if the key was opened, otherwise [`.F.`](../literals/false.md).

**Raises:**
- **When `sKey` is [`NIL`](../literals/nil.md):** `Argument sKey cannot be null.`

### `RegQueryValue`

Reads a named value from the currently open registry key.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `sSubKey` | [string](../types/string.md) | yes | Name of the value to read from the open key. |
| `nType` | [number](../types/number.md) | yes | Accepted by the method signature, but currently ignored. |

**Returns:** [object](../types/object.md) — The stored registry value, or [`NIL`](../literals/nil.md) if the named value does not exist.

**Raises:**
- **When no registry key is currently open:** raises an argument error (runtime message: `RegSetup:RegQueryValue()`)
- **When `sSubKey` is [`NIL`](../literals/nil.md):** `Argument sSubKey cannot be null.`

### `RegCloseKey`

Closes the current registry key handle.

**Returns:** [boolean](../types/boolean.md) — Always [`.T.`](../literals/true.md).

## Inheritance

**Base class:** [`object`](../types/object.md)

## Best practices

!!! success "Do"
    - Check the return value of `RegOpenKey()` before calling `RegQueryValue()`.
    - Pass registry paths relative to `HKEY_LOCAL_MACHINE`.
    - Treat `RegQueryValue()` results as dynamic values and validate them before use.
    - Call `RegCloseKey()` after finishing registry reads.

!!! failure "Don't"
    - Assume the `nAccess` argument changes the open mode — the current behavior does not use it.
    - Assume the `nType` argument converts the result — the returned value comes from the stored registry value.
    - Call `RegQueryValue()` before a successful `RegOpenKey()` — it raises an error.
    - Leave the key open after reading values — open handles should be released promptly.
    - Assume a missing value raises an error — `RegQueryValue()` returns [`NIL`](../literals/nil.md) when the value name is not present.

## Caveats

- `RegCloseKey()` always returns [`.T.`](../literals/true.md), so its return value does not tell you whether a key was previously open.

## Examples

### Read a value from an existing key

Opens a key under `HKEY_LOCAL_MACHINE\SOFTWARE\MyApplication`, reads the `InstallPath` value, and closes the key. Checks the return value of `RegOpenKey()` before querying and checks for [`NIL`](../literals/nil.md) to distinguish a missing value from an empty one.

```ssl
:PROCEDURE ReadRegistryInstallPath;
    :DECLARE oRegistry, bOpened, vInstallPath;

    oRegistry := RegSetup{};
    bOpened := oRegistry:RegOpenKey("SOFTWARE\MyApplication", 1);

    :IF bOpened;
        vInstallPath := oRegistry:RegQueryValue("InstallPath", 1);
        oRegistry:RegCloseKey();

        :IF vInstallPath == NIL;
            UsrMes("InstallPath is not defined");
        :ELSE;
            UsrMes("Install path: " + LimsString(vInstallPath));
        :ENDIF;
    :ELSE;
        UsrMes("Registry key not found");
    :ENDIF;
:ENDPROC;

/* Usage;
DoProc("ReadRegistryInstallPath");
```

### Read multiple values and always close the key

Uses [`:TRY`](../keywords/TRY.md)/[`:FINALLY`](../keywords/FINALLY.md) to guarantee `RegCloseKey()` runs even if an exception is raised mid-read. Initialising `bOpened` to [`.F.`](../literals/false.md) before the [`:TRY`](../keywords/TRY.md) block lets the [`:FINALLY`](../keywords/FINALLY.md) guard skip the close call when the key was never opened.

```ssl
:PROCEDURE ReadRegistryDetailsSafely;
    :DECLARE oRegistry, bOpened, vVersion, vInstallPath, oErr;

    oRegistry := RegSetup{};
    bOpened := .F.;

    :TRY;
        bOpened := oRegistry:RegOpenKey("SOFTWARE\MyApplication", 1);

        :IF .NOT. bOpened;
            UsrMes("Registry key not found");
        :ELSE;
            vVersion := oRegistry:RegQueryValue("Version", 1);
            vInstallPath := oRegistry:RegQueryValue("InstallPath", 1);

            :IF vVersion == NIL;
                UsrMes("Version is not defined");
            :ELSE;
                UsrMes("Version: " + LimsString(vVersion));
            :ENDIF;

            :IF vInstallPath != NIL;
                UsrMes("Install path: " + LimsString(vInstallPath));
            :ENDIF;
        :ENDIF;

    :CATCH;
        oErr := GetLastSSLError();
        ErrorMes("Registry Error", oErr:Description);

    :FINALLY;
        :IF bOpened;
            oRegistry:RegCloseKey();
        :ENDIF;
    :ENDTRY;
:ENDPROC;

/* Usage;
DoProc("ReadRegistryDetailsSafely");
```

## Related

- [`boolean`](../types/boolean.md)
- [`number`](../types/number.md)
- [`string`](../types/string.md)
- [`object`](../types/object.md)
