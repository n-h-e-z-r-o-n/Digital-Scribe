string = "hello world"
capitalized_string = string.capitalize()
print(string[0].lower()+string[1:])  # Output: "Hello world"


import inflect


def get_singular_or_plural(word):
    p = inflect.engine()
    singular = p.singular_noun(word)
    plural = p.plural_noun(word)

    if singular and plural:
        return f"Singular: {singular}, Plural: {plural}"
    elif singular:
        return f"Singular: {singular}"
    elif plural:
        return f"Plural: {plural}"
    else:
        return "Not found"


# Example usage:
word = "apple"
result = get_singular_or_plural(word)
print(result)
