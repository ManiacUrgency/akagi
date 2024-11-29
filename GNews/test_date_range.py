# n = int(input())
# count = 1
# for i in range(1, n + 1):
#   for a in range(1, i+1):
#       print("%4d" % count, end = " " )
#       count+=1
#   print()

from datetime import datetime, timedelta

first_date = datetime(2023, 11, 1)
last_date = datetime(2024, 11, 27)
step = timedelta(days=5)
step_four_days = timedelta(days=4)

current_date = first_date
while current_date <= last_date:
    start_date = current_date
    end_date = current_date + step_four_days
    print(f"\nStart Date: {start_date.strftime('%Y-%m-%d')}, End Date: {end_date.strftime('%Y-%m-%d')}")
    current_date += step

  