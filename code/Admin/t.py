from datetime import datetime

# Example start and end times
start_time = "12:00"
end_time = "14:30"

# Convert strings to datetime objects (assuming time format is HH:MM)
start_time_obj = datetime.strptime(start_time, "%H:%M")
end_time_obj = datetime.strptime(end_time, "%H:%M")

# Calculate the time difference
time_difference = end_time_obj - start_time_obj

# Get the total number of hours as a float (including minutes)
hours = time_difference.total_seconds() / 3600  # seconds in an hour

print(f"The difference is {hours} hours")
