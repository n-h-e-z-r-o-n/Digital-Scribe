from gradientai import ExtractParamsSchemaValueType, Gradient
import os
# import gradientai
# print(dir(Gradient))
# help(Gradient.extract)

# # Set the environment variables for gradient.ai
os.environ['GRADIENT_ACCESS_TOKEN'] = "Fz8v1bayVU3mQ11BoCLgtvquK8OHTL68"
os.environ['GRADIENT_WORKSPACE_ID'] = "345ce93a-40e9-4940-aa2e-fa76f1668fcd_workspace"

mygradient = Gradient()



document = (
    "When Apple released the Apple Watch in 2015, it was business as "
    + "usual for a company whose iPhone updates had become cultural "
    + "touchstones. Before the watch went on sale, Apple gave early "
    + "versions of it to celebrities like Beyoncé, featured it in fashion "
    + "publications like Vogue and streamed a splashy event on the "
    + "internet trumpeting its features."
)
schema_ = {
    "company": {
        "type": ExtractParamsSchemaValueType.STRING,
        "required": True,
    },
    "product": {
        "type": ExtractParamsSchemaValueType.STRING,
    },
    "magazine": {
        "type": ExtractParamsSchemaValueType.STRING,
    },
    "year": {
        "type": ExtractParamsSchemaValueType.NUMBER,
    }
}

print(type(schema_))
result = mygradient.extract(
    document=document,
    schema_=schema_,
)
print(result)
for key, value in result["entity"].items():
    print(key," - ", value)
