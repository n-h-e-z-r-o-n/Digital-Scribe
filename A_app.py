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
        word1 = original_list[count]
        word2 = edited_list[count]
        if word1 == word2:
            integreted += word1


        count += 1




    return integreted


# Example usage:
original = "hello world today."
edited = "hallo welt today."
integrated = integrate_strings(original, edited)
print(integrated)