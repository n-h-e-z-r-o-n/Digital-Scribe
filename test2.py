string_dict = "{'name': 'John', 'age': 30, 'city': 'New York'}"

# Convert the string to a dictionary
dict_obj = eval(string_dict)

print(dict_obj)
print(type(dict_obj))