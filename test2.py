def contains_any_element(lst, elements):
    return any(elem in lst for elem in elements)

# Example usage
my_list = ['a', 'b', 'c', 'd']
elements_to_check = ['a', 'e']

print(contains_any_element(my_list, 'g'))  # Output: True


