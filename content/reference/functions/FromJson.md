---
title: "FromJson"
summary: "Parses a JSON string into the closest SSL-native value or returns the input unchanged if it is not a string. JSON arrays become arrays, objects become SSLExpando instances, numbers become numbers, booleans become booleans, and strings become strings or dates when the value starts with SSLDate|. Null input, empty strings, and JSON null values return NIL. Invalid JSON tokens raise an error."
id: ssl.function.fromjson
element_type: function
doc_status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# FromJson

Parses a JSON string into the closest SSL-native value or returns the input unchanged if it is not a string. JSON arrays become arrays, objects become [`SSLExpando`](../classes/SSLExpando.md) instances, numbers become numbers, booleans become booleans, and strings become strings or dates when the value starts with `SSLDate|`. Null input, empty strings, and JSON `null` values return [`NIL`](../literals/nil.md). Invalid JSON tokens raise an error.

## When to use

- When ingesting or handling JSON payloads and you need native SSL data types.
- When processing API responses, reading configuration, or loading structured data from other systems in JSON format.
- When normalizing input data with unknown but possibly JSON-encoded content.
- When you want fail-fast behavior if an invalid JSON string is provided.

## Syntax

```ssl
FromJson(vValue)
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `vValue` | any | yes | — | A JSON string to parse into native SSL values, or a non-string value returned as-is. |

## Returns

**any** — The return type depends on the content of `vValue`:

- **[array](../types/array.md)** — when `vValue` is a JSON array.
- **[object](../types/object.md)** ([`SSLExpando`](../classes/SSLExpando.md)) — when `vValue` is a JSON object.
- **[number](../types/number.md)** — when `vValue` is a JSON number.
- **[boolean](../types/boolean.md)** — when `vValue` is a JSON boolean.
- **[date](../types/date.md)** — when `vValue` is a JSON string starting with `SSLDate|`.
- **[string](../types/string.md)** — when `vValue` is any other JSON string.
- **NIL** — when `vValue` is [`NIL`](../literals/nil.md), an empty string, or a JSON null.
- **any** — when `vValue` is not a string, it is returned unchanged.

## Exceptions

| Trigger | Exception message |
| --- | --- |
| An unknown or invalid token is encountered while parsing the JSON string. | `Invalid json token: {tokenType}` |

## Best practices

!!! success "Do"
    - Validate that input data is a valid JSON string before calling this function.
    - Pair `FromJson` with [`ToJson`](ToJson.md) when round-tripping data between SSL and JSON.

!!! failure "Don't"
    - Assume all incoming values are parseable without checking.
    - Use on data serialized with custom delimiters or non-JSON formats.

## Caveats

- Input JSON objects become [`SSLExpando`](../classes/SSLExpando.md) instances and do not implement all methods of a standard SSL object.
- Extra whitespace and line breaks are tolerated by the parser, but stray text before or after valid JSON raises an error.

## Examples

### Parse a JSON array and sum the values

Converts a JSON number array to an SSL array and accumulates the total.

```ssl
:PROCEDURE ParseJsonNumberArray;
	:DECLARE sJson, aTemperatures, nIndex, nSum, nValue;

	sJson := "[72, 85, 91, 78, 88]";
	aTemperatures := FromJson(sJson);

	nSum := 0;
	:FOR nIndex := 1 :TO ALen(aTemperatures);
		nValue := aTemperatures[nIndex];
		nSum := nSum + nValue;
	:NEXT;

	UsrMes("Total of temperature readings: " + LimsString(nSum));
:ENDPROC;

/* Usage;
DoProc("ParseJsonNumberArray");
```

[`UsrMes`](UsrMes.md) displays:

```text
Total of temperature readings: 414
```

### Access properties of a parsed JSON object

Parses a nested JSON configuration object and reads properties from the resulting [`SSLExpando`](../classes/SSLExpando.md) instance.

```ssl
:PROCEDURE ProcessDatabaseConfig;
	:DECLARE sJson, oConfig, oDatabase, sHost, nPort, sResult;

	sJson := '{"database":{"host":"dbserver.example.com","port":1433},"timeout":30}';
	oConfig := FromJson(sJson);

	oDatabase := oConfig:database;
	sHost := oDatabase:host;
	nPort := oDatabase:port;

	sResult := "Host: " + sHost + ", Port: " + LimsString(nPort);
	UsrMes(sResult);  /* Displays database host and port;

	:IF oConfig:IsProperty("timeout");
		sResult := "Timeout is set to " + LimsString(oConfig:timeout);
		UsrMes(sResult);  /* Displays timeout value;
	:ENDIF;

	:RETURN oConfig;
:ENDPROC;

/* Usage;
DoProc("ProcessDatabaseConfig");
```

## Related

- [`ToJson`](ToJson.md)
- [`SSLExpando`](../classes/SSLExpando.md)
- [`array`](../types/array.md)
- [`number`](../types/number.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
- [`date`](../types/date.md)
