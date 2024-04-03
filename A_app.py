def integrate_strings(original, edited):
    original_list =  original.strip()
    edited_list = edited.strip()

    original_len = len(original_list)
    edited_len = len(edited_list)
    integreted = ""
    print(original_list)
    print(edited_list)
    original_index = 0
    edited_index = 0
    count = 0
    while count < edited_len:
        o_word = original_list[original_index]
        e_word = edited_list[edited_index]
        if o_word == e_word:
            integreted += o_word
        else:
            integreted += e_word



        original_index += 1
        edited_index += 1
        count += 1

    integreted += original_list[original_index: -1]

    return integreted


# Example usage:
original = "hello world today hezron. sample string containing words."
edited = "hallo welt boy today heron."

integrated = integrate_strings(original, edited)
print(integrated)