import time

# Get the current time in seconds since the epoch
current_time_seconds = time.time()

# Convert the current time to a struct_time object
current_time_struct = time.localtime(current_time_seconds)

# Format the current time in words
current_time_words = time.strftime("%A %B %d %Y %I %p", current_time_struct)

# Print the current time in words
print("Current date and time:", current_time_words)
