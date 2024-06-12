import re
import ast
# Example string
text = """
```python
[
    "Current Condition",
    "Past Medical History",
    "Surgical History",
    "Hospitalizations",
    "Medications",
    "Allergies",
    "Social History",
    "Family History",
    "Additional Information"
]
``` . """
text = text.replace("\n", "")
pattern = r'\[.*?\]'

# Find all matches
matches = re.findall(pattern, text)

print("matches: ", matches)
# Print matches
match = ''
for match in matches:
    print(match)



# Convert string to list
list_from_string = ast.literal_eval(match)

# Print the resulting list
print(list_from_string)
