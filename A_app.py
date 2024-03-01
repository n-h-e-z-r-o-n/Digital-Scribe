from gradientai import ExtractParamsSchemaValueType, Gradient



schema = '{ "131313" { "type": ExtractParamsSchemaValueType.NUMBER, "required": True, }, "ddfsf" { "type": ExtractParamsSchemaValueType.STRING, "required": True, }, "dfg" { "type": ExtractParamsSchemaValueType.STRING, "required": True, }, }'

dictionary = eval(schema)
print(dictionary)

