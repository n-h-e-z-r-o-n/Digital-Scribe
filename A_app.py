def integrate_strings(old , edited, new):
    old = old.split()
    edited = edited.split()
    new = new.split()
    index = 0
    for i in old:
        if i == new[index]:

            old[index] = new[index]
        index += 1

    return integreted


# Example usage:

old = "hallo world boy today hezron"
edited = "hallo welt boy today hezron."
new = "hello world today hezron. sample string containing words."


integrated = integrate_strings(old , edited, new)
print("-------------------------")
print(integrated)