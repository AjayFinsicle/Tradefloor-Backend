from datetime import datetime, timedelta

# Assuming you have a datetime object
original_datetime = datetime.strptime("2025-04-04 07:18:09+00:00", "%Y-%m-%d %H:%M:%S%z")

# Add 7 days to the original datetime
new_datetime = original_datetime + timedelta(days=7)

print(new_datetime)
