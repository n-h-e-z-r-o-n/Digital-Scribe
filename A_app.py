def integrate_strings(original, edited):
    original_list =  original.strip()
    edited_list = edited.strip()

    original_len = len(original_list)
    edited_len = len(edited_list)
    integreted = ""
    print(original_list)
    print(original_list[0])

    #print(edited_list)


    count = 0
    while count < edited_len:
        o_word = original_list[count]
        e_word = edited_list[count]
        if o_word == e_word:
            integreted += o_word
        else:
            integreted += e_word

        count += 1

    integreted += original_list[count: -1]

    return integreted


# Example usage:
original = "hello world today hezron. sample string containing words."
edited = "hallo welt boy today hezron."

integrated = integrate_strings(original, edited)
#print(integrated)