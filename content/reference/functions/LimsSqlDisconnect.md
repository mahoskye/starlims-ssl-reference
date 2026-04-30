---
title: "LimsSqlDisconnect"
summary: "Closes an active database connection by name and removes it from the internal registry."
id: ssl.function.limssqldisconnect
element_type: function
status: published
starlims:
  applies_to: [11]
  verified_against: [11]
---

# LimsSqlDisconnect

Closes an active database connection by name and removes it from the internal registry.

`LimsSqlDisconnect` closes the named connection and removes it from the active connection set. It returns [`.T.`](../literals/true.md) when the disconnect succeeds and [`.F.`](../literals/false.md) when the name does not exist or the connection is already closed. The function does not raise an error on failure. Closing a connection affects all code that targets it by name until it is re-registered with [`LimsSqlConnect`](LimsSqlConnect.md).

## When to use

- When you need to explicitly clean up a named database connection after data operations.
- When switching from one database connection to another and ensuring the old connection is closed first.
- When implementing error handling that guarantees allocated connections are always cleared.

## Syntax

```ssl
LimsSqlDisconnect([sConnectionName]);
```

## Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `sConnectionName` | [string](../types/string.md) | no | [`NIL`](../literals/nil.md) | Connection name of the connection to disconnect. When [`NIL`](../literals/nil.md), falls back to the system default connection. |

## Returns

**[boolean](../types/boolean.md)** — [`.T.`](../literals/true.md) if the disconnect operation succeeded; [`.F.`](../literals/false.md) otherwise.

## Best practices

!!! success "Do"
    - Check the boolean return value to confirm the disconnect succeeded.
    - Disconnect all named database connections during application shutdown or cleanup routines.
    - Use [`:FINALLY`](../keywords/FINALLY.md) to guarantee disconnection regardless of whether the block succeeds or raises an error.

!!! failure "Don't"
    - Assume success without checking the return value.
    - Leave connections open unnecessarily.
    - Silently ignore a [`.F.`](../literals/false.md) return; it can indicate the connection was never registered or was already closed.

## Caveats

- Calling with [`NIL`](../literals/nil.md), an empty string, or a misspelled name will not disconnect any connection and returns [`.F.`](../literals/false.md).
- Disconnecting a connection that is in use by other operations can cause those operations to fail.

## Examples

### Disconnect after a read operation

Connect to a named database, query a sample, and then disconnect explicitly. A warning is shown if the disconnect fails.

```ssl
:PROCEDURE FetchSampleData;
	:DECLARE sConnName, sSampleID, aResults, bDisconnected;

	sConnName := "AnalyticalDB";
	sSampleID := "SAMPLE-2024-001";

	LimsSqlConnect(sConnName);

	aResults := SQLExecute("
	    SELECT sample_name
	    FROM samples
	    WHERE sample_id = ?
	",
		, {sSampleID});

	:IF ALen(aResults) > 0;
		/* Displays fetched sample name;
		UsrMes("Fetched: " + LimsString(aResults[1, 1]));
	:ENDIF;

	bDisconnected := LimsSqlDisconnect(sConnName);

	:IF !bDisconnected;
		/* Displays on failure: disconnect failed;
		UsrMes("Failed to disconnect from " + sConnName);
	:ENDIF;

	:RETURN bDisconnected;
:ENDPROC;

/* Usage;
DoProc("FetchSampleData");
```

### Guarantee cleanup with [`:FINALLY`](../keywords/FINALLY.md)

Use [`:FINALLY`](../keywords/FINALLY.md) to guarantee that the named connection is always closed, even if the query or error handling raises an exception.

```ssl
:PROCEDURE ProcessSampleData;
	:PARAMETERS sConnectionName, sSampleID;
	:DEFAULT sConnectionName, "WorkstationDB";
	:DEFAULT sSampleID, "SAMP-2024-001";
	:DECLARE aResults, bSuccess, oErr;

	bSuccess := LimsSqlConnect(sConnectionName);
	:IF !bSuccess;
		ErrorMes("Failed to connect to " + sConnectionName);
		:RETURN .F.;
	:ENDIF;

	:TRY;
		aResults := SQLExecute("
		    SELECT sample_name, status
		    FROM samples
		    WHERE sample_id = ?
		",
			, {sSampleID});

		:IF ALen(aResults) == 0;
			RaiseError("No sample found with ID: " + sSampleID);
		:ENDIF;

		/* Displays sample name and status;
		UsrMes(
			"Sample: " + LimsString(aResults[1, 1]) +
			" Status: " + LimsString(aResults[1, 2])
		);
	:CATCH;
		oErr := GetLastSSLError();
		/* Displays on failure: processing error;
		ErrorMes("Error processing sample: " + oErr:Description);
		:RETURN .F.;
	:FINALLY;
		LimsSqlDisconnect(sConnectionName);
	:ENDTRY;

	:RETURN .T.;
:ENDPROC;

/* Usage;
DoProc("ProcessSampleData");
```

### Disconnect all connections matching a prefix

Retrieve all registered connection names and disconnect each one whose name starts with `TEMP_`.

```ssl
:PROCEDURE CleanupTempConnections;
	:DECLARE aAllConns, sPrefix, sConnName, nIndex, nCleaned;

	aAllConns := GetConnectionStrings();
	sPrefix := "TEMP_";
	nCleaned := 0;

	:FOR nIndex := 1 :TO ALen(aAllConns);
		sConnName := aAllConns[nIndex];
		:IF Left(sConnName, Len(sPrefix)) == sPrefix;
			:IF IsDBConnected(sConnName);
				LimsSqlDisconnect(sConnName);
				nCleaned := nCleaned + 1;
			:ENDIF;
		:ENDIF;
	:NEXT;

	/* Displays cleared connection count;
	UsrMes("Temp connections cleared: " + LimsString(nCleaned));
	:RETURN nCleaned;
:ENDPROC;

/* Usage;
DoProc("CleanupTempConnections");
```

## Related

- [`GetConnectionByName`](GetConnectionByName.md)
- [`GetConnectionStrings`](GetConnectionStrings.md)
- [`GetDefaultConnection`](GetDefaultConnection.md)
- [`LimsSqlConnect`](LimsSqlConnect.md)
- [`boolean`](../types/boolean.md)
- [`string`](../types/string.md)
