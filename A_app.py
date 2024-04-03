def integrate_strings(old , edited, new):
    old = old.split()
    edited = edited.split()
    new = new.split()
    print(len(old))
    pos = len(old)-1
    data = new[pos:]

    return data


# Example usage:

old = "hallo world boy today hezron"
edited = "hallo welt boy today hezron."
new = "hello world today hezron. sample string containing words."

pri
integrated = integrate_strings(old , edited, new)
print("-------------------------")
print(integrated)