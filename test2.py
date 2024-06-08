import datetime
from datetime import date, datetime

# Define a specific date


# Get the current date
current_date = date.today()

# Calculate the difference
difference = current_date - specific_date
# Get the current date and time
now = datetime.datetime.now()


formatted_date = now.strftime("%Y,%m,%d")
formatted_time = now.strftime("%H:%M:%S")

m = formatted_date.split(',')

specific_date = date(m[0],m[1], m[2])

print("Formatted date:", formatted_date)
print("Formatted time:", specific_date)
