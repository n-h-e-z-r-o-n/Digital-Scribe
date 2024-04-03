def integrate_strings(original, edited):
    original_list =  original.split()
    edited_list = edited.split()

    original_len = len(original_list)
    edited_len = len(edited_list)
    integreted = ""
    print(original_list)
    print(edited_list)


    count = 0
    o_word_index = 0
    while count <= edited_len-1:
        o_word = original_list[o_word_index]
        e_word = edited_list[count]
        if o_word == e_word:
            integreted += o_word + " "
            o_word_index += 1
        else:
            integreted += e_word + " "



        count += 1

    print(original_list[o_word_index:])
    for i in original_list[count:]:
        integreted += i
    print(count)
    return integreted


# Example usage:

old = "hallo world boy today hezron"
edited = "hallo welt boy today hezron."
new = "hello world today hezron. sample string containing words."


integrated = integrate_strings(old , edited, new)
print("-------------------------")
print(integrated)