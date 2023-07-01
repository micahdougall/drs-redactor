from jsonschema import validate, exceptions


def is_valid_payload(payload: dict, schema: dict) -> bool:
    """Validates a payload against a JSON schema
    
    Args:
        payload: the payload to validate
        schema: the JSON schema to validate against

    Returns:
        True if the payload is valid, False otherwise
    """
    try:
        validate(instance=payload, schema=schema)
    except exceptions.SchemaError as e:
        print(e)
        return False
    return True
