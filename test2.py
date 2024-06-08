import datetime

# Get the current date and time
now = datetime.datetime.now()

# Print the current date and time
print("Current date and time:", now)

# If you want the date and time separately, you can do the following
current_date = now.date()
current_time = now.time()

print("Current date:", current_date)
print("Current time:", current_time)

# You can also format the date and time as needed
formatted_date = now.strftime("%Y,%m,%d")
formatted_time = now.strftime("%H:%M:%S")

print("Formatted date:", formatted_date)
print("Formatted time:", formatted_time)
