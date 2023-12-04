import pytest

import python_jsonschema_objects as pjo


def test_simple_array_anyOf():
    basicSchemaDefn = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "Test",
        "properties": {
            "ExampleAnyOf": {"$ref": "#/definitions/exampleAnyOf"}
        },
        "required": ["ExampleAnyOf"],
        "type": "object",
        "definitions": {
            "exampleAnyOf": {
                #"type": "string", "format": "email"
                "anyOf": [
                    {"type": "string", "format": "email"},
                    {"type": "string", "maxlength": 0},
                ]
            }
        },
    }

    builder = pjo.ObjectBuilder(basicSchemaDefn)

    ns = builder.build_classes(any_of="use-first")
    ns.Test().from_json('{"ExampleAnyOf" : "test@example.com"}')
    
    with pytest.raises(pjo.ValidationError):
        # Because string maxlength 0 is not selected, as we are using the first validation in anyOf:
        ns.Test().from_json('{"ExampleAnyOf" : ""}')
        # Because this does not match the email format:
        ns.Test().from_json('{"ExampleAnyOf" : "not-an-email"}')
