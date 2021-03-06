from validator import get_schema, get_schema_from_file, get_schema_from_url
from validator.exceptions import InvalidSchemaException


print("---- Meta schema from url")
meta_schema_url = "http://json-schema.org/draft-04/schema"
meta_schema = get_schema_from_url(meta_schema_url)
print(meta_schema.validate({"type": "string"}))
print(meta_schema.validate({"type": 1}))


print("---- Meta schema from file")
file = "validator/meta_schema.json"
schema = get_schema_from_file(file)
print(schema.validate({"type": "string"}))
print(schema.validate({"type": 1}))


print("---- Meta schema url with json pointer fragment")
meta_schema_array_url = meta_schema_url + "#/definitions/schemaArray"
meta_schema_array = get_schema_from_url(meta_schema_array_url)
print(meta_schema_array.validate([{"type": "string"}, {"type": "integer"}]))
print(meta_schema_array.validate([{"type": "string"}, {"type": "integer"}, 1]))


print("---- Schema from python dict")
d = {"type": "integer", "maximum": 10, "exclusiveMaximum": True}
d_schema = get_schema(d)
print(d_schema.validate(9))
print(d_schema.validate(10))
print(d_schema.validate(11))


print("---- Invalid json schema")
try:
    get_schema({"type": 1})
except InvalidSchemaException as e:
    print("This is not a valid JSON Schema")

try:
    get_schema({
        "definitions": {
            "S": {
                "not": {
                    "$ref": "#/definitions/S"
                }
            }
        },
        "$ref": "#/definitions/S"
    })
except InvalidSchemaException as e:
    print("This is a JSON Schema with circular references")

print("---- Using response object")
d2 = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "maxLength": 10
        }
    }
}
d2_schema = get_schema(d2)
response = d2_schema.validate({
    "name": "12345678901234"
})
if not response:
    print("Failed on document:", response.document_pointer)
    print(response.document_pointer.get_json())
    print("Failed on schema:", response.schema_pointer)
    print(response.schema_pointer.get_json())
