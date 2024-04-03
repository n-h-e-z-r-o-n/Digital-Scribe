def integrate_strings(original, edited):
    original_list =  original.split()
    edited_list = edited.split()

    original_len = len(original_list)
    edited_len = len(edited_list)
    integreted = ""
    print(original_list)
    print(edited_list)
    original_list[count:]

    count = 0
    while count <= edited_len-1:
        o_word = original_list[count]
        e_word = edited_list[count]
        if o_word == e_word:
            integreted += o_word + " "
        else:
            integreted += e_word + " "

        count += 1
    for i in original_list[count:]:
        integreted += i
    print(count)
    return integreted


# Example usage:
original = "hello world today hezron. sample string containing words."
edited = "hallo welt boy today hezron."

integrated = integrate_strings(original, edited)
print("-------------------------")
print(integrated)