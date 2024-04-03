def integrate_strings(original, edited):
    original_list =  original.strip()
    edited_list = edited.strip()

    original_len = len(original_list)
    edited_len = len(edited_list)
    integreted = ""
    print(original_list)
    print(edited_list)
    count = 0
    while True:
        o_word = original_list[count]
        e_word = edited_list[count]
        if o_word == e_word:
            integreted += o_word
        else:
            integreted += e_word



        count += 1




    return integreted


# Example usage:
original = "hello world today."
edited = "hallo welt today."
integrated = integrate_strings(original, edited)
print(integrated)