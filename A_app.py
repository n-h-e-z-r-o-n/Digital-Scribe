def integrate_strings(original, edited):
    original_list =  original.strip()
    edited_list = edited.strip()

    original_len = len(original_list)
    edited_len = len(edited_list)
    integreted = ""
    print(original_list)
    print(edited_list)
    count = 0
    for i in original_list:
        if i == edited_list[count]:
            integreted += i + ' '
        count += 1

    return integreted


# Example usage:
original = "hello world today."
edited = "hallo welt today."
integrated = integrate_strings(original, string2)
print(integrated)