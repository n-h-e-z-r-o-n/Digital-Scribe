import datetime
from datetime import date

# Define a specific date


# Get the current date
current_date = date.today()

# Calculate the difference
# Get the current date and time
now = datetime.datetime.now()


formatted_date = now.strftime("%Y,%m,%d")
formatted_time = now.strftime("%H:%M:%S")

m = formatted_date.split(',')
specific_date = date(int(m[0]), int(m[1]),int( m[2])-1)

n = current_date - specific_date
print("Formatted date:", formatted_date)
print("Formatted time:", specific_date)
print("Formatted time:", n)
